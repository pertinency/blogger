# 코랩에 셀레니움을 설치합니다.
!apt-get update
!apt install chromium-chromedriver
!pip install selenium
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

# 셀레니움을 임포트하고, 크롬 드라이버를 PATH에 추가합니다.
from selenium import webdriver
import time
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

# Headless 옵션을 준 셀레니움 객체를 생성합니다.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=chrome_options)

# 구글 검색 예제
driver = webdriver.Chrome('chromedriver',options=chrome_options)
try:
    driver.get('https://www.google.com/')
    time.sleep(1)

    element = driver.find_element_by_name('q')
    print(element)
    element.send_keys("안녕 구글")

    element.submit()
    time.sleep(5)

    element = driver.find_element_by_xpath('//*')
    element = element.get_attribute('innerHTML')
    print(element)
except Exception as e:
    print(e)
    driver.close()
finally:
    driver.close()
