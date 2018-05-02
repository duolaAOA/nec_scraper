# -*-coding:utf-8 -*-

from nec_scraper.commands.mysqlHelper import MysqlHelper, sql_create_table


class MysqlInit(object):
    """数据库初始化操作"""
    def __init__(self):
        self.db_helper = MysqlHelper()

    def start(self):
        # 新建数据库
        print("trying to create database")
        try:
            self.db_helper.create_database()
        except Exception as e:
            print("create data_base with problem\n", e)
        else:
            print("Create Data_base Successful!")

        # 新建表
        print("trying to create table")
        try:
            for i in range(len(sql_create_table)):
                # 在命令行中sql执行创建多张表没问题， 但程序执行就出问题，
                # 所以改为循环执行
                self.db_helper.create_table(sql_create_table[i])
        except Exception as e:
            print("create table with problem \n", e)
        else:
            print("Create table Successful!")


if __name__ == "__main__":
    MysqlInit().start()
