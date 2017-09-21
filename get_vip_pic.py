#coding=utf-8
import sys
from selenium import webdriver
import time
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

def get_category():
    driver.get("http://category.vip.com/")
    time.sleep(1)
    
    nodes = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]//li/a')
    query_set = set()
    for node in nodes:
        query_set.add(node.get_attribute('href'))    
    return query_set

def get_detail(url):
    driver.get(url)
    time.sleep(1)
    try:
        driver.find_element_by_xpath('//*[@id="J_catOperArea"]/div[1]/div[1]/dl[1]/dd[2]/span[1]').click()
    except Exception, e:
        #print 'cannot find more'
        #print url
        pass
    #time.sleep(3)
    content = driver.page_source
    tree = etree.HTML(content)
    pic_list = tree.xpath('//*[@id="J_catOperArea"]/div[1]/div[1]/dl[1]/dd[1]/div[1]/div[1]/div[1]/a')
    #pic_list = driver.find_elements_by_xpath('//*[@id="J_catOperArea"]/div[1]/div[1]/dl[1]/dd[1]/div[1]/div[1]/div[1]/a')
    for pic_info in pic_list:
        title = pic_info.xpath('@title')[0]
        pic = pic_info.xpath('img/@data-original')[0]
        #title = pic_info.get_attribute('title')
        #pic = pic_info.find_element_by_xpath('img').get_attribute('src')
        if title not in pic_dic.keys():
            pic_dic[title] = pic
        #pic_dic.append(title + '\t' + pic)
if __name__ == '__main__':
    driver = webdriver.PhantomJS('/Users/xuyikai/phantomjs')
    query_set = get_category()
    print len(query_set)
    pic_dic = dict()
    count, t = 0 , 1
    for url in query_set:
        get_detail(url)
        count += 1
        if count >= 50 and count % 50 == 0:
            print count
            print 'pic_dic : ' + str(len(pic_dic))
    print len(pic_dic)
    with open('/Users/xuyikai/Downloads/work/spider/brand/vip_brand.txt', 'a+') as f:
        for k, v in pic_dic.iteritems():
            f.write(k + '\t' + 'http:' + v + '\n')
    driver.close()
    