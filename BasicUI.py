import sys
import numpy as np
import matplotlib as plt
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QPushButton, QLabel, QSlider, QHBoxLayout, QGroupBox, QRadioButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

data = np.load('copper_data.npy')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        

        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 354, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        

        
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStatusTip('Open File')
        ##self.file = self.actionOpen.triggered.connect(QFileDialog.getOpenFileName())

        
        self.shapeLabel = QLabel(self.centralwidget)
        shape = []
        shape.append (data.shape)
        phi = data.shape[2]
        theta = data.shape[3]
        self.shapeLabel.setText("Shape: "+','.join(str(s) for s in shape))
        self.shapeLabel.adjustSize()
        self.shapeLabel.move(400, 200)
        self.typeLabel = QLabel(self.centralwidget)

        dataType = set()
        dataType.add (data.dtype)
        self.typeLabel.setText("Data Type: "+','.join(str(d) for d in dataType))
        self.typeLabel.adjustSize()
        self.typeLabel.move(400, 250)

 
        self.sliderPhi = QtWidgets.QSlider(self.centralwidget)
        self.sliderPhi.setGeometry(QtCore.QRect(400, 90, 160, 16))
        self.sliderPhi.setOrientation(QtCore.Qt.Horizontal)
        self.sliderPhi.setObjectName("sliderPhi")
        self.sliderPhi.setMaximum(phi-1)
        self.labelTitlePhi = QLabel(self.centralwidget)
        self.labelTitlePhi.move(400,65)
        self.labelTitlePhi.setText("Phi")
        self.labelPhi = QLabel(self.centralwidget)
        self.labelPhi.move(580, 90)
        self.labelPhi.setText("0")
        self.sliderPhi.valueChanged.connect(self.changeValuePhi)
        
        
        self.sliderTheta = QtWidgets.QSlider(self.centralwidget)
        self.sliderTheta.setGeometry(QtCore.QRect(400, 150, 160, 16))
        self.sliderTheta.setOrientation(QtCore.Qt.Horizontal)
        self.sliderTheta.setObjectName("sliderTheta")
        self.sliderTheta.setMaximum(theta-1)
        self.labelTitleTheta = QLabel(self.centralwidget)
        self.labelTitleTheta.move(400,125)
        self.labelTitleTheta.setText("Theta")
        self.labelTheta = QLabel(self.centralwidget)
        self.labelTheta.move(580, 150)
        self.labelTheta.setText("0")
        self.sliderTheta.valueChanged.connect(self.changeValueTheta)
        
       
        
        self.sc = MplCanvas(self.centralwidget, width=4, height=4, dpi=100)       
        self.sc.axes.imshow(data[...,self.sliderPhi.value(),self.sliderTheta.value()])
        self.sc.show()
        
        self.sc1 = MplCanvas(self.centralwidget, width=4, height=4, dpi=100) 
        self.sc1.axes.imshow(data[5,5,...])
        self.sc1.show()

        
        self.sliderPhi.valueChanged.connect(self.update_plot)
        self.sliderTheta.valueChanged.connect(self.update_plot)
        layout = QtWidgets.QHBoxLayout(self.centralwidget)
        layout.addWidget(self.sc)
        layout2 = QtWidgets.QVBoxLayout(self.centralwidget)
        layout3 = QtWidgets.QHBoxLayout(self.centralwidget)
        layout3.addWidget(self.sliderPhi)
        layout3.addWidget(self.labelPhi)
        layout4 = QtWidgets.QHBoxLayout(self.centralwidget)
        layout4.addWidget(self.sliderTheta)
        layout4.addWidget(self.labelTheta)
        layout2.addWidget(self.shapeLabel)
        layout2.addWidget(self.typeLabel)
        layout2.addWidget(self.labelTitlePhi)
        layout2.addLayout(layout3)
        layout2.addWidget(self.labelTitleTheta)
        layout2.addLayout(layout4)
        layout.addLayout(layout2)
        layout.addWidget(self.sc1)
        
       

         
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        
    def update_plot(self):
        
        self.sc.axes.cla()
        self.sc.axes.imshow(data[...,self.sliderPhi.value(),self.sliderTheta.value()])
        self.sc.draw()
       
    def imageChange(self):
        self.sc = MplCanvas(self.centralwidget, width=4, height=4, dpi=100)       
        self.sc.axes.imshow(data[...,self.sliderPhi.value(),self.sliderTheta.value()])
        self.sc.show()

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        
    def actionOpenHandler(self):
        file = QFileDialog.getOpenFileName()

        
    def initUI(self):
        shapeLabel = QLabel(self)
        shape = set()
        shape.add (data.shape)
        shapeLabel.setText("Shape; "+','.join(str(s) for s in shape))
        shapeLabel.adjustSize()
        shapeLabel.move(300, 150)
        typeLabel = QLabel(self)
        dataType = set()
        dataType.add (data.dtype)
        typeLabel.setText("Data Type: "+','.join(str(d) for d in dataType))
        typeLabel.adjustSize()
        typeLabel.move(300, 200)
        
    def changeValuePhi(self):
        size = self.sliderPhi.value()
        self.labelPhi.setText(str(size))
        self.labelPhi.adjustSize()
        
    def changeValueTheta(self):
        size = self.sliderTheta.value()
        self.labelTheta.setText(str(size))
        self.labelTheta.adjustSize()
        
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

