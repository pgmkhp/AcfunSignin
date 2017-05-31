# coding:utf8

from selenium import webdriver
import urllib2
import time
import json
import os

# 模拟登陆获取cookie，并将其保存到文件
def get_cookie(account, passwd):
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get('http://www.acfun.cn/login/')

    account_input = driver.find_element_by_id('ipt-account-login')
    passwd_input = driver.find_element_by_id('ipt-pwd-login')
    account_input.clear()
    passwd_input.clear()
    account_input.send_keys(account)
    passwd_input.send_keys(passwd)
    driver.find_element_by_class_name('btn-login').click()
    time.sleep(4)

    cookie = {}
    for item in driver.get_cookies():
        cookie[item['name']] = item['value']

    # 保存cookie到文件中
    cookie_file = open('cookie', 'w')
    cookie_file.write(json.dumps(cookie))
    cookie_file.close()
    driver.quit()
    return cookie


# 签到函数
def signin(account, passwd):
    # 判断cookie文件是否存在，存在则使用文件中的cookie，若不存在则获取cookie并创建
    if os.path.exists('cookie'):
        cookie_file = open('cookie', 'r')
        cookie = json.loads(cookie_file.readline())
        cookie_file.close()
    else:
        cookie = get_cookie(account, passwd)
    
    cookie_list = [{'name':k, 'value':v} for k, v in cookie.items()]

    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get('http://www.acfun.cn')
    for item in cookie_list:
        driver.add_cookie(item)
    
    driver.get('http://www.acfun.cn/member/')

    # 当cookie过期时，获取新的cookie
    if driver.current_url != 'http://www.acfun.cn/member/':
        cookie = get_cookie(account, passwd)
        cookie_list = [{'name':k, 'value':v} for k, v in cookie.items()]
        for item in cookie_list:
            driver.add_cookie(item)
        driver.get('http://www.acfun.cn/member/')
    
    driver.find_element_by_id('btn-sign-user').click()
    if driver.find_element_by_id('btn-sign-user').text == '签到':
        print '签到失败'
    else:
        print '签到成功'
    
    driver.quit()


if __name__ == '__main__':
    account = '' # 用户名
    passwd = '' # 密码
    signin(account, passwd)