# Spider-for-brand
simple spider based on selenium

这个文件夹包含了一些爬虫实现爬取网页内容的Python脚本，包括爬出静态内容和异步请求的内容（Ajax），对于静态内容直接调用Python内部的urllib2库配合etree中的xpath语句可以解决大部分问题，对于动态网页，可以用模拟浏览器的方式来获取想要获取的内容，Python有一个selenium的库可以实现模拟浏览器的功能，文件夹里的爬虫脚本基本都是基于selenium包。

summary文件，包含了配置爬虫环境教程，以及一些我自己安装过程中碰到的问题以及解决方法。
Hi，last few days I had some demands of grasp at some website, so I learned the Python crawler, my purpose is to grab the brands of all relevant categories, I originally thought to write static crawler which may be completed, and that tures out the task was not so simple, finally after a few days of study,I found that senelium + XPath is a very good choice and to meet the basic requirements of dynamic web crawling.

You need to be familiar with CSS, JavaScript, HTML, and some XPath syntax related knowledge, and you need to know about selenium's API.
编写爬虫之前需要了解一些关于网页的基础知识，css/javascript/html，xpath是解析网页的利器，需要了解，selenium的一些接口函数也需要知道。

After few websites I had parsed, it is difficult to implement a versatile crawler to satisfy the crawl requirement. Every website has its distinct source code. So it's a good idea to complete a versatile crawler to parse all site! But I don't know how to do yet.
要编写一个通用性的爬虫很困难，目前我的水平只限于对各个网页逐一分析，对于任务量比较大爬取任务，考虑用多线程或多进程来并行处理。

下面是爬虫程序功能介绍：
program introduction:

taobao_spider.py is a simple spider on taobao.com, it's mission is to grasp all categories on homepage.

jingdong_spider.py is a simple spider on jd.com, it's mission is to grasp all categories on homepage.

58_spider.py aimes to grasp some companies of 58 local training institutions.

autohome_spider.py is a spider on autohome.com, grasp car brand with selected type and price.

quna_hotel_spider.py grasps all hotel brand in beijing at different star degree. To be continued.

mbaidu_spider.py grasps m.baidu.com, finds related recommentation and grasp its brand logo and description. This version contains time controller and multithreads because of it's a scale task.

china10.py grasps www.china-10.com. To to improved by multithread.
