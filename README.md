# Django - Blog
---

## Step - 1
---

### Start project

```python
> django-admin startproject blog
```

### Run server

```python
> python3 manage.py runserver
```

### Default language

In `blog/blog/settings.py`, change the settings:

```python
# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'

# 把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'

```
