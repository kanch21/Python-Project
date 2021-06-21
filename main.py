import sys,os
from PyQt4 import QtGui,QtCore
import commands
import time
import sqlite3
from urlparse import urlparse
from subprocess import Popen
import subprocess
import csv
import hashlib
from hashlib import md5

status,date_time = commands.getstatusoutput("date +%Y%d%m%H%M")
status,path = commands.getstatusoutput("pwd")
class WelcomeWindow(QtGui.QWidget):			#First Welcome Window

	def __init__(self):
		super(WelcomeWindow, self).__init__()
		self.initUI()

	    
	def initUI(self):

		self.label1 = QtGui.QLabel(self)
		self.label2 = QtGui.QLabel(self)
		self.label1.move(200,50 )
		self.label2.move(200,100 )
		self.setGeometry(100, 100, 600, 600)
		self.setWindowTitle('KKGM')
		self.label1.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;};")
		self.label1.setText("WELCOME")
		self.label2.setGeometry(100, 100, 300, 300)
		self.label2.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 14pt;qproperty-alignment: AlignTop;background-color: white};")
		self.label2.setText("Instructions To The User\n\n\n\n1.Attach your phone to the laptop\n\n2.Press OK to continue ")
		self.button1 = QtGui.QPushButton('OK', self)
		self.button1.move(300, 500)
		self.button1.clicked.connect(self.callSecondWin)
		self.button2 = QtGui.QPushButton('Cancel', self)
		self.button2.move(100, 500)
		self.button2.clicked.connect(self.cancel)
		
		
	def cancel(self):
		self.close()
	def callSecondWin(self):
		self.deviceObject = DeviceInfoWindow()
		self.deviceObject.show()
		self.close()
class DeviceInfoWindow(QtGui.QWidget):			#Second Information Window
	def __init__(self):
		
		super(DeviceInfoWindow, self).__init__()
		self.initUIdevice()
	def initUIdevice(self):
		

		self.setWindowTitle('KKGM')
		self.setGeometry(100, 100, 600, 600)
		self.label1 = QtGui.QLabel(self)
		self.label2 = QtGui.QLabel(self)
		self.label3 = QtGui.QLabel(self)
		self.label4 = QtGui.QLabel(self)
		self.label1.move(200,50 )
		self.label2.move(100,100 )
		self.label3.move(100,150 )
		self.label4.move(100,300 )

		self.edit1 = QtGui.QLineEdit(self)
		self.edit2 = QtGui.QLineEdit(self)
		self.edit1.move(270,100 )
		self.edit2.move(270,150 )
		self.edit2.setGeometry(270,150,290,30)

		
		status,output=commands.getstatusoutput("adb shell getprop ro.product.model")
		self.edit1.setText(output)	
		
		status,output=commands.getstatusoutput("adb shell getprop ro.build.display.id")
		self.edit2.setText(output)
		
		self.label1.setText("Phone Information")
		self.label1.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;};")
		self.label2.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 14pt;};")
		self.label2.setText("Model")

		self.label3.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 14pt;};")
		self.label3.setText("Build number")
		self.label4.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 14pt;};")
		self.label4.setText("Is this the device you want to scan?")

		self.button1 = QtGui.QPushButton('Cancel', self)
		self.button1.move(250,350)
		self.button1.clicked.connect(self.cancel)

		self.button2 = QtGui.QPushButton('Back', self)
		self.button2.move(350,350)
		self.button2.clicked.connect(self.backButton)

		self.button3 = QtGui.QPushButton('OK', self)
		self.button3.move(450,350)
		self.button3.clicked.connect(self.okButton)	
	
	def backButton(self):
		wc.show()
		self.close()
	def cancel(self):
		self.close()
	
	def okButton(self):
		self.extract=ExtractionWindow()
		self.extract.show()
		self.close()	
