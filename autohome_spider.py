#coding=utf-8
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time


def get_autohome():
    driver.get("http://www.autohome.com.cn/car/")
    time.sleep(1)

    type_nodes = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div[1]/div/div[1]/dl/*/a')
    for node in type_nodes:
        type_list.append(node.text)
        
#    section_nodes = driver.find_elements_by_xpath('//*[@id="local"]/a')
#    for node in section_nodes:
#        section_list[node.text.encode('utf-8', 'ignore')] = node
   
def get_types(types, res):
    driver.get("http://www.autohome.com.cn/car/")
    type_nodes = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div[1]/div/div[1]/dl/*/a')
    for node in type_nodes:
        if node.text == types:
            chains = ActionChains(driver)
            chains.click(node).perform()
            time.sleep(3)
            price_nodes = driver.find_elements_by_xpath('//*[@id="param-box"]/dd[1]/div[2]/ul/*/a')
            price_list = list()
            for price_node in price_nodes:
                price_list.append(price_node.text)
            for price in price_list:
                get_price(price, res + types.encode('utf-8', 'ignore'))
            break
            
def get_price(price, res): 
        price_nodes = driver.find_elements_by_xpath('//*[@id="param-box"]/dd[1]/div[2]/ul/*/a')
        for node in price_nodes:
            if node.text == price:
                try:
                    ActionChains(driver).click(node).perform()
                    select_node = driver.find_element_by_xpath('//*[@id="view-tab"]/li[2]')
                    ActionChains(driver).click(select_node).perform()
                except:
                    continue
                car_nodes = driver.find_elements_by_xpath('//*[@id="tab-content"]/div[3]/*/div[2]/ul/li')
                info = ''
                for car in car_nodes:
                    car_info = car.text.split('\n')
                    info += '\t' + '|'.join(i.encode('utf-8', 'ignore') for i in car_info[0:-1])
                f.write(res + '\t' + price.encode('utf-8', 'ignore') + '\t' + info + '\n')
                break
               
    
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
#    section_list = dict()
    type_list = list()
    get_autohome()
    with open('/Users/xuyikai/Downloads/work/spider/brand/autohome_spider.txt' ,'a+') as f:
        for item in type_list[1:]:
            time.sleep(1)
            get_types(item, '')
   
    driver.close()