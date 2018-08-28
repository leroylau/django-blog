# Flask tutorial

Flask作为一种轻量型的Web开发框架，只提供了web开发的核心功能，但是保留了功能扩展的能力，这一点和Python语言的理念是一致的。

基于Flask开发大型Web应用时，需要将不同功能隔离开，这一点是通过蓝图实现的。使用蓝图的flask应用实际上就是包含了不同子包的Python程序包，每个子包是一个蓝图，蓝图本身在子包内部定义，最终在Python程序包的顶层`__init__.py`文件中导入并注册。

蓝图经过注册后，在子包内部(视图函数)便可以使用蓝图来创建路由。

>针对大型应用的理想方案：
>一个项目实例化一个应用，初始化多个扩展，并注册很多个蓝图。

蓝图不仅可以提供视图功能，还可以提供模板过滤器、静态文件、模板和其他工具，而不必执行应用或者视图函数。

## 一个基本的flask应用

首先创建一个文件夹，如果需要进行版本控制的话，例如使用`git`，可以首先`git init`一下。然后创建flask应用文件夹，一般以flask应用的名称来命名，例如`blog`,`todo`等，其他先不要管，后续会慢慢增加。

```
|-blog-project
    |-blog/
    |-README.md
    |-.gitignore
```

以`blog`为例，首先将此文件夹设置为一个Python包，也即创建一个`__init__.py`文件。

```
|-blog
    |-__init__.py
```

由于Python解释器在导入一个程序包时，首先会读取包内的`__init__.py`文件，因此flask应用的构建可以在`__init__.py`文件中实现。


```python
from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello World!"
```

这样便实现了一个最简单的flask应用。

运行这个应用有以下两种方式：

* flask run

`cd`进入项目文件夹`blog-project`路径下，首先配置一些临时的系统环境变量：


```bash
$ export FLASK_APP=blog
$ export FLASK_ENV=development
```

第一个是让flask知道哪个才是我们的应用文件夹，第二个是将flask设置为开发模式。

然后继续输入`flask run`，点击或输入提示给出的url，会出现错误，这是因为我们没有实现base url的页面，而是实现了`http://127.0.0.1:5000/hello`页面。

* 创建一个py文件


```python
# run.py
from blog import app
app.run(debug=True)
```

在命令行输入`python run.py`即可。

## 使用html模板

在(1)中，我们实际上没有创建任何html页面，只是返回了一个固定的字符串，让浏览器渲染输出`Hello World!`，如果我们想要根据用户输入来创建动态显示的页面呢？

例如用户访问`http://127.0.0.1:5000/William`，浏览器渲染输出为`Hello William!`。

对于此例而言，其实直接将字符串返回也可以，但是对于复杂的html页面将会面临维护难和难扩展的问题，因此需要将html内容和视图函数解耦(也就是不在一个地方实现)。

此时需要一个html页面来完成，html内容如下：

```html
<!DOCTYPE html>
<html>
    <head>
        <title>
            My Blog
        </title>
    </head>
    <body>
        Hello {{name}}!
    </body>
</html>
```

Flask引入了`templates`概念，基于`jinjia2`模板引擎，可以将业务逻辑处理代码中的相关参数传入到模板中，然后返回一个完整的html页面。这一过程是通过Flask中的`render_template`函数实现的，这个函数需要传入模板名(str)，以及所需的模板内部的变量(如果模板中设置了变量的话)。

```python
# __init__.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

## 视图和构建隔离

在(2)中，视图和应用构建(`__init__.py`)整合在一起，当视图增加时，会导致构建文件非常臃肿，也不利于维护。

在flask应用文件夹下(`blog`)，新建`views.py`文件，将(2)中`__init__.py`中的视图函数转移到`views.py`中。


```python
from flask import render_template
from blog import app

