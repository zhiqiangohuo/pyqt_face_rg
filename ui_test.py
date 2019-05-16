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
from def_gender import get_emotion_gender
from update_facebank import update_face
from def_take_pic import take_pic
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
        self.choice = 1
        
 
    def set_ui(self):
 
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

 
        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_take_pic = QtWidgets.QPushButton(u'人脸录入')
        self.button_rg_face = QtWidgets.QPushButton(u'人脸识别')
        self.button_rg_gender = QtWidgets.QPushButton(u'表情识别')
        self.button_rg_all = QtWidgets.QPushButton(u'整体识别')
        self.button_close = QtWidgets.QPushButton(u'退出')
 
 
        #Button 的颜色修改
        button_color = [self.button_open_camera,  
                        self.button_take_pic,
                        self.button_rg_face,
                        self.button_rg_gender,
                        self.button_rg_all,
                        self.button_close,]
        for i in range(6):
            button_color[i].setStyleSheet("QPushButton{color:black}"
                                          "QPushButton:hover{color:red}"
                                          "QPushButton{background-color:rgb(78,255,255)}"
                                          "QPushButton{border:2px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}")
 
        self.button_open_camera.setMinimumHeight(50)
        self.button_take_pic.setMinimumHeight(50)
        self.button_rg_face.setMinimumHeight(50)
        self.button_rg_gender.setMinimumHeight(50)
        self.button_rg_all.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)
 
        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。

        self.move(0, 0)
 
        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        # 
        self.label_move.setFixedSize(100,0)
        # 整个窗口边框大小
        self.label_show_camera.setFixedSize(1820, 980)
        self.label_show_camera.setAutoFillBackground(False)
        # 按钮顺序
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_take_pic)
        self.__layout_fun_button.addWidget(self.button_rg_face)
        self.__layout_fun_button.addWidget(self.button_rg_gender)
        self.__layout_fun_button.addWidget(self.button_rg_all)
        self.__layout_fun_button.addWidget(self.button_close)
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
        # 定义表情性别识别方法
        self.button_rg_gender.clicked.connect(self.button_rg_gender_click)
        # 定义全体识别方法
        self.button_rg_all.clicked.connect(self.button_rg_all_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)
    def button_take_pic_click(self):
        '''录入人脸模块'''
        text, okPressed = QInputDialog.getText(self, "输入用户名","Your name:", QLineEdit.Normal, "")
        print(text)
        self.name = text
        # test.take_photo(name=self.name)
        test.take_photo(self.name)
        # self.choice = 5
    def button_rg_face_click(self):
        '''人脸识别模块'''
        #self.show_camera()
        # 更新人脸库
        update_face()
        print("完成人脸库更新")
        # print("开始识别")
        # 1 点击 如果摄像头关闭 先打开摄像头
        # self.button_open_camera_click()
        # # 2 进入人脸识别部分，加载识别模块
        # # 3 获取
        # face = rg_face(self.cap)
        # self.show_camera(face)

        self.choice = 2
    def button_rg_gender_click(self):
        '''性别表情识别模块'''
        print("开始性别表情识别")
        self.choice = 3
    def button_rg_all_click(self):
        '''整体识别模块'''
        pass
    def button_open_camera_click(self):
        '''打开摄像头'''
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
            self.choice=1
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'打开相机')
            
 
 
    def show_camera(self):
        if self.choice ==1:
            #print(self.choice)
            flag, self.image = self.cap.read()
            # print(self.image)
            # face = self.face_detect.align(self.image)
            # if face:
            #     pass
            # 相机窗口大小
            show = cv2.resize(self.image, (1820,980))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            # print(show.shape[1], show.shape[0])
            #show.shape[1] = 640, show.shape[0] = 480
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
            # self.x += 1
            # self.label_move.move(self.x,100)
    
            # if self.x ==320:
            #     self.label_show_camera.raise_()
        elif self.choice == 2:
            # 1 加载模型 人脸识别
            conf = get_config(False)
            mtcnn = MTCNN()
            print('mtcnn loaded')
            learner = face_learner(conf, True)
            # learner.threshold = args.threshold
            if conf.device.type == 'cpu':
                learner.load_state(conf, 'cpu_final.pth', True, True)
            else:
                learner.load_state(conf, 'final.pth', True, True)
            learner.model.eval()
            face_image = rg_face(self.cap,conf=conf,mtcnn=mtcnn,learner=learner)
            show = cv2.resize(face_image, (1820, 980))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        elif self.choice == 3:
            # 表情识别
            print(self.timer_camera.isActive())
            face_image = get_emotion_gender(self.cap)
            show = cv2.resize(face_image, (1820, 980))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        
        elif self.choice ==4:
            # 整体识别
            pass
        elif self.choice ==5:
           pass
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