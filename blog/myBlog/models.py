from django.db import models
# django.contrib.auth是Django的内置App，专门用于处理网站用户的注册、登陆等流程，User是Django已经写好的用户模型

from django.contrib.auth.models import User

class Category(models.Model):
    """
    Django要求数据库模型必须继承models.Model类
    Category类只需要定义简单的表的列名即可
    CharField表示列名的数据类型，也即字符型
    max_length指定了字符串的最大长度，超过这个长度将不会存入数据库
    """
    name = models.CharField(max_length=100)

class Tag(models.Model):
    """
    标签表和分类表类似
    """
    name = models.CharField(max_length=100)

class Post(models.Model):
    """
    文章表的数据有些复杂，涉及的字段较多。
    而且还需要实现与Tag、Category表的关联
    """

    # 文章标题字段
    title = models.CharField(max_length=70)

    # 正文字段
    # 由于正文较长，需要使用TextFiele类型
    body = models.TextField()

    # 创建时间和修改时间字段
    created_time  = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要字段
    # 这是一个可选字段，也即可以是空的，需要指定blank=True
    excerpt = models.CharField(max_length=200, blank=True)

    # 还需要分类和标签字段
    # 这两个字段需要与分类、标签表相关联
    # 由于一篇文章只能对应一个分类，但是一个分类下可以存在多篇文章，也即1对多的关联关系，实现方式为ForeignKey
    # 对于标签而言，一个文章可以存在多个标签，一个标签下也可以存在多篇文章，为多对多的关联关系，实现方式为ManyToMany
    # 同时，文章必须分类，但是可以没有标签，因此tags字段需要指定blank=True
    category = models.ForeignKey(Category)
    tags = models.ManyToMany(Tag, blank=True)

    # 文章作者字段
    # 文章和作者之间也是1对多关联关系
    author = models.ForeignKey(User)