class ExtractionWindow(QtGui.QWidget):			#

	def __init__(self):
	
		super(ExtractionWindow, self).__init__()
		self.initExtract()
	def initExtract(self):
		self.setWindowTitle('KKGM')
		self.setGeometry(100, 100, 600, 600)
		self.label1= QtGui.QLabel(self)
		self.label2= QtGui.QLabel(self)
		self.label3= QtGui.QLabel(self)
		self.label1.setText("\tPress OK to intialize Extraction")
		self.label1.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 18pt; font-weight:bold};")

		self.label2.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 14pt;qproperty-alignment: AlignTop;background-color: white};")
		self.label2.move(180,130 )
		self.label2.setGeometry(180,130,290,30)
		self.button1=QtGui.QPushButton("OK",self)
		self.button1.move(270,80)
		self.button4=QtGui.QPushButton("Cancel",self)
		self.button4.move(170,200)
		self.button3=QtGui.QPushButton("Back",self)
		self.button3.move(270,200)
		self.button2=QtGui.QPushButton("Next",self)
		self.button2.move(370,200)
		self.button2.setEnabled(False)
		self.button1.clicked.connect(self.extractButton)
		
		
		self.button2.clicked.connect(self.next)
		self.show()
		self.button3.clicked.connect(self.backButton)
		self.show()
		self.button4.clicked.connect(self.cancel)
		self.show()


	def extractButton(self):
		self.button1.setEnabled(False)	
		
		
		sqlite_file2= 'owners.sqlite'
		table_name1='accounts'
		column_1 = 'name'
		db_path1='/data/system/users/0/accounts.db'
		conn2= sqlite3.connect(sqlite_file2)
		cursor= conn2.execute('select count(serial_no) from path_name')
		for row in cursor:
			count=row[0]
		count=(count+1)
		for i in range(1,count+1):	
			cursor= conn2.execute('SELECT full_path from path_name where serial_no={ino}' .\
				format(ino=i))
			
			for row in cursor:
				db_path= row[0]	
				status,output = commands.getstatusoutput("adb pull '%s' '%s'/kkgm/'%s'/" % (db_path,path,date_time))
		os.chdir("%s/kkgm/%s" % (path,date_time))
		status,output = commands.getstatusoutput("adb pull '%s' '%s'/kkgm/'%s'/" % (db_path1,path,date_time))
		conn1=sqlite3.connect('accounts.db')
			
		cursor1=conn1.execute("select {cn_1} from {tn} where {cn_1} like '%@%' ".\
			format(cn_1=column_1,tn=table_name1))
		for row in cursor1:	
			acc=row[0]

		status,output = commands.getstatusoutput("adb pull /data/data/com.google.android.gm/databases/mailstore.'%s'.db '%s'/kkgm/'%s'/mailstore.db" % (acc,path,date_time))
		status,output = commands.getstatusoutput("cp '%s'/owners.sqlite '%s'/kkgm/'%s'/" % (path,path,date_time))

		os.system('adb shell ls -lR | grep "jpg"| sort -r -k 5 | tail -100 | tee jpg17.txt > /dev/null 2>&1')
		os.system('sed "s/[[:space:]]\+/,/g" jpg17.txt > topjpg.csv')
		
		
		self.button2.setEnabled(True)
		self.label2.setText("Extracted Successfully")
		
		#full_path='/home/mudita/kkgm/logs.db'
		#print hashlib.md5(open(full_path, 'rb').read()).hexdigest()
		#full_path='/home/mudita/kkgm/browser2.db'
		#print hashlib.md5(open(full_path, 'rb').read()).hexdigest()
		#full_path='/home/mudita/kkgm/msgstore.db'
		#print hashlib.md5(open(full_path, 'rb').read()).hexdigest()
	def backButton(self):
		di.show()
		self.close()
	def cancel(self):
		self.close()
	def next(self):
		self.selection= SelectionWindow()
		self.selection.show()
		self.close()
