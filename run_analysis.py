from add_patient_medicine_connector import PatientMedicineHelper
from adding_patients_diag import PatientDiagHelper
from analysis import get_all_keywords
from add_patients_summary import PatientSummary
from analysis import get_most_important_sentences_summary
from analysis import return_top_ten

class PatientSummaryGenerator:
	def __init__(self):
		self.patient_diagnosis = PatientDiagHelper()
		self.add_patient_summary = PatientSummary()

	def do_analysis(self,patient_id):
		diagnosis_result = self.patient_diagnosis.get_patients_diag(patient_id)
		print("inside do analysis")
		print("patient_id : " ,patient_id)
		med_con_dic = {}
		symptoms_dic = {}
		tests_dic = {}
		medicine_dic = {}
		remarks = []
		diagnosis = []
		for curr in diagnosis_result:
			date = curr[2]
			diag = curr[3]
			diagnosis.append(diag)
			remark = curr[4]
			medicines = curr[5]
			remarks.append(remark)
			medical_conditions , symptoms , tests = get_all_keywords(diag)
			"""Getting just the top 10 most important terms"""
			medical_conditions = return_top_ten(diagnosis , medical_conditions)
			symptoms = return_top_ten(diagnosis , symptoms)
			tests = return_top_ten(diagnosis , tests)


			print("medicines b/f spliting : ", medicines)
			medicines = medicines.split("\n")
			print("medicines first : " , medicines)

			for condition in medical_conditions:
				med_con_dic[condition] = date 

			for symptom in symptoms:
				symptoms_dic[symptom] = date 

			for test in tests: 
				tests_dic[test] = date 

			for medicine in medicines:
				medicine_dic[medicine] = date

		medical_condition_string = ""
		medical_symptoms_string = ""
		medical_test_string = ""
		medicine_string = ""
		for key in med_con_dic.keys():
			 curr_string = key + ":" + str(med_con_dic[key]) + "\n"
			 medical_condition_string += curr_string

		for key in symptoms_dic.keys():
			 curr_string = key + ":" + str(symptoms_dic[key]) + "\n"
			 medical_symptoms_string += curr_string

		for key in tests_dic.keys():
			 curr_string = key + ":" + str(tests_dic[key]) + "\n"
			 medical_test_string += curr_string

		for key in medicine_dic.keys():
			 curr_string = key + ":" + str(medicine_dic[key]) + "\n"
			 medicine_string += curr_string

		print("Medical conditions : ",medical_condition_string)
		print("Medical symptoms: ",medical_symptoms_string)
		print("Medical tests: ",medical_test_string)
		print("Medicine string: ",medicine_string)

		remark_summary = get_most_important_sentences_summary(remarks)
		#insert_summary(self , patient_id , medicines , medical_procedures , health_conditions , symptoms , remarks):
		self.add_patient_summary.insert_summary(patient_id ,  medicine_string , medical_test_string , medical_condition_string , medical_symptoms_string , remark_summary)


