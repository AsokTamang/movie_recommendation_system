import pickle
import requests


def load_obj():  #function which loads the trained pickle object
    movies = pickle.load(open('artifacts/movie_df.pkl','rb'))
    similarity_data = pickle.load(open('artifacts/similarity_data.pkl','rb'))
    return movies , similarity_data



def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_url


def recommend_movies(movie_name):
    movies , similarity_data = load_obj()
    movie_index = movies[movies['title'].str.strip().str.lower() == movie_name.strip().lower()].index[0]  #finding the index of the movie in the similarity variable using the movie name
    movie_similarity_data = sorted(list(enumerate(similarity_data[movie_index])),reverse=True,key=lambda x:x[1])  #sorting the list based on the similarity value not the index in descending order, cause using enumerate we get both the index as well as cosine similarity value
    result = []
    #finding the top 5 most similar movies names as well as their posters
    for i in movie_similarity_data[1:6]:
        similar_movie_index = i[0]
        title =  movies.iloc[similar_movie_index]['title']
        similar_movie_id = movies.iloc[similar_movie_index]['id']  #based on the movie index we are extracting the movie id

        result.append({
            "title":title,
            "poster": fetch_poster(similar_movie_id)  # using the actual movie_id column
        })
    return result
print(recommend_movies('Avatar'))



   