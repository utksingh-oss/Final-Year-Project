# D:\Final Year Project\new_model\model-best\ner

import spacy
from spacy.matcher import Matcher 
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config


nlp = spacy.load("en_core_web_lg")

matcher = Matcher(nlp.vocab)


pattern_1 = [{"POS": "ADJ"}, {"POS": "NOUN"}]
pattern_2 = [{"POS": "ADJ"}, {"POS": "NOUN"}, {"POS" : "NOUN"}]
pattern_3 = [{"POS": "PROPN"}]
pattern_4 = [{"POS": "PROPN"},{"POS": "ADJ"},{"POS":"NOUN"}]
pattern_5 = [{"POS": "PROPN"}, {"POS": "NOUN"},{"POS": "NOUN"}]
pattern_6 = [{"POS": "PROPN"}, {"POS": "NOUN"}]
pattern_7 = [{"POS": "NOUN"}]
pattern_8 = [{"POS": "NOUN"},{"POS": "NOUN"}]
pattern_9 = [{"POS": "NOUN"},{"POS": "NOUN"},{"POS":"NOUN"}]
pattern_10= [{"POS": "NOUN"},{"POS": "NOUN"},{"POS":"NOUN"},{"POS":"NOUN"}]

patterns_p = [pattern_1 , pattern_2 , pattern_3 , pattern_4 , pattern_5 , pattern_6, pattern_7 , pattern_8 , pattern_9 , pattern_10]

matcher.add("noun phrase" , patterns = patterns_p)

# model = spacy.load("D:\\Final Year Project\\model-best") 

sentence1 = "Asthma is a condition that can cause the airways in your lungs to swell and narrow, making it harder for air to move in and out. Airways can also become inflamed and produce more mucus than normal. These changes in the airways cause symptoms such as difficulty breathing, coughing, and wheezing. This animation from the American Lung Association can help you understand the difference between healthy lungs and lungs with asthma.\r"
sentence2 = """Osteoarthritis (OA) is a well-known cause of disability in the United States and around the world. It is characterized by degeneration of articular cartilage and other joint changes, and it commonly presents as joint pain with ambulation or other activities of daily living, depending on the joint(s) affected. According to the analysis of data from 3 large US population‐based studies, it is estimated that almost 27 million Americans 25 years of age and older suffer from clinical OA, a number that has increased from estimates in the 1990s.6 Prevalence is much higher in women, as females comprise approximately 78 of adults with OA.7 Prevalence also increases with age; 43 of adults over the age of 65 years have OA. This age group is expected to increase from 15 of the US population to 24 in the next 40 years.8 It should be noted that exact figures for incidence and prevalence are difficult to obtain due to differences in study designs and definitions of OA.\r"""
sentence3 = "Cholesterol can be measured in the blood. There are 2 different types of cholesterol: low-density lipoprotein (LDL) and high-density lipoprotein (HDL). To simplify things, we think of LDL as “bad” and HDL as “good.” Too much LDL causes a fatty build-up in your arteries (also known as plaque), increasing the risk of heart attack, stroke, and other diseases. HDL can help remove some of the LDL by transporting it back to your liver, which then removes it from your body.\r"
sentence4 = "People with hyperhidrosis tend to sweat heavily, even at rest, and this can interfere with normal activities. For example, sweaty hands can make simple activities like writing or turning a doorknob difficult. Hyperhidrosis can also put you at greater risk for skin infections, like athlete’s foot. Unsurprisingly, all of this often negatively impacts the quality of life. Many people with hyperhidrosis report that it leads to negative emotions, lack of self-confidence, and social anxiety.\r"
sentence5 = "Infection from Listeria can occur in any trimester of pregnancy. It can cause mild or serious illness in a pregnant woman, but it can also pass from mother to baby. That means it can harm the unborn baby, causing serious infections like sepsis and meningitis. It can also cause permanent damage to a baby’s vital organs, like the brain and heart. Listeria infection can also result in preterm (early) labor, miscarriage, and stillbirth. Because this infection can be life-threatening for both mom and baby, the risk should be taken seriously."

documents = [sentence1 , sentence2 , sentence3 , sentence4 , sentence5]