class SelectionWindow(QtGui.QWidget):				#LAst Window

	def __init__(self):
	
		super(SelectionWindow, self).__init__()
		self.initSelect()
	def initSelect(self):
		
		self.setWindowTitle('KKGM')
		self.setGeometry(100, 100, 600, 600)
		self.label1= QtGui.QLabel(self)
		self.label2= QtGui.QLabel(self)
		self.label2.move(100,150)
		
		self.label3= QtGui.QLabel(self)
		self.label4= QtGui.QLabel(self)
		self.label5= QtGui.QLabel(self)
		self.label6= QtGui.QLabel(self)
		self.label7= QtGui.QLabel(self)
		self.label8= QtGui.QLabel(self)
		self.label9= QtGui.QLabel(self)
		self.label10= QtGui.QLabel(self)
		self.label3.move(100,170)
		self.label4.move(100,190)
		self.label5.move(100,210)
		self.label6.move(100,230)
		self.label7.move(100,250)
		self.label8.move(100,270)
		self.label9.move(100,290)
		self.label10.move(100,310)
		self.label1.setText("\t\tSelect Report")
		self.label1.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 18pt; font-weight:bold};")
		self.label2.setText("1.")
		self.label2.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox1=QtGui.QCheckBox('URL visits',self)
		self.checkBox1.move(150,150)
		#if self.checkBox1.isChecked():
		
		#self.checkBox1.setChecked(True)
		self.checkBox1.stateChanged.connect(self.url_visits)
			#self.url_visits
		#-----------------------------------------------------
		self.label3.setText("2.")
		self.label3.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox2=QtGui.QCheckBox('Contacted people on whatsapp',self)
		self.checkBox2.move(150,170)
		#self.checkBox2.setChecked(True)
		self.checkBox2.stateChanged.connect(self.whatsapp)
		#-----------------------------------------------------	
		self.label4.setText("3.")
		self.label4.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox3=QtGui.QCheckBox('Recently used jpg files',self)
		self.checkBox3.move(150,190)
		self.checkBox3.stateChanged.connect(self.jpg_file)
		#--------------------------------------------------
		self.label5.setText("4.")
		self.label5.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox4=QtGui.QCheckBox('Call logs',self)
		self.checkBox4.move(150,210)
		self.checkBox4.stateChanged.connect(self.call_logs)
		#-----------------------------------------------------
		self.label6.setText("5.")
		self.label6.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox5=QtGui.QCheckBox('Whatsapp and SMS ',self)
		self.checkBox5.move(150,230)
		self.checkBox5.stateChanged.connect(self.wa_sms_join)
		#-----------------------------------------------------
		self.label7.setText("6.")
		self.label7.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox6=QtGui.QCheckBox('SMS ',self)
		self.checkBox6.move(150,250)
		self.checkBox6.stateChanged.connect(self.sms_count)
		#----------------------------------------------------------
		self.label8.setText("7.")
		self.label8.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox7=QtGui.QCheckBox('Facebook to Gmail  ',self)
		self.checkBox7.move(150,270)
		self.checkBox7.stateChanged.connect(self.fb_gmail)
		#------------------------------------------------------------
		self.label9.setText("8.")
		self.label9.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox8=QtGui.QCheckBox('WhatsApp to Gmail ',self)
		self.checkBox8.move(150,290)
		self.checkBox8.stateChanged.connect(self.wa_gmail)
		#----------------------------------------------------------------------------
		self.label10.setText("9.")
		self.label10.setStyleSheet("QLabel{font-family: Arial;font-style: normal;font-size: 12pt; font-weight:bold};")
		self.checkBox9=QtGui.QCheckBox('Messenger Contacts ',self)
		self.checkBox9.move(150,310)
		self.checkBox9.stateChanged.connect(self.messenger_contacts)
		#-----------------------------------------------------------------------------
		
		self.button5=QtGui.QPushButton("Cancel",self)
		self.button5.move(250,500)
		self.button5.clicked.connect(self.cancel)
		self.button6=QtGui.QPushButton("Generate Report",self)
		self.button6.move(350,500)
		self.button6.clicked.connect(self.open_file)
		self.show()
#-------------------------------------------------------------------------------------------------------------------------

	def cancel(self):
		self.close()
	def url_visits(self,state):
		if self.checkBox1.isChecked()== True:
			sqlite_file1 = 'History'
			sqlite_file2 = 'owners.sqlite'    # name of the sqlite database file
			table_name = 'urls'   # name of the table to be queried
			id_column = 'id'
			column_2 = 'title'
			column_3 = 'url'
			column_6= 'visit_count'
	

			conn1 = sqlite3.connect(sqlite_file1)
			conn2= sqlite3.connect(sqlite_file2)


			conn2.executescript('drop table if exists total_visit_count')
			cursor=conn1.execute('SELECT {cnn},{v} FROM {tn} order by {cnn}'.\
					format(cnn=column_3,v=column_6,tn=table_name))

			conn2.execute('Create table total_visit_count(id integer primary key,url varchar(20),visits integer)')
			cnt=0
			id=1
			for row in cursor :

				parsed_uri=urlparse(row[0])
				domain='{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

				read_url=domain
				read_cnt=row[1]
				if (cnt==0):
					cnt+=1
					temp_url=domain
					temp_cnt=row[1]
				else:
					if(read_url==temp_url):
						temp_cnt=temp_cnt+read_cnt
					else:
						conn2.execute(' insert into total_visit_count(id,url,visits) values (?,?,?)',(id,temp_url,temp_cnt))
						id+=1
						temp_url=read_url
						temp_cnt=read_cnt
			conn2.execute(' insert into total_visit_count(id,url,visits) values (?,?,?)',(id,temp_url,temp_cnt))
			
			fh=open("Report.txt","a")
			cursor1=conn2.execute("select * from total_visit_count")
			fh.write("Serial number\t\tURL\t\tMax Count\n")	
			for row in cursor1:
				#fh.write("%s\n" % str(row))
				fh.write("%s\t\t%s\t\t%s\n" % (str(row[0]),row[1],str(row[2])))
			cursor2=conn2.execute('select id, url,max(visits) from total_visit_count')
			fh.write("--------URL which is the most visited--------\n")	
			for row in cursor2:
				fh.write("%s\t\t%s\t\t%s\n" % (row[0],row[1],row[2]))
			#fh.write("%s\n" % str(all_rows))
				
			
			fh.close()
			conn2.commit()
			conn1.close()
			conn2.close()
		else:
			fh=open("Report.txt","a")
			
