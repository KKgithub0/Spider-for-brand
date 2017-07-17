#coding=utf-8
import urllib
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
import time

def get_taobao():
    driver.get("https://www.taobao.com/")
    time.sleep(3)
    content = driver.page_source
    tree = etree.HTML(content)
    nodes = tree.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li')
#    print len(nodes)
    query_list = []
    for i in range(1, len(nodes)):
        ele = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li[%d]' % i)
        ActionChains(driver).move_to_element(ele).perform()
        time.sleep(3)
        content = driver.page_source
        tree = etree.HTML(content)
        items = tree.xpath('/html/body/div[4]/div[1]/div[1]/div/div[3]/div[@data-index="%d"]/div[1]/*/*/a' % (i - 1))
 #       print len(items)
        for item in items:
            try:
                query_list.append(item.text.encode('utf-8', 'ignore'))
            except:
                continue
        
    return query_list

def get_detail(brand):
    url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170705&ie=utf8&spm=a21bo.50862.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=' + urllib.quote(brand) + '&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest'
    driver.get(url)
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="J_NavCommonRow_0"]/div[3]/span[2]').click()
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
        nodes = tree.xpath('//*[@id="J_NavCommonRowItems_0"]/a')
    except:
        return
#    print len(nodes)
    output = []
    for node in nodes:
        try:
 #           print node.xpath('@title')[0].encode('utf-8')
            output.append(node.xpath('@title')[0].encode('utf-8'))
        except:
            continue
    f.write(brand + '\t' + '\\'.join(output) + '\n')
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    query_list = get_taobao()
    visited_list = []
    with open('/Users/xuyikai/Downloads/work/spider/brand/taobao_brand.txt', 'a+') as f:
        for query in query_list:
            if query not in visited_list:
                get_detail(query)
    driver.close()