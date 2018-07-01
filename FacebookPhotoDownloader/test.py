import re
import os
import time
import requests
from urllib.request import urlopen
import urllib
from urllib.error import HTTPError

try:
    image_src = 'https://scontent-lax3-2.xx.fbcdn.net/v/t1.0-0/q81/p206x206/31949105_1655270151216694_1071723047636959232_n.jpg?_nc_cat=0&oh=024564b6ff0a119aad9ef52afff28d6f&oe=5B965065'
    #image_src = 'https://static.bufferoverflow.cn/full//e770cf763ea4f067fa0518431b8d689518658ba1.jpg'

    proxies =  {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087",
    }
    ir = requests.get(image_src,timeout=10, proxies=proxies)
    if ir.status_code == 200:
        open(os.path.join(os.getcwd(), 'sdsd.jpg'), 'wb').write(ir.content)

except HTTPError as e:
    print(e.code)
    print(e)


#
#
# print
# pattern = re.compile(r'(.*?)&fref.*?',re.S)
# pattern = re.compile(r'(.*?)\?fref.*?',re.S)
#
# friend_link = 'https://www.facebook.com/profile.php?id=2434sw.2...?3&fref'
# friend_link = 'https://www.facebook.com/sadam.umarbsk?fref=pb&hc_location=friends_tab'
# print (len(friend_link))
# print (friend_link[25:])
# print (friend_link[10:])

# friend_link = friend_link[25:]
# print (friend_link)
# groups = re.findall(pattern,friend_link);
# print (groups[0])
# pattern = re.compile('https://www.facebook.com/profile.php?id=(.*?)&fref',re.S)
