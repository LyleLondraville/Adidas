import requests, json, time
from selenium import webdriver
from requests.utils import dict_from_cookiejar
from threading import Thread

#'6Le4AQgUAAAAAABhHEq7RWQNJwGR_M-6Jni9tgtA'


def c(prxy, sitekey, url) :

    ## 2captcha key - 90183367e53b95cb465c6fba6f9b6cdf
    try :
        P = False

        sesh = requests.Session()

        postData={
                 "key":'90183367e53b95cb465c6fba6f9b6cdf',
                 "method":"userrecaptcha",
                 "googlekey":sitekey,
                 "proxy":prxy,
                 "proxytype":"HTTP",
                 "pageurl":url,
                 "json":'1'
                 }

        captchaPost = sesh.post('http://2captcha.com/in.php', data = postData)

        JSONdict = json.loads(captchaPost.text)

        if JSONdict['status'] == 1 :
            P = True

        else :
            while P == False :
                captchaPost = sesh.post('http://2captcha.com/in.php', data = postData)
                JSONdict = json.loads(captchaPost.text)

                if JSONdict['status'] == 1 :
                    P = True
                else :
                    pass

        getData={
               "key":'90183367e53b95cb465c6fba6f9b6cdf',
               "action":"get",
               "json":'1',
               "id":JSONdict['request'],
               }

        captchaGet=sesh.get("http://2captcha.com/res.php", params = getData)

        while 'CAPCHA_NOT_READY' in captchaGet.text :
            print 'Waiting for captcha'
            time.sleep(1)
            captchaGet = sesh.get("http://2captcha.com/res.php", params = getData)

        JSONDict2 = json.loads(captchaGet.text)

        print 'Captcha found!'

        return str(JSONDict2['request'])
    except  :
        print 'Captcha error'


def add(sz, pid, prxy, sitekey, url):

    added = False



    headers = {
          'Host': 'www.adidas.com',
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'en-US,en;q=0.8'
          }

    addHeaders = {
            'Host': 'www.adidas.com',
            'Connection': 'keep-alive',
            'Content-Length': '1080',
            'Accept': '*/*',
            'Origin': 'http://www.adidas.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'
            }

    sizeIndex = {
        '4'    : '530',
        '4.5'  : '540',
        '5'    : '550',
        '5.5'  : '560',
        '6'    : '570',
        '6.5'  : '580',
        '7'    : '590',
        '7.5'  : '600',
        '8'    : '610',
        '8.5'  : '620',
        '9'    : '630',
        '9.5'  : '640',
        '10'   : '650',
        '10.5' : '660',
        '11'   : '670',
        '11.5' : '680',
        '12'   : '690',
        '12.5' : '700',
        '13'   : '710',
        '14'   : '720',
        '15'   : '730',
        '16'   : '740'
        }

    for s, p in sizeIndex.iteritems():
        if s == sz :
            longPID = pid + '_' + p
            break

    #ca = c(prxy, sitekey, url)

    data = {
            'layer':'Add To Bag overlay',
            'pid':longPID,
            'Quantity':'1',
            #'g-recaptcha-response':ca,
            'masterPid':pid,
            'sessionSelectedStoreID':'null',
            'ajax':'true'
            }


    sesh = requests.Session()
    sesh.cookies.clear()

    proxy = {
    'http': ('http://%s' % prxy)
    }

    getPage = sesh.get('http://www.adidas.com/us/', headers = headers, proxies = proxy)

    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, proxies = proxy)

    if add.status_code == 200 :

        if 'true' in add.content:
            added = True

        else :
            while added == False :

                errJSON = json.loads(add.text)

                if 'INVALID_CAPTCHA' in errJSON['error'] :
                    print 'Invalid captcha error, retrying...'
                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            #'g-recaptcha-response':c(prxy, sitekey, url),
                            'masterPid':pid,
                            'sessionSelectedStoreID':'null',
                            'ajax':'true'
                            }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, proxies = proxy)

                elif 'OUT-OF-STOCK' in errJSON['error'] :
                    print 'OOS error, retrying...'
                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            #'g-recaptcha-response':c(prxy, sitekey, url),
                            'masterPid':pid,
                            'sessionSelectedStoreID':'null',
                            'ajax':'true'
                            }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, proxies = proxy)

                else :
                    print 'Unknow error ' + errJSON + ' retrying...'
                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            #'g-recaptcha-response':c(prxy, sitekey, url),
                            'masterPid':pid,
                            'sessionSelectedStoreID':'null',
                            'ajax':'true'
                            }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, proxies = proxy)


                if add.status_code == 200 :
                    if 'true' in add.content :
                        added = True
                    else :
                        pass

                else :
                    print "Error status code : " + str(add.status_code)
    else :
        print "Error status code : " + str(add.status_code)

    print 'Added size %s of %s to cart!' % (sz, pid)

    cookies = dict_from_cookiejar(sesh.cookies)
    driver=webdriver.Chrome('C:/Python27/chromedriver.exe')
    driver.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show')
    driver.delete_all_cookies()
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})
    driver.refresh()

    raw_input()



def addT(sz, pid, prxy, sitekey, url):

    added = False



    headers = {
          'Host': 'www.adidas.com',
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'en-US,en;q=0.8'
          }

    addHeaders = {
            'Host': 'www.adidas.com',
            'Connection': 'keep-alive',
            'Content-Length': '1080',
            'Accept': '*/*',
            'Origin': 'http://www.adidas.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8'
            }

    sizeIndex = {
        '4'    : '530',
        '4.5'  : '540',
        '5'    : '550',
        '5.5'  : '560',
        '6'    : '570',
        '6.5'  : '580',
        '7'    : '590',
        '7.5'  : '600',
        '8'    : '610',
        '8.5'  : '620',
        '9'    : '630',
        '9.5'  : '640',
        '10'   : '650',
        '10.5' : '660',
        '11'   : '670',
        '11.5' : '680',
        '12'   : '690',
        '12.5' : '700',
        '13'   : '710',
        '14'   : '730',
        '15'   : '750',
        '16'   : '770'
        }

    for s, p in sizeIndex.iteritems():
        if s == sz :
            longPID = pid + '_' + p
            break

    ca = c(prxy, sitekey, url)

    data = {
            'layer':'Add To Bag overlay',
            'pid':longPID,
            'Quantity':'1',
            'g-recaptcha-response':ca,
            'masterPid':pid,
            'sessionSelectedStoreID':'null',
            'ajax':'true'
            }


    sesh = requests.Session()
    sesh.cookies.clear()

    proxy = {
    'http': ('http://%s' % prxy)
    }

    getPage = sesh.get('http://www.adidas.com/us/', headers = headers, proxies = proxy)

    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, proxies = proxy)

    print add.url
    print add.status_code
    print add.content

addT('10', 'BY1604', '45.76.16.191:3128', '6Le4AQgUAAAAAABhHEq7RWQNJwGR_M-6Jni9tgtA', 'https://www.adidas.com/us/nmd_r1-shoes/BA7251.html')



#BA7251
#45.76.16.191:3128
#6Le4AQgUAAAAAABhHEq7RWQNJwGR_M-6Jni9tgtA
