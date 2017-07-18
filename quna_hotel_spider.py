#coding=utf-8
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time


def get_quna_hotel():
    driver.get("http://hotel.qunar.com/city/beijing_city/#fromDate=2017-07-18&cityurl=beijing_city&from=qunarHotel&toDate=2017-07-19&QHFP=ZSI0A5484F56")
    time.sleep(1)

    type_nodes = driver.find_elements_by_xpath('//*[@id="gradeFilter"]/div/div/ul/li/em[@title]')
    for node in type_nodes:
#        print node.text
        type_list.append(node.text)
   
def get_types(types):
    driver.get("http://hotel.qunar.com/city/beijing_city/#fromDate=2017-07-18&cityurl=beijing_city&from=qunarHotel&toDate=2017-07-19&QHFP=ZSI0A5484F56")
    type_nodes = driver.find_elements_by_xpath('//*[@id="gradeFilter"]/div/div/ul/li/em[@title]')
    for node in type_nodes:
        if node.text == types:
            chains = ActionChains(driver)
            chains.click(node).perform()
            time.sleep(3)
            brand_nodes = driver.find_elements_by_xpath('//*[@id="brandFilter"]/div/div/ul/li/em[@title]')
            brand_list = list()
            for brand_node in brand_nodes:
                brand_list.append(brand_node.text.encode('utf-8', 'ignore'))
            try:
                more_node = driver.find_element_by_xpath('//*[@id="brandFilter"]/div/div/p[2]/a')
                ActionChains(driver).click(more_node).perform()
                time.sleep(2)
                content = driver.page_source
                tree = etree.HTML(content)
                all_nodes = tree.xpath('//*[@id="brandFilter"]/div/div/div[2]/div/div/div/ul/li')
                for brand in all_nodes:
                    res = brand.xpath('em/@title')[0].encode('utf-8', 'ignore')
                    if res not in brand_list:
                        brand_list.append(res)
            except:
                print 'no more'
                pass
            f.write(types.encode('utf-8', 'ignore') + '\t' + '|'.join(i for i in brand_list if i != '') + '\n')
            break
    
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
#    section_list = dict()
    type_list = list()
    get_quna_hotel()
    
    with open('/Users/xuyikai/Downloads/work/spider/brand/quna_hotel_spider.txt' ,'a+') as f:
        for item in type_list:
            time.sleep(1)
            get_types(item)
    
    driver.close()