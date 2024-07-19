from logging import setLoggerClass
from re import S
import re
import pymysql,jsonify,json
from flask import flash, request
from pymysql.cursors import DictCursor

class DBHandler:
   def __init__(self, host, user, password, database):
       self.host = host
       self.user = user
       self.password = password
       self.database = database
   def connection(self):
        try:
            self.db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            self.cursor=self.db.cursor(DictCursor)
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS `client` ( `user_id` INT NOT NULL AUTO_INCREMENT ,  `name` VARCHAR(20) NOT NULL ,  `mobile` BIGINT NOT NULL ,  `city` VARCHAR(20) NOT NULL ,  `email` VARCHAR(30) NOT NULL ,  `password` VARCHAR(30) NOT NULL ,  `isAdmin` BOOLEAN NOT NULL DEFAULT FALSE ,    PRIMARY KEY  (`user_id`, `email`));")
            # self.db.commit()
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS `worker` ( `worker_id` INT NOT NULL AUTO_INCREMENT ,  `name` VARCHAR(20) NOT NULL ,  `mobile` BIGINT NOT NULL ,  `city` VARCHAR(20) NOT NULL ,  `email` VARCHAR(30) NOT NULL ,  `password` VARCHAR(30) NOT NULL ,  `title` VARCHAR(30) NOT NULL ,  `rating` INT NOT NULL DEFAULT '0' ,    PRIMARY KEY  (`worker_id`, `email`));")
            # self.db.commit()
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS `job` ( `job_id` INT NOT NULL AUTO_INCREMENT ,  `worker_id` INT NOT NULL ,  `job_title` VARCHAR(30) NOT NULL ,  `rate` INT NOT NULL ,  `description` LONGTEXT NULL ,    PRIMARY KEY  (`job_id`));")
            # self.db.commit()
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS `requested` ( `job_id` INT NOT NULL ,  `worker_id` INT NOT NULL ,  `client_id` INT NOT NULL );")
            # self.db.commit()
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS `accepted` ( `job_id` INT NOT NULL ,  `worker_id` INT NOT NULL ,  `client_id` INT NOT NULL );")
            # self.db.commit()
        except Exception:
            raise Exception("DB Connection Faild")
   def close(self):
        if not self.cursor==None and not self.db==None:
            self.cursor.close()
            self.db.close()
   def validation(self,status,email,password):
        self.connection()
        if status == "As Client":
            self.cursor.execute("SELECT user_id FROM client WHERE EMAIL = %s AND password = %s ",(email,password))
            result = self.cursor.fetchone()
        elif status == "As Worker":
            self.cursor.execute("SELECT worker_id FROM worker WHERE EMAIL = %s AND password = %s ",(email,password))
            result = self.cursor.fetchone()
        if result:
            self.close()
            return result
        else:
            self.close()
            return False
   def isAdmin(self,email):
       self.connection()
       self.cursor.execute("SELECT * FROM client WHERE EMAIL = %s AND isAdmin = %s ",(email,'1'))
       result = self.cursor.fetchone()
       if result:
            self.close()
            return True
       else:
            self.close()
            return False
   def insertClient(self,name,mobile,city,email,password):
        self.connection()
        query="INSERT INTO `client`(`name`,`mobile`,`city`,`email`,`password`)VALUES (%s,%s,%s,%s,%s)"
        args=(name,mobile,city,email,password)
        try:
            self.cursor.execute(query,args)
            self.db.commit()
        except Exception as e:
            self.close()
            return False
        self.close()
        return True
   def updateClient(self,cid,name,mobile,city,email,password):
        self.connection()
        query="UPDATE `client` SET `name`= %s,`mobile`=%s,`city`=%s,`email`=%s,`password`= %s where user_id=%s " 
        args=(name,mobile,city,email,password,cid)
        try:
            self.cursor.execute(query,args)
            self.db.commit()
        except Exception as e:
            print(e)
            self.close()
            return False
        self.close()
        return True
   def insertWorker(self,name,mobile,title,city,email,password):
        self.connection()
        query="INSERT INTO `worker`(`name`,`mobile`,`title`,`city`,`email`,`password`)VALUES (%s,%s,%s,%s,%s,%s)"
        args=(name,mobile,title,city,email,password)
        try:
            self.cursor.execute(query,args)
            self.db.commit()
        except Exception as e:
            self.close()
            return False
        self.close()
        return True
   def isClinetExist(self,email):
       self.connection()
       self.cursor.execute("SELECT * FROM client WHERE EMAIL = %s ",(email))
       result = self.cursor.fetchone()
       if result:
            self.close()
            return True
       else:
            self.close()
            return False
   def isWorkerExist(self,email):
       self.connection()
       self.cursor.execute("SELECT * FROM worker WHERE EMAIL = %s ",(email))
       result = self.cursor.fetchone()
       if result:
            self.close()
            return True
       else:
            self.close()
            return False
   def getjobs(self):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate from worker w,job j where w.worker_id=j.worker_id")
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def getSearchedjobs(self,searchTeaxt):
       jobList = []
       self.connection()
       search = "%{}%".format(searchTeaxt.upper())
       self.cursor.execute("SELECT name,w.worker_id,job_id,email,mobile,job_title,city,rating,rate from worker w,job j where w.worker_id=j.worker_id and UPPER(j.job_title) like %s",(search))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def getWorkerInfo(self,nemail):
        self.connection()
        self.cursor.execute("SELECT * FROM worker WHERE email=%s",(nemail))
        catchData = self.cursor.fetchall()
        self.close()
        return catchData
   def getClientInfo(self,nemail):
        self.connection()
        self.cursor.execute("SELECT * FROM client WHERE email=%s",(nemail))
        catchData = self.cursor.fetchall()
        self.close()
        return catchData
   def getJobDetails(self,id):
       self.connection()
       self.cursor.execute("SELECT name,w.worker_id,job_id,email,mobile,job_title,city,description,rating,rate from worker w,job j where w.worker_id=j.worker_id and JOB_ID=%s",(id))
       catchData = self.cursor.fetchall()
       return catchData
   def sendRequest(self,jid,wid,cid):
       self.connection()
       query="INSERT INTO `requested` (`job_id`, `worker_id`, `client_id`) VALUES (%s, %s, %s)"
       args=(jid,wid,cid)
       try:
            self.cursor.execute(query,args)
            r=self.db.commit()
       except Exception as e:
            self.close()
            print(e)
            return False
       self.close()
       return True
   def getClientId(self,email):
       self.connection()
       self.cursor.execute("select user_id from client where email=%s",(email))
       catchData= self.cursor.fetchone()
       return catchData['user_id']
   def getWorkerId(self,email):
       self.connection()
       self.cursor.execute("select worker_id from worker where email=%s",(email))
       catchData= self.cursor.fetchone()
       return catchData['worker_id']
   
   def getRequestedJobs(self,cid):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT w.name,r.client_id,w.worker_id,j.job_id,w.email,w.mobile,job_title,w.city,rating,rate from worker w,job j,requested r where w.worker_id=r.worker_id and j.job_id=r.job_id and r.client_id=%s",(cid))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def getConfirmJobs(self,cid):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT w.name,w.email,r.client_id,w.worker_id,j.job_id,w.email,w.mobile,job_title,w.city,rating,rate from worker w,job j,accepted r where w.worker_id=r.worker_id and j.job_id=r.job_id and r.client_id=%s",(cid))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def checkRequestedJobs(self,cid):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT c.name,c.user_id,c.city,r.worker_id,j.job_id,c.email,c.mobile,job_title,c.city from client c,job j,requested r where c.user_id=r.client_id and j.job_id=r.job_id and r.worker_id=%s",(cid))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def checkMyJobs(self,cid):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT job_id,job_title,rate,description from job  where worker_id=%s",(cid))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def checkConfirmJobs(self,cid):
       jobList = []
       self.connection()
       self.cursor.execute("SELECT c.name,c.user_id,r.worker_id,j.job_id,c.email,c.mobile,job_title,c.city from client c,job j,accepted r where c.user_id=r.client_id and j.job_id=r.job_id and r.worker_id=%s",(cid))
       catchData = self.cursor.fetchall()
       for item in catchData:
           jobList.append(item)
       self.close()
       return jobList
   def insertNewJob(self,wid,title,rate,desc):
        self.connection()
        query="INSERT INTO `job`(`worker_id`,`job_title`,`rate`,`description`)VALUES (%s,%s,%s,%s)"
        args=(wid,title,rate,desc)
        try:
            self.cursor.execute(query,args)
            self.db.commit()
        except Exception as e:
            self.close()
            return False
        self.close()
        return True
   def cancelRequest(self,worker_id,job_id,client_id):
       self.connection()
       query="DELETE from requested where job_id=%s and worker_id=%s and client_id=%s"
       args=(job_id,worker_id,client_id)
       try:
           self.cursor.execute(query,args)
           self.db.commit()
       except Exception as e:
            return False
       finally:
           self.close()
   def deletejobP(self,job_id):
       self.connection()
       query="DELETE from job where job_id=%s"
       args=(job_id)
       try:
           self.cursor.execute(query,args)
           self.db.commit()
       except Exception as e:
            return False
       finally:
           self.close()
   def jobClose(self,worker_id,job_id,client_id,ratings):
       self.connection()
       self.cursor.execute("SELECT rating from worker where worker_id=%s",(worker_id))
       starRate=self.cursor.fetchone()
       starRate=starRate["rating"]
       finalRate=(int(starRate)+int(ratings))/2
       print(finalRate)
       query="UPDATE `worker` SET `rating` = %s WHERE `worker`.`worker_id` = %s"
       args=(finalRate,worker_id)
       try:
           self.cursor.execute(query,args)
           self.db.commit()
       except Exception as e:
            return e
       query="DELETE from accepted where job_id=%s and worker_id=%s and client_id=%s"
       args=(job_id,worker_id,client_id)
       try:
           self.cursor.execute(query,args)
           self.db.commit()
       except Exception as e:
            return False
       finally:
           self.close()
       
   def acceptRequest(self,worker_id,job_id,client_id):
       self.connection()
       query="INSERT INTO `accepted` (`job_id`, `worker_id`, `client_id`) VALUES (%s, %s, %s)"
       args=(job_id,worker_id,client_id)
       try:
            self.cursor.execute(query,args)
            r=self.db.commit()
       except Exception as e:
            self.close()
            print(e)
            return False
       self.close()
       return True
