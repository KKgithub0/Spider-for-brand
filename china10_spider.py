#coding=utf-8

import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import threading
reload(sys)
sys.setdefaultencoding('utf-8')

def get_trade_url(url):
    try:
        driver.get(url)
    except:
        pass
    finally:
        trade_nodes = driver.find_elements_by_xpath('//*[@id="conmenu"]/li')
        i = 1
        for node in trade_nodes:
            trade_url = list()
            ActionChains(driver).move_to_element(node).perform()
            elements = driver.find_elements_by_xpath('//*[@id="conmenu"]/li[%s]/div/ul/li/a' % str(i))
            i += 1
            for ele in elements:
                herf = ele.get_attribute('href')
                title = ele.get_attribute('title')
                trade_url.append(title + '|' + herf)
            arg = '\t'.join(trade_url)
            thread_list.append(threading.Thread(target = spider, args = (arg,)))

def get_detail(driver, k, url):
    try:
        driver.get(url)
    except:
        pass
    finally:
        detail_dic = dict()
        try:
            nodes = driver.find_elements_by_xpath('//*[@id="pagebelowcat"]/ul/li/a')
            for node in nodes:
                herf = node.get_attribute('href')
                detail_dic[node.text] = herf
        except:
            detail_dic[k] = url
        return detail_dic

def get_brand(driver, trade, url, brand_url):
    try:
        driver.get(url)
    except:
        pass
    finally:
        try:
            res = list()
            try:
                nodes = driver.find_elements_by_xpath('//*[@id="top10"]/div/div[2]/dl/dt/a[1]')
                for node in nodes:
                    res.append(node.get_attribute('title'))
                    brand_url[node.get_attribute('title')] = node.get_attribute('href')
            except:
                pass
            try:
                nodes = driver.find_elements_by_xpath('//*[@id="rightlay"]/div[3]/div[1]/div[2]/a')
                for node in nodes:
                    res.append(node.get_attribute('title'))
                    brand_url[node.get_attribute('title')] = node.get_attribute('href')
            except:
                pass

            threadLock.acquire()
            trade_brand_file.write(trade + '\t' + '|'.join(res) + '\n')
            threadLock.release()
        except:
            print trade + '\tget top brand error'
            pass
 
def get_info(driver, k, url):
    info_dic = dict()
    try:
        driver.get(url)
    except:
        pass
    finally:
        try:
            driver.find_element_by_xpath('//*[@id="rightlay"]/div[2]/div[1]/div[2]/div[3]/a[contains(text(),"更多品牌介绍")]').click()
        except:
            pass
        try:
            desc = ''
            nodes = driver.find_elements_by_xpath('//*[@id="rightlay"]/div[2]/div[1]/div[2]/div[2]/p')
            for node in nodes:
                desc += node.text.strip()
            info_dic['Desc'] = desc
        except:
            info_dic['Desc'] = 'unknown'
        try:
            img_node = driver.find_element_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/div[1]/div[1]/a/div/img')
            info_dic['Img'] = img_node.get_attribute('src')
        except:
            info_dic['Img'] = 'unknown'
        try:
            intro_node = driver.find_element_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/div[1]/div[2]/div')
            info_dic['Introduce'] = intro_node.text.strip()
        except:
            info_dic['Introduce'] = 'unknown'
        info_list = ['Concern Index', 'Birthplace', 'AdWords', 'Official Website', 'Tel', 'Brand Website', 'Top10 Brand']
        for item in info_list:
            info_dic[item] = 'unknown'
        try:
            detail_node = driver.find_elements_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/ul/li')
            for node in detail_node:
                arr = node.text.strip().split('：')
                if len(arr) != 2:
                    if '十大' in arr[0]:
                        top = []
                        top_node = driver.find_elements_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/ul/li/a[contains(@title,"十大品牌")]')
                        for ele in top_node:
                            top.append(ele.text.strip('>>'))
                        info_dic['Top10Brand'] = '|'.join(top)
                else:
                    if '关注指数' in arr[0]:
                        info_dic['ConcernIndex'] = arr[1]
                    elif '发源地' in arr[0]:
                        info_dic['Birthplace'] = arr[1]
                    elif '广告词' in arr[0]:
                        info_dic['AdWords'] = arr[1]
                    elif '企业官网' in arr[0]:
                        info_dic['OfficialWebsite'] = arr[1]
                    elif '电话' in arr[0]:
                        info_dic['Tel'] = arr[1]
                    elif '品牌官网' in arr[0]:
                        info_dic['BrandWebsite'] = arr[1]
                    else:
                        continue
        except:
            pass
        threadLock.acquire()
        brand_info_file.write(k + '\t' + json.dumps(info_dic, ensure_ascii=False) + '\n')
        threadLock.release()

def spider(arg):
    print time.strftime("%Y-%m-%d %H:%M:%S")
    print '    -----start....' 
    trade_dic = dict()
    fields = arg.split('\t')
    for field in fields:
        arr = field.split('|')
        if len(arr) != 2:
            continue
        trade_dic[arr[0]] = arr[1]
#    print len(trade_dic)
    driver = webdriver.PhantomJS('./phantomjs')
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)
    for key, value in trade_dic.iteritems():
        dic = get_detail(driver, key, value)
        print time.strftime("%Y-%m-%d %H:%M:%S")
        print '%s    -----processing --trade....' % key
        brand_url = dict()
        for k, v in dic.iteritems():
            trade = key + '/' + k
            get_brand(driver, trade, v, brand_url)
        for k, v in brand_url.iteritems():
            get_info(driver, k, v)
    print time.strftime("%Y-%m-%d %H:%M:%S")
    print '    -----end....' 
    driver.quit()

if __name__ == '__main__':
#    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    print time.strftime("%Y-%m-%d %H:%M:%S")
    driver = webdriver.PhantomJS('./phantomjs')
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(5)
    driver.set_script_timeout(5)

    trade_brand_file = open('./china_trade_brand.txt' ,'w')
    brand_info_file = open('./china_brand_detail.txt' ,'w')
    url = 'http://www.china-10.com/'
    threadLock = threading.Lock()
    thread_list = list()
    trade_url = get_trade_url(url)

    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()
     
    print time.strftime("%Y-%m-%d %H:%M:%S")
    trade_brand_file.close()
    brand_info_file.close()
 #   res_file.close()
    driver.quit() 
