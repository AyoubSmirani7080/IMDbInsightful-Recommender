# importing necessary libraries for the program.
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk





# Load movies data 
movies_df = pd.read_csv('data.csv')

# The code snippet is performing the following tasks:

# Combine textual features into one column
movies_df['text_features'] = movies_df['Genre'] + ' ' + movies_df['Realisation'] + ' ' + movies_df['Actors']

# Feature extraction using TfidfVectorizer for text features
tfidf = TfidfVectorizer(stop_words='english')
feature_matrix = tfidf.fit_transform(movies_df['text_features'])


for i,value in enumerate(movies_df['Ratings']):
    movies_df['Ratings'][i] = value.split('/')[0]
 
movies_df.Ratings.astype('float64')
# Include numerical features (release year and ratings)
numerical_features = movies_df[['ReleaseYear', 'Ratings']].values

# Combine text and numerical features into a final feature matrix
final_feature_matrix = pd.DataFrame(feature_matrix.toarray(), columns=tfidf.get_feature_names_out())\
    .join(pd.DataFrame(numerical_features, columns=['ReleaseYear', 'Ratings']))

# Calculate cosine similarity matrix
cosine_sim = cosine_similarity(final_feature_matrix, final_feature_matrix)






# The function recommends similar movies based on a given movie title, a similarity matrix, and movie data.
# param movie_title: The title of the movie for which you want to find similar movies
# param similarity_matrix: The similarity_matrix is a matrix that represents the similarity between movies. Each row and column in the matrix corresponds to a movie, and the value in each cell
# represents the similarity between the movies. The higher the value, the more similar the movies are
# param movies_data: The movies_data parameter is a pandas DataFrame that contains information about movies. It should have columns such as 'name', 'genre', 'director', 'rating', etc. Each row
# represents a movie and each column represents a specific attribute of the movie
# param N: The parameter N represents the number of similar movies to recommend. It determines how many similar movies will be returned in the output, defaults to 5 (optional)
# return: a DataFrame containing the N most similar movies to the given movie title.
    


def recommend_similar_movies(movie_title, similarity_matrix, movies_data, N=5):

    movie_index = movies_data[movies_data['Name'] == movie_title].index[0]

    similar_movies_indices = pd.Series(similarity_matrix[movie_index])\
        .sort_values(ascending=False).iloc[1:N+1].index
    return movies_data.iloc[similar_movies_indices]





# The function "search" takes a chosen movie title as input, destroys any existing movie widgets,retrieves recommended similar movies based on the chosen movie
# title, and displays the recommended movies in a table format.
# param chosen_movie_title: The chosen_movie_title parameter is the title of the movie that the user has selected or entered. It is used as input to the recommend_similar_movies function to find
# similar movies based on this title

def search(chosen_movie_title):    

    global current_movies_displayed

    for widget in current_movies_displayed:
        widget.destroy()

    recommended_movies = recommend_similar_movies(chosen_movie_title, cosine_sim, movies_df)
    recommended_movies =  recommended_movies[['Name', 'Genre', 'Realisation', 'Actors', 'ReleaseYear', 'Ratings']]
    choice_film = tk.Label(text='Recommended movies based on this film',font=tkFont.Font(size=20),bg='#fff',fg='#094366')
    canvas.create_window(500, 250, anchor=tk.NW, window=choice_film)
    show_table_titles(recommended_movies)
    show_table_Content(recommended_movies)
    



# The function `show_table_titles` creates labels for each column title in a table and positions them on a canvas.
# param movies: The parameter "movies" is expected to be a pandas DataFrame object that contains the
# data for the movies table

def show_table_titles(movies):

    addCOL = 100
    for col_index, col_name in enumerate(movies.columns):

        label = tk.Label( text=col_name,font=tkFont.Font(size=16),fg='#888888')
        canvas.create_window(addCOL,350 , anchor=tk.NW, window=label)
        addCOL+=230
        print(addCOL)





    
# The function `show_table_Content` displays the content of a table of movies on a canvas.
# param movies: The parameter "movies" is expected to be a pandas DataFrame containing the data of movies. Each row of the DataFrame represents a movie, and each column represents a specific
# attribute of the movie (e.g., title, genre, release date, etc.)

def show_table_Content(movies):

    col = 350
    row = 100        
    for index, movie in movies.iterrows():
        row = 100
        col +=50
        for col_index, col_value in enumerate(movie):

            label = tk.Label(text=str(col_value))
            canvas.create_window(row,col , anchor=tk.NW, window=label)
            if col_index == 3:
                row +=110
            row+=230
            current_movies_displayed.append(label)
    

current_movies_displayed = []



#    The `display_interface` function creates a graphical user interface (GUI) using the Tkinter library
#    in Python, with a background image, labels, and an option menu for selecting a film.
def display_interface(): 
   
        window = tk.Tk()
        window.geometry("1400x900")     
        movies_ToShow =movies_df['Name'].to_list()
        img= tk.PhotoImage(file='icons.png', master= window)
        img_label= tk.Label(window,image=img)
        img_label.grid()
        background_image_pil = Image.open("./vector.png")  # Replace with the path to your image
        background_image = ImageTk.PhotoImage(background_image_pil)
        global canvas
        canvas = tk.Canvas(window, width=1400, height=900)
        canvas.grid(row=0, column=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
        canvas.lower(background_image)
        
        paddings = {'padx': 5, 'pady': 5}
        Recommendation = tk.Label(text='Recommendation System',font=tkFont.Font(size=24),bg='#fff',fg='#094366')

        choice_film = tk.Label(text='choice a film :',font=tkFont.Font(size=18))

        canvas.create_window(530, 5, anchor=tk.NW, window=Recommendation)
        canvas.create_window(20, 100, anchor=tk.NW, window=choice_film)
        option_menu = tk.OptionMenu(
                    window,
                    tk.StringVar(window),
                    movies_ToShow[0],
                    *movies_ToShow,
                    command=search)

        option_menu.config(font=('Arial', 12), borderwidth=6, bg='lightblue',highlightthickness=6, fg='black')
        canvas.create_window(200, 100, anchor=tk.NW, window=option_menu)
        window.mainloop()




display_interface()







