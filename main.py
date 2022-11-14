import streamlit as st 
from add_patient_connector import PatientHelper
from adding_patients_files import PatientFileHelper
from adding_patients_diag import PatientDiagHelper
from add_patient_medicine_connector import PatientMedicineHelper
from run_analysis import PatientSummaryGenerator
from add_patients_summary import PatientSummary
import pandas as pd
from datetime import datetime



selection = st.sidebar.radio("Navigation",["Add Patient's Details","Add Patient's Diagnosis","Get Patient's Summary"])
if selection == "Add Patient's Details":
	st.title("Patient's Registration Form")
	first,middle,last = st.columns(3)

	first_val = first.text_input("First Name")
	mid_val = middle.text_input("Middle Name")
	last_val = last.text_input("Last Name")

	email,number = st.columns(2)

	email_val = email.text_input("Email Add.")
	num_val = number.text_input("Mobile No.")

	add_val = st.text_area("Address")

	gender, dob = st.columns(2)
	gender_val = gender.selectbox("Gender",["Male","Female","Other"])
	dob_val = dob.date_input("DOB")

	blank1 , sub , blank2 = st.columns(3)
	sub_val = sub.button("Submit Patient Details")

	if sub_val:
		patient_helper = PatientHelper()
		patient_helper.insert_user(first_val,mid_val,last_val,email_val, num_val, add_val,gender_val,dob_val)


elif selection == "Add Patient's Diagnosis":
	st.title("Add Patient's Diagnosis")
	patient_id = st.text_input("Patient's Id")
	patient_diag_det = st.text_area("Patient's Diagnosis Details")
	
	text_of_medicine = st.text_area("Enter each medicine in new line.")

	doctor_comment = st.text_area("Doctor's Comments")
	st.subheader("OR")
	file_type = st.selectbox("Type of File",["TXT" , "PDF" , "DOC"])
	uploaded_files = st.file_uploader("Upload Existing Files: ",accept_multiple_files = True)
	
	if st.button("Submit"):
		if len(uploaded_files) != 0:
			st.write(uploaded_files[0])
			file_upload = PatientFileHelper()
			for file in uploaded_files:
				file_upload.insert_user_files(patient_id , file , file_type)

		patient_diag_upload = PatientDiagHelper()
		patient_diag_upload.insert_patients_diag(patient_id,patient_diag_det, doctor_comment, text_of_medicine)
		print("Inserted Successfully")
		# patient_medicine_upload = PatientMedicineHelper()
		# patient_medicine_upload.insert_medicine(patient_id, text_of_medicine)
		patient_summary_generator = PatientSummaryGenerator()
		print("This is the value of patient_id: ", patient_id)
		patient_summary_generator.do_analysis(patient_id)


elif selection == "Get Patient's Summary":
	st.title("Patient's Analysis")
	patient_diag_upload = PatientDiagHelper()
	patient_id = st.text_input("Patient's Id")
	text = ''
	if st.button("Submit"):
		patient_summary = PatientSummary()
		result = patient_summary.fetch_single(patient_id)
		#Genral Info of Patient ============================================================
		patient_info = PatientHelper()
		info = patient_info.fetch_single(patient_id)

		if result != None and info != None:
			# st.write(info)
			st.write("ID: ",info[0])
			st.write("Name: " + info[1] + " " + info[2] + " " + info[3])
			st.write("Gender: " + info[7])
			format_code = '%d-%m-%Y'
			st.write("DOB: " + info[8].strftime(format_code))



			#===================================================================================
			
			st.write("MEDICAL CONDITIONS")
			medical_conditions_table = {
				"date" : [],
				"medical condition" : []
			}
			for res in result:
				medical_conditions = res[3]
				medical_conditions = medical_conditions.split("\n")
				for condition in medical_conditions:
					print(condition)
					condition = condition.split(":")
					print(condition)
					if len(condition) == 2:
						medical_conditions_table["date"].append(condition[1])
						medical_conditions_table["medical condition"].append(condition[0])

			condition_table = pd.DataFrame(medical_conditions_table)
			st.write(condition_table)
			text += condition_table.to_string()

			#==================================================================================
			st.write("MEDICATIONS")
			medications_table = {
				"date" : [],
				"medication" : []
			}
			for res in result:
				medications = res[2]
				medications = medications.split("\n")
				for medication in medications:
					print(medication)
					medication = medication.split(":")
					print(medication)
					if len(medication) == 2:
						medications_table["date"].append(medication[1])
						medications_table["medication"].append(medication[0])

			medication_table = pd.DataFrame(medications_table)
			st.write(medication_table)
			text += medication_table.to_string()
			#==================================================================================
			st.write("MEDICAL TESTS & PROCEDURES")
			tests_table = {
				"date" : [],
				"test" : []
			}
			for res in result:
				tests = res[4]
				print("inside medical tests and procedures : ",tests )
				tests = tests.split("\n")
				for test in tests:
					print(test)
					test = test.split(":")
					print(test)
					if len(test) == 2:
						tests_table["date"].append(test[1])
						tests_table["test"].append(test[0])

			test_table = pd.DataFrame(tests_table)
			st.write(test_table)
			text += test_table.to_string()

			#=================================================================================
			st.write("OTHER MEDICAL SYMPTOMS")
			symptoms_table = {
				"date" : [],
				"symptoms" : []
			}
			for res in result:
				symptoms = res[5]
				symptoms = symptoms.split("\n")
				for symptom in symptoms:
					print(symptom)
					symptom = symptom.split(":")
					print(symptom)
					if len(symptom) == 2:
						symptoms_table["date"].append(symptom[1])
						symptoms_table["symptoms"].append(symptom[0])

			symptom_table = pd.DataFrame(symptoms_table)
			st.write(symptom_table)
			text += symptom_table.to_string()


			st.write("PATIENT'S SUMMARY")
			st.write(res[6])

			text += "\n" + res[6]

			#=================================================================================



			st.download_button('Download as Text' , text )
		else:
			st.write("No Patient with patient id : {}".format(patient_id))