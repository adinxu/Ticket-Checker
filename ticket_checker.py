#!/usr/bin/python3
import requests
import os
import sys
import time
import selenium
from enum import Enum
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

class TICKET_TYPE(Enum):
    NONE   = 0
    V_930  = 1
    SV_930 = 2
    V_101  = 3
    SV_101 = 4

class PLAT_TYPE(Enum):
    XIUDONG  = "秀动"
    DAMAI    = "大麦"

ticket_name={
                TICKET_TYPE.NONE    :"",
                TICKET_TYPE.V_930   :"930 v", 
                TICKET_TYPE.SV_930  :"930 sv",
                TICKET_TYPE.V_101   :"101 v",
                TICKET_TYPE.SV_101  :"101 sv"
            }

class USERS():
    def __init__(self,sk:str,t:set()) -> None:
        self.sk = sk
        self.t = t
        pass 
    def notify(self, plat:PLAT_TYPE, msg:str):
        requests.get("https://sctapi.ftqq.com/"+ self.sk +".send?title=" +plat.value+" "+ " : " + msg)

    def notify_ticket_state(self, plat:PLAT_TYPE, p_type:TICKET_TYPE, msg:str):
        if p_type in self.t:
            self.notify(plat,ticket_name[p_type] + " state is " + msg)

#=================val need to config==========================#
plat = PLAT_TYPE.XIUDONG
chrome_driver_path = "/Users/xuweidong/chromedriver-mac-arm64/chromedriver"
phone_nums = ["11111111111", "22222222222"]
MAIN_URL = "https://wap.showstart.com/pages/activity/detail/detail?activityId=203508"
need_select_people = True
me = USERS("SCTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",{TICKET_TYPE.SV_930,TICKET_TYPE.SV_101})
users_to_notify= \
    [   
        me,                                                                                                       #me      930 sv 101 sv
        #USERS("SCTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",{TICKET_TYPE.SV_930,TICKET_TYPE.SV_101}),                      #vanilla  930 101 sv
    ]
auto_pay_set = {}
#=================val need to config==========================#
def get_phone_num():
    global phone_num
    phonenum_list_str = ""
    for i,p in enumerate(phone_nums):
        phonenum_list_str+=f"{i} {p}\n"

    while True:
        phone_num_index =int(input(f"select phone num between 0 to {len(phone_nums)-1} \n{phonenum_list_str}:")) 
        if phone_num_index < 0 or phone_num_index > len(phone_nums):
            print("wrong select")
            time.sleep(1)
            continue
        phone_num =  phone_nums[phone_num_index]
        print(f"start with phone num {phone_num}")
        break


def notify_all_users_ticket_state(type:TICKET_TYPE, msg:str):
    global plat
    for u in users_to_notify:
        u.notify_ticket_state(plat,type,msg)
    pass

class TICKET_RES():
    def __init__(self) -> None:
        self.res = "票已售罄"
        pass
    def clear(self):
        self.res = "票已售罄"
    def ischange(self, curr_res:str) -> bool:
        if curr_res != self.res:
            self.res = curr_res
            return True
        else:
            return False

class DRIVER():
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        #self.options.add_argument("--headless")
        self.service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        pass
    def access_page(self,page:str):
        self.driver.get(page)
        time.sleep(5)

    def click(self,ele:str,delay = 1, by:str=By.XPATH):
        self.driver.find_element(by,ele).click()
        time.sleep(delay)

    def send_keys(self,ele:str,content:str,by:str=By.XPATH):
        self.driver.find_element(by,ele).send_keys(content)
        time.sleep(1)

    def get_content(self,ele:str,by:str=By.XPATH) -> str:
        return self.driver.find_element(by,ele).text
    
    def refresh(self):
        self.refresh()
        time.sleep(5)
    
class MAIN_PAGE():
    def __init__(self,start_page,start_login_btn,phonenum_input,code_input,login_checkbox,getcode_btn,login_btn,open_ticket_page_btn,close_ticket_page_btn) -> None:
        self.start_page             = start_page
        self.start_login_btn        = start_login_btn
        self.phonenum_input         = phonenum_input
        self.code_input             = code_input
        self.login_checkbox         = login_checkbox
        self.getcode_btn            = getcode_btn
        self.login_btn              = login_btn
        self.open_ticket_page_btn   = open_ticket_page_btn
        self.close_ticket_page_btn  = close_ticket_page_btn
        pass

class PAY_PAGE():
    def __init__(self,start_pay,open_select_people_win,select_first_people,close_select_people_win,pay,close_pay) -> None:
        self.start_pay               = start_pay
        self.open_select_people_win  = open_select_people_win
        self.select_first_people     = select_first_people
        self.close_select_people_win = close_select_people_win
        self.pay                     = pay
        self.close_pay               = close_pay
        pass

class TICKET_PAGE():
    def __init__(self, select_date_btn:str, select_ticket_btn:str, res_text:str) -> None:
        self.select_date_btn        = select_date_btn
        self.select_ticket_btn      = select_ticket_btn
        self.res_text               = res_text
        pass
