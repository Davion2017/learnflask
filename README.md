- 创建虚拟环境，添加所需的模块
```bash
pip install -r ./requirements.txt
```

- 根据自己本机配置修改config.py里的USERNAME和PASSWORD

- 创建数据库
```bash
create database test_demo character set utf8 collate utf8_general_ci;
```

- 合并数据库
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```