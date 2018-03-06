# -*- coding: UTF-8 -*-

import pymysql
import traceback

import config
from logger_manager import controller_logger as logger

class DBHelper:
    conn = None
    cursor = None

    def __init__(self):
        self.conn = pymysql.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASS, config.MYSQL_DB,\
                                    use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()
        self.conn.autocommit(1)

    def get_connection(self):
        return self.conn

    def release(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None
        except Exception as e:
            logger.debug('close cursor failure:' + str(e) + '. ' + traceback.format_exc())
        try:
            if self.conn is not None:
                self.conn.close()
                self.conn = None
        except Exception as e:
            logger.debug('close connection failure:' + str(e) + '. ' + traceback.format_exc())

    def query_one(self, sql, param=None):
        """ 
        @summary: 执行查询，并取出第一条 
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来 
        @param param: 可选参数，条件列表值（元组/列表） 
        @return: result list/boolean 查询到的结果集 
        """
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        if count > 0:
            result = self.cursor.fetchone()
        else:
            result = False
        return result

    def query_all(self, sql, param=None):
        """ 
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来 
        @param param: 可选参数，条件列表值（元组/列表） 
        @return: result list/boolean 查询到的结果集 
        """
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        if count > 0:
            result = self.cursor.fetchall()
        else:
            result = False
        return result

    def query_many(self, sql, num, param=None):
        """ 
        @summary: 执行查询，并取出num条结果 
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来 
        @param num:取得的结果条数 
        @param param: 可选参数，条件列表值（元组/列表） 
        @return: result list/boolean 查询到的结果集 
        """
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        if count > 0:
            result = self.cursor.fetchmany(num)
        else:
            result = False
        return result

    def insert_one(self, sql, value):
        """ 
        @summary: 向数据表插入一条记录 
        @param sql:要插入的ＳＱＬ格式 
        @param value:要插入的记录数据tuple/list 
        @return: insertId 受影响的行数 
        """
        self.cursor.execute(sql, value)
        return self.get_insert_id()

    def insert_many(self, sql, values):
        """ 
        @summary: 向数据表插入多条记录 
        @param sql:要插入的ＳＱＬ格式 
        @param values:要插入的记录数据tuple(tuple)/list[list] 
        @return: count 受影响的行数 
        """
        count = self.cursor.executemany(sql, values)
        return count

    def get_insert_id(self):
        """ 
        获取当前连接最后一次插入操作生成的id,如果没有则为０ 
        """
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        result = self.cursor.fetchone()
        return result[0]

    def query(self, sql, param=None):
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """ 
        @summary: 更新数据表记录 
        @param sql: ＳＱＬ格式及条件，使用(%s,%s) 
        @param param: 要更新的  值 tuple/list 
        @return: count 受影响的行数 
        """
        return self.query(sql, param)

    def delete(self, sql, param=None):
        """ 
        @summary: 删除数据表记录 
        @param sql: ＳＱＬ格式及条件，使用(%s,%s) 
        @param param: 要删除的条件 值 tuple/list 
        @return: count 受影响的行数 
        """
        return self.query(sql, param)

    def transaction_begin(self):
        """ 
        @summary: 开启事务 
        """
        self.conn.autocommit(0)

    def transaction_end(self, option='commit'):
        """ 
        @summary: 结束事务 
        """
        if option == 'commit':
            self.conn.commit()
        else:
            self.conn.rollback()

        self.conn.autocommit(1) # 重置事务状态


if __name__ == '__main__':
    db = DBHelper()
    db.query("select * from host_list")
    db.release()

