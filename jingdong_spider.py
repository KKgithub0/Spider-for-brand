#coding=utf-8
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time

def get_brand(brand):
    url = 'https://search.jd.com/Search?keyword=' + urllib.quote(brand) + '&enc=utf-8&wq=shou%27ji&pvid=f748b2de8a2a4b97b7b9c17c3535b4e7'
    driver.get(url)
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="J_selector"]/div[1]/div/div[3]/a[1]').click()
    except:
        try:
            driver.get(url)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="J_selector"]/div[1]/div/div[3]/a[1]').click()
        except:
            return 
    time.sleep(3)
    #//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul
#    elem = driver.find_element_by_xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul')
    content = driver.page_source
    #print content
    tree = etree.HTML(content)
    #nodes = tree.xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul/li')
    try:
        nodes = tree.xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul/li')
    except:
        return
    output = []
    for node in nodes:
        try:
            output.append(node.xpath('a/@title')[0].encode('utf-8'))
        except:
            continue
    f.write(brand + '\t' + '\\'.join(output) + '\n')
        #.decode('utf-8','ignore').encode('gbk', 'ignore')
        
def get_trade(query):       
    url = 'https://search.jd.com/Search?keyword=' + urllib.quote(query) + '&enc=utf-8&wq=%E5%8D%8E%E4%B8%BA&pvid=57d099012c7b494688118c3d1345e495'
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    #    print response.read()
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    #'<strong>分类：</strong>.*?确定'      
    content = response.read()
    pattern = re.compile('J_selectorLine s\-category.*?确定', re.S)
    items = re.findall(pattern, content)
    for item in items:
        brand_pattern = re.compile('title=\".*?\"')
        arrs = re.findall(brand_pattern, item)
        for arr in arrs:
            brand = arr.strip('title=\"')
            get_brand(brand)

def get_jd():
    get_query = list()
#    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    url = 'https://www.jd.com/'
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
    #    print response.read()
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        
    content = response.read()
    pattern = re.compile('<!-- leftcate start -->.+?<!-- leftcate start -->', re.S)
    items = re.findall(pattern, content)
    for item in items:
        query_pattern = re.compile('\">.+?</a>')
        query_list = re.findall(query_pattern, item)
        for query in query_list:
            arrs = query.strip('\"><[a-zA-Z0-9]/\.').split('>')
            if len(arrs) == 1:
                get_query.append(arrs[0])
            else:
                get_query.append(arrs[2])
                
    driver.get("https://www.jd.com/")
    time.sleep(3)
    ele = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/div/ul/li[1]/a')
    ActionChains(driver).move_to_element(ele).perform()
    time.sleep(5)
    content = driver.page_source
    #print content
    tree = etree.HTML(content)
    #    print tree
    #nodes = tree.xpath('//*[@id="J_selector"]/div[1]/div/div[2]/div[2]/ul/li')
    nodes = tree.xpath('/html/body/div[5]/div[1]/div[1]/div/div/div[@class="cate_part clearfix"]')
    for node in nodes:
        items = node.xpath('div[1]/div[2]/*/dd/a')
        for item in items:
            get_query.append(item.text.encode('utf-8','ignore'))
    #    driver.close()
    
    return get_query
      
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    query_list = get_jd()
    visited_list = []
    print len(query_list)
    with open('/Users/xuyikai/Downloads/work/spider/brand/jingdong_brand.txt', 'a+') as f:
        for brand in query_list:
            time.sleep(1)
            if brand not in visited_list:
                visited_list.append(brand)
                get_brand(brand)

    driver.close()
      
      
