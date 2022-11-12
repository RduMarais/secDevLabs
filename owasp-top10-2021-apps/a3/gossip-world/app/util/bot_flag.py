from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
import re
import time
import os
from bs4 import BeautifulSoup
import subprocess


class BotSession:

    def __init__(self,debug,flag=''):
        self.DEBUG = debug
        self.session = requests.Session()
        proxy_selenium = None
        if(self.DEBUG):
            proxy_selenium=Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': 'http://127.0.0.1:8080' })
        self.driver = webdriver.Firefox(proxy=proxy_selenium)
        self.csrf_token = ''
        self.user_name = 'user_flag'
        self.user_pass = 'Fl4gUs3r_priv'
        # self.headers =  {'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User':'?1'}
        self.proxy_servers = {}
        if(self.DEBUG):
            self.proxy_servers = {'http':'http://127.0.0.1:8080'}

        if(flag):
            self.flag_value = flag
        else:
            self.flag_value=''
            with open("app/util/.flag.txt", "r") as flag_file:
                self.flag_value=flag_file.read().splitlines()[0] # this looks complicated but it just removes the \n at the end
        if(self.DEBUG):
            print('flag value : '+self.flag_value)

    def init_web_driver(self):
        # init web driver
        self.driver.get('http://localhost:10007')
        self.driver.add_cookie({'name':'flag','value':self.flag_value,'httpOnly':False,'secure':False})
        if(self.DEBUG):
            print('driver initiated')
            # print(self.driver.get_cookies())

    def __enter__(self):
        return self

    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.driver.quit()
        print('exiting...')

    def get_csrf_token(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        self.csrf_token = soup.select_one('input[name="_csrf_token"]')['value']
        if(self.DEBUG):
            print("new csrf token : "+self.csrf_token)

    # create the user
    def create_user_flag(self):
        r = self.session.get("http://localhost:10007/register",proxies=self.proxy_servers)
        self.get_csrf_token(r)
        r = self.session.post("http://localhost:10007/register",data={'_csrf_token':self.csrf_token,'username':self.user_name,'password1':self.user_pass,'password2':self.user_pass,'_csrf_token':self.csrf_token},proxies=self.proxy_servers)
        if(self.DEBUG):
            print('### user creation')
            # print(r.content)

    # log in and updates cookies
    def update_user_cookie(self):
        r = self.session.get("http://localhost:10007/login",proxies=self.proxy_servers)
        self.get_csrf_token(r)
        r = self.session.post("http://localhost:10007/login",data={'_csrf_token':self.csrf_token,'username':self.user_name,'password':self.user_pass,'_csrf_token':self.csrf_token},proxies=self.proxy_servers)
        if(self.DEBUG):
            print('### user connection')

    def update_cookie_session_to_driver(self):
        cookie_dict = self.driver.get_cookie('session')
        cookie_dict['value'] = self.session.cookies.get('session')
        self.driver.delete_cookie('session')
        del cookie_dict['domain']
        del cookie_dict['secure']
        del cookie_dict['sameSite']
        del cookie_dict['path']   # test
        del cookie_dict['httpOnly'] # test
        self.driver.add_cookie(cookie_dict)
        if(self.DEBUG):
            print("### cookie updated session -> webdriver")

    def update_cookie_driver_to_session(self):
        cookie_str = self.driver.get_cookie('session')['value']
        self.session.cookies.clear()
        self.session.cookies.set('session',cookie_str,domain='localhost.local',path='/')
        if(self.DEBUG):
            print("### cookie updated webdriver -> session")

    def print_session_cookies(self,prefix):
        if(self.DEBUG):
            print(prefix+"driver  cookie : "+str(self.driver.get_cookie('session')['value']))
            print(prefix+"session cookie : "+str(self.session.cookies.get('session')))

    def loop_check(self):
        while(True):
            print('-- scan starting')

            # self.update_user_cookie()

            # get gossips with session
            r = self.session.get("http://localhost:10007/gossip")
            gossips = re.findall("href=\"/gossip/\\d{1,4}\"",str(r.content))
            print("-- "+str(len(gossips))+" gossips found")
    
            # pass on session cookies to driver
            self.update_cookie_session_to_driver()

            # browse gossips with web driver
            for gossip in gossips:
                url = 'http://localhost:10007/gossip/'+gossip[14:-1]
                self.update_cookie_session_to_driver()
                # self.print_session_cookies('pre  > ')
                self.driver.get(url)
                # self.print_session_cookies('post > ')


                print("---- gossip "+gossip[14:-1] + f" : done ({url})")

            # pass on driver cookies to session
            self.update_cookie_driver_to_session()

            print('-- scan done, --> time to sleep')
            
            time.sleep(20)




with BotSession(True) as bot:
    # create user
    bot.create_user_flag()

    # initialize the session cookie
    bot.update_user_cookie()

    bot.init_web_driver()

    bot.loop_check()