def get_all_keywords_util(sentence):
	sentence = nlp(sentence)
	result = matcher(sentence, as_spans = True)
	
	for i in range(len(result)):
		for j in range(i + 1, len(result)):
			if j >= len(result):
				continue
			if result[i].text in result[j].text:
				result.remove(result[i])
			elif result[j].text in result[i].text:
				result.remove(result[j])


	#HANDLING NEGATION
	negated_words = {}
	for tok in sentence:
	  has_negation = False
	  for child in tok.children:
	    if child.dep_ == 'neg':
	      has_negation = True
	  if not has_negation:
	    continue
	  if tok.text in negated_words.keys():
	    negated_words[tok.text] += 1
	  else:
	    negated_words[tok.text] = 1
	   
	  for child in tok.children:
	    if child.dep_ == "neg":
	      continue
	    if child.text in negated_words.keys():
	      negated_words[child.text] += 1
	    else :
	      negated_words[child.text] = 1



	# print("THIS IS CONDITIONS FILE : ")
	file = open("Conditions.txt" , )
	medical_conditions = []
	# for line in file:
	# 	medical_conditions.append(line)
	with open('Conditions.txt' , 'r') as reader:
		text = reader.read()
		medical_conditions = text.split("\n")

	# print(medical_conditions)

	detected_medical_conditions = []

	visited_words = set()
	finished_words = 0 
	total_words = len(result)
	percentage = 0

	symptoms = []
	with open("symptoms.txt" , 'r') as reader:
		text = reader.read()
		symptoms = text.split("\n")

	finished_words = 0 
	total_words = len(result) - len(visited_words)
	detected_symptoms = []

	print("EXTRACTING THE SYMPTOMS")

	for word in result:
		if word in visited_words:
			continue
		max_similarity = 0
		found_word = ""
		for symptom in symptoms:
			temp_1 = nlp(symptom.lower())
			temp_2 = nlp(word.text.lower())
			curr_similarity = temp_1.similarity(temp_2)
			if curr_similarity > max_similarity:
				max_similarity = curr_similarity
				found_word = symptom
				# print(symptom)
		if max_similarity >= 0.80:
			detected_symptoms.append(word)
			print(found_word , " " , word , " " , max_similarity)
			visited_words.add(word)
		finished_words += 1
		percentage = (finished_words / total_words) * 100
		sys.stdout.write("\r{0}".format(int(percentage)))
		sys.stdout.flush()

	finished_words = 0 
	total_words = len(result) - len(visited_words)


	print("EXTRACTING THE MEDICAL CONDITIONS : ")

	for word in result:
		max_similarity = 0
		found_word = ""
		if word in visited_words :
			continue
		for conditions in medical_conditions:
			temp_1 = nlp(conditions.lower())
			temp_2 = nlp(word.text.lower())
			curr_similarity = temp_1.similarity(temp_2)
			if curr_similarity > max_similarity:
				max_similarity = curr_similarity
				found_word = conditions
		if max_similarity >= 0.75:
			detected_medical_conditions.append(word)
			print(found_word , " " , word , " " , max_similarity)
			visited_words.add(word)
		finished_words += 1
		percentage = (finished_words / total_words) * 100
		sys.stdout.write("\r{0}".format(int(percentage)))
		sys.stdout.flush()
	


	print("EXTRACTING THE MEDICAL TESTS : ")
	finished_words = 0 
	total_words = len(result) - len(visited_words)

	medical_tests = []
	with open('medical_tests.txt' , 'r') as reader:
		text = reader.read()
		medical_tests = text.split("\n")

	tests_done = []

	for word in result:
		if word in visited_words:
			continue
		max_similarity = 0
		found_word = ""
		for test in medical_tests:
			temp_1 = nlp(test.lower())
			temp_2 = nlp(word.text.lower())
			curr_similarity = temp_1.similarity(temp_2)
			if curr_similarity > max_similarity:
				max_similarity = curr_similarity
				found_word = test
				# print(symptom)
		if max_similarity >= 0.95:
			tests_done.append(word)
			print(found_word , " " , word , " " , max_similarity)
			visited_words.add(word)
		finished_words += 1
		percentage = (finished_words / total_words) * 100
		sys.stdout.write("\r{0}".format(int(percentage)))
		sys.stdout.flush()

	for condition in detected_medical_conditions:
		if condition in negated_words.keys():
			if negated_words[condition] != 0:
				detected_medical_conditions.remove(condition)
				negated_words[condition] -= 1

	for symptom in detected_symptoms:
		if symptom in negated_words.keys():
			if negated_words[symptom] != 0:
				detected_symptoms.remove(symptom)
				negated_words[symptom] -= 1

	for test in tests_done:
		if test in negated_words.keys():
			if negated_words[test] != 0:
				tests_done.remove(test)
				negated_words[test] -= 1

	detected_medical_conditions = list(set(detected_medical_conditions))
	detected_symptoms = list(set(detected_symptoms))
	tests_done = list(set(tests_done))

	return [detected_medical_conditions , detected_symptoms , tests_done]


