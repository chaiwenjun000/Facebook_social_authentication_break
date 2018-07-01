from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from blog.models import BlogsPost
from blog.models import IMG
from blog.models import ImgEncoding
# Create your views here.
import face_recognition
import cv2
import os
import json
from mysite import settings
import numpy as np

def blog_index(request):
    blog_list = BlogsPost.objects.all()
    return render(request, 'index.html', {'blog_list': blog_list})

def blog_verify_face_recognition(request):
    pass

def blog_train_face_recognition(request):
    # 先跑一边模型加载。
    face_recognition.compare_faces
    # 照片路径
    #friends_images_path = 'media/friends_images2_faces/'
    #friends_images_path = '/Users/pro/fb_zhouwei/chaiwnejun_bishe/face_recognition_demo/special_friend_img'

    #训练集合样本
    friends_images_path = '/Users/pro/fb_zhouwei/chaiwenjun_bishe/face_recognition_demo/train_img'

    # 已知照片的人脸编码列表
    # 遍历路径下的文件
    for filename in os.listdir(friends_images_path):
        # 忽略macos 的 .DS_Store
        if filename.startswith('.'):
            continue
        image_path = friends_images_path + '/' + filename
        print(image_path)
        friend_image = face_recognition.load_image_file(image_path)
        # 只获取第一个人的 人脸编码 和 名称
        # print (face_recognition.face_encodings(friend_image))
        # break
        # print(face_recognition.face_encodings(friend_image))
        friend_face_encoding = face_recognition.face_encodings(friend_image)

        if len(friend_face_encoding) != 0:
            friend_face_encoding = friend_face_encoding[0]
            #print(type(friend_face_encoding))
            face_name = filename.split('.')[0]
            settings.known_face_encodings.append(friend_face_encoding)
            settings.known_face_names.append(face_name)

            #将获得的 人脸编码保存到数据库。
            img_encoding = ImgEncoding(
                name = face_name,
                face_recognition_encoding = friend_face_encoding
            )
            img_encoding.save()
        # request.session['known_face_encodings'] = json.dumps(settings.known_face_encodings)
        # request.session['known_face_names'] = json.dumps(settings.known_face_names)

    print(settings.known_face_names)
    # 跳转到 上传页面
    #return render(request, 'img_tem/uploadimg.html')
    return HttpResponse('建模成功')

def sort_dict(dict_words):
    """
    字典排序
    :param dict_words:
    :return:
    """
    keys = dict_words.keys()
    values = dict_words.values()
    list_one = [(key, val) for key, val in zip(keys, values)]
    list_sort = sorted(list_one, key=lambda x: x[1], reverse=False)
    return list_sort

def blog_face_verify(request):
    # settings.known_face_names = request.session.get['known_face_names']
    # settings.known_face_encodings = request.session.get['known_face_encodings']

    if request.method == 'POST':

        image_path = request.FILES.get('img')
        print('图片上传路径',image_path)
        predict_image = face_recognition.load_image_file(image_path)
        predict_face_encodings = face_recognition.face_encodings(predict_image)
        # 遍历一张图中多个脸 编码信息
        name = 'unknown'

        # 存放图片中所有脸对应的名称
        name_list = []
        dis_list = []
        for i in range(len(predict_face_encodings)):
            predict_encoding = predict_face_encodings[i]

            # 将已知人脸的编码，和未知人脸的编码作比较，结果存入results数组中
            # results 数组中的每一个元素都是True 或者 False
            # results 数组与已知人脸一一对应
            print(type(predict_encoding))
            print(type(settings.known_face_encodings))
            face_distances = face_recognition.face_distance(settings.known_face_encodings, predict_encoding)
            ans = {}
            for i, face_distance in enumerate(face_distances):
                # print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
                # print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
                # print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
                name = settings.known_face_names[i]
                ans[name] = face_distance
                # print(name,face_distance)
            ans = sort_dict(ans)
            cnt = 0

            for key in ans:
                name_list.append(key[0])
                dis_list.append(key[1])
                cnt += 1
                if cnt == 1:
                    print('识别结果', key)
                    print('备选项：')
                    continue
                print(key)
                if cnt == 6:
                    break

        # predict_image_rgb = cv2.cvtColor(predict_image, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Output",predict_image_rgb)
        # cv2.waitKey(0)
        name_list_string = " \n ".join(name_list)
        name_list_string = ""
        for i in range(len(name_list)):
            name_list_string += ("<h3>" + str(i) + "</h3><p>" + name_list[i] + "</p>")

        print('savename: ', name_list_string)
        new_img = IMG(
            img = image_path,
            name = name_list_string
        )
        new_img.save()
        print(request.FILES.get('img'))
        print(new_img)
        # new_img.save()
        print('识别结果存储成功')
        content = {
            'img': new_img,
            'name_list':name_list,
            'dis_list':dis_list,
        }
        return render(request, 'img_tem/show_verify.html', content)
def blog_uploadimg(request):
    # settings.known_face_encodings = []
    # settings.known_face_names =[]
    # img_encodings = ImgEncoding.objects.all()
    #
    # for i in img_encodings:
    #     settings.known_face_encodings.append(np.array(i.face_recognition_encoding))
    #     settings.known_face_names.append(i.name)

    if request.method == 'POST':

        image_path = request.FILES.get('img')
        print('图片上传路径', image_path)
        predict_image = face_recognition.load_image_file(image_path)
        predict_face_encodings = face_recognition.face_encodings(predict_image)
        # 遍历一张图中多个脸 编码信息
        name = 'unknown'

        # 存放图片中所有脸对应的名称

        name_list = []
        for i in range(len(predict_face_encodings)):
            predict_encoding = predict_face_encodings[i]

        # 将已知人脸的编码，和未知人脸的编码作比较，结果存入results数组中
        # results 数组中的每一个元素都是True 或者 False
        # results 数组与已知人脸一一对应
            print(type(predict_encoding))
            print(type(settings.known_face_encodings))
            results = face_recognition.compare_faces(settings.known_face_encodings, predict_encoding)
            for j in range(len(results)):
                if results[j]:
                    name = settings.known_face_names[j]
                    print('the picture is ' + image_path.name + ", predicted the people is " + name)
                    name_list.append(name)
                    # 在图片中标注姓名
                    #           cv2.putText(predict_image,name,(left-10,top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    break
        # predict_image_rgb = cv2.cvtColor(predict_image, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Output",predict_image_rgb)
        # cv2.waitKey(0)
        #name_list_string = " \n ".join(name_list)
        name_list_string = ""
        for i in range(len(name_list)):
            name_list_string += ("<h3>"+str(i)+"</h3><p>" + name_list[i]+"</p>")

        print('savename: ',name_list_string)
        new_img = IMG(
            img = request.FILES.get('img'),
            name = name_list_string
        )
        new_img.save()
        print('识别结果存储成功')
        content = {
            'img': new_img
        }
        return render(request,'img_tem/show_uploadimg.html',content)
        # return redirect('/showimg');
        #
# GET
    return render(request, 'img_tem/uploadimg.html')

def blog_showimg(request):
    imgs = IMG.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        print(i.img.url)
    return render(request, 'img_tem/showimg.html', content)
