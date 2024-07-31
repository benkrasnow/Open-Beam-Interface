import sys
import asyncio
import logging
logger = logging.getLogger()

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QHBoxLayout, QMainWindow, QDialog,
                             QMessageBox, QPushButton, QComboBox,
                             QVBoxLayout, QWidget, QLabel, QGridLayout,
                             QSpinBox, QFileDialog, QLineEdit, QDialogButtonBox,
                             QDockWidget)
import pyqtgraph as pg

import qasync
from qasync import asyncSlot, asyncClose, QApplication, QEventLoop

from .components import ImageDisplay, CombinedScanControls

from transfer import TCPConnection, setup_logging
from macros import FrameBuffer

setup_logging({"GUI": logging.DEBUG, "Command": logging.DEBUG})

class ScanControlWidget(QDockWidget):
    def __init__(self):
        super().__init__(
            windowTitle="Picture Control", 
            features = QDockWidget.DockWidgetFeature.DockWidgetMovable |
                        QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.inner = CombinedScanControls()
        self.setWidget(self.inner)

class Window(QMainWindow):
    _logger = logging.getLogger("GUI")
    def __init__(self):
        super().__init__()
        self.conn = TCPConnection("localhost", 2224)
        self.fb = FrameBuffer(self.conn)

        self.image_display = ImageDisplay(511, 511)
        self.setCentralWidget(self.image_display)

        self.scan_control = ScanControlWidget()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scan_control)

        self.scan_control.inner.live.start_btn.clicked.connect(self.start_live_scan)
    
    @asyncSlot()
    async def start_live_scan(self):
        resolution, dwell_time = self.scan_control.inner.live.getval()
        async for frame in self.fb.capture_frame_iter_fill(
            x_res=resolution, y_res=resolution, dwell_time=dwell_time, latency=65536
            ):
            self.image_display.setImage(frame.as_uint8())
            self._logger.debug("set image")


def run_gui():
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    window = Window()
    # if not args.window_size == None:
    #     window.resize(args.window_size[0], args.window_size[1])
    window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())


if __name__ == "__main__":
    run_gui()