import inspect
def attr_from_locals(locals_dict):
    self = locals_dict.pop('self')
    args = inspect.getargspec(self.__init__.__func__).args[1:]
    # print(args) # ['name']
    for k in args:
        setattr(self, k, locals_dict[k])
    keywords = inspect.getargspec(self.__init__.__func__).keywords
    # print(keywords) #kwargv
    if keywords:
        keywords_dict = locals_dict[keywords]
        # print(keywords_dict) # {'color': 'yellow', 'num': 1}
        for k in keywords_dict:
            setattr(self, k, keywords_dict[k])

class Foo(object):
    def __init__(self, name, **kwargv):
        # print(locals()) # {'kwargv': {'color': 'yellow', 'num': 1}, 'name': 'bar', 'self': <__main__.Foo object at 0x036B6B70>}
        attr_from_locals(locals())

f = Foo('bar', color='yellow', num=1)
print(f.__dict__)  # {'name': 'bar', 'color': 'yellow', 'num': 1}
