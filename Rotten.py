#please Note that the use of this scrapper will likely get your IP address blocked from Rotten tomatoes
#this is due to the scraper isn't implementing any form of delay etc; and will send alot of requests to there server and they will likely block you for it
#this is your warning, you maybe able to implement some delay etc and prevent yourself from being blocked

import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_rotten_tomatoes(movie_title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://www.rottentomatoes.com/m/{movie_title.replace(' ', '_').replace(':', '').replace(',', '').replace('.', '')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find audience score
    audience_score_elem = soup.find('rt-button', slot='audienceScore')
    audience_score = audience_score_elem.find('rt-text').text.strip() if audience_score_elem else "Audience score not found"

    # Find critic score
    critic_score_elem = soup.find('rt-button', slot='criticsScore')
    critic_score = critic_score_elem.find('rt-text').text.strip() if critic_score_elem else "Critic score not found"

    critics_reviews_elem = soup.find('rt-link', slot='criticsReviews')
    critics_reviews = critics_reviews_elem.text.strip() if critics_reviews_elem else "Critics reviews not found"

    audience_reviews_elem = soup.find('rt-link', slot='audienceReviews')
    audience_reviews = audience_reviews_elem.text.strip() if audience_reviews_elem else "Audience reviews not found"

    # Find streaming platforms
    streaming_platforms = []
    where_to_watch_bubbles = soup.find_all('where-to-watch-bubble')
    for bubble in where_to_watch_bubbles:
        platform = bubble['image']
        streaming_platforms.append(platform)

    return audience_score, critic_score, critics_reviews, audience_reviews, ', '.join(streaming_platforms)

# Prompt user for input CSV file name
input_csv_file = input("Enter the name of the input CSV file (e.g., 'movies.csv'): ")

# Prompt user for output CSV file name
output_csv_file = input("Enter the name of the output CSV file (e.g., 'movie_data.csv'): ")

# Read movie titles, IMDB ratings, IMDB votes, and genres from the original CSV file
existing_titles = set()
if os.path.isfile(output_csv_file):
    with open(output_csv_file, 'r', newline='', encoding='utf-8') as existing_csv:
        reader = csv.reader(existing_csv)
        next(reader)  # Skip header row
        for row in reader:
            existing_titles.add(row[0])  # Add movie title to the set of existing titles

movie_data = []
with open(input_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        title, imdb_rating, imdb_votes, genres = row
        if title not in existing_titles:  # Check if the title already exists
            movie_data.append((title, imdb_rating, imdb_votes, genres))
        else:
            print(f"Skipping {title} because it already exists in the CSV file.")

# Scraping Rotten Tomatoes and writing to a new CSV file
with open(output_csv_file, 'a', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)
    for title, imdb_rating, imdb_votes, genres in movie_data:
        print(f"Processing: {title}")
        audience_score, critic_score, critics_reviews, audience_reviews, streaming_platforms = scrape_rotten_tomatoes(title)
        writer.writerow([title, imdb_rating, imdb_votes, genres, audience_score, critic_score, critics_reviews, audience_reviews, streaming_platforms])
        print(f"Completed: {title}")
