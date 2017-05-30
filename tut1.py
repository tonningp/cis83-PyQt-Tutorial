#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget

"""
For this tutorial, modify the following source and set the window title 
to Hello World
"""
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('First Window')
    w.show()
    
    sys.exit(app.exec_())
