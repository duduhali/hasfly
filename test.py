from flytemplate import Templite
from collections import namedtuple

template_text = """
<p>Welcome, {{user_name}}!</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    <li>{{ product.name }}:
        {{ product.price|format_price}}</li>
{% endfor %}
</ul>
"""

Product = namedtuple("Product",["name", "price"])
product_list = [Product("Apple", 1), Product("Fig", 1.5), Product("Pomegranate", 3.25)]

def format_price(price):
    return "$%.2f" % price

#product_list2 = [{'name':'123','price':1},{'name':'abc','price':1.25}]
t = Templite(template_text, {"user_name":"Charlie", "product_list":product_list}, {"format_price":format_price})
print(t.render())