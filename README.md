1. 首先下载源代码

	```bash
	$ git clone https://github.com/2021-SPM/Forum.git
	```

2. 进入代码目录后创建虚拟环境，然后安装模块

	```bash
	$ pip install -r requirements.txt
	```

3. 转移数据库

	```bash
	$ python manage.py makemigrations
	```

	```bash
	$ python manage.py migrate
	```

4. 创建管理员

	```bash
	$ python manage.py createsuperuser
	```

5. 运行

	```bash
	$ python manage.py runserver
	```

