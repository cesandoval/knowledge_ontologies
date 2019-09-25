import random
import requests
from spellcheck import spellcheck
import re
import json
from pprint import pprint
import Levenshtein
import nltk

from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


data={}

ontologyl1=['sciences','earth','life','humanity','community','leisure','entertainment','arts','society','industry']

ontologyl2=['sports','hobbies','places','events','sharing','religion','history','philosophy','brain science','health','medical specialties','biomedical sciences','biology','ecology','earth sciences','engineering','physical sciences','computation','social science','internet and logistics','industries','economy','military','law','politics','education','literature','performing arts', 'film','visual arts','design','fashion','food and drink','pop music','celebrities','adult']
ontologyl3=['gaming','sports','recreation and fitness',
'pets','crafts','home improvement', 'cars and vehicles', 
'maps and places','travel',
'holidays','weather','local events','crime and prosecution', 'people','social network','search engine',
'email','chats and forums', 'file sharing', 'dating', 'philanthropy','genealogy',
'death','religion','spirituality',
'classical studies','history',
'comparative  literature','philosophy','languages',
'neuroscience','psychiatry','physcology',
'mental health', 'alternative and natural medicine',
'personal health data',
'pharmacy and health products','dental health','senior health','childs health', 'reproductive health', 'diseases',
'medical imaging', 'medical specialties',
'biotechnology and pharmaceuticals',
'immunology','molecular biology','cell biology',
'animal and plant biology', 'veterinary',
 'food and science technology','agriculture', 'climate','environment',
 'geology','metals and mining','materials',
 'nanotechnology','aerospace','civil engineering','mechanical engineering', 'electrical engineering',
 'chemistry','physics','mathematics',
 'computer and electronics','computer science', 'linguistics','anthropology','sociology','communication science',
 'telecommunications','web administration',
 'shipping','transport','construction and maintenance','real estate', 'industrial goods and services','energy','associations',
 'marketing and advertising','economics','finance','business',
 'military','war',
 'law','criminal justice',
 'government','political science','immigration and visas','daily politics',
 'educational policy','careers','jobs and employment','business training','schools',
 'publishing','non-fiction','fiction','poetry',
 'theater','dance','music',
 'film','animation and comics',
 'photography','new media and installation art','sculpture','painting',
 'web and graphic design','product design','architecture','city planning','landscape and garden',
 'fashion','apparel','beauty',
 'food preparation','places to eat and drink',
 'pop music',
 'celebrities',
 'adult','gambling'
]
full_ontology=ontologyl1+ontologyl2+ontologyl3

#look into hypernyms, more general


def main():
	nltk.download('wordnet')
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')
	wordnet_lemmatizer=WordNetLemmatizer()
	key2lemmas={}
	lemma2key={}
	synset_info={}

	for phrase in full_ontology:
		tokens=nltk.word_tokenize(phrase)
		tagged_words=nltk.pos_tag(tokens)
		filtered_fillers=[]
		for text,tag in tagged_words:
			if tag!='CC' and tag!='TO' and tag!='IN':
				filtered_fillers.append(text)
		for word in filtered_fillers:
			try:
				#phrase could already be in dict
				lemma=wordnet_lemmatizer.lemmatize(word)
				parent=wn.synsets(lemma)[0]
				related_lemmas=parent.lemmas()
				related_lemma_names=parent.lemma_names()
				if phrase not in key2lemmas:
					key2lemmas[phrase]=related_lemma_names
				else:
					key2lemmas[phrase].extend(related_lemma_names)
				for lemma in related_lemma_names:
					lemma2key[lemma.lower()]=phrase

			except:
				print ('error',word)
				lemma=wordnet_lemmatizer.lemmatize(word)
				lemma2key[lemma.lower()]=phrase

	with open('OntologyToLemmas.json', 'w') as fp:
	    json.dump(key2lemmas, fp)


	with open('LemmasToOntology.json', 'w') as fp:
	    json.dump(lemma2key, fp)

if __name__=="__main__":
	main()