def get_all_keywords(text):
	doc = nlp(text)
	medical_conditions = []
	detected_symptoms = []
	tests_done = []
	for sent in doc.sents:
		med_con , det_sym , tes_don = get_all_keywords_util(sent.text)
		medical_conditions.extend(med_con)
		detected_symptoms.extend(det_sym)
		tests_done.extend(tes_don)


	medical_conditions = list(set(medical_conditions))
	detected_symptoms = list(set(detected_symptoms))
	tests_done = list(set(tests_done))

	return [medical_conditions , detected_symptoms , tests_done]

def get_TF_IDF_Values(docouments):
	tfidf = TfidfVectorizer()
	result = tfidf.fit_transform(documents)
	values = {}
	for ele1, ele2 in zip(tfidf.get_feature_names(), tfidf.idf_):
		values[ele1] = ele2
	return values


def get_TF_IDF_Values_for_word(documents, list):
	tfidf = TfidfVectorizer()
	result = tfidf.fit_transform(documents)
	values = {}
	for ele1, ele2 in zip(tfidf.get_feature_names() , tfidf.idf_):
		if ele1 in list:
			values[ele1] = ele2
	return values

def get_summary(text):
	
	#initialize the pretrained model
	model = T5ForConditionalGeneration.from_pretrained('t5-small')
	tokenizer = T5Tokenizer.from_pretrained('t5-small')
	device = torch.device('cpu')
	t5_prepared_Text = "summarize: "+ text

	tokenized_text = tokenizer.encode(t5_prepared_Text,  max_length=1024,return_tensors="pt")

	summary_ids = model.generate(tokenized_text,
	                                    num_beams=4,
	                                    no_repeat_ngram_size=2,
	                                    min_length=30,
	                                    max_length=100,
	                                    early_stopping=True)
	summary = tokenizer.decode(summary_ids[0], skip_special_tokens = True)
	return summary

def get_most_important_sentences_summary(documents):
	values = get_TF_IDF_Values(documents)
	sentences = {}	
	for curr in documents:
		doc = nlp(curr)
		for sent in doc.sents:
			total_sum = 0
			count = 0
			for token in sent:
				if token.text in values.keys():
					total_sum += values[token.text]
					count += 1
			if count != 0:
				avg_value = total_sum/count
				sentences[sent.text] = avg_value

	sorted_by_imp = sorted(sentences)
	 
	sorted_by_imp = sorted_by_imp[0:10]

	text_to_be_summarized = ("").join(sorted_by_imp)
	summary_text = get_summary(text_to_be_summarized)
	doc = nlp(summary_text)
	list_of_complete_sentences = []
	for sent in doc.sents:
		if sent.text.endswith("."):
			list_of_complete_sentences.append(sent.text)

	final_summary = ''.join(list_of_complete_sentences)
	return final_summary



def return_top_ten(document , list_of_words):
	new_list_of_word = []
	for word in list_of_words:
		if not isinstance(word,str):
			new_list_of_word.append(word.text)
		else:
			new_list_of_word.append(word)
	values = get_TF_IDF_Values_for_word(document, new_list_of_word)
	sorted_list = sorted(values)
	print(values)
	if len(values) < 10:
		return values
	new_values = []
	for i in range(10):
		if i < len(values):
			new_values.append(values[i])
	return new_values
