import re
class TempliteSyntaxError(ValueError):
    """Raised when a template has a syntax error."""
    pass

# 代码构建器是为了方便Templite生成代码而编写的小工具，它的工作主要有添加代码、控制缩进、返回完整的代码字符串等
class CodeBuilder(object):
    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    # 返回生成的代码字符串，遍历code的内容时如果遇到CodeBuilder对象，则会递归调用该对象的__str__方法。
    def __str__(self):
        return "".join(str(c) for c in self.code)

    # 添加一行代码，它会自动缩进
    def add_line(self, line):
        self.code.extend([" " * self.indent_level, line, "\n"])

    #会在code上追加一个section(CodeBuilder对象)并返回，可以理解为section在code中先占一个位置，其中的代码会在之后通过操作返回的section(CodeBuilder对象)补上
    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    INDENT_STEP = 4      # PEP8 标准4空格缩进
    # indent与dedent分别表示增长与减小缩进等级：
    def indent(self):
        """增加一级缩进"""
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        """减小一级缩进"""
        self.indent_level -= self.INDENT_STEP

    # 返回代码的运行结果
    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace

class Templite(object):

    def __init__(self, text, *contexts):
        """`text`是输入的模板
        `contexts`是输入的数据与过滤器函数

        使用的是*contexts，这意味着可以输入多个上下文，下面这些做法都是有效的：
        t = Templite(template_text)
        t = Templite(template_text, context1)
        t = Templite(template_text, context1, context2)
        """
        self.context = {}
        for context in contexts:
            self.context.update(context)

        # 所有的变量名
        self.all_vars = set()
        # 属于循环的变量名
        self.loop_vars = set()

        # 创建CodeBuilder对象，开始往里面添加代码
        code = CodeBuilder()
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        # 先加个section占位，从上下文提取变量的代码在之后实现
        vars_code = code.add_section()
        code.add_line("result = []")
        code.add_line("append_result = result.append")
        code.add_line("extend_result = result.extend")
        code.add_line("to_str = str")
        #为什么添加这些代码，可以参考 test_one.py

        #定义一个flush_output函数，分析模板时，分析的结果会暂存在一段缓冲区中，每分析完一段就会通过flush_output根据缓存的内容往code中添加新代码
        buffered = []
        def flush_output():
            #如果追加的代码段只有一个使用append
            if len(buffered) == 1:
                code.add_line("append_result(%s)" % buffered[0])
            # 其余则使用extend
            elif len(buffered) > 1:
                code.add_line("extend_result([%s])" % ", ".join(buffered))
            # 清空缓存
            del buffered[:]

        # 因为分析控制结构的表达式时会有明确的开始标签与关闭标签，我们需要栈ops_stack来检查是否嵌套得正确
        ops_stack = []

        # 举个例子，当我们遇到{ % if..%}时就会往栈内压入一个if，当遇到{ % endif %}时if就会从栈上被弹出。
        # 我们使用正则表达式将模板文本分解成一系列token
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        # 括起来的标签或者表达式会把字符串分割，括起来的部分本身也是保留下来的。 (?s)是一个flag，它表示.同样可以匹配一个\n。

        """这里举个例子，如果输入以下文本：
        < p > Topicsfor {{name}}: { %for t in topics %}{{t}}, {% endfor %} < / p >
        那么正则后会得到：
            [
                '<p>Topics for ',  # 文本
                '{{name}}',  # 表达式
                ': ',  # 文本
                '{% for t in topics %}',  # 标签
                '',  # 文本 (空)
                '{{t}}',  # 表达式
                ', ',  # 文本
                '{% endfor %}',  # 标签
                '</p>'  # 文本
            ]  
        一旦文本被被分割成了一系列的token，我们就能遍历token一段一段处理了：
        得到的token类型可能有四种：
            文本
            注释：{# ... #}
            数据替换：{{ ... }}
            控制结构：{% ... %}
        """
        for token in tokens:
            if token.startswith('{#'):
                # 处理注释{  # ... #}  它的处理方式就是不处理
                continue
            elif token.startswith('{{'):
                # 处理数据替换{{ ... }}
                # 我们将花括号切掉，然后调用_expr_code()得到结果，_expr_code()的作用是将模板内的表达式转换成Python表达式，它会在之后实现
                expr = self._expr_code(token[2:-2].strip())
                buffered.append("to_str(%s)" % expr)
            elif token.startswith('{%'):
                # 处理控制结构{% ... %} 需要对token内的表达式进一步分割进行分析
                flush_output()
                words = token[2:-2].strip().split()
                # 控制结构表达式有三种标签：if ， for ，end，可以通过读取words[0]进行判断
                if words[0] == 'if':
                    # 处理if 标签
                    if len(words) != 2:
                        self._syntax_error("Don't understand if", token)
                    ops_stack.append('if')
                    code.add_line("if %s:" % self._expr_code(words[1]))
                    code.indent()
                    # 这里的if只能支持一个表达式，所以如果words大于2就直接报错。我们往栈中弹入一个if标签，直到找到一个endif标签才弹出
                elif words[0] == 'for':
                    # 处理for 标签
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    ops_stack.append('for')
                    # 其中_variable函数的作用是检查变量名是否合法，如果合法则将变量名存入变量集中，这里的变量集是loop_vars，否则会报语法错误，它也会在之后实现
                    self._variable(words[1], self.loop_vars)
                    code.add_line(
                        "for c_%s in %s:" % (
                            words[1],
                            self._expr_code(words[3])
                        )
                    )
                    code.indent()
                    # words[3] 是迭代表达式需要经过_expr_code转换
                elif words[0].startswith('end'):
                    # 处理end标签  主要工作就是ops_stack弹出检查和取消一级缩进：
                    if len(words) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if not ops_stack:
                        self._syntax_error("Too many ends", token)
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error("Mismatched end tag", end_what)
                    code.dedent()
                else:
                    self._syntax_error("Don't understand tag", words[0])
            else:
                # 处理文本 文本追加进buffered就行。
                if token:
                    buffered.append(repr(token))
                """注意需要使用repr函数在字符串外面加一层引号：
                print repr('abc')     # => 'abc' 
                这是因为buffered内的内容都是转换好的Python代码，如果我们直接追加abc不带引号，那么abc就会被理解成变量名而不是字符串了。
                repr还有自动帮我们添加反斜杠转义特殊字符的功能。
            """

        # 在解析完所有的模板文本之后，检查栈是否为空，最后将缓存刷新到结果之中
        if ops_stack:
            self._syntax_error("Unmatched action tag", ops_stack[-1])
        flush_output()

        """再看一眼模板文本：
            <p>Welcome, {{user_name}}!</p>
            <p>Products:</p>
            <ul>
            {% for product in product_list %}
                <li>{{ product.name }}:
                    {{ product.price }}</li>
            {% endfor %}
            </ul>
        可以看到模板中存在三个变量user_name、product_list与product，all_vars会包含以上所有的变量名，loop_vars只会包含product。
        所以我们根据它们的差集提取数据，vars_code就是之前add_section得到的CodeBuilder对象："""
        for var_name in self.all_vars - self.loop_vars:
            vars_code.add_line("c_%s = context[%r]" % (var_name, var_name))

        code.add_line("return ''.join(result)")
        code.dedent()
        # 调用code的get_globals方法会运行我们编译好的代码（注意，代码只是定义了渲染函数，并没有运行该函数），然后我们能够从它返回的名字空间中得到渲染函数
        self._render_function = code.get_globals()['render_function']

    def _expr_code(self, expr):
        """
        它处理的对象可能只是一个简单的数据名：{{user_name}}
        也可能是需要包括一系列的属性检索和过滤：{{user.name.localized|upper|escape}}
        因为复杂的表达式可以由简单的表达式组成，所以我们将_expr_code设计成递归调用的函数
        """
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                # 管道的剩余部分都是过滤器，我们将过滤器函数更新进all_vars
                self._variable(func, self.all_vars)#判断函数名是否合法并加入集合
                code = "c_%s(%s)" % (func, code)
        # 接下来处理过滤器中的点操作，因为有了do_dots这个函数的帮助（在渲染阶段实现，之后会具体讲），只要将诸如a.b.c.d形式的表达式转换成do_dots(a, 'b', 'c', 'd')就可以了
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])#repr() 函数将对象转化为供解释器读取的形式
            code = "do_dots(%s, %s)" % (code, args)
        else:
            self._variable(expr, self.all_vars)
            code = "c_%s" % expr  #Python语言本身就支持的表达式不用处理，原样返回即可
        return code

    def _syntax_error(self, msg, thing):
        """抛出一个语法错误"""
        raise TempliteSyntaxError("%s: %r" % (msg, thing))

    def _variable(self, name, vars_set):
        # 实现_variable函数帮助我们将变量存入指定的变量集中，同时帮我们验证变量名的有效性
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._syntax_error("Not a valid name", name)
        vars_set.add(name)

    def render(self, context=None):
        # 实现render几乎就是把_render_function封装一下
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, *dots):
        # 在编译阶段，一个模板表达式x.y.z会被编译为do_dots(x, 'y', 'z')。_do_dots同时实现了取属性与取词典键值，同时如果value能够被调用则调用并更新value
        for dot in dots:
            try:
                value = getattr(value, dot) #获取对象属性值
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value