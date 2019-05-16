import cv2
from PIL import Image
import argparse
from pathlib import Path
from multiprocessing import Process, Pipe,Value,Array
import torch
from config import get_config
from mtcnn import MTCNN
from Learner import face_learner
from utils import load_facebank, draw_box_name, prepare_facebank
import time
# 调用之前摄像头已经打开
# conf = get_config(False)

# mtcnn = MTCNN()
# print('mtcnn loaded')

# learner = face_learner(conf, True)
# # learner.threshold = args.threshold
# if conf.device.type == 'cpu':
#     learner.load_state(conf, 'cpu_final.pth', True, True)
# else:
#     learner.load_state(conf, 'final.pth', True, True)
# learner.model.eval()
# print('learner loaded')
def rg_face(cap,conf,mtcnn,learner):
    """params : cap 摄像头
                conf
                mtcnn
                learner 
    """
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-s", "--save", help="whether save",action="store_true")
    parser.add_argument('-th','--threshold',help='threshold to decide identical faces',default=1.54, type=float)
    # 更新人脸识别库
    parser.add_argument("-u", "--update", help="whether perform update the facebank",action="store_true")
    parser.add_argument("-tta", "--tta", help="whether test time augmentation",action="store_true")
    # 是否显示置信度得分
    parser.add_argument("-c", "--score", help="whether show the confidence score",action="store_true")
    args = parser.parse_args()

    conf = get_config(False)

    # mtcnn = MTCNN()
    # print('mtcnn loaded')
    
    # learner = face_learner(conf, True)
    # learner.threshold = args.threshold
    # if conf.device.type == 'cpu':
    #     learner.load_state(conf, 'cpu_final.pth', True, True)
    # else:
    #     learner.load_state(conf, 'final.pth', True, True)
    # learner.model.eval()
    # print('learner loaded')
    targets, names = load_facebank(conf)
    print('facebank loaded')
        # frame rate 6 due to my laptop is quite slow...
    while cap.isOpened():
        isSuccess,frame = cap.read()
        if isSuccess:            
            try:
                image = Image.fromarray(frame[...,::-1]) #bgr to rgb
#
                print("1")
                bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
                print("2")
                bboxes = bboxes[:,:-1] #shape:[10,4],only keep 10 highest possibiity faces
                print("3")
                bboxes = bboxes.astype(int)
                print("4")
                bboxes = bboxes + [-1,-1,1,1] # personal choice    
                print("5")
                results, score = learner.infer(conf, faces, targets,)
                print("6")
                for idx,bbox in enumerate(bboxes):
                    frame = draw_box_name(bbox, names[results[idx] + 1], frame)
                    print(names[results[idx] + 1])
                        # 这里增加表情以及年龄模块
  
            except:
                print('detect error')    
            # return cv2.imshow('',frame)
            return frame

            #cv2.imshow('face Capture', frame)
          