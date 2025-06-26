import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('data.csv')
selected_features = ['title','authors','categories','published_year']
for feature in selected_features:
    df[feature] = df[feature].fillna('')
combined_features = df['title'] + ' ' + df['categories'] + ' ' + df['authors'] + ' ' + f"{df['published_year']}"
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors, feature_vectors)
list_of_all_titles = df['title'].tolist()
book_name = input('Enter your favourite book name : ')
find_close_match = difflib.get_close_matches(book_name, list_of_all_titles)
close_match = find_close_match[0]
index_of_the_book = df[df.title == close_match]['index'].values[0]
similarity_score = list(enumerate(similarity[index_of_the_book]))
sorted_similar_books = sorted(similarity_score, key=lambda x:x[1], reverse=True)
print('Books suggested for you:\n')
i = 1
for book in sorted_similar_books:
    index = book[0]
    title_from_index = df[df.index==index]['title'].values[0]
    if i < 6:
        print(i, '.', title_from_index)
        i += 1
