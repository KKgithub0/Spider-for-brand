#coding=utf-8
import sys
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def get_58():
    driver.get("http://bj.58.com/zhiyepeix/?key=%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD&cmcskey=%E6%95%99%E8%82%B2&jump=3&searchtype=1&sourcetype=5&pgtid=0d303877-0000-1bb4-1f72-1170ffb264d4&clickid=2")
    time.sleep(1)

    type_nodes = driver.find_elements_by_xpath('//*[@id="ObjectType"]/a')
    for node in type_nodes:
        type_list.append(node.text.encode('utf-8', 'ignore'))
        
#    section_nodes = driver.find_elements_by_xpath('//*[@id="local"]/a')
#    for node in section_nodes:
#        section_list[node.text.encode('utf-8', 'ignore')] = node
   
def get_detail(types):
    driver.get("http://bj.58.com/zhiyepeix/?key=%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD&cmcskey=%E6%95%99%E8%82%B2&jump=3&searchtype=1&sourcetype=5&pgtid=0d303877-0000-1bb4-1f72-1170ffb264d4&clickid=2")
    time.sleep(2)
    type_nodes = driver.find_elements_by_xpath('//*[@id="ObjectType"]/a')
    for type in type_nodes:
#        print type.text.encode('utf-8', 'ignore')
        if (type.text.encode('utf-8', 'ignore')) == types:
 #       type_list[node.text.encode('utf-8', 'ignore')] = node
            chains = ActionChains(driver)
            chains.click(type).perform()
            time.sleep(2)
            section_nodes = driver.find_elements_by_xpath('//*[@id="local"]/a')
            for i in range(1, len(section_nodes)):
                node = driver.find_element_by_xpath('//*[@id="local"]/a[%d]' % i)
                outstr = types + '\t' + node.text.encode('utf-8', 'ignore')
                chains = ActionChains(driver)
                chains.click(node).perform()
                time.sleep(3)
                items = driver.find_elements_by_xpath('//*[@class="sellername"]')
                result = []
                for item in items:
                    '''
                    print item.xpath('div/p[@class="item-tags"]/span[2]/@title')[0].encode('utf-8')
                    #if u'认证'.encode('utf-8','ignore') not in node.xpath('//*[@class="item-tags"]').
                    if '认证' not in item.xpath('div/p[@class="item-tags"]/span[2]/@title')[0]:
                        continue 
                    res = item.xpath('div/p[@class="seller"]')[0]
                    '''
                    res = item.text.encode('utf-8', 'ignore')
                    if res not in result and '*' not in res:
        #              print res
                        result.append(res)
                f.write(outstr + '\t' + '\\'.join(result) + '\n')
            break
    
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
#    section_list = dict()
    type_list = []
    get_58()
    visited_list = []
    with open('/Users/xuyikai/Downloads/work/spider/brand/58_brand.txt', 'a+') as f:
        for types in type_list:
            get_detail(types)
    driver.close()