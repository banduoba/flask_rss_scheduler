# 0x00 项目说明

这是一个RSS文章聚合的WEB项目，可以自行加入喜欢的rss任务，该程序会自动爬取并展示在网页上。

> 部分rss订阅数据来源：https://docs.rsshub.app/

**博客地址：https://blog.otakuzx.com/archives/2022/02/05/67.html**

# 0x01 项目截图

![QQ截图20220205153742.png][1]

# 0x02 部署说明

1.配置数据库，位于`config/config.json`

```
...
"db": {
    ...
    "user": "数据库用户名",
    "pass": "数据库密码",
    "dbnm": "数据库名"
  },
...
```

2.修改一个`.py`文件，位于`common/common_utils.py`，这一步是代码问题可以自行修改
```python
...
    # 将 xxx 改为你的工程名
    @staticmethod
    def get_project_root_path():
        return os.path.abspath(os.path.dirname(__file__)).split("xxx")[0] + "xxx"
...
```

3.创建数据库
```
flask db init
flask db migrate
flask db upgrade
```

4.运行项目
```
# 虚拟环境自行安装
python app.py
```

5.添加`rss`订阅任务

> 在`tasks`表中按照字段添加即可。

其它自行参考代码，懒~

  [1]: https://blog.otakuzx.com/usr/uploads/2022/02/2100693474.png
