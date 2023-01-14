import os
import jieba
import pymysql


## mine 
inputs = open('medicine.txt', "r")

medicine = set()
for line in inputs:
    medicine.append(line)
inputs.close()


inputs = open('keyword.txt', "r")

keyword = set()
for line in inputs:
    keyword.append(line)
inputs.close()


tag_map = {}

datasetDir = "./dataset"
for name in os.listdir(datasetDir):

    dataFile = datasetDir + "/" + name
    with open(dataFile, 'r') as fr:
        data = jieba.cut(fr.read())

    data = dict(Count(data))
    for k, v in data.items():
        if k in keyword:
            tag_map[k] = {}

    for k, v in data.items():
        if k in medicine:
            for kk in tag_map:
                if k not in tag_map[kk]:
                    tag_map[kk][k] = 0
                tag_map[kk][k] += v


for k in tag_map:
    cnt = 0
    for kk in tag_map[k]:
        cnt += tag_map[k][kk]
    
    for kk in tag_map[k]:
        tag_map[k][kk] = tag_map[k][kk] * 1.0 / cnt

### insert mysql
conn=pymysql.connect(host = '127.0.0.1' # 连接名称，默认127.0.0.1
    ,user = 'root' # 用户名
    ,passwd='password' # 密码
    ,port= 3306 # 端口，默认为3306
    ,db='recommend_db' # 数据库名称
    ,charset='utf8' # 字符编码
)

cur = conn.cursor() # 生成游标对象

for k in tag_map:
    for kk in tag_map[k]:
        sql = "INSERT INTO tag_recommend('tag', 'medicine', 'ratio') VALUES ('" + k + "', '"+ kk + "', " tag_map[k] + ")"

        try:
            cur.execute(sql1) # 执行插入的sql语句
            conn.commit() # 提交到数据库执行
        except:
            coon.rollback()# 如果发生错误则回滚

conn.close() # 关闭数据库连接
