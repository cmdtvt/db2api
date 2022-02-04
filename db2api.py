import pymysql.cursors
import json
 

class Database():
	def __init__(self, host="localhost", port=3306, username=None, password=None,database=None):

		self.host = host
		self.port = port
		self.username = username
		self.password = password
		self.database = database
		self.connection = None

		self.objects = []

		try:
			self.connection = pymysql.connect(
				host = self.host,
				port = self.port,
				user = self.username,
				password = self.password,
				database = self.database,
				charset = 'utf8mb4',
				cursorclass=pymysql.cursors.DictCursor
			)
			print("Connection to: "+str(host)+":"+str(port)+" successfull")
		except:
			print("Connection to: "+str(host)+":"+str(port)+" failed")


	### Check if database connection was established successfully.
	def checkConnection(self,):
		if self.connection == None:
			return False
		else:
			return True

	def getTables(self,):
		sql = "SHOW TABLES"
		results = []
		for t in self.execute(sql):
			results.append(list(t.values())[0])
		return results

	def getDescription(self,table):
		sql = "DESC {table}"
		sql = sql.format(table=table)
		return self.execute(sql)

	def Insert(self,table):
		pass

	def Select(self,table):
		sql = "SELECT * FROM {table}"
		sql = sql.format(table=table)
		return self.execute(sql)

	# Execute a sql query and return it.
	def execute(self,sql):
		print("Running sql: "+sql)
		try:
			with self.connection.cursor() as cursor:
				cursor.execute(sql)
				result = cursor.fetchall()
				print("----Success!")
				return result
		except:
			print("----Fail!")


	def ApiGenerateStructure(self,):
		tables = self.getTables()
		cols = {}
		for t in tables:
			desc = self.getDescription(t)
			data = self.Select(t)
			primary = None

			cols[t] = {}
			cols[t]['fields'] = {}

			for de in desc:
				if(de['Key']=="PRI"):
					primary = de['Field']
				
				cols[t]['fields'][de['Field']] = de

			cols[t]['data'] = {}
			for d in data:
				cols[t]['data'][d[primary]] = d

		return cols

	
	def ApiGenerateObjects(self,):
		data = self.ApiGenerateStructure()
		tables = data.keys()




if __name__ == '__main__':
	d = Database(username="#",password="#",database="#")
	if(d.checkConnection()):
		struc = d.ApiGenerateObjects()
		print(struc['orders'])
		with open('data.json', 'w') as fp:
			json.dump(struc, fp, indent=4)

