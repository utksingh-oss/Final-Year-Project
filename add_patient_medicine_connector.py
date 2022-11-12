import mysql.connector as connector
from datetime import date

class PatientMedicineHelper:
	def __init__(self):
		self.con = connector.connect(host = 'localhost',port = '3306', user='root',password = '858684Arsh123!',database = 'final_year_project')
		query = 'create table if not exists patients_medicine(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,patient_id INT NOT NULL , FOREIGN KEY(patient_id) References patients(patientId),medicine_name MEDIUMTEXT,date DATE)'		
		cur = self.con.cursor()
		cur.execute(query)
		print("Created")

	#Insert Patient's Details
	def insert_medicine(self , patient_id , medicine_details):
		query = "insert into patients_medicine(patient_id , medicine_name , date) values('{}','{}','{}')".format(patient_id , medicine_details ,date.today())
		cur = self.con.cursor()
		cur.execute(query)
		self.con.commit()
		return cur.lastrowid

	#Fetching Patient's Data:= returns a tuple
	def fetch_single(self , patient_id):
		query = "select * from patients_medicine where patient_id = '{}'".format(patient_id)
		cur = self.con.cursor(buffered = True)
		cur.execute(query)
		res = []
		for row in cur:
			res.append(row)
		return res


