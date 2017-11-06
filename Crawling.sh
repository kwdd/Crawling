#! /bin/bash
#这是一个获取log日志真实ip的脚本,需要传入log日志的名字

#更新频率：周更3-5篇
echo '/***********东北证券行业报告抓取日志***************/' >> ./error_log/dbzq.log
echo "东北证券爬取开始"
./东北证券/spider.py >> ./error_log/dbzq.log
echo "东北证券爬取结束"
echo '/***********东北证券行业报告抓取结束***************/' >> ./error_log/dbzq.log
echo '                                                ' >>./error_log/dbzq.log
#更新频率：工作日（每周五天）
echo '/***********中国证监会招股说明书抓取开始***************/' >> ./error_log/dbzq.log
echo "中国证监会爬取开始"
./中国证监会/spider.py >> ./error_log/dbzq.log
echo "中国证监会爬取结束"
echo '/***********中国证监会招股说明书抓取结束***************/' >> ./error_log/dbzq.log
echo '                                                ' >>./error_log/dbzq.log
#更新频率：周更3-5篇
echo '/***********投中研究院报告抓取开始***************/' >> ./error_log/dbzq.log
echo "投中研究院报告爬取开始"
./投中研究院/spider.py >> ./error_log/dbzq.log
echo "投中研究院报告爬取结束"
echo '/***********投中研究院报告抓取结束***************/' >> ./error_log/dbzq.log
echo '                                                ' >>./error_log/dbzq.log