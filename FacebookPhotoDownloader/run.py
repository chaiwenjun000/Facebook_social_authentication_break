import sys, os, time, re
from urllib.request import urlopen
import urllib
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
# Selenium 初始化
driver = webdriver.Chrome()

# 將視窗放到最大，因為 Facebook 會隨著瀏覽器長寬，來決定不同的圖片尺寸
driver.maximize_window()
wait = WebDriverWait(driver,10)
# 登入 FaceBook
def loginFacebook(url):
    # 走訪連結
    print('0')
    driver.get(url_login)
    print('1')
    # 填入 email 帳號
    elem_email = driver.find_element_by_name("email")
    elem_email.clear()
    elem_email.send_keys("youremail@gmail.com")
    
    # 輸入密碼
    elem_pass = driver.find_element_by_name("pass")
    elem_pass.clear()
    elem_pass.send_keys("yourpassword")
    
    # 按下登入鈕（這個 loginbutton 是個 label）
    elem_btn_login = driver.find_element_by_id("loginbutton")
    elem_btn_login.click()
def isElementExist(element):
    flag = True
    try:
        driver.find_elements_by_css_selector(element)
        return flag
    except Exception as e:
        flag = False
        return flag


def getFriendsList(user_id,url):
    driver.get(url)

    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    elm_li = driver.find_elements_by_css_selector("ul._262m li")

    print ("len1 : ",len(elm_li))
    print ("len 51sx :",len(driver.find_elements_by_css_selector("a._51sx")))
    
    #滑到底部，监测一个标签的数量，如果为1，则图片还没有加载完全
    
    while 1 == len(driver.find_elements_by_css_selector("a._51sx")):
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(3)
     

    elm_li = driver.find_elements_by_css_selector("ul._262m li")

    print ("len2 :",len(elm_li))

    try:
        friend_names = []
        friend_ids = []
        #inStart = False
        for index, li in enumerate(elm_li):
            elm_a = li.find_elements_by_css_selector('a')

            print ('cnt ',index)

            print ('len elm_a',len(elm_a))
            friend_link = ""
            possible_f_link = ""
            head_img_link = ""
            cnt = 0
            for ea in elm_a:
                #print(cnt,ea.get_attribute('href'))
                cnt += 1
                possible_f_link = ea
                if cnt == 1 and "friends_tab" in possible_f_link.get_attribute('href'):
                    head_img_link = possible_f_link.find_elements_by_css_selector('img')
                if cnt != 1 and "friends_tab" in possible_f_link.get_attribute('href'):
                    friend_link = possible_f_link.get_attribute('href')
                    break
            if friend_link == "":
                print ('bug link',friend_link)
                continue
            else:
                print(possible_f_link.text,friend_link)


            friend_name = possible_f_link.text

            #下载头像
            if head_img_link != "":
                #print(head_img_link)
                head_img_link = head_img_link[0]

                image_src = head_img_link.get_attribute("src")
                # 用正規表達式，來取得檔案名稱與副檔名
                p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
                m = p.findall(image_src)
                try:
                    path = 'downloads/friend531/'+user_id+'/'+friend_name
                    path_exist = path + '/'+m[0][0];
                    # 重复的不下载
                    if os.path.exists(path_exist):
                        continue
                    if not os.path.exists(path):
                        os.makedirs(path)
                    proxies = {
                        "http": "http://127.0.0.1:1087",
                        "https": "http://127.0.0.1:1087",
                    }

                    ir = requests.get(image_src, timeout=10, proxies=proxies)# 通过代理请求image_src图片地址，超过10s则报超时异常
                    if ir.status_code == 200:#如果http状态吗200则请求成功
                          open(os.path.join(os.getcwd(), path + '/' + m[0][0]), 'wb').write(ir.content)#打开指定位置，保存图片
                    #
                    # image = urlopen(image_src)
                    # f = open( os.path.join(os.getcwd(), path+'/' + m[0][0]), 'wb' )
                    # time.sleep(1)
                    # f.write( image.read() )
                    # f.close()
                except Exception as e:
                    print(e.code)
                    print(e)
                    print("{} cant't be read".format(m[0][0]))
                    return
            
            if 'profile.php' in friend_link:
                pattern = re.compile(r'(.*?)&fref',re.S)
                friend_link = friend_link[40:]
            else:
                pattern = re.compile(r'(.*?)\?fref',re.S)
                friend_link = friend_link[25:]
           
            friend_id = re.findall(pattern,friend_link);
            if friend_id:
                friend_id = friend_id[0]
            print("index: ",len(friend_ids))
            print ("id: ",friend_id," name: ", friend_name)

            #time.sleep(5)
            
            friend_ids.append(friend_id)
            friend_names.append(friend_name)
        
        start = True
        for i in range(len(friend_ids)):
            # 朋友的关于自己的照片url
            photo_url = 'https://www.facebook.com/'+friend_ids[i]+'/photos_all'
            #if friend_names[i] == 'Real Delva':
             #   start = True
            if start:
                parseFriendPhotoPage(user_id,friend_names[i],photo_url,i)
    except Exception as e:
        print ("bug",e)

        #elm_a[0].click()
        #break


