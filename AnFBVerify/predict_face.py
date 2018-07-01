# -*- coding: utf-8 -*-

from skimage import io,transform
import tensorflow as tf
import numpy as np
import os
import cv2
import dlib

#数据集地址
path='./Faces'
#要识别的图片的地址
image_path='./PredictedFaces'
#处理后的图片的地址
re_image_path='./RePredictedFaces'
#模型保存地址
model_path='./Model/model.ckpt.meta'

size=64
w=100
h=100
c=3

#把人名组成字典，来对应结果
faces_dict = {}
def get_labels(path):
    index = 0
    for dir in os.listdir(path):
        faces_dict[index] = dir
        index += 1

get_labels(path)
print (faces_dict)

#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()

#处理图片
def re_image(path):
    for filename in os.listdir(path):
        im_path=path+'/'+filename
        # 从文件读取图片
        img = cv2.imread(im_path)
        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用detector进行人脸检测 dets为返回的结果
        dets = detector(gray_img, 1)

        #使用enumerate 函数遍历序列中的元素以及它们的下标
        #下标i即为人脸序号
        #left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离
        #top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0
            # img[y:y+h,x:x+w]
            face = img[x1:y1,x2:y2]
            # 调整图片的尺寸
            face = cv2.resize(face, (size,size))
            #cv2.imshow('image',face)
            # 保存图片
            cv2.imwrite(re_image_path+'/'+filename, face)

            key = cv2.waitKey(30) & 0xff
            if key == 27:
                sys.exit(0)
            
re_image(image_path)

#获取要识别的处理后的图片地址
data_path = []
def get_image_path(path):
    for filename in os.listdir(path):
        im_path=path+'/'+filename
        data_path.append(im_path)
        
get_image_path(re_image_path)
print (data_path)

def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    data = []
    for d in data_path:
        data.append(read_one_image(d))

    #恢复模型
    saver = tf.train.import_meta_graph(model_path)
    saver.restore(sess,tf.train.latest_checkpoint('./Model/'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)

    #打印出预测矩阵
    print(classification_result)
    #打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    #根据索引通过字典对应人的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        print("第",i+1,"个人预测:"+faces_dict[output[i]])