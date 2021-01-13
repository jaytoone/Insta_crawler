from selenium import webdriver  # 라이브러리(모듈) 가져오라
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from tqdm import tqdm_notebook
import re
import json
from time import sleep
from datetime import datetime
import time


from urllib import parse

keyword = '거실'
url_tmp = "www.instagram.com/explore/tags/" + keyword
url = "http://" + parse.quote(url_tmp)
print(url)

user_data_path = 'D:/PycharmProject/Instar_Scrapper/tmp/Instar'
options = Options()
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-gpu')
options.add_argument("user-data-dir=%s" % user_data_path)
options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome("../chromedriver.exe", options=options)  # 크롬 드라이버 로드

driver.get(url)  # "keyword" 검색
driver.implicitly_wait(3)
# print(driver.page_source)  # results

#       Login Once      #
# login_btn_class = 'sqdOP.L3NKy.y3zKF'
# login_btn = driver.find_element_by_class_name(login_btn_class)
# # login_btn.click()
# # driver.implicitly_wait(3)
#
# #       Input Login info      #
# user_id = ''
# user_pw = ''
# id_box = driver.find_element_by_name('username')
# pw_box = driver.find_element_by_name('password')
# id_box.send_keys(user_id)
# pw_box.send_keys(user_pw)
# pw_box.send_keys(Keys.RETURN)
# # driver.close()
# # quit()
# driver.save_screenshot('test.jpg')
# 사진 클릭
CSS_tran = "div.Nnq7C.weEfm"  # 사진 버튼 정의 ("div.Nnq7C.weEfm")
tran_button = driver.find_element_by_css_selector(CSS_tran)  # 사진 버튼 찾기
AC(driver).move_to_element(tran_button).click().perform()  # 사진 버튼 클릭
time.sleep(1)

# 크롤링 시작
len_insta = 10000  # 몇 개 글을 크롤링 할건지

dict_ = {}
for i in range(0, len_insta):  # range : 숫자가 1씩하는 함수

    target_info = {}  # 사진별 데이터를 담을 딕셔너리 생성
    try:
        # 사진(pic) 크롤링 시작
        # overlays1 = "div._2dDPU.vCf6V.FFVAD"  # 사진창 속 사진   # "RzuR0 kHt39  plVq-
        # overlays1 = "div.RzuR0.kHt39.plVq-.eLAPa._23QFA.KL4Bh.FFVAD"  # 사진창 속 사진   #
        # xpath1 = '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img'
        # class1 = 'FFVAD'
        class1 = 'PdwC2.fXiEu.s2MYR'     # 사진창
        pic_frame = driver.find_element_by_class_name(class1)
        class2 = 'KL4Bh'        # one more frame
        pic_frame2 = pic_frame.find_element_by_class_name(class2)
        # img = driver.find_element_by_css_selector(overlays1)  # 사진 선택
        # img = driver.find_element_by_xpath(xpath1)  # 사진 선택
        class3 = 'FFVAD'
        img = pic_frame2.find_element_by_class_name(class3)  # 사진 선택
        print('img :', img)
        pic = img.get_attribute('src')  # 사진 url 크롤링 완료
        target_info['picture'] = pic
        print('pic :', pic)

        # 날짜(date) 크롤링 시작
        overlays2 = "c-Yi7>time"  # 날짜 지정
        # datum2 = driver.find_element_by_css_selector(overlays2)  # 날짜 선택
        datum2 = driver.find_element_by_class_name(overlays2)  # 날짜 선택
        date = datum2.get_attribute('title')
        #         get_attribute('title')                                    # 날짜 크롤링 완료
        target_info['date'] = date
        # print(target_info)
        print('date :', date)

        # 좋아요(like) 크롤링 시작
        overlays3 = ".Nm9Fw"  # 리뷰창 속 날짜
        datum3 = driver.find_element_by_css_selector(overlays3)  # 리뷰 선택 <-- selector working ? working
        like = datum3.text  # 좋아요 크롤링 완료
        target_info['like'] = like
        # print(target_info)
        print('like :', like)

        # 해시태그(tag) 크롤링 시작
        overlays4 = ".C7I1f.X7jCj"  # 태그 지정
        datum3 = driver.find_element_by_css_selector(overlays4)  # 태그 선택
        tag_raw = datum3.text
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)  # ""#OOO"만 뽑아오기(OOO: 한글,숫자,영어,_)
        tag = ''.join(tags).replace("#", " ")  # "#" 제거
        target_info['tag'] = tag
        # print(target_info)
        print('tag :', tag)

        dict_[i] = target_info  # 토탈 딕셔너리로 만들기

        print("{0} saved!".format(i))

        # 다음장 클릭
        hit = 0
        while hit < 1:  # 몇 번에 한번씩 크롤링할 것인지 숫자 지정
            hit += 1
            CSS_tran2 = "a._65Bje.coreSpriteRightPaginationArrow"  # 다음 버튼 정의
            tran_button2 = driver.find_element_by_css_selector(CSS_tran2)  # 다음 버튼 find
            AC(driver).move_to_element(tran_button2).click().perform()  # 다음 버튼 클릭
            time.sleep(2)

    except Exception as e:
        print(e)
        # 다음장 클릭
        CSS_tran2 = "a._65Bje.coreSpriteRightPaginationArrow"  # 다음 버튼 정의
        tran_button2 = driver.find_element_by_css_selector(CSS_tran2)  # 다음 버튼 find
        AC(driver).move_to_element(tran_button2).click().perform()  # 다음 버튼 클릭
        time.sleep(2)

driver.close()
driver.quit()

print(dict_)
crawl_date = str(datetime.now()).split(' ')[0]
with open('./Insta_Data/%s.json' % crawl_date, 'w') as fp:
    json.dump(dict_, fp)
