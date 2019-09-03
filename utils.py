import datetime
import os
import random
import subprocess
from fake_useragent import UserAgent


def get_random_ua():
    """
    根据今天周几打开相应的UA文件，随机获取一个UA
    :return: {string} UA
    """
    day = datetime.datetime.now().isoweekday()
    file_name = f'{day}.txt'
    file_path = os.path.join(r'E:\AD\111111\UA', file_name)
    try:
        with open(file=file_path, mode='r') as fp:
            ua_list = fp.readlines()
            length = len(ua_list)
            random_ua = ua_list[random.randint(0, length - 1)]
            print('UA来自文件')
            return random_ua.strip()
    except Exception as e:
        print('文件打开失败：%s' % e)
        print('正尝试通过fake-useragent获取UA')
        try:
            ua = UserAgent()
            chrome_ua = ua.chrome
            print('UA来自fake-useragent')
            return chrome_ua
        except Exception as e:
            print('fake-useragent出现出错：%s' % e)
            return None


def switch_ip(state):
    """
    随机切换IP
    :return:
    """
    subprocess.Popen(f"start E:\\AD\\111111\\aa\\ProxyTool\\Autoproxytool.exe -changeproxy/US/{state}")
    print('自动切换IP成功')


def open_client():
    """
    运行登录IP代理程序
    :return:
    """
    pass


if __name__ == '__main__':
    print(get_random_ua())
