# Movie Recommendation Chatbot

The Movie Recommendation Chatbot is a Python application that recommends movies based on selected genres. It retrieves movie data from IMDb using web scraping techniques and provides a user-friendly graphical user interface (GUI) for interacting with the chatbot.

## Features

- Select up to three movie genres to get personalized movie recommendations.
- Displays recommended movies with their IMDb ratings, release year, box office gross, and runtime.
- Provides additional information about a movie by clicking on its title, including the year of release, box office gross, runtime, and IMDb rating.

## Scraping Process

The Movie Recommendation Chatbot scrapes movie data from IMDb using web scraping techniques. It follows these steps to gather the necessary information:

1. Constructs the IMDb search URL for each genre and movie page to scrape.
2. Sends HTTP requests to IMDb, retrieves the HTML response, and parses it using BeautifulSoup.
3. Extracts movie details such as genre, title, release year, runtime, IMDb rating, metascore, number of votes, and box office gross from the HTML.
4. Stores the extracted data in a Pandas DataFrame for further processing.

## Technical Concepts

The Movie Recommendation Chatbot utilizes the following technical concepts:

- Web Scraping: The process of extracting data from websites by sending HTTP requests and parsing the HTML response.
- Graphical User Interface (GUI): A user interface that allows users to interact with the chatbot visually, using checkboxes and buttons.
- Data Processing: The extracted movie data is processed using Pandas to filter, manipulate, and present the recommendations.

## Technologies Used

The Movie Recommendation Chatbot is built using the following technologies and libraries:

- Python: The programming language used for developing the chatbot.
- Pandas: A powerful library for data manipulation and analysis.
- BeautifulSoup: A Python library for parsing HTML and XML documents.
- Tkinter: The standard Python interface for creating GUI applications.

## How to Install and Configure?

Follow these steps to install and configure the Movie Recommendation Chatbot:

### Prerequisites

- Python 3.7 or higher
- Required Python packages: pandas, numpy, requests, bs4, tkinter

### Installation

Clone the repository:

git clone https://github.com/your-username/movie-recommendation-chatbot.git

Usage

1. Run the chatbot by executing main.py:  python main.py

2. The chatbot GUI window will open, presenting you with a list of movie genres in checkboxes.

3. Select one to three genres by clicking on the checkboxes. (Note: Selecting more than three genres will prompt a warning message.)

4. Click the "Recommend" button to get movie recommendations based on the selected genres.

5. The recommended movies will be displayed in the GUI, showing the movie title, IMDb rating


Contributing:

Contributions to the Movie Recommendation Chatbot are welcome! If you encounter any bugs, have suggestions for improvements, or would like to add new features, please open an issue or submit a pull request. Please follow the existing code style and maintain clear commit messages.

License


Acknowledgments:
The movie data is fetched from IMDb using web scraping techniques.

Disclaimer:
The Movie Recommendation Chatbot is a personal project and not affiliated with IMDb or any other movie-related organization. The movie data provided is for informational purposes only. Use at your own discretion.
