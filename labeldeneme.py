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
import numpy as np
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
        self.tmp_im = None
        self.figure = Figure()
        self.figure2 = Figure()
        self.figure3 = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas3 = FigureCanvas(self.figure3)
        self.lookupRed = np.zeros((256,1))
        self.lookupGreen = np.zeros((256,1))
        self.lookupBlue = np.zeros((256,1))
        self.eq = None
        self.qImg = None
        self.qImg2 = None
        self.qImgResult = None
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
        sumArray = np.sum(self.redArray)
        self.cdf = np.cumsum(self.redArray)/sumArray
        
        sumArray = np.sum(self.redArray2)
        self.cdf2 = np.cumsum(self.redArray2)/sumArray
        
        i=0
        for i in range(256):
            j=0
            while self.cdf2[j]<self.cdf[i] and j<=255:
                j= j+1
            self.lookupRed[i] = j
        
        matchRed =np.zeros(self.red.shape)
      #  h=0
       # w=0
        #for w in range(0,self.width):
         #   matchRed.append([])
          #  h=0
           # for h in range(0,self.height):
            #    matchRed[w].append(self.lookupRed[self.red[w][h]])
        h=0
        w=0
        for w in range(0,self.width):
            h=0
            for h in range(0,self.height):
                matchRed[w][h] = self.lookupRed[self.red[w][h]]
                
                
        matchRedH = [0]*256
        h=0
        w=0
        for w in range(0,self.width):
            for h in range(0,self.height):
                tempR = matchRed[w][h]
                matchRedH[int(tempR)]+=1 
        
        #plt.plot(matchRed)
        #plt.show()        
        
        #self.tmp_im[:,:,2]= matchRed
  ##########################################################################
        sumArray2 = np.sum(self.greenArray)
        self.cdfG = np.cumsum(self.greenArray)/sumArray2
        
        sumArray2 = np.sum(self.greenArray2)
        self.cdfG2 = np.cumsum(self.greenArray2)/sumArray2
        
        
        
        i=0
        for i in range(256):
            j=0
            while self.cdfG2[j]<self.cdfG[i] and j<=255:
                j= j+1
            self.lookupGreen[i] = j
        
        matchGreen =np.zeros(self.green.shape)
        h=0
        w=0
        for w in range(0,self.width):
            h=0
            for h in range(0,self.height):
                matchGreen[w][h] = self.lookupGreen[self.green[w][h]]
         
        matchGreenH = [0]*256
        h=0
        w=0
        for w in range(0,self.width):
            for h in range(0,self.height):
                tempG = matchGreen[w][h]
                matchGreenH[int(tempG)]+=1 
        #self.tmp_im[:,:,1]= matchGreen
##########################################################################
        sumArray3 = np.sum(self.blueArray)
        self.cdfB = np.cumsum(self.blueArray)/sumArray3
        
        sumArray3 = np.sum(self.blueArray2)
        self.cdfB2 = np.cumsum(self.blueArray2)/sumArray3
        
        
        
        i=0
        for i in range(256):
            j=0
            while self.cdfB2[j]<self.cdfB[i] and j<=255:
                j= j+1
            self.lookupBlue[i] = j
        
        matchBlue = np.zeros(self.blue.shape)
        h=0
        w=0
        for w in range(0,self.width):
            h=0
            for h in range(0,self.height):
                matchBlue[w][h] = self.lookupBlue[self.blue[w][h]]
       
        matchBlueH = [0]*256
        h=0
        w=0
        for w in range(0,self.width):
            for h in range(0,self.height):
                tempB = matchBlue[w][h]
                matchBlueH[int(tempB)]+=1          
       # self.tmp_im[:,:,0]= matchBlue
        self.image[:,:,2] = matchRed
        self.image[:,:,1] = matchGreen
        self.image[:,:,0] = matchBlue
        heightI,widthI,channelsI = self.image.shape
        bytesPerLine = channelsI * widthI
        self.qImgResult = QImage(self.image.data,widthI,heightI,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
        imageLabel = QLabel('image')
        imageLabel.setPixmap(QPixmap.fromImage(self.qImgResult))
        imageLabel.setAlignment(Qt.AlignCenter)
        self.resultBox.layout().addWidget(imageLabel)
        
        blueplot3 = self.figure3.add_subplot(313)
        redplot3 = self.figure3.add_subplot(311)
        greenplot3 = self.figure3.add_subplot(312)
        self.canvas3.draw()
        
        redplot3.bar(range(256),matchRedH,color = 'red')
        blueplot3.bar(range(256),matchBlueH,color = 'blue')
        greenplot3.bar(range(256),matchGreenH,color = 'green')

        self.resultBox.layout().addWidget(self.canvas3)
        
    def createHistogram(self):
        self.red = self.image[:,:,2]
        self.green = self.image[:,:,1]
        self.blue = self.image[:,:,0]
        self.width,self.height = self.blue.shape
        self.blueArray = [0]*256
        self.redArray = [0]*256
        self.greenArray = [0]*256
        for w in range(0,self.width):
            for h in range(0,self.height):
                temp = self.blue[w][h]
                self.blueArray[temp]+=1
        for w in range(0,self.width):
            for h in range(0,self.height):
                temp = self.red[w][h]
                self.redArray[temp]+=1        
        for w in range(0,self.width):
            for h in range(0,self.height):
                temp = self.green[w][h]
                self.greenArray[temp]+=1 
        blueplot = self.figure.add_subplot(313)
        redplot = self.figure.add_subplot(311)
        greenplot = self.figure.add_subplot(312)
        
        blueplot.bar(range(256),self.blueArray,color = 'blue')
        redplot.bar(range(256),self.redArray,color = 'red')
        greenplot.bar(range(256),self.greenArray,color = 'green')
        self.canvas.draw()
        self.inputBox.layout().addWidget(self.canvas)
    def createHistogram2(self):
        self.red2 = self.image2[:,:,2]
        self.green2 = self.image2[:,:,1]
        self.blue2 = self.image2[:,:,0]
        self.width2,self.height2 = self.blue2.shape
        self.blueArray2 = [0]*256
        self.redArray2 = [0]*256
        self.greenArray2 = [0]*256
        
        for w in range(0,self.width2):
            for h in range(0,self.height2):
                temp = self.blue2[w][h]
                self.blueArray2[temp]+=1
        for w in range(0,self.width2):
            for h in range(0,self.height2):
                temp = self.red2[w][h]
                self.redArray2[temp]+=1        
        for w in range(0,self.width2):
            for h in range(0,self.height2):
                temp = self.green2[w][h]
                self.greenArray2[temp]+=1 
        blueplot = self.figure2.add_subplot(313)
        redplot = self.figure2.add_subplot(311)
        greenplot = self.figure2.add_subplot(312)
        
        blueplot.bar(range(256),self.blueArray2,color = 'blue')
        redplot.bar(range(256),self.redArray2,color = 'red')
        greenplot.bar(range(256),self.greenArray2,color = 'green')
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