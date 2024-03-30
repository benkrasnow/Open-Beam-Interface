import asyncio
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QMessageBox, QPushButton,
                             QVBoxLayout, QWidget, QLabel, QGridLayout,
                             QSpinBox)

from beam_interface import Connection, FrameBuffer, DACCodeRange
from image_display import ImageDisplay


class SettingBox(QGridLayout):
    def __init__(self, label, lower_limit, upper_limit, initial_val):
        super().__init__()
        self.name = label
        self.label = QLabel(label)
        self.addWidget(self.label,0,1)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(lower_limit, upper_limit)
        self.spinbox.setSingleStep(1)
        self.spinbox.setValue(initial_val)
        self.addWidget(self.spinbox,1,1)

    def getval(self):
        return int(self.spinbox.cleanText())
    
    def setval(self, val):
        self.spinbox.setValue(val)

class Settings(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.rx = SettingBox("X Resolution",128, 16384, 512)
        self.addLayout(self.rx)
        self.ry = SettingBox("Y Resolution",128, 16384, 512)
        self.addLayout(self.ry)
        self.dwell = SettingBox("Dwell Time",0, 65536, 2)
        self.addLayout(self.dwell)
        self.latency = SettingBox("Latency",0, pow(2,28), pow(2,16))
        self.addLayout(self.latency)
        self.capture_btn = QPushButton("Capture")
        self.addWidget(self.capture_btn)

class Window(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.addLayout(self.settings)
        self.settings.capture_btn.clicked.connect(self.capture_image)
        self.image_display = ImageDisplay(512,512)
        self.addWidget(self.image_display)
    def capture_image(self):
        self.conn = Connection('localhost', 2223)
        self.fb = FrameBuffer(self.conn)
        x_res = self.settings.rx.getval()
        y_res = self.settings.ry.getval()
        dwell = self.settings.dwell.getval()
        latency = self.settings.latency.getval()
        x_range = DACCodeRange(0, x_res, int((16384/x_res)*256))
        print(f'x step size: {(16384/x_res)}')
        y_range = DACCodeRange(0, y_res, int((16384/y_res)*256))
        res = asyncio.run(self.fb.capture_image(x_range, y_range, dwell=dwell, latency=latency))
        self.display_image(self.fb.output_ndarray(res, x_range, y_range))
    def display_image(self, array):
        x_width, y_height = array.shape
        print(f'x width {x_width}, y height {y_height}')
        self.image_display.setImage(y_height, x_width, array)

app = pg.mkQApp()
w = QWidget()
window = Window()
w.setLayout(window)
w.show() 
pg.exec()