#------------------------------------------------------------------------------------------------------------------------
	def whatsapp(self,state):
		if self.checkBox2.isChecked():
			sqlite_file1 = 'msgstore.db'
			sqlite_file3 = 'wa.db'
			sqlite_file2 = 'owners.sqlite'    # name of the sqlite database file
			table_name2 = 'wa_contacts'   # name of the table to be queried
			table_name1 = 'messages'   # name of the table to be queried
			#id_column = 'id'
			column_1 = 'key_remote_jid'
			column_2 = 'wa_name'
			#column_6= ''


			conn1 = sqlite3.connect(sqlite_file1)
			conn3= sqlite3.connect(sqlite_file3)
			conn2 = sqlite3.connect(sqlite_file2)

			conn2.executescript('drop table if exists whatsapp')
			conn2.executescript('drop table if exists whatsapp_final')
			cursor=conn1.execute("SELECT {cnn} FROM {tn} where {cnn} like '%@s%'order by {cnn}".\
					format(cnn=column_1,tn=table_name1))

			conn2.execute('Create table whatsapp(id integer,count integer)')
			conn2.execute('Create table whatsapp_final(id integer,count integer)')
			id1=1
			for row in cursor :
				string1=row[0]
				str1=string1.split("@")
				string1=str1[0]
				#print string1

				conn2.execute(' insert into whatsapp(id,count) values (?,?)',(string1,id1))

			cursor=conn2.execute('select * from whatsapp')
			cnt=0
			for row in cursor:

				read_num=row[0]
				read_cnt=row[1]
				if (cnt==0):
					cnt+=1
					temp_num=row[0]
					temp_cnt=row[1]
				else:
					if(read_num==temp_num):
						temp_cnt=temp_cnt+read_cnt
					else:
						conn2.execute(' insert into whatsapp_final(id,count) values (?,?)',(temp_num,temp_cnt))
						temp_num=read_num
						temp_cnt=read_cnt

			conn2.execute(' insert into whatsapp_final(id,count) values (?,?)',(temp_num,temp_cnt))
			#conn2.execute('select * from whatsapp_final order by count')
			fh=open("Report.txt","a")
			cursor1=conn2.execute("select * from whatsapp_final")
			fh.write("--------Contacted people on Whatsapp--------\n")	
			fh.write("Id\t\tCount\n")	
		
			for row in cursor1:
				#fh.write("%s\n" % str(row))
				fh.write("%s\t\t%d\n" % (row[0],row[1]))

			conn2.commit()
			conn1.close()
			conn2.close()
			#full_path='/home/mudita/kkgm/msgstore.db'
			#print hashlib.md5(open(full_path, 'rb').read()).hexdigest()
