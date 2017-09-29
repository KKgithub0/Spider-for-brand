#coding=gbk
import urllib
import urllib2
import sys
import cStringIO
import random
from PIL import Image
reload(sys)
sys.setdefaultencoding('gbk')
outdir = '/Users/xuyikai/Downloads/work/img/all_pic/'
logfile = open('/Users/xuyikai/Downloads/work/img/log','w')
my_headers=[
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",  
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]  
count = 1
with open('/Users/xuyikai/Downloads/work/img/test.txt', 'r') as f:
    for line in f:
        arr = line.strip().split('\t')
        if len(arr) < 1:
            continue
        if count > 10:
            break
        brand = arr[0]
        #turl = arr[1]#.split(' ')
        #turl = 'http://slp.hiphotos.bdimg.com/slp/pic/item/267f9e2f070828385b3a230eb399a9014c08f1f1.jpg'
        #turl = 'http://t10.baidu.com/it/u=2529967458,3085354399&fm=58'
        turl = arr[0]
        picname = str(count)
        #picname = name[-2] + name[-1]
        try:
            #headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
            #req = urllib.request.Request(url=turl, headers=headers)  
            #pic = urllib.request.urlopen(req).read()
            randdom_header=my_headers[1]#random.choice(my_headers)  
            request = urllib2.Request(url=turl)#, headers=headers)
            request.add_header("User-Agent",randdom_header)
            request.add_header("POST",turl)
            response = urllib2.urlopen(request)
            pic = response.read()
            tmpIm = cStringIO.StringIO(response.read())
            img = Image.open(tmpIm)
            (x, y) = img.size()
            print x , y
            '''
            with open(outdir + picname + '.jpg', 'wb') as picfile:
                picfile.write(pic)
            '''
            #break
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
            logfile.write(brand + turl + '\n')
            #break
        count += 1
        #break
        
        
        
    
logfile.close()