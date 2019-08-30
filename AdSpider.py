from selenium import webdriver
from utils import get_random_ua


class AdSpider:
    def __init__(self, driver_path):
        chrome_option = webdriver.ChromeOptions()
        self.ua = get_random_ua()
        if self.ua:
            chrome_option.add_argument(argument=f'user-agent={self.ua}')
            try:
                self.web_driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_option)
            except Exception as e:
                print('web_driver初始化出错：%s' % e)
                self.close()

    def check_user_agent(self):
        """
        检测useragent是否更换
        :return:
        """
        try:
            self.web_driver.get('http://service.spiritsoft.cn/ua.html')
            element = self.web_driver.find_element_by_xpath('//tbody/tr[2]/td')
            if element.text != self.ua:
                print(f'UA设置未成功, source_ua:{element.text}, target_ua:{self.ua}')
                return False
            return True
        except Exception as e:
            print('webdriver检查user_agent发生错误：%s' % e)
            self.close()

    def check_ip(self):
        """
        检测该代理ip是否可用
        :return:
        """
        try:
            # 检测是否代理
            self.web_driver.get('http://mobivst.com/7roi/checkip/no.html')
            element = self.web_driver.find_element_by_tag_name('title')
            status = element.text.trim()
            if status == '代理!!!':
                flag = False
                print(f'该IP为代理，请切换有效IP')
            elif status == 'IP可以使用':
                pass

            # TODO 检测IP是否正确,两个待检测网站
            self.web_driver.get('http://whoer.net/')
        except Exception as e:
            print('检测IP未通过：%s' % e)
            return False

    def clean_cache(self):
        """
        清理浏览器缓存、cookie
        :return:
        """
        try:
            self.web_driver.get('chrome://settings/clearBrowserData')
            clean_button = self.web_driver.find_element_by_id(id_='clearBrowsingDataConfirm')
            clean_button.click()
        except Exception as e:
            print('清理缓存发生错误：%s' % e)
            return False

    def close(self):
        """
        关闭浏览器，释放资源
        :return:
        """
        self.web_driver.close()
        self.web_driver.quit()


if __name__ == '__main__':
    pass