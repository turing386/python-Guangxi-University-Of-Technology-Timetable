import urllib
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors

def insertTameTable(classCode,semester):
	connection = pymysql.connect(
		host='localhost',
		user='root',
		password='',
		db='python',
		charset="utf8",
		cursorclass=pymysql.cursors.DictCursor)


	response = urllib.request.urlopen('http://202.193.177.7:8081/(S(tik2z2rsppomza45zqmxnh55))/web_jxrw/cx_kb_bjkb_bj.aspx?xsbh='+classCode+'&xq='+semester)
	if response.code == 200:
		print ("succeed to open the url, code=",response.code)
		html = response.read()
		soup = BeautifulSoup(
			html,
			'html.parser',
			from_encoding = 'gbk')
		arr = soup.find(id="GVkb").find_all("td")
		note = soup.find(id="TextBox1")
		timeTable = []
		for x in arr:
			ch = x.get_text()
			strings = str(ch).replace("\xa0","none")+"\n"
			timeTable.append(strings)
			if len(timeTable) == 8:
				try:
					with connection.cursor() as cursor:
						sql = "INSERT INTO `timetable` (`classCode`,`semester`,`section`,`one`,`two`,`three`,`four`,`five`,`six`,`seven`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						cursor.execute(sql, (classCode,semester,timeTable[0],timeTable[1],timeTable[2],timeTable[3],timeTable[4],timeTable[5],timeTable[6],timeTable[7]))
						connection.commit()
				finally:
					timeTable = []
					print("insert succeed!")
				pass
		try:
			with connection.cursor() as cursor:
				sql = "INSERT INTO `timetablenote` (`classCode`,`semester`,`note`) VALUES (%s,%s,%s)"
				cursor.execute(sql, (classCode,semester,note.get_text()))
				connection.commit()
		finally:
			print("note insert succeed!")
		pass

	else:
		print("failed to open the url, code=", response.code)
		pass