#--------------------------------------------------------------------------------------------------
	def jpg_file(self,state):
		if self.checkBox3.isChecked():
			conn = sqlite3.connect("owners.sqlite")
			curs = conn.cursor()
			curs.execute("drop table if exists top_jpg_photos")
			curs.execute("CREATE TABLE top_jpg_photos ( permissions TEXT, Description TEXT, Description2 TEXT,size integer, date TEXT, time integer,name TEXT)")
			reader = csv.reader(open('topjpg.csv', 'r'), delimiter=',')
		
			for row in reader:
				to_db = [unicode(row[0], "utf8"), unicode(row[1], "utf8"), unicode(row[2], "utf8"), unicode(row[3], "utf8"), unicode(row[4], "utf8"), unicode(row[5], "utf8"), unicode(row[6], "utf8")]
				curs.execute("INSERT INTO top_jpg_photos (permissions, Description, Description2 ,size, date, time,name) values (?,?,?,?,?,?,?);", to_db)
		
			cursor=curs.execute("select * from top_jpg_photos")
			fh=open("Report.txt","a")
			fh.write("################TOP 100 JPG FILES USED RECENTLY#################\n")
			for row in cursor:
				fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
					
				
			fh.close()
			conn.commit()
			conn.close()
#--------------------------------------------------------------------------------------------------
	def call_logs(self,state):
		if self.checkBox4.isChecked():
			sqlite_file1 = 'logs.db'    
			table_name = 'logs'
			sqlite_file2 = 'owners.sqlite'  
			id_column = '_id'
			column_1 = 'number'
			column_2 = 'type'
			column_3 = 'logtype'
			column_4 = 'geocoded_location'
			column_5 = 'frequent'
			column_6 = 'name'


			conn1 = sqlite3.connect(sqlite_file1)
			conn2 = sqlite3.connect(sqlite_file2)
			#conn2.execute('drop table if exists call_logs')
			conn2.execute('drop table if exists call_logs_final')
			conn2.execute('create table call_logs(id integer primary key,number varchar(15),call_type integer,geocode varchar(30),count integer,name varchar(20) )')
			conn2.execute('create table call_logs_final(id integer primary key,number varchar(15),call_type integer,geocode varchar(30),count integer,name varchar(20) )')

			cursor=conn1.execute('select {id_1},{cn_1},{cn_2},{cn_4},{cn_5},{cn_6} from {tn} where {cn_3}=100; '.\
				format(id_1=id_column,tn=table_name, cn_1=column_1,cn_2=column_2,cn_3=column_3,cn_4=column_4,cn_5=column_5,cn_6=column_6))
			id1=1
			for row in cursor:
				num=row[1]
				if num.startswith("+"):
					num=num[3:]
	
				if num.startswith("0"):
					num=num[1:]
	
				conn2.execute(' insert into call_logs(id,number,call_type,geocode,count,name) values (?,?,?,?,?,?)',(id1,num,row[2],row[3],row[4],row[5]))
				id1+=1
		
		
			cursor=conn2.execute("select * from call_logs order by number")

			cnt=0
			id2=1
			for row in cursor:
	
				num=row[1]
				read_num=num
				read_cnt=row[4]
				read_call_type=row[2]
				read_geocode=row[3]
				read_name=row[5]
				if (cnt==0):
					cnt+=1
					temp_num=num
					temp_cnt=row[4]
					temp_call_type=row[2]
					temp_geocode=row[3]
					temp_name=row[5]
				else:
					if(read_num==temp_num):
						temp_cnt=temp_cnt+read_cnt
				
					else:
						conn2.execute(' insert into call_logs_final(id,number,call_type,geocode,count,name) values (?,?,?,?,?,?)',(id2,temp_num,temp_call_type,temp_geocode,temp_cnt,temp_name))
						id2+=1
						temp_num=read_num
						temp_cnt=read_cnt
						temp_call_type=read_call_type
						temp_geocode=read_geocode	
						temp_name=read_name
	
				id2+=1
			conn2.execute(' insert into call_logs_final(id,number,call_type,geocode,count,name) values (?,?,?,?,?,?)',(id2,temp_num,temp_call_type,temp_geocode,temp_cnt,temp_name))

			fh=open("Report.txt","a")
		
			fh.write("#################CALL LOGS########################\n")
			cursor=conn2.execute("select * from  call_logs_final")
			for row in cursor:
				fh.write("%s\t%s\t%s\t%s\t%s\n" % (row[1],row[2],row[3],row[4],row[5]))
			conn2.execute('drop table if exists call_logs')


			conn1.close()
			conn2.commit()
			conn2.close()

