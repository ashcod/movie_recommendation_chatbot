import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import pandas as pd
import random


genres = [
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western"
]

pages = np.arange(1, 100, 50)
final_df = pd.DataFrame()

for page in pages:
    for genre_ in genres:
        imdb_url = f"https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres={genre_}&sort=user_rating,desc&start={page}&ref_=adv_nxt"
        headers = {"Accept-Language": "en-US, en;q=0.5"}
        results = requests.get(imdb_url, headers=headers)
        movie_soup = BeautifulSoup(results.text, "html.parser")

        movie_data = []
        movie_divs = movie_soup.find_all("div", class_="lister-item mode-advanced")
        for container in movie_divs:
            genre_info = container.find('span', class_='genre').text.strip()
            genres = [genre.strip() for genre in genre_info.split(',')]
            genre = ', '.join(genres)

            name = container.h3.a.text
            year = container.h3.find('span', class_='lister-item-year').text
            runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
            imdb = float(container.strong.text)
            m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
            nv = container.find_all('span', attrs={'name': 'nv'})
            vote = nv[0].text
            grosses = nv[1].text if len(nv) > 1 else '-'

            movie_data.append({
                'genre_info': genre_,
                'multi_genre': genre,
                'movie_name': name,
                'movie_year': year,
                'movie_runtime': runtime,
                'imdb_ratings': imdb,
                'metascore': m_score,
                'number_votes': vote,
                'us_gross_millions': grosses
            })

        genre_df = pd.DataFrame(movie_data)
        final_df = final_df.append(genre_df, ignore_index=True)

final_df['movie_year'] = final_df['movie_year'].str.extract('(\d+)').fillna(0).astype(int)
final_df['movie_runtime'] = final_df['movie_runtime'].str.extract('(\d+)').fillna(0).astype(int)
final_df['metascore'] = final_df['metascore'].replace('-', 0).astype(int)
final_df['number_votes'] = final_df['number_votes'].str.replace(',', '').fillna('0').astype(int)
final_df['us_gross_millions'] = final_df['us_gross_millions'].map(lambda x: str(x).lstrip('$').rstrip('M'))
final_df['us_gross_millions'] = pd.to_numeric(final_df['us_gross_millions'], errors='coerce')

# Function to recommend 5 random movies based on popularity
def recommend_movies(genres):
    if len(genres) == 1:
        genre_movies = final_df[final_df['genre_info'] == genres[0]]
    else:
        genre_movies = final_df[final_df['multi_genre'].apply(lambda x: sum(genre in x for genre in genres) >= 2)]

    shuffled_movies = genre_movies.sample(frac=1)
    recommended_movies = shuffled_movies[['movie_name', 'imdb_ratings', 'movie_year', 'us_gross_millions', 'movie_runtime']].head(5)
    return recommended_movies

# Function to display additional information when a movie title is clicked
def show_additional_info(movie_name):
    movie_info = final_df[final_df['movie_name'] == movie_name]
    info_window = tk.Toplevel(window)
    info_window.title(movie_name)
    info_window.geometry("300x150")

    movie_year = movie_info['movie_year'].values[0]
    us_gross = movie_info['us_gross_millions'].values[0]
    runtime = movie_info['movie_runtime'].values[0]
    imdb_rating = movie_info['imdb_ratings'].values[0]

    movie_info_label = ttk.Label(info_window, text=f"Year: {movie_year}  |  Gross: {us_gross}  |  Runtime: {runtime} mins  |  IMDb Rating: {imdb_rating:.1f}")
    movie_info_label.pack(pady=20)

# Create the GUI window
def recommend_movies_gui():
    def get_recommendations():
        selected_genres = []
        for genre, var in genre_variables.items():
            if var.get() == 1:
                selected_genres.append(genre)

        if len(selected_genres) > 3:
            tk.messagebox.showwarning("Genre Selection", "Please select a maximum of three genres.")
            return

        recommended_movies = recommend_movies(selected_genres)
        recommendations_text.config(state=tk.NORMAL)
        recommendations_text.delete('1.0', tk.END)
        for movie in recommended_movies.values:
            movie_name, imdb_rating, movie_year, us_gross, movie_runtime = movie
            recommendations_text.insert(tk.END, movie_name, "clickable")
            recommendations_text.insert(tk.END, f"  |  IMDb Rating: {imdb_rating:.1f}\n")
        recommendations_text.config(state=tk.DISABLED)

    window = tk.Tk()
    window.title("Movie Recommendation Chatbot")

    # Create a stylish frame for the genre buttons
    genre_frame = ttk.Frame(window)
    genre_frame.pack(pady=10)

    genres = [
        "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family",
        "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance",
        "Sci-Fi", "Sport", "Thriller", "War", "Western"
    ]

    genre_variables = {}
    for genre in genres:
        genre_variables[genre] = tk.IntVar()
        genre_checkbutton = ttk.Checkbutton(genre_frame, text=genre, variable=genre_variables[genre])
        genre_checkbutton.pack(side=tk.LEFT, padx=10)

    # Create a stylish frame for the movie recommendations
    recommendations_frame = ttk.Frame(window)
    recommendations_frame.pack(pady=20)

    recommendations_label = ttk.Label(recommendations_frame, text="Movie Recommendations (Select Min.1 and Max.3 genres):")
    recommendations_label.pack()

    # Create a scrollable text box for displaying movie recommendations
    recommendations_scrollbar = ttk.Scrollbar(recommendations_frame)
    recommendations_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    recommendations_text = tk.Text(recommendations_frame, height=15, width=40, wrap=tk.WORD, yscrollcommand=recommendations_scrollbar.set)
    recommendations_text.pack()

    recommendations_scrollbar.config(command=recommendations_text.yview)

    # Function to handle movie title click event
    def click_event(event):
        index = recommendations_text.index("@%s,%s" % (event.x, event.y))
        start, end = index.split(".")
        movie_name = recommendations_text.get(start, end)
        show_additional_info(movie_name)

    recommendations_text.tag_configure("clickable", foreground="blue", underline=True)
    recommendations_text.tag_bind("clickable", "<Button-1>", click_event)

    recommend_button = ttk.Button(window, text="Recommend", command=get_recommendations)
    recommend_button.pack(pady=10)

    window.mainloop()