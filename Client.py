import socket, time, ast
from bs4 import BeautifulSoup
from selenium import webdriver 
 
class client :
	
	def __init__(self, url, homeIP, port):
		self.url =  url
		self.IP = homeIP


	def spalshWaiter(self):
		
		url = self.url
		passed = False 

		phantom = webdriver.PhantomJS()

		for t in range(0,15):
			phantom.execute_script('window.open("")')

		for t in range(0, 15):
			phantom.switch_to_window(phantom.window_handles[t])
			phantom.get(url)
			

		while passed == False :
			
			time.sleep(30)
			
			for t in range(0,15):
				phantom.switch_to_window(phantom.window_handles[t])
				html = phantom.page_source

				try :
					soup = BeautifulSoup(html, 'html.parser')
					soup.find('div',{'class':'g-recaptcha'})['data-sitekey']
					cookies = phantom.get_cookies()
					passed = True 
					break 
				
				except :
					pass

		phantom.quit()

		s = socket.socket()
		s.connect((self.homeIP, self.port))
		s.sendall(str(cookies))
		s.close()


class server :
	
	def waitForCookies(self, port, url):
		s = socket.socket()

		s.bind(('', port))
		s.listen(1)


		conn, addr = s.accept()

		d = conn.recv(10000000)
		
		chrome = webdriver.Chrome('/Applications/Python 2.7/chromedriver')
		chrome.get('http://www.adidas.com/us/ultraboost-reigning-champ-shoes/BW1116.html')

		for c in ast.literal_eval(d):
			chrome.add_cookie(c)

		chrome.refresh()

	def test(self):
		phantom = webdriver.PhantomJS()
		phantom.get('http://www.adidas.com/us/ultraboost-reigning-champ-shoes/BW1116.html')
		cookies = phantom.get_cookies()
		phantom.quit()
		chrome = webdriver.Chrome('/Applications/Python 2.7/chromedriver')
		chrome.get('http://www.adidas.com/us/ultraboost-reigning-champ-shoes/BW1116.html')

		for c in cookies:
			#print c
			#print '\n'
			chrome.add_cookie(c)

		chrome.quit()

c = client()
c.test()







