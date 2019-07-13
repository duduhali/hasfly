from flysql.base.field import Field

class ModelMetaclass(type):#元类创建的类的子类会再次调用
    def __new__(cls,name,bases,attrs):
        if name == 'Model' or name == 'BaseModel':
            return type.__new__(cls,name,bases,attrs)
        table = name
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v,Field):
                mappings[k] = v
            elif k == '__table__':
                table = v;
        for k in mappings.keys():
            attrs.pop(k)
        #把属性从类中删除，放到mppings中
        attrs['__mappings__'] = mappings
        attrs['__table__'] = table
        return type.__new__(cls,name,bases,attrs)