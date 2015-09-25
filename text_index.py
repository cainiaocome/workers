#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import os
import sys
import time
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
from whoosh.analysis import Tokenizer,Token
import jieba
from jieba.analyse import ChineseAnalyzer
from pymysql.cursors import DictCursor
import pymysql as mdb
from config import DB_HOST, DB_USER, DB_PASS

#用中文分词器代替原先的正则表达式解释器。
analyzer=ChineseAnalyzer()
schema = Schema(id=NUMERIC(stored=True), name=TEXT(stored=True, analyzer=analyzer))
if not os.path.exists("/var/indexdir"):
    os.mkdir("/var/indexdir")
ix = create_in("/var/indexdir", schema)
dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'ssbc', charset='utf8')
dbconn.autocommit(False)
dbcurr = dbconn.cursor(DictCursor)
dbcurr.execute('SET NAMES utf8')


while True:
    try:
        dbcurr.execute('select * from rt_search_hash')
        rt_rows = dbcurr.fetchall()
        for rt_row in rt_rows:

            # check whether we have met this info_hash
            sql = 'select id from search_hash where info_hash=%s'.format(rt_row['info_hash'])
            row_number = dbcurr.execute(sql)
            if row_number > 0:
                sql = 'delete from rt_search_hash where info_hash=%s'.format(rt_row['info_hash'])
                dbcurr.execute(sql)
                continue

            # now insert it
            placeholders = ', '.join(['%s'] * len(rt_row))
            columns = ', '.join(rt_row.keys())
            sql = 'INSERT INTO search_hash ( %s ) VALUES ( %s )' % (columns, placeholders)
            dbcurr.execute(sql, rt_row.values())

            # we have to retrive it back...
            sql = 'select id from search_hash where info_hash=%s'.format(rt_row['info_hash'])
            row_number = dbcurr.execute(sql)
            rt_row['id'] = dbcurr.fetchone()['id']
            writer = ix.writer()
            writer.add_document(id=rt_row['id'], name=rt_row['name'])
            writer.commit()

            # delete this row from rt_search_hash
            sql = 'delete from rt_search_hash where info_hash=%s'.format(rt_row['info_hash']) 
            dbcurr.execute(sql)

            dbcurr.commit()
    except:
        t,v,_ = sys.exc_info()
        print t,v
    time.sleep(10)

#dbcurr.close()
#dbconn.close()
