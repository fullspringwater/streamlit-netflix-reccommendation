import numpy as np
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# 추천 시스템
# indices = 가장 가까운 요소들
def recommended_movie(title):
    X = pd.read_csv('data/X.csv', index_col=0)
    y = pd.read_csv('data/y.csv', index_col=0)
    kn = joblib.load('data/kn.pkl')

    _, indices = kn.kneighbors(np.array(X.loc[title]).reshape(1,144))
    nearest_title = [y.iloc[i][0] for i in indices.flatten()][1:]
    sim_rates = []

    for nt in nearest_title :
        sim = cosine_similarity(np.array(X.loc[title]).reshape(1,144),
                                    np.array(X.loc[nt]).reshape(1,144)).flatten()
        sim_rates.append(sim[0])
        
    recommended_movies = pd.DataFrame({
                            'Title' : nearest_title,                                 
                            'Similarity' : sim_rates} )
    recommended_movies.sort_values('Similarity', ascending =False)

    return recommended_movies