import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from PIL import ImageGrab


class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')   #类名.传参方法名
    excel = DATA_PATH + '/baidu.xlsx'  #excel地址

    locator_kw = (By.ID, 'kw')  #引入 from selenium.webdriver.common.by import By
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a') 

    def sub_setUp(self):
        self.driver = webdriver.Ie(executable_path=DRIVER_PATH + '\IEDriverServer.exe') #默认参数
        self.driver.get(self.URL)

    def sub_tearDown(self):
        self.driver.quit()

    def test_search(self):
        datas = ExcelReader(self.excel,title_line=False).data     #类名.方法名
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.driver.find_element(*self.locator_kw).send_keys(d['ABC'])
                self.driver.find_element(*self.locator_su).click()
                time.sleep(2)
                #ActionChains(driver).move_to_element(****).perform()把页面移动到指定位置截图
                im = ImageGrab.grab()
                im.save('E:\\Test_framework\\test\\pic\\13.png')
                links = self.driver.find_elements(*self.locator_result)
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()

 
if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='修改html报告')
        runner.run(TestBaiDu('test_search'))
"""e = Email(title='百度搜素测试报告',
		  message='这是今天的测试报告，请查收！',
		  receiver='wdhlogo@126.com',
		  server='...',
		  sender='...',
		  password='wdhlogo336*',
		  path=report
		  )
e.send()
"""
