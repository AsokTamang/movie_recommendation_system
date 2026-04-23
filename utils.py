import pickle
import requests
movies = pickle.load(open('artifacts/movie_df.pkl','rb'))
similarity_data = pickle.load(open('artifacts/similarity_data.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend_movies(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]  #finding the index of the movie in the similarity variable using the movie name
    movie_similarity_data = sorted(list(enumerate(similarity_data[movie_index])),reverse=True,key=lambda x:x[1])  #sorting the list based on the similarity value not the index in descending order, cause using enumerate we get both the index as well as cosine similarity value
    result = []
    #finding the top 5 most similar movies names as well as their posters
    for i in movie_similarity_data[1:6]:
        similar_movie_index = i[0]
        result.append({
            "title": movies.iloc[similar_movie_index]['title'],
            "poster": fetch_poster(similar_movie_index)  # use actual movie_id column
        })
    return result
    
   