#these element need be reconfig when new url is set!!!!!!!
web_ticket_page_dict = {
        TICKET_TYPE.NONE    :None,
        TICKET_TYPE.V_930   :TICKET_PAGE(
            select_date_btn         = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]",
            select_ticket_btn       = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[3]",
            res_text                = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[3]/uni-view[1]/uni-view[1]/uni-view/uni-text/span",
        ), 
        TICKET_TYPE.SV_930  :TICKET_PAGE(
            select_date_btn         = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]",
            select_ticket_btn       = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[4]",
            res_text                = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[4]/uni-view[1]/uni-view[1]/uni-view/uni-text/span",
        ),
        TICKET_TYPE.V_101   :TICKET_PAGE(
            select_date_btn         = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[3]",
            select_ticket_btn       = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[3]",
            res_text                = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[3]/uni-view[1]/uni-view[1]/uni-view/uni-text/span",
        ),
        TICKET_TYPE.SV_101  :TICKET_PAGE(
            select_date_btn         = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[3]",
            select_ticket_btn       = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[4]",
            res_text                = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[4]/uni-view[1]/uni-view[1]/uni-view/uni-text/span",
        ),
}

class TICKET_CHECKER():
    #class var
    driver = DRIVER()
    main_page = MAIN_PAGE( 
        start_page              = MAIN_URL,
        start_login_btn         = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]",
        phonenum_input          = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-form/span/uni-view[1]/uni-view[2]/uni-input/div/input",
        code_input              = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-form/span/uni-view[2]/uni-view[1]/uni-input/div/input",
        login_checkbox          = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-view[2]/uni-checkbox-group/uni-label/uni-checkbox/div/div",
        getcode_btn             = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-form/span/uni-view[2]/uni-view[2]",
        login_btn               = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-form/span/uni-button",
        open_ticket_page_btn    = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]",
        close_ticket_page_btn   = "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[1]/uni-view[1]"
    )
    pay_page = PAY_PAGE(
        start_pay="/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view/uni-view[2]/uni-view",
        open_select_people_win="/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view/uni-view[2]/uni-view",
        select_first_people="/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view[2]/uni-view/uni-view[2]/uni-scroll-view/div/div/div/uni-checkbox-group/uni-label[1]/uni-checkbox/div/div",
        close_select_people_win="/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view[2]/uni-view/uni-view[1]/uni-view[2]",
        pay="/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view[2]",
        close_pay= "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[10]/uni-view/uni-view[2]/uni-view/uni-view[1]/uni-view[2]" 
    )
    select_people = need_select_people

    def __init__(self,type:TICKET_TYPE,ticket_page:TICKET_PAGE)-> None:
        self.type = type
        self.ticket_page = ticket_page
        self.res = TICKET_RES()
        pass
    @classmethod
    def prepare(cls):
        cls.driver.access_page(cls.main_page.start_page)
        cls.driver.click(cls.main_page.start_login_btn)
        cls.driver.send_keys(cls.main_page.phonenum_input,phone_num)
        cls.driver.click(cls.main_page.login_checkbox)
        cls.driver.click(cls.main_page.getcode_btn)
        vcode = input("请输入6位验证码:")
        cls.driver.send_keys(cls.main_page.code_input,vcode)
        cls.driver.click(cls.main_page.login_btn)
        pass
    @classmethod
    def pay_on_ticket_win(cls):
        me.notify(plat,"try to pay...")
        cls.driver.click(cls.pay_page.start_pay)
        if cls.select_people:
            cls.driver.click(cls.pay_page.open_select_people_win) 
            cls.driver.click(cls.pay_page.select_first_people) 
            cls.driver.click(cls.pay_page.close_select_people_win) 
            pass
        cls.driver.click(cls.pay_page.pay)
        cls.driver.click(cls.pay_page.close)
        me.notify(plat,"pay success...")
        #restart
        raise()

    def get_res(self) -> str:
        self.driver.click(self.ticket_page.select_date_btn,0)
        return self.driver.get_content(self.ticket_page.res_text)
        pass
    def auto_pay(self):
        self.driver.click(self.ticket_page.select_ticket_btn)
        self.pay_on_ticket_win()
        pass
    def process_once(self):
        self.driver.click(self.main_page.open_ticket_page_btn)
        r = self.get_res()
        if self.res.ischange(r):
            notify_all_users_ticket_state(self.type,r)
            if self.type in auto_pay_set:
                self.auto_pay()
        self.driver.click(self.main_page.close_ticket_page_btn)

    @classmethod
    def reset(cls):
        cls.driver.access_page(cls.main_page.start_page)
        cls.driver.refresh()
    def clear_res(self):
        self.res.clear()
    pass

def do_work():
    count = 0
    while True:
        for t in task_list:
            t.process_once()

        count = count +1 
        if count == 100:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            print(f"running on {phone_num}...") 
        elif count > 100:
            count=0
        pass

if __name__ == "__main__":
    get_phone_num()
    task_list = [
        TICKET_CHECKER(TICKET_TYPE.V_930,web_ticket_page_dict[TICKET_TYPE.V_930]),
        TICKET_CHECKER(TICKET_TYPE.SV_930,web_ticket_page_dict[TICKET_TYPE.SV_930]),
        TICKET_CHECKER(TICKET_TYPE.V_101,web_ticket_page_dict[TICKET_TYPE.V_101]),
        TICKET_CHECKER(TICKET_TYPE.SV_101,web_ticket_page_dict[TICKET_TYPE.SV_101])
    ]
    TICKET_CHECKER.prepare()
    while True:
        try:
            do_work()
            pass
        except Exception as e:
            print(f"error occur : {e}")
            me.notify(plat,"error occur")
            TICKET_CHECKER.reset()
            for t in task_list:
                t.clear_res()
            pass
            continue