#--------------------------------------------------------------------------------------------------
	def wa_sms_join(self,state):
		if self.checkBox5.isChecked():
			sqlite_file3 = 'mmssms.db'   
			table_name1='threads'
			table_name2 = 'sms'   
			id_column = '_id'
			column_1 = 'thread_id'
			column_2 = 'address'
			column_3= 'snippet'
			column_4='message_count'
			#-------------------------
			sqlite_file1 = 'msgstore.db'
			sqlite_file2 = 'owners.sqlite'
			table_name3 = 'frequents'
			#id_column = '_id'
			column_5 = 'jid'
			#column_3 = 'message_count'
			#---------------------------------    
			table_name6 = 'Whatsapp_msg_count'
			table_name4 = 'sms_count'
			table_name5 = 'wa_sms_count'
			#no1='jid'
			#no2='address'
			column_6='count'
			#column2='message_count'



			
			conn1 = sqlite3.connect(sqlite_file1)
			conn2 = sqlite3.connect(sqlite_file2)
			conn3 = sqlite3.connect(sqlite_file3)
			#-------------------------------------------------sms----------------------------------
			conn2.execute('drop table if exists sms_count')

			cursor=conn3.execute('select  distinct {cnn},{cnn2},{cnn3},{cnn4} from {tn1} inner join {tn2} on threads._id=sms.thread_id order by {cnn4} desc;'.\
					format(cnn=column_1,cnn2=column_2,cnn3=column_3,cnn4=column_4,tn1=table_name1,tn2=table_name2))

			conn2.execute('Create table sms_count(id integer primary key autoincrement,address varchar(20),snippet varchar(100), message_count integer)')
			id1=1
			for row in cursor :
				string1=row[1]
				if string1.startswith("+"):
					string1=string1[3:]
	
				if string1.startswith("0"):
					string1=string1[1:]
	
				if string1.startswith("+"):
					string1=re.sub("\\D", "", string1)
				conn2.execute(' insert into sms_count(id,address,snippet,message_count) values (?,?,?,?)',(id1,string1,row[2],row[3]))
				id1+=1	

			cursor2=conn2.execute('select max(message_count) as id,address,snippet,message_count from sms_count')
			#----------------------------------------------------WA join-----------------------------------
			
			conn2.execute('drop table if exists Whatsapp_msg_count')
			conn2.execute('Create table Whatsapp_msg_count(id integer primary key,jid integer,count integer)')
			cursor=conn1.execute('SELECT {id_1},{cn},{cn_2} FROM {tn} order by {cn_2} desc'.\
				format(id_1=id_column,tn=table_name3, cn=column_5,cn_2=column_4))
			id2=1
			for row in cursor:
				string1=row[1]
				spl=string1.split("@")
				num=spl[0]
				num=num[2:]
	
	
				conn2.execute(' insert into Whatsapp_msg_count(id,jid,count) values (?,?,?)',(id2,num,row[2]))
				id2+=1
			#--------------------------WA-SMS-Join---------------------------------------------
			conn2.execute('drop table if exists wa_sms_count')
			conn2.execute('drop table if exists wa_sms_count_final')

			cursor=conn2.execute('select {n1},coalesce({cnn1},{cnn2}) as merged_count  from {tn1} left outer join {tn2} on {tn1}.{n1}={tn2}.{n2} union select {n2},coalesce({cnn2},{cnn1}) as merged_count  from {tn2} left outer join {tn1} on {tn2}.{n2}={tn1}.{n1};'.\
				format(n1=column_5,n2=column_2,cnn1=column_6,cnn2=column_4,tn1=table_name6,tn2=table_name4))

			conn2.execute('Create table wa_sms_count(id integer primary key,address varchar(20),message_count integer)')
			conn2.execute('Create table wa_sms_count_final(id integer primary key,address varchar(20),message_count integer)')
			id1=1
			for row in cursor:

				conn2.execute(' insert into wa_sms_count(id,address,message_count) values (?,?,?)',(id1,row[0],row[1]))
				id1=id1+1
			cursor1=conn2.execute('select * from {tn3} order by {n2}'.\
				format(n2=column_2,tn3=table_name5))
	
			cnt=0
			id2=1
			for row in cursor1 :
				domain=row[1]
				read_no=domain
				read_cnt=row[2]
				if (cnt==0):
					cnt+=1
					temp_no=domain
					temp_cnt=row[2]
				else:
					if(read_no==temp_no):
						temp_cnt=temp_cnt+read_cnt
				
					else:
						conn2.execute(' insert into wa_sms_count_final(id,address,message_count) values (?,?,?)',(id2,temp_no,temp_cnt))
			
						id2+=1
						temp_no=read_no
						temp_cnt=read_cnt
			fh=open("Report.txt","a")

			fh.write("#################WHATSAPP AND SMS########################\n")
			cursor=conn2.execute("select * from wa_sms_count_final order by message_count desc")
			for row in cursor:
				fh.write("%s\t%d\n" % (row[1],row[2]))
			conn2.commit()
			conn2.close()
			conn1.close()
			conn3.close()

