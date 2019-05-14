# -*- coding: utf-8 -*-

#Please Refer the Code Manual

#Importing the Libraries
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



#Loading the Data
initial = pd.read_excel('C:\Sameer\Data Science\Aegis\Capstone\Recommendation\Algorithms_ex.xlsx', encoding='utf-8',sheet_name='Sheet2')
initial=initial[0:39]
initial.head()
initial.columns

#Content Based Recommendation


#Removing the lowercase and strip all the spaces between them

#create  "soup", which is a string that contains all the data that you want to feed to your
#vectorizer (namely actors, director and genre).
def create_soup(x):
    return x['title'] + ' ' + x['summarized'] + ' ' + x['topic']

initial['soup'] = initial.apply(create_soup, axis=1)

#Convert a collection of text documents to a matrix of token counts
count = CountVectorizer()
count_matrix = count.fit_transform(initial['soup'])

#finding cosine similarity
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
#Construct a map of indices and movie titles
indices = pd.Series(initial.index,  index=initial['summarized'])


# Function that takes in movie title as input and outputs most similar movies

def recommend(title):
    indx=indices[title]
    similar_score = list(enumerate(cosine_sim2[indx]))
    print(similar_score)

	#sort the movie based on the similarity score as we want top 10 similar movies
    similar_score=sorted(similar_score,key=lambda x:x[1],reverse=True)
	#print(sim_score)

    sim_score = list(similar_score[1:6])
    print(sim_score)

    blog_list=[]
    for i in sim_score:
        blog_list.append(initial['title'].iloc[i[0]])
        
    return blog_list
#-------------------------------------------------------------------------------------------------
import sklearn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from Data_cleaning import *

stopwords_list = stopwords.words('english')
vectorizer = TfidfVectorizer(analyzer='word')
tfidf_matrix = vectorizer.fit_transform(initial['summarized'])
tfidf_matrix.shape
tfidf_feature_name = vectorizer.get_feature_names()
cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(initial['summarized'].index)


#Function to get the most similar books
def recommend1(index, method):
    id = indices[index]
    # Get the pairwise similarity scores of all books compared that book,
    # sorting them and getting top 5
    similarity_scores = list(enumerate(method[id]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:6]
    
    #Get the books index
    blog_index = [i[0] for i in similarity_scores]
    
    #Return the top 5 most similar books using integar-location based indexing (iloc)
    return initial['title'].iloc[blog_index]


