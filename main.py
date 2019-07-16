import os
import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.by import By


BASE_ROOT = os.path.dirname(os.path.realpath(__file__))
chrome_driver = os.path.join(BASE_ROOT, 'chromedriver')
# browser = webdriver.Chrome(os.path.join(BASE_ROOT, 'chromedriver'))
service = service.Service(chrome_driver)
service.start()
# capabilities = {'chrome.binary': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}
browser = webdriver.Remote(service.service_url)
browser.get('http://www.baidu.com')
# print(browser.page_source)
# time.sleep(2)  # Let the user actually see something!
search_box = browser.find_element(By.NAME, 'wd')
search_box.send_keys('斗罗大陆')
search_box.submit()
print(browser.page_source)
# time.sleep(2)
browser.quit()
