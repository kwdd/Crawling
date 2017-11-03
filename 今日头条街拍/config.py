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
#设置全局变量
GROUP_START = 1
GROUP_END = 20
KEYWORD = '街拍'
