class Metatype(type):
    def __call__(self,*args,**kwargs):
        print('Metatype:',*args)
        obj = object.__new__(self)
        self.__init__(obj,*args,**kwargs)
        return obj

    def __new__(cls, name, bases, attrs):
        print(name,bases)
        print(attrs)
        return type.__new__(cls, name, bases, attrs)
    # def __new__(cls, *args, **kwargs):  # 优先调用这种写法，这种写法不存在时才调用上面那种
    #     # args是包含(name,bases,attrs)的元组
    #     print(2, cls)
    #     print(2, args)
    #     print(2, kwargs)
    #     return type.__new__(cls, *args, **kwargs)

class Chain(object,metaclass=Metatype):
    def __init__(self, path=''):
        print('__init__:',path)
        self._path = path
    def __getattr__(self, path):#属性或者方法不存在时才会调用此方法
        print('__getattr__:', path)
        return self.yang
        return Chain('%s/%s' % (self._path, path))
    def __call__(self, kw): #调用的方法不存在时才会调用此方法
        print('Chain:',kw)
        return Chain('%s/:%s'%(self._path,kw))

    def yang(self,kw): #若是没有此方法，会先执行__getattr__获取yang然后再执行('dudu')
        print('Chain.yang:', kw)
        return Chain('%s/<>%s'%(self._path,kw))

    def __str__(self):
        return self._path
    __repr__ = __str__
    #__str__是面向用户的(只有用print输出时才起作用)，
    # 而__repr__面向程序员(适用性广，交换环境也起作用)
# print(Chain().status.user.list)
Chain().user('fly').yang('dudu')


#light heavy develop

# request.args.get('name', 'World!')