@app.route('/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

此时`__init__.py`只保留了flask应用的构建。


```python
from flask import Flask
app = Flask(__name__)
from blog import views
```

`__init__.py`中最后`from blog import views`非常重要，由于`views.py`中需要从`blog`包导入构建的`app`对象，这样可以避免循环导入。

现在就可以根据网页的设计不断的增加视图函数了，由于视图函数与url是一种映射关系，随着视图函数的增加会出现两个问题：

* 视图函数文件随着网页功能的增加会变得非常臃肿，而且难以协同维护
* 视图函数对应的html文件会相应的增加，如果每个html文件都是各自维护的话，会导致风格统一问题，维护难度也会增加。

上述两个问题可以总结为如何将flask应用视图和html页面的`可扩展`和`易维护`的问题。

对于html而言，Flask借助`jinjia2`的模板继承解决了这一问题。

## 模板继承

将不同的html内容中共同的部分移出，然后放在一个基础html页面中，其他html页面可以从这个基础html页面导入得到这些共同部分。

我们来修改一下我们的html文件，`hello.html`实际上是用户登录后显示的页面，修改一下html文件和视图函数中的名称，相应修改为`user.html`和`after_login()`函数，在`user.html`三个地方需要优化：

* title标签采用用户名字来显示是谁的blog
* html页面显示`Hi user.name`
* 将所有该用户的blog以列表的形式显示

首先实现一个`base.html`：


```html
<!DOCTYPE html>
<html>
    <head>
        {% if name %}
            <title>{{ name }} - Blog</title>
        {% else %}
            <title>Blogr</title>
        {% endif %}
    </head>
    <body>
        <div>
            <b>Hi {{ name }}</b>
        </div>
        <hr>
        {% block content %}
        {% endblock %}
    </body>
</html>
```

然后`user.html`从`base.html`继承：


```html
{% extends 'base.html' %}

{% block content %}
    {% for post in posts %}
    <ul>
        <li>
            {{ name }} says: {{ post }}
        </li>
    </ul>
    {% endfor%}
{% endblock %}
```

这样在使用`render_template`渲染这个页面时，不仅要传入用户名称，还需要传入该用户的blog内容，正常情况下，用户名称来源于用户登录时填写的表单，而用户blog内容来源于数据库，这些先不要管，将这些内容以`hard coding`的形式写到代码中。

实际上还需要一个用户没有登录时的home页面，也可以从`base.html`继承，但是由于`base.html`写入了用户没有登录时的页面逻辑，因此这一点可以在业务代码中实现，方式如下就是使用两个装饰器函数来装饰视图函数。

这样视图函数：


```python
from flask import render_template
from blog import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/<name>')
def user(name):
    posts = [
        {
            'name' : 'William',
            'body' : "A lovely day."
        },
        {
            'name' : 'William',
            "body" : 'A trip to Japan.'
        }
    ]
    return render_template('user.html', name=name, posts=posts)
```

## 蓝图(blueprint)

实现了html模板和模板继承，就实现了业务代码和网页设计的分离，下一步是解决视图函数的问题。以blog项目为例，这个项目可以划分为两大部分，一部分是用户管理，主要是用户的注册和登录，这一部分需要与数据库相关联，另外一部分是blog本身，例如blog的home页面，用户登录后的user页面，以及用户写blog的create页面，两个部分之间的关系就是用户登录后需要重定向到用户页面，并将数据库中的内容渲染到html页面中。

有两种处理方式：

(1) 将`views.py`文件拆分为两个视图函数文件(`auth.py`和`post.py`)，将templates文件夹中的除base.html外，划分为auth和blog两个文件夹，然后在两个视图函数文件中分别定义两个蓝图对象，最后在`__init__.py`中注册一下就可以了。

第一种处理方式的项目结构如下：


```
|-blog
    |-__init__.py
    |-auth.py
    |-post.py
    |-templates/
        |-base.html
        |-auth/
        |-post/
```

如果觉得第一种方式对功能分离的还不够彻底的话，可以采用第二种方式：

(2) 将templates和视图函数文件按照`auth`和`post`拆分为两个Python子包，这两个子包内部结构和blog项目的结构是一样的。

第二种处理方式的项目结果如下：


```
|-blog
    |-__init__.py
    |-auth/
        |-__init__.py
        |-views.py
        |-templates/
    |-post/
        |-__init__.py
        |-views.py
        |-templates/
    |-templates
```

第二种方式解耦的更加彻底一下。

### 蓝图的定义和注册

蓝图不是一个可插拔的应用，应为蓝图并非真正的应用，而是一套可以注册在应用中的操作，而且支持反复注册。蓝图有自己的缺点，就是一旦应用被创建，必须销毁整个应用对象才可以注销蓝图。

>蓝图的基本概念：
>在蓝图被注册到应用后，当被分配请求时，Flask会将蓝图和其对应的视图函数关联起来，并生成两个端点之间的URL，进而执行相关操作。

以`post`蓝图为例，该功能的蓝图定义如下：


```python
from flask import Blueprint

blog = Blueprint('auth', __name__)
```

对于第一种方式，上述代码位于`post.py`文件中，`blog`包的`__init__.py`文件中注册该蓝图如下：

```python
from flask import Flask
from blog.post import blog

app = Flask(__name__)
app.register_blueprint(blog)
```

对于第二种方式，蓝图定义一般放在蓝图构建文件`__init__.py`中，而且蓝图子包内部的文件结构与整个项目的文件结构类似，其内部也存在一个templates文件夹。为了让flask找到蓝图对应的模板文件，就需要在创建蓝图时指定模板文件夹的位置。方式如下：


```python
from flask import Blueprint

blog = Blueprint('blog', __name__, template_folder='templates')

from blog.post import views
```

也即使用了`Blueprint`的*template_folder*参数，对于静态文件，路径可以使绝对或者相对于蓝图的资源文件夹，上述代码中就使用了相对于蓝图的文件夹。

>由于存在多个templates文件夹，模板文件的搜索规则为：
>模板文件夹被添加到模板的搜索路径，但优先级低于实际应用的模板文件夹。这样就 可以轻松地重载在实际应用中蓝图提供的模板。这也意味着如果你不希望蓝图模板出 现意外重写，那么就要确保没有其他蓝图或实际的应用模板具有相同的相对路径。 多个蓝图提供相同的相对路径时，第一个注册的优先。

为了避免蓝图加载时的模板被实际应用的模板文件重载，在上述的代码的路径设定下，实际加载的模板路径为`blog/post/templates/post/index.html`。因此蓝图文件夹内的templates文件夹最好按照这样的结构存在模板文件，也即：


```
|-blog
    |-__init__.py
    |-templates/
    |-auth/
    |-post/
        |-__init__.py
        |-templates/
            |-base.html
            |-post/
                |-index.html
                |-user.html
```

此时`post`蓝图的视图文件为：


```python
from flask import render_template, url_for
from flaskr.post import blog

@blog.route('/')
@blog.route('/index')
def index():
    return render_template('post/index.html')

@blog.route('/<name>')
def user(name):
    posts = [
        {
            'name' : 'William',
            'body' : "A lovely day."
        },
        {
            'name' : 'William',
            "body" : 'A trip to Japan.'
        }
    ]
    return render_template('post/user.html', name=name, posts=posts)
```
