# importing the necessary libraries for web scraping and data manipulation.

import requests
from bs4  import BeautifulSoup
import pandas as pd



# The function `GetaSoup` takes a URL as input, sends a GET request to that URL with specific headers and returns the parsed HTML content using BeautifulSoup.
# param url: The `url` parameter is the URL of the webpage you want to scrape. It is the address of the webpage you want to retrieve the HTML content from
# return: The function `GetaSoup` returns a BeautifulSoup object.

def GetaSoup(url):
     
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36'
       }
    page = requests.get(url, headers=headers)

    return BeautifulSoup(page.text , "html.parser")




# The function `get_films_data` scrapes data from the IMDb top films chart and returns a dictionary
# containing information about the films such as name, realization, actors, genre, release year, and ratings.
# return: The function `get_films_data()` returns a dictionary containing the following keys and their corresponding values

def get_films_data() -> pd.DataFrame:
             
      soup =  GetaSoup('https://www.imdb.com/chart/top/')
      nameArray = []
      genreArray = []
      ratingsArray = []
      releaseyearArray = []
      RealizationArray = []
      actorsArray = []

      tags = soup.find_all("a")
      cleanTags = [i for i in tags if '.' in i.text] 
      for i,value in enumerate(cleanTags):
            name,Realization,actors,genre,ratings,releaseyear = get_film_data(value['href'])
            nameArray.append(name)
            genreArray.append(genre)
            ratingsArray.append(ratings)
            releaseyearArray.append(releaseyear)
            RealizationArray.append(Realization)
            actorsArray.append(actors)
            print(i)
            if i == 248:
               
               return {"Name":nameArray,"Realisation":RealizationArray,"Actors":actorsArray,"Genre":genreArray, "ReleaseYear":releaseyearArray,"Ratings":ratingsArray}

     


# The function `joinGenre` takes a string `genre` and splits it into separate words based on uppercase letters then joins them together with commas.
# param genre: The `genre` parameter is a string representing a genre or a combination of genres
# return: a string that is the result of joining the elements of the "array" list with commas.

def joinGenre(genre):
   
    array =[]
    ch = ""
    for i,value in enumerate(genre):
         if value.isupper() and i>0:
              array.append(ch)
              ch=""
              ch+=value
         else:
              ch+=value
    array.append(ch) 

    return ",".join(array)


# The function `getReleaseData` extracts the release year from a given URL and returns it.
# param urlreleaseyear: The parameter `urlreleaseyear` is the URL of a webpage that contains information about release dates for a specific year
# return: the release year of a movie or TV show.

def getReleaseData(urlreleaseyear):

    soup = GetaSoup(urlreleaseyear) 
    datebyCountry = soup.find("div",{'data-testid':'sub-section-releases'}).find("ul").find_all('li')
    array =[i.text for i in datebyCountry]
    ch = ''
    """only to test then i will return the array"""
    for i in array[0]:
      if i != '(':
         ch += i
      else:
        break        
    print(ch[-4:]) 

    return ch[-4:]     


# The function `get_film_data` retrieves various data about a film from a given IMDb URL.
# param urlToC: The parameter `urlToC` is the URL of the film's page on IMDb. It is used to fetch the necessary data from the webpage
# return: The function `get_film_data` returns the following information about a film:
# - `Name`: the name of the film
# - `Realisation`: the name of the director
# - `Actors`: a string containing the names of the actors in the film, separated by commas
# - `FormattedGenre`: a string containing the genres of the film, formatted in a specific way
# - `Ratings
# - `releaseyear

def get_film_data(urlToC):

    soup = GetaSoup(f'https://www.imdb.com/{urlToC}') 
    name = soup.find("span",{'class':'hero__primary-text'}).text
    genre =  soup.find("div",{'data-testid':'genres'}).text
    ratings =  soup.find("div",{'data-testid':'hero-rating-bar__aggregate-rating__score'}).text       
    Realization = soup.find("li",{'data-testid':'title-pc-principal-credit'}).find("a").text  
    actorsItem = soup.find_all("li",{'data-testid':'title-pc-principal-credit'})[2].find_all("a")[1:]
    actors = ",".join(i.text for i in actorsItem)
    formattedGenre = joinGenre(genre)    
    urlreleaseyear =  soup.find("div",{"class":"sc-e226b0e3-3 dwkouE"}).find("a",{'class':'ipc-link ipc-link--baseAlt ipc-link--inherit-color'})['href']            
    ReleaseDate = getReleaseData(f'https://www.imdb.com/{urlreleaseyear}')  
    
    return name,Realization,actors[:-1],formattedGenre,ratings,ReleaseDate 



# The code is calling the `get_films_data()` function to scrape data from the IMDb top films chart.
# The returned data is then converted into a pandas DataFrame using `pd.DataFrame()` and saved as a CSV file named "data.csv" using `data.to_csv()`.

films_data = get_films_data()
data = pd.DataFrame(films_data,columns=films_data.keys())
data.to_csv('data.csv',index=False)








