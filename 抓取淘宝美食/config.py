#数据库配置文件
import pymysql
config = {
          'host':'192.168.10.10',
          'user':'homestead',
          'password':'secret',
          'db':'toutiao',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }

#设置PhantomJS的配置（在官网的api中寻找）
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
#设置全局变量
KEYWORD = '美食'