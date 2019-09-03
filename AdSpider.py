from selenium import webdriver
from utils import get_random_ua
import time
from exception import CustomException
import settings


class AdSpider:
    def __init__(self, driver_path):
        chrome_option = webdriver.ChromeOptions()
        # 不加载图片, 提升速度
        chrome_option.add_argument('blink-settings=imagesEnabled=false')
        chrome_option.binary_location = settings.BROWSER_PATH
        # 随机获取UA
        self.ua = get_random_ua()
        if self.ua:
            chrome_option.add_argument(argument=f'user-agent={self.ua}')
            try:
                self.web_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_option)
                # 删除cookies
                self.web_driver.delete_all_cookies()
            except Exception:
                raise CustomException('浏览器驱动启动异常，请检测浏览器配置')
        else:
            raise CustomException('UA未取到，请检查相关数据')

    def check_user_agent(self):
        """
        检测useragent是否更换
        :return:
        """
        try:
            self.web_driver.get('http://service.spiritsoft.cn/ua.html')
            element = self.web_driver.find_element_by_xpath('//tbody/tr[2]/td')
            if element.text.strip() != self.ua:
                print(f'UA设置未成功, source_ua:{element.text}, target_ua:{self.ua}')
                raise CustomException('UA未切换成功')
        except Exception:
            self.close()
            raise CustomException('检测UA时，出现错误')

    def check_ip(self):
        """
        检测该代理ip是否可用
        :return:
        """
        ip_flag1 = False
        ip_flag2 = False
        ip_flag3 = False
        try:
            # 检测是否代理
            self.web_driver.get('http://mobivst.com/7roi/checkip/no.html')
            element = self.web_driver.find_element_by_tag_name('title')
            status = element.text.trim()
            if status == '代理!!!!!':
                ip_flag1 = False
                print(f'该IP为代理，请切换有效IP')
            elif status == 'IP可以使用':
                ip_flag1 = True

            # whoer网站IP检测
            self.web_driver.get('http://whoer.net/')
            # 是否为代理
            element = self.web_driver.find_element_by_class_name('cont proxy-status-message')
            proxy_status = element.text.trim()
            # 是否为匿名服务器
            element = self.web_driver.find_element_by_xpath('//div[@id="anonymizer"]//span[@class="value"]')
            anonymizer_status = element.text.trim()
            # 是否为黑名单
            element = self.web_driver.find_element_by_xpath(
                '//div[@class="row main-ip-info__ip-data"]/div[2]/div[4]/div[3]/div')
            blacklist_status = element.text.trim()
            if proxy_status == anonymizer_status == blacklist_status == 'NO':
                ip_flag2 = True
            else:
                print('whoer网站IP检测失败，请切换有效IP')

            # check2ip网站IP检测
            self.web_driver.get('http://check2ip.com/')

            # 是否在黑名单
            elements = self.web_driver.find_elements_by_xpath('//tbody/tr[1]/td[2]//tbody//tbody//font')
            good_elements = [e for e in elements if
                             'IP IS NOT Blacklisted' in e.text or 'IP IS NOT blacklisted! / Dynamic IP' in e.text]
            blacklist_status = len(elements) == len(good_elements)

            # 检测系统时间
            element = self.web_driver.find_element_by_xpath('//tbody//tbody/tr[9]/td[2]/font')
            time_status = element.text.trim() == 'OK'

            # 检测是否是匿名服务器，请求头是否安全
            element = self.web_driver.find_element_by_xpath('//tbody//tbody/tr[-3]/td[2]')
            anonymizer_status = element.text.trim()
            element = self.web_driver.find_element_by_xpath('//tbody//tbody/tr[-2]/td[2]')
            header_status = element.text.trim()
            if blacklist_status and time_status and anonymizer_status and header_status:
                ip_flag3 = True
            else:
                print('check2ip网站检测IP失败，请切换有效IP')

            return ip_flag1 == ip_flag2 == ip_flag3
        except Exception:
            self.close()
            raise CustomException('IP检测未通过')

    def spider(self):
        self.web_driver.get(r'https://www.douban.com/')
        time.sleep(2)
        print(self.web_driver.page_source)

    def close(self):
        """
        关闭浏览器，释放资源
        :return:
        """
        self.web_driver.close()
        self.web_driver.quit()


if __name__ == '__main__':
    pass
