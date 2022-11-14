import mysql.connector as connector

class PatientSummary:
	def __init__(self):
		self.con = connector.connect(host = 'localhost',port = '3306', user='root',password = '858684Arsh123!',database = 'final_year_project')
		query = 'create table if not exists patients_summary(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,patient_id INT NOT NULL , FOREIGN KEY(patient_id) References patients(patientId), medicines MEDIUMTEXT , health_conditions MEDIUMTEXT , medical_procedures MEDIUMTEXT , symptoms MEDIUMTEXT , remark MEDIUMTEXT)'		
		cur = self.con.cursor()
		cur.execute(query)
		print("Created")


	#Delete a patient's details
	def delete_user_entry(self , patient_id):
		query = "delete from patients_summary where patient_id = '{}'".format(patient_id)
		cur = self.con.cursor()
		cur.execute(query)
		self.con.commit()


	#Insert Patient's Details
	def insert_summary(self , patient_id , medicines , medical_procedures , health_conditions , symptoms , remarks):
		print("INSERTING FOR PATIENT : ", patient_id)
		self.delete_user_entry(patient_id)
		query = "insert into patients_summary(patient_id , medicines , health_conditions , medical_procedures , symptoms , remark) values('{}','{}','{}','{}','{}','{}')".format(patient_id , medicines , health_conditions , medical_procedures , symptoms, remarks)
		cur = self.con.cursor()
		cur.execute(query)
		self.con.commit()
		return cur.lastrowid

	#Fetching Patient's Data:= returns a tuple
	def fetch_single(self , patient_id):
		sql = "SELECT * FROM patients_summary WHERE patient_id = %s"
		mycursor = self.con.cursor()
		adr = (patient_id, )
		mycursor.execute(sql, adr)
		myresult = mycursor.fetchall()
		print(myresult)
		for x in myresult:
		  print(x)
		return myresult