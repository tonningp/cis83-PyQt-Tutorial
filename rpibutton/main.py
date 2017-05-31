#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.ledOn = True 
        self.initUI()
        
        
    def initUI(self):      

        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colours')
        self.show()


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawLED(qp,self.ledOn)
        qp.end()

        
    def drawLED(self, qp,on):
      
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        if on:
            qp.setBrush(QColor(200, 0, 0))
        else:
            qp.setBrush(QColor(255, 255, 255))

        qp.drawEllipse(0, 0, 50, 50)

              
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
