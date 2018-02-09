# ChinaEInvoice
Chinese electronic incovice management and identification by Flask0.12 and Apache2.4
# requirements：
Flask_SQLAlchemy==2.2
Wand==0.4.4
Werkzeug==0.12.2
WTForms==2.1
Flask_Bootstrap==3.3.7.1
pyzbar==0.1.4
Flask_WTF==0.14.2
Flask==0.12.2
SQLAlchemy==1.1.11
Flask_Login==0.4.0
Pillow==5.0.0
Flask==0.12.2
Jinja2==2.9.6
# deployment
flask 0.12+python3.5+windows server 2008 R2+Apache24

http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/

apache版本选择：需要和python的visual C++编译版本和CPU位数版本一致
python VC版本对比
https://stackoverflow.com/questions/2676763/what-version-of-visual-studio-is-python-on-my-computer-compiled-with
For this version of Visual C++  Use this compiler version
Visual C++ 4.x                  MSC_VER=1000
Visual C++ 5                    MSC_VER=1100
Visual C++ 6                    MSC_VER=1200
Visual C++ .NET                 MSC_VER=1300
Visual C++ .NET 2003            MSC_VER=1310
Visual C++ 2005  (8.0)          MSC_VER=1400
Visual C++ 2008  (9.0)          MSC_VER=1500
Visual C++ 2010 (10.0)          MSC_VER=1600
Visual C++ 2012 (11.0)          MSC_VER=1700
Visual C++ 2013 (12.0)          MSC_VER=1800
Visual C++ 2015 (14.0)          MSC_VER=1900
Visual C++ 2017 (15.0)          MSC_VER=1910
python版本：Python 3.5.0 (v3.5.0:374f501f4567, Sep 13 2015, 02:27:37) [MSC v.1900 64 bit (AMD64)] on win32
apache下载版本https://www.apachelounge.com/download/VC14/
注意：要安装VC_redist.x64.exe 后解压httpd-2.4.29-Win64-VC15.zip

安装 mod_wsgi：
windows 2008 直接 pip install mod_wsgi 失败
手动下载地址：
https://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi
下载mod_wsgi-4.5.24+ap24vc14-cp35-cp35m-win_amd64.whl 手动安装

在网站根目录下新建.wsgi文件

Ei.wsgi:
import sys, os

#Expand Python classes path with your app's path
sys.path.insert(0, os.path.dirname(__file__))
from app import app as application

application为mod_wsgi可以识别名，不能修改

配置apache httpd.config
mod_wsgi配置
安装号mod_wsgi 后 命令行运行mod_wsgi-express module-config
C:\Users\Administrator>mod_wsgi-express module-config
LoadFile "c:/users/administrator/appdata/local/programs/python/python35/python35.dll"
LoadModule wsgi_module "c:/users/administrator/appdata/local/programs/python/python35/lib/sitepackages/mod_wsgi/server/mod_wsgi.cp35-win_amd64.pyd"
WSGIPythonHome "c:/users/administrator/appdata/local/programs/python/python35"
将结果复制到httpd.config下

编写虚拟路径
<VirtualHost *:8080>
    ServerName example.com
    WSGIScriptAlias / D:\Project\Ei\Ei.wsgi
    <Directory D:\Project\Ei>
        Order deny,allow
        Allow from all
		Require all granted
    </Directory>
</VirtualHost>

 修改监听端口
Listen 8080

部署apache服务：
httpd.exe -k install
