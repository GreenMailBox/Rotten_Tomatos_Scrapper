# Rotten_Tomatos_Scrapper

This Python script scrapes data about movies from Rotten Tomatoes and adds it to a CSV file. It retrieves information such as audience score, critic score, critics reviews, audience reviews, and streaming platforms.

## Features

- Scrapes movie data from Rotten Tomatoes
- Retrieves audience score, critic score, critics reviews, audience reviews, and streaming platforms
- Supports multi-word movie titles and handles special characters in movie titles
- Skips movies that are already in the CSV file
- Prints progress messages to the console
- Saves data to a CSV file for easy access and analysis

## Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `csv` library

## Installation


## Usage
1. Prepare a CSV file (`movies.csv`) containing movie titles, IMDB ratings, IMDB votes, and genres.
2. Run the script:


3. The script will scrape Rotten Tomatoes for each movie in the CSV file, retrieve the desired information, and append it to a new CSV file (`movie_data.csv`).

## Example CSV Format

Title,IMDB Rating,IMDB Votes,Genres,Audience Score,Critic Score,Critics Reviews,Audience Reviews,Streaming Platforms
No Way Up,4.6,4185,"Action, Adventure, Drama, Thriller",90%,80%,556 Reviews,50,000+ Ratings,Netflix, Amazon Prime Video
Immaculate,5.9,20476,Horror,88%,75%,450 Reviews,30,000+ Ratings,Netflix


## Contributors

- John Doe (@john-doe)
- Jane Smith (@jane-smith)

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.


