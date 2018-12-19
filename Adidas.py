import requests, json, time, Tkinter, smtplib, datetime
from Tkinter import *
from requests.utils import dict_from_cookiejar
from threading import Thread
from selenium import webdriver
from requests.utils import dict_from_cookiejar
from pytz import timezone
from datetime import datetime

global sizeMB
global PID
global proxy
global sitekey
global consoleLog

def logWrite(box, message):
        currentTime = timezone('US/Eastern')
        cur_time = datetime.now(currentTime)
        print_time = cur_time.strftime('%H-%M-%S')

        box.configure(state = 'normal')
        box.insert(END, ((print_time + ' : '+ message)+'\n'))
        box.configure(state = 'disabled')

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

            logWrite(consoleLog, 'Waiting for captcha')
            time.sleep(1)
            captchaGet = sesh.get("http://2captcha.com/res.php", params = getData)

        JSONDict2 = json.loads(captchaGet.text)



        return str(JSONDict2['request'])

    except  :

        logWrite(consoleLog, 'Captcha error!')


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
            'DhnjhrCA':ca,
            'ajax':'true'
            }

    params = {
        'clientId' : '52f5ef25-e003-41eb-94b4-39d2f21ae295'
    }
    
    sesh = requests.Session()
    sesh.cookies.clear()

    proxies = {
    'http': ('http://%s' % prxy)
    }

    getPage = sesh.get('http://www.adidas.com/us/', headers = headers, proxies = proxies)

    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, params = params, proxies = proxies)

    if add.status_code == 200 :

        if 'true' in add.content:
            added = True

        else :
            while added == False :

                errJSON = json.loads(add.text)

                if 'INVALID_CAPTCHA' in errJSON['error'] :
                    logWrite(consoleLog, 'Invalid captcha error, retrying...')

                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            'g-recaptcha-response':ca,
                            'masterPid':pid,
                            'DhnjhrCA':ca,
                            'ajax':'true'
                            }

                    params = {
                        'clientId' : '52f5ef25-e003-41eb-94b4-39d2f21ae295'
                    }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, params = params, proxies = proxies)

                elif 'OUT-OF-STOCK' in errJSON['error'] :

                    logWrite(consoleLog, 'OOS error, retrying...')
                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            'g-recaptcha-response':ca,
                            'masterPid':pid,
                            'DhnjhrCA':ca,
                            'ajax':'true'
                            }

                    params = {
                        'clientId' : '52f5ef25-e003-41eb-94b4-39d2f21ae295'
                    }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, params = params, proxies = proxies)

                else :

                    logWrite(consoleLog, ('Unknow error ' + errJSON + ' retrying...'))

                    data = {
                            'layer':'Add To Bag overlay',
                            'pid':longPID,
                            'Quantity':'1',
                            'g-recaptcha-response':ca,
                            'masterPid':pid,
                            'DhnjhrCA':ca,
                            'ajax':'true'
                            }

                    params = {
                        'clientId' : '52f5ef25-e003-41eb-94b4-39d2f21ae295'
                    }
                    add = sesh.post('http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct', headers = addHeaders, data = data, params = params, proxies = proxies)

                if add.status_code == 200 :
                    if 'true' in add.content :
                        added = True
                    else :
                        pass

                else :
                    logWrite(consoleLog, ("Error status code : " + str(add.status_code)))

    else :
        logWrite(consoleLog, ("Error status code : " + str(add.status_code)))

    logWrite(consoleLog, ('Added size %s of %s to cart!' % (sz, pid)))

    cookies = dict_from_cookiejar(sesh.cookies)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % prxy)
    driver=webdriver.Chrome('C:/Python27/chromedriver.exe', chrome_options=chrome_options)
    driver.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show')
    driver.delete_all_cookies()
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})
    driver.refresh()

    raw_input()

#6LdWWg0UAAAAAC8WfY76UaQ13PlSLeK8F71RtU89

def call():
    T = Thread(target = add, args = (sizeMB.get(), PID.get(), proxy.get(), sitekey.get(), 'http://www.adidas.com/us/nmd_r1-shoes/BA7251.html'))
    T.start()
###########################################################################################################################################################################################################################################################################

app = Tk()
app.title('Adidas')
app.geometry('800x500')
app.configure(background='gray8')

PIDl = Label(app, text = 'PID', background = 'gray8', fg = 'white')
PIDl.place(x = 30, y = 20)
PID = Entry(app, bd = 3, width = 17, background = 'white')
PID.place(x = 55, y = 20)

sizeMB = StringVar(app)
sizeMB.set('Size')
size = OptionMenu(app, sizeMB, '4', '4.5', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12', '12.5', '13', '14', '15', '16')
size.place(x = 180, y = 17)

localMB = StringVar(app)
localMB.set('Local')
local = OptionMenu(app, localMB, 'US', 'UK', 'AU', 'CA', 'DE', 'FR', 'JP')
local.place(x = 265, y = 17)

redirectVar = IntVar()
redirect = Checkbutton(app, text = "Open with proxy", variable = redirectVar, onvalue = 1, offvalue = 0, background = 'gray8', activebackground= 'gray8' , fg = 'white', activeforeground='white', selectcolor= 'gray8')#, height=5, width = 20
redirect.place(x=225, y=60)

proxyl = Label(app, text = 'Proxy', background = 'gray8', fg = 'white')
proxyl.place(x = 17, y = 60)
proxy = Entry(app, bd = 3, width = 26, background = 'white')
proxy.place(x = 55, y = 60)

sitekeyl = Label(app, text = 'Sitekey', background = 'gray8', fg = 'white')
sitekeyl.place(x = 10, y = 100)
sitekey = Entry(app, bd = 3, width = 45, background = 'white')
sitekey.place(x = 55, y = 100)

consoleLog = Text(app, height = 12, width = 79, bd = 3, state = 'disabled')
consoleLog.place(x = 15, y = 255)

btn = Tkinter.Button(text = 'Add', bd = 3, bg = 'white', fg = 'gray8', height = 1, width = 6, command = call)
btn.place(x = 160, y = 140)

app.mainloop()

###########################################################################################################################################################################################################################################################################
