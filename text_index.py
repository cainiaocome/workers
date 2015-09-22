#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import os
from whoosh.index import create_in, open_dir
from whoosh.query import Term
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
from whoosh.analysis import Tokenizer,Token
import jieba
from jieba.analyse import ChineseAnalyzer
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
dbcurr = dbconn.cursor()
dbcurr.execute('SET NAMES utf8')

row_number = dbcurr.execute('select id,name from search_hash')
while row_number>0:
    row = dbcurr.fetchone()
    row_number = row_number - 1
    writer = ix.writer()
    writer.add_document(id=row[0], name=row[1])
    writer.commit()
    print row[0],row[1]

dbcurr.close()
dbconn.close()
