import random
import requests
from spellcheck import spellcheck
import re
import json
from pprint import pprint
##import Levenshtein
from Scraper import *
from nltk.corpus import wordnet as wn
import sys
import spacy
import itertools
import numpy as np
import check_lemmas
from sklearn.metrics.pairwise import cosine_similarity


full_list=set(full_ontology)
nlp = spacy.load('en_core_web_md')

# treeL1={'technology':['health','engineering','industry and logistics','information science'],
# 'society':['social science','economy','politics','education'],
# 'entertainment':['gastronomy','popular culture','leisure activities'],
# 'culture':['education','literature','performing arts','visual arts','design','fashion','gastronomy'],
# 'humanity':['leisure activities', 'religion','humanities','philosophy','mathematics'],
# 'science':['natural and physical sciences']}

# treeL2={'gastronomy':['meals','food prepartation','food and drink','cuisines'],'popular culture':['sports','celebrities','corporate branding','pop media','pop music'],'leisure activities':['geography and places','travel','recreation','games','sports'], 'religion':['irrelegion','sprituality','religion'],'humanities':['languages','comparitive literature','history','classical studies','archaelogoy'],'philosophy':['philosophy'],'mathematics':['mathematics','logic'],'natural and physical sciences':['biology','chemistry','physics','mathematics'],'health':['agriculture','biotechnology','health sciences','medicine'],'engineering':['energy','electrical engineering', 'mechanical engineering', 'aerospace','chemical engineering','nanotechnology','forensic science', 'civil engineering','earth science','agriculture'],'industry and logistics':['communication and transport', 'industries','construction','energy'],'information science':['communication','knowledge classification','information science','computing'],'social science':['physcology','sociology','archaelogoy','anthropology','future studies','semiotics','linguistics','neuroscience'],'economy':['business','economics'],'politics':['politics','political science','rights','law','military','business'],'education':['education'],'literature':['poetry','fiction','non-fiction','education'],'performing arts':['film','music','dance','theater'],'visual arts':['painting','sculpture','installation','new media art','film'],'design':['landscape design','city planning','architecture','product design','graphic design'],'fashion':['costumes','fashion design']}

treeL1={'sciences':['engineering', 'social science', 'computation', 'physical sciences', 'investigation', 'research', 'empirical', 'data', 'experiment', 'matter'], 
	'earth':['earth sciences', 'engineering', 'earth sciences', 'ecology', 'biology', 'planet'], 
	'life':['biology', 'biomedical', 'medicine', 'health', 'evolution', 'growth', 'being', 'organism', 'viable'], 
	'humanity':['health', 'brain science', 'philosophy', 'history', 'religion', 'culture', 'rational', 'mind', 'consciousness', 'compassion'], 
	'community':['religion', 'sharing', 'events', 'neighbors', 'local'], 
	'leisure':['sports', 'hobbies', 'places', 'events', 'relaxation', 'relief', 'respite'], 
	'entertainment':['sports', 'adult', 'celebrities', 'pop music',  'food and drink', 'fashion',  'show',  'performance',  'entertainment',  'spectacle'], 
	'arts':['fashion',  'design',  'visual arts', 'film', 'performing arts', 'literature', 'creative', 'expression'], 
	'society':['military', 'law', 'politics', 'education', 'literature',  'education', 'government', 'bureaucracy'], 
	'industry':['military', 'economy', 'industries', 'internet and logistics', 'production', 'fabrication']

}

