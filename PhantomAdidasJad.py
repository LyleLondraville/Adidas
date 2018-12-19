from selenium.webdriver.support.ui import Select
from threading import Thread
from bs4 import BeautifulSoup

import threading


def phantom():

    browser = webdriver.PhantomJS('phantomjs.exe')

    i = 15

    while i > 0:
        browser.get('https://doprdele.github.io/adidas-wait-page-simulator/')
        browser.implicitly_wait(360000)
        browser.find_element_by_class_name('g-recaptcha')
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for s in soup.select('.g-recaptcha'):
            sk = s['data-sitekey']
            print(sk)
        browser.quit()
        i -= 1

    print('done')


def strtT():
    t = Thread(target=phantom, args=())
    t.start()


for i in range(0, 21):
    strtT()
