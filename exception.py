class CustomException(Exception):
    def __init__(self, errMsg):
        super(CustomException, self).__init__()
        self.errMsg = errMsg

    def __str__(self):
        return self.errMsg


if __name__ == '__main__':
    print(CustomException("UA设置错误"))