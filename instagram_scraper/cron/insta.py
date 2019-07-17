# -*- coding: utf-8 -*-
import os
import psycopg2
import sys
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from instagram_scraper import db
from flask_script import Command
from instagram_scraper.model.insta import User, Comment, Post
from instagram_scraper.api.user import create_comment,create_post,create_user


cwd = os.getcwd()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def after_login():
    curr_url="https://www.instagram.com/accounts/login"
    while(curr_url != "https://www.instagram.com/"):
        print("Please Wait while we log you in....")
        curr_url=driver.execute_script("return document.URL")
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()

def login_insta():
    url = "https://www.instagram.com/accounts/login"
    driver.get(url)
    driver.find_element_by_name("username").send_keys(uname)
    driver.find_element_by_name("password").send_keys(pwd)
    driver.find_element_by_css_selector("button[type='submit']").click()
    after_login()

def login_fb():
    driver.find_element_by_class_name("KPnG0").click()
    driver.find_element_by_name("email").send_keys(uname)
    driver.find_element_by_name("pass").send_keys(pwd)
    driver.find_element_by_css_selector("button[type='submit']").click()
    after_login()

class Insta(Command):

    def run(self):
        
        user=str(input("Enter the username : "))
        url = "https://www.instagram.com/" + user
        print("\n Current Url : ",url)

        u_exists=False
        try:
            users=User.query.all()
            print("\nLoaded Users")
            for i in users:
                if "@"+user == i.handle:
                    u_exists=True
                    new_user=i
                    print("\n ",user," Already Exists....")
        except:
            users=None
        
        if(u_exists):
            try:
                last_post=Post.query.order_by(Post.created_at).first()
            except:
                last_post=None

        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            #options.add_argument('--headless')
            driver = webdriver.Chrome(cwd + '/instagram_scraper/driver/chromedriver', options=options)
            driver.get(url)
        except:
            print("\nFailed to load Chrome Driver")
        
        try:
            pub=driver.find_element_by_class_name("rkEop").get_attribute("innerHTML")
            print(pub)
            ch=str(input("This profile is Private. Would you like to login ? (y/n) : "))
            if ch=='y' or ch=='Y':
                login_insta()
            else:
                print("Cant work with private profiles. Follow the user ?")
        except Exception as e:
            print("Loaded Profile is public")


        try:
            photo_total = int(driver.find_element_by_class_name("g47SY").text.replace(".", "").replace(",", ""))
            username = driver.execute_script("return document.title.split(\"(\")[0].substr(0,document.title.split(\"(\")[0].length-1)").translate(non_bmp_map)
            taghandle = driver.execute_script("return document.title.split(\"(\")[1].split(\")\")[0]").translate(non_bmp_map)
            followers=int(driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title"))
            print("\nNumber of Followers : ",followers)
            print("\nTotal number of posts : ", photo_total)
            print("\nSelected User : ", username)
            print("\nInsta Handle : ",taghandle)
            if u_exists:
                print("User already Exists")
            else:
                new_user=create_user(name=username,i_handle=taghandle)
        except Exception as e:
            print("Error Occured : \n",e)

        #print("Loaded User : ",new_user.username,"\t User ID : ",new_user.id)
        
        filename=user+"links.txt"
        
        try:
            imgLinks = [line.rstrip('\n') for line in open(filename,"r+")]
        except Exception as e:
            imgLinks=[]
            print(str(e).split("]")[1][1:])

        print("\nLoading Post Links\n\n Post \t Link")
        
        try:
            wf=open(cwd+"/instagram_scraper/imagelinks/"+filename,"w+")
        except Exception as e:
            print(e)

        try:
            last_height = driver.execute_script("return document.body.scrollHeight")
            while len(imgLinks) < 20: #photo_total:
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except Exception as e:
                    pass
                    #print("\n Scroll Error : ",e)
                try:
                    imgList = driver.find_elements_by_css_selector(".v1Nh3 a")
                except Exception as e:
                    pass
                    #print("Get Error : ",e)
                try:
                    for idx, img in enumerate(imgList):
                        link = img.get_property("href")
                        if not link in imgLinks:
                            imgLinks.append(link)
                            print(len(imgLinks),"\t",link)
                            wf.write("%s\n" % link)
                        else:
                            break
                except Exception as e:
                    pass
                    #print("Link Error : ",e)
            wf.close()
        except Exception as e:
            pass
            #print("\n Post Link Error : ",e)

        pic_path="/home/stark/Desktop/Images/"+username
        
        try:
            os.mkdir(pic_path)
        except Exception as e:
            print(e)
        
        try:
            for i in imgLinks:
                try:
                    driver.get(i)
                except Exception as error:
                    print(error)
                hasMoreComments=True
                while hasMoreComments:
                    try:
                        if driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button/span'):
                            print("Loading More Comments")
                            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li/div/button/span').click()
                    except Exception as e:
                        hasMoreComments=False
                        print("Error loading more comments")
                
                users_list=[]
                text_list=[]
                
                try:
                    WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,"_6lAjh")))
                    comment_users=driver.find_elements_by_class_name('_6lAjh')
                    for a in comment_users:
                        users_list.append(a.text)
                except Exception as e:
                    print("Error getting Users who commented. : ",e)
                print("\n\n Loading Comments")
                comments_count=len(users_list)
                i1=0 
                try:
                    WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,"C4VMK")))
                    comments=driver.find_elements_by_class_name('C4VMK')
                    for a in comments:
                        text_list.append(a.text.split(users_list[i1])[1].replace("\r", " ").replace("\n", " "))
                        i1+=1
                except Exception as e:
                    print("Error loading comments : ",e)

                try:
                    for j in range(1, comments_count):
                        user = users_list[j].translate(non_bmp_map)
                        text = text_list[j].translate(non_bmp_map)
                        print("User ", user)
                        print("Text ", text)
                        idxs = [m.start() for m in re.finditer('@', text)]
                        for idx in idxs:
                            handle = text[idx:].split(" ")[0]
                            print(handle)
                except:
                    print("No comments Found....")

        except Exception as e:
            print("Error while downloading the post : ",e)