#--------------------------------------------------------------------------------------------------
	def sms_count(self,state):
		if self.checkBox6.isChecked():
			sqlite_file1 = 'mmssms.db'
			sqlite_file2 = 'owners.sqlite'    
			table_name1='threads'
			table_name2 = 'sms'   
			id_column = '_id'
			column_1 = 'thread_id'
			column_2 = 'address'
			column_3= 'snippet'
			column_4='message_count'
			
			
			conn1 = sqlite3.connect(sqlite_file1)
			conn2= sqlite3.connect(sqlite_file2)


			conn2.execute('drop table if exists sms_count')

			cursor=conn1.execute('select  distinct {cnn},{cnn2},{cnn3},{cnn4} from {tn1} inner join {tn2} on threads._id=sms.thread_id order by {cnn4} desc;'.\
					format(cnn=column_1,cnn2=column_2,cnn3=column_3,cnn4=column_4,tn1=table_name1,tn2=table_name2))

			conn2.execute('Create table sms_count(id integer primary key autoincrement,address varchar(20),snippet varchar(100), message_count integer)')
			id1=1
			for row in cursor :
				string1=row[1]
				if string1.startswith("+"):
					string1=string1[3:]

				if string1.startswith("0"):
					string1=string1[1:]
				conn2.execute(' insert into sms_count(id,address,snippet,message_count) values (?,?,?,?)',(id1,string1,row[2],row[3]))
				id1+=1	


			fh=open("Report.txt","a")

			fh.write("#################SMS########################\n")
			cursor=conn2.execute("select * from sms_count order by message_count desc limit 5")
			for row in cursor:
				fh.write("%s\t%s\t%d\n" % (row[1],row[2],row[3]))

			conn2.commit()
			conn2.close()
			conn1.close()

#--------------------------------------------------fb_gmail------------------------------------------------
	def fb_gmail(self,state):
		if self.checkBox7.isChecked():
			sqlite_file1="mailstore.db"
			sqlite_file2="owners.sqlite"
			table1_name="messages"
			column_1="fromAddress"
			column_2="toAddresses"
			column_3="subject"
			column_4="snippet"
			column_5="joinedAttachmentInfos"
			
			conn1 = sqlite3.connect(sqlite_file1)
			conn2= sqlite3.connect(sqlite_file2)
			conn2.execute("drop table if exists fb_gmail")
			conn2.execute("create table fb_gmail(fromAddress varchar(50),toAddresses varchar(50), subject varchar(50),snippet varchar(20))")
			cursor=conn1.execute("select {cnn1},{cnn2},{cnn3},{cnn4} from {tn1} where {cnn5} like '%.facebook_%';".\
format(cnn1=column_1,cnn2=column_2,cnn3=column_3,cnn4=column_4,cnn5=column_5,tn1=table1_name))
			
			for row in cursor:
				conn2.execute(' insert into fb_gmail(fromAddress,toAddresses,subject,snippet) values (?,?,?,?)',(row[0],row[1],row[2],row[3]))
			fh=open("Report.txt","a")

			fh.write("#################facebook to gmail########################\n")
			cursor=conn2.execute("select * from fb_gmail")
			for row in cursor:
				fh.write("%s\t%s\t%s\t%s\n" % (row[0],row[1],row[2],row[3]))

			conn2.commit()
			conn2.close()
			conn1.close()


		
