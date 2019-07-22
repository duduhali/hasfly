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
    #返回生成的渲染时执行的Python
    def show_python(self):
        assert self.indent_level == 0
        return str(self)

class Templite(object):
    #contexts`是输入的数据与过滤器函数
    def __init__(self, text, *contexts):
        self.context = {}
        for context in contexts:
            self.context.update(context)

        # 创建CodeBuilder对象，开始往里面添加代码
        code = CodeBuilder()
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        for k in self.context.keys():
            code.add_line( "%s = context[%r]" % (k,k) )
        code.add_line("result = []")
        #定义一个flush_output函数，分析模板时，分析的结果会暂存在一段缓冲区中，每分析完一段就会通过flush_output根据缓存的内容往code中添加新代码
        buffered = []
        def flush_output():
            #如果追加的代码段只有一个使用append
            if len(buffered) == 1:
                code.add_line("result.append(%s)" % buffered[0])
            # 其余则使用extend
            elif len(buffered) > 1:
                code.add_line("result.extend([%s])" % ", ".join(buffered))
            # 清空缓存
            del buffered[:]

        # 因为分析控制结构的表达式时会有明确的开始标签与关闭标签，我们需要栈ops_stack来检查是否嵌套得正确
        ops_stack = []

        # 举个例子，当我们遇到{ % if..%}时就会往栈内压入一个if，当遇到{ % endif %}时if就会从栈上被弹出。
        # 我们使用正则表达式将模板文本分解成一系列token
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        # 括起来的标签或者表达式会把字符串分割，括起来的部分本身也是保留下来的。 (?s)是一个flag，它表示.同样可以匹配一个\n。
        for token in tokens:
            if token.startswith('{#'):
                continue # 处理注释{  # ... #}  它的处理方式就是不处理
            elif token.startswith('{{'):
                # 处理数据替换{{ ... }}
                # 我们将花括号切掉，然后调用_expr_code()得到结果，_expr_code()的作用是将模板内的表达式转换成Python表达式，它会在之后实现
                expr = self._expr_code(token[2:-2].strip())
                buffered.append("str(%s)" % expr)
            elif token.startswith('{%'):
                # 处理控制结构{% ... %} 需要对token内的表达式进一步分割进行分析
                flush_output()
                words = token[2:-2].strip().split()
                # 控制结构表达式有三种标签：if ， for ，end，可以通过读取words[0]进行判断
                if words[0] == 'if':
                    # 处理if 标签, 可以接复杂的表达式
                    ops_stack.append('if')
                    code.add_line("if %s:" % self._expr_code(' '.join(words[1:])))
                    code.indent()
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("Don't understand for", token)
                    ops_stack.append('for')
                    code.add_line( "for %s in %s:" % ( words[1],self._expr_code(words[3]) ) )
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
                # 处理文本 文本追加进buffered 就行。
                if token:
                    buffered.append(repr(token))
        if ops_stack: # 在解析完所有的模板文本之后，检查栈是否为空，最后将缓存刷新到结果之中
            self._syntax_error("Unmatched action tag", ops_stack[-1])
        flush_output()


        code.add_line("return ''.join(result)")
        code.dedent()
        # 调用code的get_globals方法会运行我们编译好的代码（注意，代码只是定义了渲染函数，并没有运行该函数），然后我们能够从它返回的名字空间中得到渲染函数
        self._render_function = code.get_globals()['render_function']
        self._show_python = code.show_python

    def _expr_code(self, expr):
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                code = "%s(%s)" % (func, code) # 管道的剩余部分都是过滤器
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])#repr() 函数将对象转化为供解释器读取的形式
            code = "do_dots(%s, %s)" % (code, args)
        else:
            code = "%s" % expr  #Python语言本身就支持的表达式不用处理，原样返回即可
        return code

    def _syntax_error(self, msg, thing):
        """抛出一个语法错误"""
        raise TempliteSyntaxError("%s: %r" % (msg, thing))

    def render(self, context=None):
        # 实现render几乎就是把_render_function封装一下
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def show_python(self):
        return self._show_python()

    def _do_dots(self, value, *dots):
        # 在编译阶段，一个模板表达式x.y.z会被编译为do_dots(x, 'y', 'z')。_do_dots同时实现了取属性与取词典键值，同时如果value能够被调用则调用并更新value
        for dot in dots:
            try:
                value = getattr(value, dot) #获取对象属性值
            except AttributeError:
                value = value[dot] #获取字典值
            if callable(value):
                value = value()    #获取函数返回值
        return value

    """
        class A:
            name = 'yang'
            age = 20
            def say(self):
                return {'one':1,'two':2}

        products = {'name':'123','a':A()}
        print( _do_dots(products, 'a', 'say','one') ) #输出1
    """

    """注意需要使用repr函数在字符串外面加一层引号：
        print repr('abc')     # => 'abc' 
        这是因为buffered内的内容都是转换好的Python代码，如果我们直接追加abc不带引号，那么abc就会被理解成变量名而不是字符串了。
        repr还有自动帮我们添加反斜杠转义特殊字符的功能。
    """

    """
        print( _expr_code( 'user.name.localized|upper|escape') )
        # 调用: _expr_code(user.name.localized|upper|escape)
        # 调用: _expr_code(user.name.localized)
        # 调用: _expr_code(user)
        # user 加入集合
        # upper 加入集合
        # escape 加入集合
        # 输出：escape(upper(do_dots(user, 'name', 'localized')))
    """