# 'fashion':['costumes', 'fashion design', 'modern', 'style']
treeL2={'sports':['gaming', 'sports', 'recreation and fitness', 'ball', 'score', 'compete', 'team', 'athletics', 'exercise'], 
'hobbies':['pets', 'crafts', 'home improvement',  'cars and vehicles', 'free time', 'fun'], 
'places':['maps and places', 'travel', 'destinations', 'tourism', 'locations', 'marvels', 'attractions'], 
'events':['holidays', 'weather', 'local events', 'crime and prosecution',  'people', 'social network', 'search engine', 'event', 'occasion', 'news'], 
'sharing':['email', 'chats and forums',  'file sharing',  'dating',  'philanthropy', 'genealogy', 'communication', 'social', 'exchange'], 
'religion':['death', 'religion', 'spirituality', 'soul', 'beliefs', 'existence'], 
'history':['classical studies', 'history', 'timeline', 'archive'], 
'philosophy':['comparative literature', 'philosophy', 'languages', 'thought', 'reasoning'], 
'brain science':['neuroscience', 'physchiatry', 'physcology', 'brain', 'neuron'], 
'health':['mental health',  'alternative and natural medicine', 
'personal health data', 
'pharmacy and health products', 'dental health', 'senior health', 'childs health',  'reproductive health',  'diseases', 'pediatrics'], 
'medical specialties':['medical imaging',  'medical specialties', 'analysis', 'diagnostics'], 
'biomedical sciences':['biotechnology and pharmaceuticals', 
'immunology', 'molecular biology', 'cell biology', ], 
'biology':['cell biology', 'animal and plant biology',  'veterinary', 'life', 'nature'], 
'ecology':['food and science technology', 'agriculture',  'climate', 'environment', 'ecology',  'ecosystem'], 
'earth sciences':['geology', 'metals and mining', 'materials'], 
'engineering':['nanotechnology', 'aerospace', 'civil engineering', 'mechanical engineering',  'electrical engineering', 'innovation', 'construction', 'solution', 'materials'], 
'physical sciences':['chemistry', 'physics', 'mathematics'], 
'computation':['computer and electronics', 'computer science', 'algorithms', 'computer', 'processing'], 
'social science':['linguistics', 'anthropology', 'sociology', 'communication science'], 
'internet and logistics':['telecommunications', 'web administration', 'internet', 'web'], 
'industries':['telecommunications', 'web administration', 
 'shipping', 'transport', 'construction and maintenance', 'real estate',  'industrial goods and services', 'energy', 'associations'], 
'economy':['marketing',  'advertising', 'economics', 'finance', 'business', 'money', 'inflation', 'deflation'], 
'military':['military', 'war', 'weapons', 'navy', 'army', 'soldiers', 'troops'], 
'law':['law', 'criminal justice', 'justice', 'crime', 'prosecution', 'defense'], 
'politics':['government', 'political science', 'immigration and visas', 'daily politics', 'politics', 'news'], 
'education':['educational policy', 'careers', 'jobs and employment', 'business training', 'schools', 'learning', 'teaching', 'knowledge'], 
'literature':['publishing', 'non-fiction', 'fiction', 'poetry', 'writing', 'reading'], 
'performing arts':['theater', 'dance', 'music', 'performance', 'arts', 'drama'], 
 'film':['film', 'animation and comics', 'movies', 'drama'], 
 'visual arts':['photography', 'new media and installation art', 'sculpture', 'painting', 'media', 'art'], 
 'design':['web and graphic design', 'product design', 'architecture', 'city planning', 'landscape and garden', 'design'], 
 'fashion':['fashion', 'apparel', 'beauty', 'trends', 'modern'], 
 'food and drink':['food preparation', 'places to eat and drink', 'restaurants', 'bars', 'cuisine'], 
 'pop music':['pop music', 'mainstream'], 
 'celebrities':['celebrities', 'fame'], 
 'adult':['adult', 'gambling', 'mature']}



with open ('vectors_map.json','r') as f:
	vector_dict=json.load(f)

keyword=None
while keyword!= 'N':
	if keyword== 'N':
		break


	keyword=input('Word to classify:')

	checked=spellcheck(keyword)

	##check if it is an existing key in the ontology
	if keyword in full_list:
		print(keyword)
		continue
	else:
		secondary_check=check_lemmas.check_lemmas(checked)
		if secondary_check:
			print(secondary_check)
			continue
	# print('keys',vector_dict.keys())

	keyword_doc = list(nlp.pipe(checked,
	  batch_size=10000,
	  n_threads=1))


	if keyword_doc[0].has_vector:
		keyword_vector=np.array([keyword_doc[0].vector])
	else:
		spacy.vocab[0].vector

	intermidiate_results=[]
	best=None
	best_similarity=0
	## First level

	l1_keys=treeL1.keys()
	arrays=[]
	order=[]
	for k in l1_keys:
		order.append(k)
		arrays.append(np.array(vector_dict[k]))

	simple_sim = cosine_similarity(keyword_vector, arrays)
	topic_idx = simple_sim.argmax(axis=1)[0]
	best_similarity=np.amax(simple_sim)
	result=order[topic_idx]
	best=result
	print('r1: ', result )
	##second LEvel
	#result=[word for word in order[topic_idx] if word in treeL2]
	#print(treeL1[result])
	l2_keys=[word for word in treeL1[result] if word in treeL2]
	print('choices: ', l2_keys)
	arrays=[]
	order=[]
	for k in l2_keys:
		order.append(k)
		arrays.append(np.array(vector_dict[k]))

	simple_sim = cosine_similarity(keyword_vector, arrays)
	topic_idx = simple_sim.argmax(axis=1)[0]
	result=order[topic_idx]
	maxv=np.amax(simple_sim)
	if (maxv>=best_similarity):
		best_similarity=maxv
		best=result
	print('r2: ',result)

	## answer

	options=[ word for word in treeL2[result] if word in full_ontology]
	print('choices: ', options)
	#print('options',options)
	arrays=[]
	for k in options:
		#print(k,len(vector_dict))
		arrays.append(np.array(vector_dict[k]))

	simple_sim = cosine_similarity(keyword_vector, arrays)
	topic_idx = simple_sim.argmax(axis=1)[0]
	maxv=np.amax(simple_sim)
	result=options[topic_idx]
	if (maxv>=best_similarity):
		best_similarity=maxv
		best=result
	print( 'classified as: '+best)


