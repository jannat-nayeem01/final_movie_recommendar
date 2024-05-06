from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_by_user', methods=['GET', 'POST'])
def search_by_user():
    if request.method == 'POST':
        user_id = request.form['userId']
        try:
            # Load user data
            user_data = pd.read_csv('finalUsers.csv')
            user_id = int(user_id)

            if user_id in user_data['userId'].values:
                user_community = user_data[user_data['userId'] == user_id]['Community'].iloc[0]
                community_users = user_data[user_data['Community'] == user_community]
                movie_ids = community_users['movieId'].unique()

                # Load movie data
                movie_data = pd.read_csv('updated_partition.csv')
                movies_info = movie_data[movie_data['movieId'].isin(movie_ids)]
                movie_titles = movies_info['title'].tolist()
                return render_template('results.html', movies=movie_titles)
            else:
                return "User ID not found"
        except ValueError:
            return "Invalid Input. Please enter a valid User ID."
    return render_template('user_search.html')

@app.route('/search_by_movie', methods=['GET', 'POST'])
def search_by_movie():
    if request.method == 'POST':
        movie_title = request.form['movieTitle']
        movie_data = pd.read_csv('updated_partition.csv')

        # Find the movie and its community
        matching_movies = movie_data[movie_data['title'].str.lower() == movie_title.lower()]
        if not matching_movies.empty:
            movie_community = matching_movies['Community'].iloc[0]

            # Get other movies in the same community
            community_movies = movie_data[movie_data['Community'] == movie_community]
            movie_titles = community_movies['title'].unique().tolist()
            return render_template('results.html', movies=movie_titles)
        else:
            return "Movie title not found"
    return render_template('movie_search.html')

if __name__ == '__main__':
    app.run(debug=True)
