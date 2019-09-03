from AdSpider import AdSpider
import settings


def run(path):
    try:
        spider = AdSpider(path)
        spider.check_user_agent()
        spider.spider()
    except Exception as e:
        print('程序出错: %s' % e)


if __name__ == '__main__':
    run(settings.DRIVER_PATH)