#-----------------------------------------------whatsapp-to-gmail---------------------------------------------------
	def wa_gmail(self,state):
		if self.checkBox8.isChecked():
			sqlite_file1="mailstore.db"
			sqlite_file2="owners.sqlite"
			table1_name="messages"
			column_1="fromAddress"
			column_2="toAddresses"
			column_3="subject"
			column_4="snippet"
			column_5="joinedAttachmentInfos"
			
			conn1 = sqlite3.connect(sqlite_file1)
			conn2= sqlite3.connect(sqlite_file2)
			conn2.execute("drop table if exists wa_gmail")
			conn2.execute("create table wa_gmail(fromAddress varchar(50),toAddresses varchar(50), subject varchar(50),snippet varchar(20))")
			cursor=conn1.execute("select {cnn1},{cnn2},{cnn3},{cnn4} from {tn1} where {cnn5} like '%-WA%';".\
format(cnn1=column_1,cnn2=column_2,cnn3=column_3,cnn4=column_4,cnn5=column_5,tn1=table1_name))
			for row in cursor:
				conn2.execute(' insert into wa_gmail(fromAddress,toAddresses,subject,snippet) values (?,?,?,?)',(row[0],row[1],row[2],row[3]))
			fh=open("Report.txt","a")

			fh.write("#################whatsapp to gmail########################\n")
			cursor=conn2.execute("select * from wa_gmail")
			for row in cursor:
				fh.write("%s\t%s\t%s\t%s\n" % (row[0],row[1],row[2],row[3]))

			conn2.commit()
			conn2.close()
			conn1.close()

#--------------------------------------------------------------------------------------------------
	def messenger_contacts(self,state):
		if self.checkBox9.isChecked():
			sqlite_file1 = 'threads_db2'
			sqlite_file2 = 'owners.sqlite'
			table_name1 = 'threads'
			table_name2 = 'messages'
			column_1 = 'sender'
			column_2 = 'thread_key'
			column_3 = 'snippet'
			column_4 = 'approx_total_message_count'

			conn1 = sqlite3.connect(sqlite_file1)
			conn2 = sqlite3.connect(sqlite_file2)
			conn2.execute('drop table if exists messenger_total_users')
			conn2.execute('drop table if exists messenger_user_names')

			

			fh=open("Report.txt","a")

			fh.write("#################CONTACTED PEOPLE ON MESSENGER APP########################\n")
			#id2=1
			thread='\0'
			cursor1=conn1.execute("select distinct {cn_1},{tn1}.{cn_2},{cn_3}, {cn_4} from {tn1} inner join {tn2} on {tn1}.{cn_2}={tn2}.{cn_2} where {cn_1} not null AND {tn1}.{cn_2} not like 'GROUP%' order by {cn_4} desc;".\
				format(tn1=table_name1,tn2=table_name2, cn_2=column_2, cn_1=column_1,cn_3=column_3, cn_4=column_4))
			for row in cursor1:
				string1=row[1]
				spl=string1.split(":")
				thread=spl[2]	
				break
			conn2.execute('create table messenger_total_users(sender varchar(30),thread_key varchar(100), snippet varchar(100), message_count integer)')
			conn2.execute('create table messenger_user_names(user_key varchar(100),name varchar(30))')
			cursor2=conn1.execute("select user_key,name from thread_users")
			for row in cursor2:
				string2=row[0]
				spl2=string2.split(":")
				thread2=spl2[1]		
				name=row[1]		
				if thread==thread2:
					name_acc = row[1]
					fh.write("ACCOUNT BELONG TO %s" % (name_acc))
				conn2.execute('insert into messenger_user_names(user_key,name) values(?,?)',(thread2,row[1]))
			for row in cursor1:
				string3=row[0]
				spl3=string3.split('"')
				thread3=spl3[5].split(":")
				thread3=thread3[1]

				if thread3!=thread:
						conn2.execute('insert into messenger_total_users(sender,thread_key,snippet,message_count) values(?,?,?,?)',(thread3,row[1],row[2],row[3]))

			cursor3=conn2.execute("select sender,name,message_count from messenger_total_users inner join messenger_user_names on messenger_total_users.sender = messenger_user_names.user_key")

			for row in cursor3:
				fh.write("\n%s\t%s\t%d\n" % (row[0],row[1],row[2]))
			conn2.commit()
			conn1.close()
			conn2.close()

#--------------------------------------------------------------------------------------------------
	def open_file(self):
		os.system("chmod 777 %s/kkgm/%s/Report.txt" % (path,date_time))
		#os.system("enscript /home/mudita/kkgm/Report.txt -o - |ps2pdf -Report.pdf")
		status,output = commands.getstatusoutput("enscript -p output.ps %s/kkgm/%s/Report.txt |ps2pdf output.ps Report.pdf" % (path,date_time))
		if sys.platform=="linux2":
			subprocess.call(["xdg-open","Report.pdf"])
		else:
			os.startfile("Report.pdf")

#------------------------------------------------------------------------------------------------		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	wc = WelcomeWindow()
	wc.show()
	di =DeviceInfoWindow()
	sys.exit(app.exec_())	
