"""
Configure PyMySQL as the MySQLdb backend so Django can talk to MySQL
without native client libraries.
"""
import pymysql

pymysql.install_as_MySQLdb()
