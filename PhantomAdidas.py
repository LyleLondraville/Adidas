import time, requests, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from threading import Thread
import threading
from bs4 import BeautifulSoup



def phantom(tabs, url, prxy):

    sitekeyFound = False
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % prxy)
    browser = webdriver.Chrome('/Applications/Python 2.7/chromedriver', chrome_options=chrome_options)


    tabList = range(0, tabs+1)
    i = tabs
    Hi = 0

    while i >= 0:
        browser.execute_script('window.open("")')
        i -= 1

    i = tabs

    while Hi <= (i) :
        browser.switch_to.window(browser.window_handles[Hi])
        browser.get(url)
        Hi += 1


    while sitekeyFound == False :
        time.sleep(30)

        for i in tabList:
            browser.switch_to.window(browser.window_handles[i])
            HTML = browser.page_source

            if 'WE STILL HAVE SOME YEEZY BOOST 350 V2 IN STOCK ' in HTML :
                pass
            else :
                try :
                    soup = BeautifulSoup(HTML, 'html.parser')
                    print 'Passed'
                    print str(soup.find('div',{'class':'g-recaptcha'})['data-sitekey'])


                except :
                    browser.refresh()
                    

def cook() :
    
    url = 'http://www.adidas.com/yeezy'

    t0 = Thread(target = phantom, args = (13, url, '45.79.167.252:3128'))
    t1 = Thread(target = phantom, args = (13, url, '45.79.176.247:3128'))
    t2 = Thread(target = phantom, args = (13, url, '45.79.3.242:3128'))
    t3 = Thread(target = phantom, args = (13, url, '45.33.23.132:3128'))
    t4 = Thread(target = phantom, args = (13, url, '45.33.68.239:3128'))
    t5 = Thread(target = phantom, args = (13, url, '23.239.15.236:3128'))
    t6 = Thread(target = phantom, args = (13, url, '66.228.37.234:3128'))
    t7 = Thread(target = phantom, args = (13, url, '45.33.83.37:3128'))
    t8 = Thread(target = phantom, args = (13, url, '45.33.75.34:3128'))
    t9 = Thread(target = phantom, args = (13, url, '45.56.99.4:3128'))
    t10 = Thread(target = phantom, args = (13, url, '104.237.146.46:3128'))


    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()




