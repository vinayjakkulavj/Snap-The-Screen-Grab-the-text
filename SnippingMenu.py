import sys
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

import SnippingTool


class Menu(QMainWindow):
    
    default_title = "Snipping Tool"

    
    def __init__(self):
        super().__init__()

        self.title = Menu.default_title
        
        # New snip
        new_snip_action = QAction('New', self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('Snip!')
        new_snip_action.triggered.connect(self.new_image_window)

        # Exit
        exit_window = QAction('Exit', self)
        exit_window.setShortcut('Ctrl+Q')
        exit_window.setStatusTip('Exit application')
        exit_window.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_snip_action)
        self.toolbar.addAction(exit_window)

        self.snippingTool = SnippingTool.SnippingWidget()
        self.show()

    # snippingTool.start() will open a new window.
    def new_image_window(self):
        
        self.snippingTool.start()

   
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())


