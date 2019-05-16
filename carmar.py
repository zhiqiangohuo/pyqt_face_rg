#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2
 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
#import take_pic
import test
from input_name import get_name
import argparse
from pathlib import Path
from multiprocessing import Process, Pipe,Value,Array
import torch
from config import get_config
from mtcnn import MTCNN
from Learner import face_learner
from utils import load_facebank, draw_box_name, prepare_facebank
import time
from PIL import Image
from verify_test import rg_face
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
 
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x =0
        self.count = 0
        self.i = 0
        self.name = ''
        
 
    def set_ui(self):
 
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

 
        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_take_pic = QtWidgets.QPushButton(u'人脸录入')
        self.button_rg_face = QtWidgets.QPushButton(u'人脸识别')
        # self.button_take_pic = QtWidgets.QPushButton(u'表情识别')
        # self.button_take_pic = QtWidgets.QPushButton(u'性别识别')
        self.button_close = QtWidgets.QPushButton(u'退出')
 
 
        #Button 的颜色修改
        button_color = [self.button_open_camera, self.button_close, self.button_close,self.button_take_pic,self.button_rg_face]
        for i in range(2):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")
 
 
        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)
        self.button_take_pic.setMinimumHeight(50)
        self.button_rg_face.setMinimumHeight(50)
 
        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)
 
        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)
        # 整个窗口边框大小
        self.label_show_camera.setFixedSize(1280, 720)
        self.label_show_camera.setAutoFillBackground(False)
 
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.button_take_pic)
        self.__layout_fun_button.addWidget(self.button_rg_face)
        self.__layout_fun_button.addWidget(self.label_move)
 
        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)
 
        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'人脸识别系统')
 
        '''
        # 设置背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background.jpg')))
        self.setPalette(palette1)
        '''
    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        # 定义拍照方法
        self.button_take_pic.clicked.connect(self.button_take_pic_click)
        # 定义人脸识别方法
        self.button_rg_face.clicked.connect(self.button_rg_face_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)
    def button_take_pic_click(self):
        '''录入人脸模块'''
        text, okPressed = QInputDialog.getText(self, "输入用户名","Your name:", QLineEdit.Normal, "")
        print(text)
        self.name = text
    
        # name = name.get_name()
        test.take_photo(name=self.name)
    def button_rg_face_click(self):
        '''人脸识别模块'''
        self.button_open_camera_click
        #self.show_camera()
        print("开始识别")
        rg_face()
    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)
 
                self.button_open_camera.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')
 
 
    def show_camera(self):
        flag, self.image = self.cap.read()
        # face = self.face_detect.align(self.image)
        # if face:
        #     pass
        # 相机窗口大小
        show = cv2.resize(self.image, (1380, 820))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # print(show.shape[1], show.shape[0])
        #show.shape[1] = 640, show.shape[0] = 480
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # self.x += 1
        # self.label_move.move(self.x,100)
 
        # if self.x ==320:
        #     self.label_show_camera.raise_()
 
 
    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()
 
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"关闭", u"是否关闭！")
 
        msg.addButton(ok,QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cacel.setText(u'取消')
        # msg.setDetailedText('sdfsdff')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            #             self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()
 
 
 
if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()

sys.exit(App.exec_())