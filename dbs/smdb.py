import mysql.connector
from datetime import date, datetime
from mysql.connector import errorcode
import random
import logging
logger = logging.getLogger('smdb')
config = {
  'user': 'root',
  'password': 'qin_XIA_2018',
  'host': '127.0.0.1',
  'database': 'suanming',
  'raise_on_warnings': True,
}


class smdb:
  def __init__(self):
    self.__cursor = []
    self.__cnx = None    
  def __openconnection(self):
    self.__cnx = mysql.connector.connect(**config)
  def __opencursor(self,buffered=False):
    if buffered:
        self.__cursor.append(self.__cnx.cursor(buffered = True))
    else:
        self.__cursor.append(self.__cnx.cursor())
    self.__cursor.append(self.__cnx.cursor())
  def __close(self):
    for c in self.__cursor:
      c.close()
      self.__cursor = []
    self.__cnx.close()
  
  def create_user(self,userid,datas):
    '''
      创建账号
    '''
    sql = 'insert into userdata(userid,datas) values (%s,%s)'
    try:
      self.__openconnection()
      self.__opencursor()
      cursor = self.__cursor[0]
      cursor.execute(sql,(userid,datas))
      self.__cnx.commit()
    except mysql.connector.Error as err:
      logger.exception('create_user:{0}'.format(err))
    finally:
      self.__close()
  def get_user_data(self,userid):
    '''
      获取用户的datas信息
    '''
    sql = 'select datas from userdata where userid = %s'
    try:
      self.__openconnection()
      self.__opencursor(buffered=True)
      cursor = self.__cursor[0]
      cursor.execute(sql,(userid,))
      if cursor.rowcount >0:
        return cursor.fetchall()[0]
      return None
    except mysql.connector.Error as err:
      logger.exception('get_user_info:{0}'.format(err))
    finally:
      self.__close()
  def get_user_info(self,account): 
    '''
      通过账号查询账号明细
    '''
    sql = 'select a.account,a.username,a.count,a.password,a.indate,a.cookies from csdn_user a where a.account = %s'
    try:
      self.__openconnection()
      self.__opencursor()
      cursor = self.__cursor[0]
      cursor.execute(sql,(account,))
      return [(account,username,count,password,'{:%Y-%m-%d}'.format(indate),cookies)for account,username,count,password,indate,cookies in cursor][0]
    except mysql.connector.Error as err:
      logger.exception('get_user_info:{0}'.format(err))
    finally:
      self.__close()
  def save_download_log(self,dlog):
    sql = 'insert into download_log(useraccount,downloaddate,sourceurl,touser,tid) values(%s,%s,%s,%s,%s)'
    try:
      self.__openconnection()
      self.__opencursor()
      cursor = self.__cursor[0]
      cursor.execute(sql,(dlog.useraccount,dlog.downloaddate,dlog.sourceurl,dlog.touser,dlog.tid))
      self.__cnx.commit() 
    except mysql.connector.Error as err:
      logger.exception('save_download_log:{0}'.format(err))
    finally:
      self.__close()
      
  def get_downloader(self,nowdate):
    sql = '''select a.account,a.password,a.cookies from csdn_user a left outer join (select a.useraccount,count(*) as dtime from download_log  a where a.downloaddate = %s group by a.useraccount
) as b on a.account = b.useraccount where ifnull(b.dtime,0) < 20'''
    try:
      self.__openconnection()
      self.__opencursor(buffered=True)
      cursor = self.__cursor[0]
      searchdate = nowdate
      cursor.execute(sql,(searchdate,))
      num = cursor.rowcount
      if num > 0:
        selrow = random.randint(0,num-1)
        rows = cursor.fetchall()
        return rows[selrow]
      return None
    except mysql.connector.Error as err:
      logger.exception('get_downloader:{0}'.format(err))
    finally:
      self.__close()
  def get_all_login_account(self):
    sql = 'select account,password from csdn_user where count > 0 and indate >= NOW()'
    try:
      self.__openconnection()
      self.__opencursor()
      cursor = self.__cursor[0]
      cursor.execute(sql)
      return cursor.fetchall()
    except mysql.connector.Error as err:
      logger.exception('get_all_login_account:{0}'.format(err))
      return None
    finally:
      self.__close()
if __name__ == '__main__':
  smdb = smdb()
  print(smdb.get_user_data('73f91998-7399-11e8-ac7a-3c970e8bb48a'))