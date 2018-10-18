#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 00:14:00 2018

@author: anildogan
"""
import sys
from PyQt5.QtWidgets import QMainWindow,QMessageBox, QApplication,QScrollArea, QWidget, QPushButton, QAction, QGroupBox, QFileDialog, QLabel, QVBoxLayout, QGridLayout, QHBoxLayout,QFrame, QSplitter,QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QPalette,QImage
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
class App(QMainWindow):
    
    def __init__(self):
        super(App,self).__init__()
        
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
    
        self.inputBox = QGroupBox('Input')
        inputLayout = QVBoxLayout()
        self.inputBox.setLayout(inputLayout)
        
        self.targetBox = QGroupBox('Target')
        targetLAyout = QVBoxLayout()
        self.targetBox.setLayout(targetLAyout)
        
        self.resultBox = QGroupBox('Result')
        resultLayout = QVBoxLayout()
        self.resultBox.setLayout(resultLayout)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.inputBox, 0, 0)
        self.layout.addWidget(self.targetBox, 0, 1)
        self.layout.addWidget(self.resultBox, 0, 2)
        
        self.window.setLayout(self.layout)
        
        self.image = None
        self.image2 = None
        self.figure = Figure()
        self.figure2 = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)
        self.eq = None
        self.qImg = None
        self.qImg2 = None
        self.pixmap01 = None
        self.pixmap_image = None
       
        self.createActions()
        self.createMenu()
        self.createToolBar()
        
        self.setWindowTitle("Histogram")
        self.showMaximized()
        self.show()
        
        
    def createActions(self):
        self.open_inputAct = QAction(' &Open Input',self)
        self.open_inputAct.triggered.connect(self.open_Input)
        self.open_targetAct = QAction(' &Open Target', self)
        self.open_targetAct.triggered.connect(self.open_Target)
        self.exitAct = QAction(' &Exit', self)
        self.exitAct.triggered.connect(self.exit)
        self.equalize = QAction(' &Equalize Histogram',self)
        self.equalize.triggered.connect(self.equalizeHistogram)
    
    def createMenu(self):
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('File')
        self.fileMenu.addAction(self.open_inputAct)
        self.fileMenu.addAction(self.open_targetAct)
        self.fileMenu.addAction(self.exitAct)
    def createToolBar(self):
        self.eq = self.addToolBar("Equalize Histogram")
        self.eq.addAction(self.equalize)
    def equalizeHistogram(self):
        print("button hazır")
    def createHistogram(self):
        red = self.image[:,:,2]
        green = self.image[:,:,1]
        blue = self.image[:,:,0]
        width,height = blue.shape
        
        blueArray = [0]*256
        redArray = [0]*256
        greenArray = [0]*256
        
        for w in range(0,width):
            for h in range(0,height):
                temp = blue[w][h]
                blueArray[temp]+=1
        for w in range(0,width):
            for h in range(0,height):
                temp = red[w][h]
                redArray[temp]+=1        
        for w in range(0,width):
            for h in range(0,height):
                temp = green[w][h]
                greenArray[temp]+=1 
        blueplot = self.figure.add_subplot(313)
        redplot = self.figure.add_subplot(311)
        greenplot = self.figure.add_subplot(312)
        
        blueplot.bar(range(256),blueArray,color = 'blue')
        redplot.bar(range(256),redArray,color = 'red')
        greenplot.bar(range(256),greenArray,color = 'green')
        self.canvas.draw()
        self.inputBox.layout().addWidget(self.canvas)
    def createHistogram2(self):
        red = self.image2[:,:,2]
        green = self.image2[:,:,1]
        blue = self.image2[:,:,0]
        width,height = blue.shape
        
        blueArray = [0]*256
        redArray = [0]*256
        greenArray = [0]*256
        
        for w in range(0,width):
            for h in range(0,height):
                temp = blue[w][h]
                blueArray[temp]+=1
        for w in range(0,width):
            for h in range(0,height):
                temp = red[w][h]
                redArray[temp]+=1        
        for w in range(0,width):
            for h in range(0,height):
                temp = green[w][h]
                greenArray[temp]+=1 
        blueplot = self.figure2.add_subplot(313)
        redplot = self.figure2.add_subplot(311)
        greenplot = self.figure2.add_subplot(312)
        
        blueplot.bar(range(256),blueArray,color = 'blue')
        redplot.bar(range(256),redArray,color = 'red')
        greenplot.bar(range(256),greenArray,color = 'green')
        self.canvas2.draw()
        self.targetBox.layout().addWidget(self.canvas2)
    def open_Input(self):
        #fileName, _ = QFileDialog.getOpenFileName(self, "Open File",QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Input', '.')
        if fileName:
            self.image = cv2.imread(fileName)
            height,width,channels = self.image.shape
            bytesPerLine = 3 * width
            if not self.image.data:
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            
        self.qImg = QImage(self.image.data,width,height,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
        #self.pixmap01 = QPixmap.fromImage(self.qImg)
        
        imageLabel = QLabel('image')
        imageLabel.setPixmap(QPixmap.fromImage(self.qImg))
        imageLabel.setAlignment(Qt.AlignCenter)
        
        self.inputBox.layout().addWidget(imageLabel)
        self.createHistogram()   
       # self.updateActions()

       
    
    def open_Target(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Input', '.')
        if fileName:
            self.image2 = cv2.imread(fileName)
            height,width,channels = self.image2.shape
            bytesPerLine = 3 * width
            if not self.image2.data:
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            
        self.qImg2 = QImage(self.image2.data,width,height,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
        #self.pixmap01 = QPixmap.fromImage(self.qImg)
        
        imageLabel = QLabel('image')
        imageLabel.setPixmap(QPixmap.fromImage(self.qImg2))
        imageLabel.setAlignment(Qt.AlignCenter)
        
        self.targetBox.layout().addWidget(imageLabel)
        self.createHistogram2()
    
    def exit(self):
        sys.exit()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())