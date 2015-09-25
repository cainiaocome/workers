#!/usr/bin/env python2.7
# encoding: utf-8

import pymysql as mdb
from config import DB_HOST, DB_USER, DB_PASS

#create_database_ssbc = 'create database if not exists ssbc;'  :(

create_table_search_filelist = '''
create table if not exists search_filelist
(
    info_hash varchar(40),
    file_list text,
    primary key (info_hash)
)
'''
# real time search_hash for whoosh to index
# one column less than search_hash: id
create_table_rt_search_hash = '''
create table if not exists rt_search_hash
(
    info_hash varchar(40) unique,
    category varchar(20),
    data_hash varchar(32),
    name varchar(255),
    extension varchar(20),
    classified boolean default 0,
    source_ip varchar(20),
    tagged boolean default 0,
    length bigint unsigned,
    create_time date,
    last_seen date,
    requests int unsigned,
    comment varchar(255),
    creator varchar(20),
    primary key (info_hash)
)
'''
create_table_search_hash = '''
create table if not exists search_hash
(
    id int unsigned AUTO_INCREMENT,
    info_hash varchar(40) unique,
    category varchar(20),
    data_hash varchar(32),
    name varchar(255),
    extension varchar(20),
    classified boolean default 0,
    source_ip varchar(20),
    tagged boolean default 0,
    length bigint unsigned,
    create_time date,
    last_seen date,
    requests int unsigned,
    comment varchar(255),
    creator varchar(20),
    primary key (id)
)
'''
create_table_search_statusreport = '''
create table if not exists search_statusreport
(
    date date unique,
    new_hashes int,
    total_requests int,
    valid_requests int
)
'''

dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, 'ssbc', charset='utf8')
dbconn.autocommit(False)
dbcurr = dbconn.cursor()
dbcurr.execute('SET NAMES utf8')

dbcurr.execute(create_table_search_filelist)
dbconn.commit()
dbcurr.execute(create_table_rt_search_hash)
dbconn.commit()
dbcurr.execute(create_table_search_hash)
dbconn.commit()
dbcurr.execute(create_table_search_statusreport)
dbconn.commit()
dbconn.close()
