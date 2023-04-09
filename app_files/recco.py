import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

udemy_df = pd.read_csv('udemy_master_df.csv', usecols = ['Title', 'Summary'])
job_descriptions_df = pd.read_excel('Task_Statements.xlsx', usecols = ['Title', 'Task'])

udemy_df = udemy_df[udemy_df['Summary'].notna()]

job_descriptions_df = job_descriptions_df.groupby(['Title'])['Task'].apply(','.join).reset_index()

job_df = job_descriptions_df.copy()
course_df = udemy_df.copy()

course_df  = course_df.drop_duplicates()

course_df = course_df[course_df['Summary'].map(lambda x: x.isascii())]

#A contractions dictionary from Wikipedia found on Stack Overflow for expanding contractions: 
#https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions_dict = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}

#This code is code to expand contractions in text created by Abhishek Sharma:
#https://www.analyticsvidhya.com/blog/2020/04/beginners-guide-exploratory-data-analysis-text-data/

#Regular expression for finding contractions
contractions_re=re.compile('(%s)' % '|'.join(contractions_dict.keys()))

#Function for expanding contractions
def expand_contractions(text,contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, text)

# Expanding Contractions in the reviews and titles for course_df; job_df doesn't include any contractions
course_df['Summary']= course_df['Summary'].apply(lambda x:expand_contractions(x))

tfidfvec = TfidfVectorizer(
            max_df=0.7,   # note: % of docs in collection
            max_features = 10000, # only top 10k by freq,
            lowercase = True, 
            min_df=2,  # note: absolute count of documents
            stop_words="english",
            ngram_range = (1,2), # include 2-word phrases
            use_idf=True, # Enable inverse-document-frequency reweighting. If False, idf(t) = 1.
            )

vectorized_data = tfidfvec.fit_transform(course_df['Summary'])

tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns=tfidfvec.get_feature_names())

tfidf_df.index = course_df['Title']

cosine_similarity_array = cosine_similarity(tfidf_df)

cosine_similarity_df = pd.DataFrame(cosine_similarity_array, columns=tfidf_df.index,index=tfidf_df.index)

tfidfvec3 = TfidfVectorizer(
            lowercase = True, 
            ngram_range = (1,2), # include 2-word phrases
            )

vectorized_data = tfidfvec3.fit_transform(course_df['Summary'])

def recommender(job_name, num):
    
    query_vec = tfidfvec3.transform([job_name])
    similarity = cosine_similarity(query_vec, vectorized_data).flatten() # calculate similarity with vectorized course summary
    indices = np.argpartition(similarity, -1)[-5:]
    
    course_name = course_df.iloc[indices][::-1]['Title'].values[0]
    
    #print(course_name)
    
    cosine_similarity_series = cosine_similarity_df.loc[course_name]
    
    ordered_similarities = cosine_similarity_series.sort_values(ascending=False)
    
    course_list = ordered_similarities[0:num]
    df = pd.DataFrame(ordered_similarities).reset_index()
    
    #return course_list
    return df['Title'].head().to_list() #return a list for plotly table creation in app