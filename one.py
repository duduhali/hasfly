import re



class Templite(object):
    def __init__(self, text, *contexts):
        self.context = {}
        for context in contexts:
            self.context.update(context)
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        #  括起来的标签或者表达式会把字符串分割，括起来的部分本身也是保留下来的。 (?s)是一个flag，它表示.同样可以匹配一个\n。
        print(tokens)
        result = []
        for token in tokens:
            if token.startswith('{#'):
                # 处理注释{  # ... #}  它的处理方式就是不处理
                continue
            elif token.startswith('{{'):
                # 处理数据替换{{ ... }}
                pass
            elif token.startswith('{%'):
                # 处理控制结构{% ... %} 需要对token内的表达式进一步分割进行分析
                pass
            else:
                result.append(token)
        print(result)
    def render(self):
        pass


template_text = """
<p>Welcome, {{user_name}}!</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    <li>{{ product.name }}:{{ product.price|format_price}}</li>
{% endfor %}
</ul>
"""
def render_function(context, do_dots):
    c_user_name = context['user_name']
    c_product_list = context['product_list']
    c_format_price = context['format_price']

    result = []
    result.extend([
        '<p>Welcome, ',
        str(c_user_name),
        '!</p>\n<p>Products:</p>\n<ul>\n'
    ])
    for c_product in c_product_list:
        result.extend([
            '\n    <li>',
            str(do_dots(c_product, 'name')),
            str(c_format_price(do_dots(c_product, 'price'))),
            '</li>\n'
        ])
    result.append('\n</ul>\n')
    return ''.join(result)
def _do_dots(value, *dots):
    # 在编译阶段，一个模板表达式x.y.z会被编译为do_dots(x, 'y', 'z')。_do_dots同时实现了取属性与取词典键值，同时如果value能够被调用则调用并更新value
    for dot in dots:
        try:
            value = getattr(value, dot) #获取对象属性值
        except AttributeError:
            value = value[dot]
        if callable(value):
            value = value()
    return value
def format_price(price):
    return "$%.2f" % price
product_list = [{'name':'123','price':1},{'name':'abc','price':1.25}]
if __name__ == '__main__':
    Templite(template_text, {"user_name": "Charlie", "product_list": product_list}, {"format_price": format_price})
    # context = {"user_name": "Charlie", "product_list": product_list, "format_price": format_price}
    # result = render_function(context,_do_dots)
    # print(result)