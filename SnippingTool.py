import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class SnippingWidget(QtWidgets.QWidget):
    num_snip = 0
    is_snipping = False
    background = True

    def __init__(self):
        super(SnippingWidget, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def start(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        SnippingWidget.background = False
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        self.show()

    def paintEvent(self, event):
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
        else:
            # reset points, so the rectangle won't show up again.
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        qp.drawRect(rect)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('Quit')
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        # SnippingWidget.num_snip += 1
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()
        
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        
        # kernel = np.ones((1, 1), np.uint8)
        # cv2.dilate(canny, kernel, iterations=1)
        # cv2.erode(img, kernel, iterations=1)
        filter_img=cv2.bilateralFilter(img, 9, 75, 75)
        custom_config = r'--oem 3 --psm 6'
        threshold_img=cv2.threshold(filter_img,100,255,cv2.THRESH_BINARY_INV)[1]
        #deatils_string= pytesseract.image_to_string(threshold_img)
        details_Dict = pytesseract.image_to_data(threshold_img,output_type=pytesseract.Output.DICT,config=custom_config,lang='eng')
        print(details_Dict["text"])
        parse_text = []
        word_list = []
        last_word = ''
        for word in details_Dict['text']:
            if word!='':
                word_list.append(word)
                last_word = word
            if (last_word!='' and word == '') or (word==details_Dict['text'][-1]):
                parse_text.append(word_list)
                word_list = []

        with open("text.txt","w+") as file1:
            for line in parse_text:
                file1.writelines(line)
                file1.write('\n')
        os.startfile("text.txt")
        cv2.imshow('Captured Image',threshold_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

        # add to the snips list the object that opens a window of the image
        #SnippingMenu.Menu(img, SnippingWidget.num_snip, (x1, y1, x2, y2))
