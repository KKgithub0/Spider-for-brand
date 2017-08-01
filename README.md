# Spider-for-brand
simple spider based on senenium aimed to grab brand

Hi，last few days I had some demands of grasp at some website, so I learned the Python crawler, my purpose is to grab the brands of all relevant categories, I originally thought to write static crawler which may be completed, and that tures out the task was not so simple, finally after a few days of study,I found that senelium + XPath is a very good choice and to meet the basic requirements of dynamic web crawling.
You need to be familiar with CCS, JavaScript, HTML, and some XPath syntax related knowledge, and you need to know about selenium's API.

After few websites I had parsed, it is difficult to implement a versatile crawler to satisfy the crawl requirement. Every website has its distinct source code. So it's a good idea to complete a versatile crawler to parse all site! But I don't know how to do yet.

program introduction:

taobao_spider.py is a simple spider on taobao.com, it's mission is to grasp all categories on homepage.

jingdong_spider.py is a simple spider on jd.com, it's mission is to grasp all categories on homepage.

58_spider.py aimes to grasp some companies of 58 local training institutions.

autohome_spider.py is a spider on autohome.com, grasp car brand with selected type and price.

quna_hotel_spider.py grasps all hotel brand in beijing at different star degree. To be continued.

mbaidu_spider.py grasps m.baidu.com, finds related recommentation and grasp its brand logo and description. This version contains time controller and multithreads because of it's a scale task.

china10.py grasps www.china-10.com.