def parseFriendPhotoPage(user_id,name,url,i):
    print('正在打印  -- ',user_id,'的朋友 ',i,name)
    # 走訪連結
    driver.get(url)
    
    # 按下 ESC，讓半透明背景消失
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    
    while 1 == len(driver.find_elements_by_css_selector("a._51sx")):
        js="var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)
        time.sleep(3)

    # 取得 Photo 列表的照片連結
    elm_li = driver.find_elements_by_css_selector("ul._69n li")
    
    # 轉成 list 後進行迭代處理
    for index, li in enumerate(elm_li):
        # 节约时间，只抓取10张
        # if index == 5:
        #     break
        try:
            print ('第'+str(index)+'张')
            # 取得圖片連結並按下，使其跳出實際的圖片
            elm_a = li.find_elements_by_css_selector('a._6i9')

            #elm_a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a._6i9')[0])

            #time.sleep(2)
            elm_a[0].click()

            # 由於圖片讀取時，縱然未下載完成，也當成讀取完成（FB 可能用串流讀取），
            # 所以這裡單純讓程式停置幾秒，讓圖片可以順利下載，而非縮圖
            time.sleep(3)
            
            # 取得圖片放大後的連結
            elm_img = driver.find_element_by_css_selector('img.spotlight')
            image_src = elm_img.get_attribute("src")

            print('img_src: ',image_src)
            # 用正規表達式，來取得檔案名稱與副檔名
            p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
            m = p.findall(image_src)
            
            # 按下關閉圖示，準備開下一張圖片
            driver.find_element_by_css_selector('a._418x').click()
        
            # 下載圖片到本機端
            try:
                path = 'downloads/friend1/'+user_id+'/'+name
                path_exist = path + '/'+m[0][0];
                # 重复的不下载
                if os.path.exists(path_exist):
                    continue
                if not os.path.exists(path):
                    os.makedirs(path)

                # 使用代理，抓取国外的图片,如果不需要则把下面requests的proxies参#数删除
                proxies = {
                    "http": "http://127.0.0.1:1087",
                    "https": "http://127.0.0.1:1087",
                }

                ir = requests.get(image_src, timeout=10, proxies=proxies)
                if ir.status_code == 200:
                    open(os.path.join(os.getcwd(), path +'/'+ m[0][0]), 'wb').write(ir.content)

            except Exception as e:
                print(e)
                print("{} cant't be read".format(m[0][0]))
        except:
            continue



try:


    # 登入頁面
    url_login = 'https://www.facebook.com/'
    loginFacebook(url_login)
    
    #user_id = '100024474816940'
    #friends_list_url = 'https://www.facebook.com/profile.php?id=100024474816940&sk=friends'

    user_id = '100022949192135'
    friends_list_url = 'https://www.facebook.com/profile.php?id=100022949192135&sk=friends'

    getFriendsList(user_id,friends_list_url)

    
    # 分析照片頁面
    #url_photo = 'https://www.facebook.com/DarrenYang1002/photos'
    # url_photo = 'https://www.facebook.com/100010793533723/photos'
    # [   'https://www.facebook.com/qiyao.liu.3/photos', # QiyaoLiu
    #     'https://www.facebook.com/shaoxiong.wang.1/photos',  # Shaoxiong Wang
         
    # ]
    # parseFriendPhotoPage(url_photo)
    
    # 粉絲團照片一覽
    #url_photo_fan_group = 'https://www.facebook.com/pg/turtledrawturtle/photos/'
    #parseFanGroupPhotoPage(url_photo_fan_group)
    
except TimeoutException:
    print("TimeoutException: \n", sys.exc_info())

except WebDriverException:
    print("WebElementException: \n", sys.exc_info())

except NoSuchElementException:
    print("NoSuchElementException: \n", sys.exc_info())

except:
    print("Unexpected error: \n", sys.exc_info())
    
finally:
    driver.quit()
