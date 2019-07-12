class ModelException(Exception):
    def __init__(self, code='', message='Error'):
        self.code = code        # 异常编号
        self.message = message  # 异常信息

    def __str__(self):
        return self.message     # 当作为字符串使用时，返回异常信息
class ArgError(ModelException):
    def __init__(self, message='参数错误'):
        super(ModelException, self).__init__(message)