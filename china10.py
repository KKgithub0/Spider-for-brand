#coding=utf-8

import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def get_trade_url(url):
    try:
        driver.get(url)
    except:
        pass
    finally:
        trade_url = dict()
        trade_nodes = driver.find_elements_by_xpath('//*[@id="conmenu"]/li')
        i = 1
#        print len(trade_nodes)
        for node in trade_nodes:
            ActionChains(driver).move_to_element(node).perform()
            elements = driver.find_elements_by_xpath('//*[@id="conmenu"]/li[%s]/div/ul/li/a' % str(i))
#            print i
            i += 1
            for ele in elements:
                herf = ele.get_attribute('href')
                title = ele.get_attribute('title')
                trade_url[title] = herf 
#                print title
        return trade_url              

def get_detail(k, url):
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
#                print node.text
        except:
            detail_dic[k] = url
        return detail_dic

def get_brand(trade, url):
    try:
        driver.get(url)
    except:
        pass
    finally:
        try:
            res = list()
            nodes = driver.find_elements_by_xpath('//*[@id="top10"]/div/div[2]/dl/dt/a[1]')
            for node in nodes:
                res.append(node.get_attribute('title'))
                brand_url[node.get_attribute('title')] = node.get_attribute('href')
            nodes = driver.find_elements_by_xpath('//*[@id="rightlay"]/div[3]/div[1]/div[2]/a')
            for node in nodes:
                res.append(node.get_attribute('title'))
                brand_url[node.get_attribute('title')] = node.get_attribute('href')
            trade_brand_file.write(trade + '\t' + '|'.join(res) + '\n')
        except:
            pass
 
def get_info(k, url):
    info_dic = dict()
    try:
        driver.get(url)
    except:
        pass
    finally:
        try:
            driver.find_element_by_xpath('//*[@id="rightlay"]/div[2]/div[1]/div[2]/div[3]/a[contains(text(),"更多品牌介绍")]').click()
            desc = ''
            nodes = driver.find_elements_by_xpath('//*[@id="rightlay"]/div[2]/div[1]/div[2]/div[2]/p')
            for node in nodes:
        #        print node.text
                desc += node.text
            info_dic['desc'] = desc
            img_node = driver.find_element_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/div[1]/div[1]/a/div/img')
            info_dic['img'] = img_node.get_attribute('src')
            intro_node = driver.find_element_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/div[1]/div[2]/div')
            info_dic['introduce'] = intro_node.text
            detail_node = driver.find_elements_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/ul/li')
            info_list = ['Concern Index', 'Birthplace', 'AdWords', 'Official Website', 'Tel', 'Brand Website', 'Top10 Brand']
            for item in info_list:
                info_dic[item] = 'Unknown'
            for node in detail_node:
                arr = node.text.strip().split('：')
                if len(arr) != 2:
                    if '十大' in arr[0]:
                        top = []
                        top_node = driver.find_elements_by_xpath('//*[@id="infobox"]/div/div[2]/div/div[1]/ul/li/a[contains(@title,"十大品牌")]')
                        for ele in top_node:
                            top.append(ele.text.strip('>>'))
                        info_dic['Top10 Brand'] = '|'.join(top)
                else:
                    if '关注指数' in arr[0]:
                        info_dic['Concern Index'] = arr[1]
                    elif '发源地' in arr[0]:
                        info_dic['Birthplace'] = arr[1]
                    elif '广告词' in arr[0]:
                        info_dic['AdWords'] = arr[1]
                    elif '企业官网' in arr[0]:
                        info_dic['Official Website'] = arr[1]
                    elif '电话' in arr[0]:
                        info_dic['Tel'] = arr[1]
                    elif '品牌官网' in arr[0]:
                        info_dic['Brand Website'] = arr[1]
                    else:
                        continue
            brand_info_file.write(k + '\t' + json.dumps(info_dic, ensure_ascii=False) + '\n')
        except:
            pass
       
if __name__ == '__main__':
    driver = webdriver.Chrome('/Users/xuyikai/Downloads/chromedriver')
    count = 0
    print time.strftime("%Y-%m-%d %H:%M:%S")
 #   driver = webdriver.PhantomJS('/Users/xuyikai/phantomjs')
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
 #   res_file = open('/Users/xuyikai/Downloads/work/spider/brand/mbaidu_brand.txt' ,'w')

    trade_brand_file = open('/Users/xuyikai/Downloads/work/spider/brand/china_trade_brand.txt' ,'w')
    brand_info_file = open('/Users/xuyikai/Downloads/work/spider/brand/china_brand_detail.txt' ,'w')
    url = 'http://www.china-10.com/'
    trade_brand = dict()
    brand_url = dict()
    brand_info = dict()
    trade_url = get_trade_url(url)
    for k, v in trade_url.iteritems():
        trade_url[k] = get_detail(k, v)
     

    for key, value in trade_url.iteritems():
        for k, v in value.iteritems():
            trade = key + '/' + k
            get_brand(trade, v)
 #           trade_brand[trade] = brand
    for k, v in brand_url.iteritems():
        get_info(k, v)

    print time.strftime("%Y-%m-%d %H:%M:%S")
    trade_brand_file.close()
    brand_info_file.close()
 #   res_file.close()
    driver.quit() 
