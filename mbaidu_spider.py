#coding=utf-8
import sys
import urllib
import threading
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")

Max_page = 2
def get_mbaidu(driver, brand, url, count, res_file):
    try:
        driver.get(url)
    except TimeoutException:
        pass
    finally:
        try:
            recom_nodes = WebDriverWait(driver, 2).until(lambda x: x.find_elements_by_xpath("//*[@class='c-container']/a[*[contains(text(),'_相关')]]"))
#            recom_nodes = driver.find_elements_by_xpath("//*[@class='c-container']/a[*[contains(text(),'_相关')]]")
            if len(recom_nodes) != 0:
                for recom_node in recom_nodes:
    #                    print recom_node.text
                    brand_json = dict()
                    brand_json[u'query'] = '%s' % brand
                    href = recom_node.get_attribute('href')
                    driver.get(href)
                    if get_brands(driver, brand_json):
                        res_file.write(json.dumps(brand_json, ensure_ascii=False) + '\n')
                    driver.back()
            else:
                #go_next_page(count)
                return          
        except:
#            go_next_page(count)
            return
'''
def go_next_page(count):
    try:
        if count == 1:
            next_page = WebDriverWait(driver, 2).until(lambda x: x.find_element_by_xpath('//*[@id="page-controller"]/div/a')).get_attribute('href')
            get_mbaidu(driver, brand, next_page, count + 1)
        elif count < Max_page:
            next_page = WebDriverWait(driver, 2).until(lambda x: x.find_element_by_xpath('//*[@id="page-controller"]/div/div[3]/a')).get_attribute('href')
            get_mbaidu(driver, brand, next_page, count + 1) 
    except:
        pass
'''        
def get_brands(driver, brand_json):
#    print 'enter get_brands'
    try:
        header = driver.find_element_by_xpath("//*[contains(text(),'_相关')]")
#        print 'get correct'
        driver.find_element_by_xpath("//*[contains(text(),'展开更多')]").click()
        brand_json[u'recom_title'] = header.text
        brand_json[u'data'] = []
        brands_node = driver.find_elements_by_xpath('//*[@class="c-span3"]/a')
        for brands in brands_node:
            dic = dict()
            brand_img = brands.find_element_by_xpath('div/img').get_attribute('src')
            dic[u'img'] = brand_img
            dic[u'name'] = brands.find_element_by_xpath('p[1]').text
            dic[u'desc'] = brands.find_element_by_xpath('p[2]').text
            brand_json[u'data'].append(dic)
        return True
    except NoSuchElementException:
#        print 'zjy error'
        return False

def spider(file_in, i):
 #   driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')phantomjs
    driver = webdriver.PhantomJS('/Users/xuyikai/phantomjs')
    print get_time() + '\t%s start' % file_in
    driver.implicitly_wait(3)
    driver.set_page_load_timeout(3)
    driver.set_script_timeout(3)
    res_file = open('/Users/xuyikai/Downloads/work/spider/brand/mbaidu_brand%s.txt' % (i) ,'a+')
    visited_set = set()
    with open('/Users/xuyikai/Downloads/work/spider/brand_dir/%s' % file_in, 'r') as f:
        for line in f:
            brand = line.strip().decode('utf-8', 'ignore')
            if brand == '':
                continue
            if brand in visited_set:
                continue
            visited_set.add(brand)
            time.sleep(1)
#            url = "http://m.baidu.com/?normalload=1#|src_" + urllib.quote(brand.encode('utf-8', 'ignore')) + "|sa_ib"
            url = 'http://dbl-wise-yqpui023-jx.dbl01.baidu.com:8080/s?word=' + urllib.quote(brand.encode('utf-8', 'ignore')) + '&ts=5217023&t_kt=371&sa=ib&rsv_sug4=6419&inputT=2652&ss=100'
            get_mbaidu(driver, brand, url, 1, res_file)
            
    print get_time() + '\t%s end' % file_in
    res_file.close()
    driver.quit()         
    
        
ab = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i', 'j','k','l' ,'m']#,'n','o','p','q','r','s','t']#,'u','v','w', 'x','y','z']   
if __name__ == '__main__':
    thread_list = list()
    for i in ab:
        file_in = 'query_%s' % (i)
        thread_list.append(threading.Thread(target = spider, args = (file_in, i)))
    for thread in thread_list:
        thread.setDaemon(True)
        thread.start()
    for thread in thread_list:
        thread.join()
        
   
