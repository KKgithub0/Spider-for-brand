#coding=utf-8
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time
import json

Max_page = 3
def get_mbaidu(brand, url, count):
    time.sleep(1)
    driver.get(url)
    try:
        recom_nodes = driver.find_elements_by_xpath("//*[@class='c-container']/a[*[contains(text(),'_相关')]]")
        if len(recom_nodes) != 0:
            for recom_node in recom_nodes:
                print recom_node.text
                brand_json = dict()
                brand_json[u'query'] = '%s' % brand
                href = recom_node.get_attribute('href')
                driver.get(href)
                if get_brands(brand_json):
                    res_file.write(json.dumps(brand_json, ensure_ascii=False) + '\n')
                driver.back()
                time.sleep(1)
        else:
            go_next_page(count)            
    except:
        go_next_page(count)

def go_next_page(count):
    if count == 1:
        print 'get %s page' % str(count + 1)
        next_page = driver.find_element_by_xpath('//*[@id="page-controller"]/div/a').get_attribute('href')
        get_mbaidu(brand, next_page, count + 1)
    elif count < Max_page:
        print 'get %s page' % str(count + 1)
        next_page = driver.find_element_by_xpath('//*[@id="page-controller"]/div/div[3]/a').get_attribute('href')
        get_mbaidu(brand, next_page, count + 1) 
        
def get_brands(brand_json):
    print 'enter get_brands'
    try:
        header = driver.find_element_by_xpath("//*[contains(text(),'_相关')]")
        print 'get correct'
        brand_json[u'recom_title'] = header.text
        brand_json[u'data'] = []
        driver.find_element_by_xpath("//*[contains(text(),'展开更多')]").click()
        brands_node = driver.find_elements_by_xpath('//*[@class="c-span3"]/a')
        for brand in brands_node:
            dic = dict()
            brand_img = brand.find_element_by_xpath('div/img').get_attribute('src')
            dic[u'img'] = brand_img
            dic[u'name'] = brand.find_element_by_xpath('p[1]').text
            dic[u'desc'] = brand.find_element_by_xpath('p[2]').text
            brand_json[u'data'].append(dic)
        return True
    except:
        print 'zjy error'
        return False
            
    
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    res_file = open('/Users/xuyikai/Downloads/work/spider/brand/mbaidu_spider.txt' ,'w')
    with open('/Users/xuyikai/Downloads/work/spider/brand/mbaidu_brand.txt', 'r') as f:
        for line in f:
            brand = line.strip()
            if brand == '':
                continue
            time.sleep(3)
            url = "http://m.baidu.com/?normalload=1#|src_" + urllib.quote(brand.encode('utf-8', 'ignore')) + "|sa_ib"
            get_mbaidu(brand, url, 1)

    
    driver.close()