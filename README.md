# Python的基于MVC模式的Web框架
研究Web框架有所心得于是自己写了一个，用来学习研究，同时也想加入一些其它语言的Web框架的功能和用法。
现在只是具备Web框架的基本功能，很多功能还没来得及实现，很多地方实现的不够优雅，框架结构还不规范。

#依赖说明
依赖： werkzeug

数据库默认使用 sqlite 不需要额外安装数据库驱动，也可以配置使用MySQL，但需要安装 pymysql


#模块说明
ORM模块：flysql

模板引擎模块：flytemplate

路由模块：flyweb

 
# 分支说明 
本人对Flask和Django风格取舍比较纠结，同时又特别喜欢Yii2的框架布局，于是建立了多个分支

*[1]* master 采用Flask的风格，demo目录是自带demo,运行demo下的app.py

*[2]* develop 采用Yii2的风格，hasDemo目录是自带demo,运行hasweb下的run.py

  
