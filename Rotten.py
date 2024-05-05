#Joshua Hemingway
#5/5/2024

import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_rotten_tomatoes(movie_title):
    url = f"https://www.rottentomatoes.com/m/{movie_title.replace(' ', '_').replace(':', '').replace(',', '').replace('.', '')}"
    response = requests.get(url)
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

# Read movie titles, IMDB ratings, IMDB votes, and genres from the original CSV file
existing_titles = set()
if os.path.isfile('movie_data.csv'):
    with open('movie_data.csv', 'r', newline='', encoding='utf-8') as existing_csv:
        reader = csv.reader(existing_csv)
        next(reader)  # Skip header row
        for row in reader:
            existing_titles.add(row[0])  # Add movie title to the set of existing titles

movie_data = []
with open('movies.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        title, imdb_rating, imdb_votes, genres = row
        if title not in existing_titles:  # Check if the title already exists
            movie_data.append((title, imdb_rating, imdb_votes, genres))
        else:
            print(f"Skipping {title} because it already exists in the CSV file.")

# Scraping Rotten Tomatoes and writing to a new CSV file
with open('movie_data.csv', 'a', newline='', encoding='utf-8') as output_csv:
    writer = csv.writer(output_csv)
    for title, imdb_rating, imdb_votes, genres in movie_data:
        print(f"Processing: {title}")
        audience_score, critic_score, critics_reviews, audience_reviews, streaming_platforms = scrape_rotten_tomatoes(title)
        writer.writerow([title, imdb_rating, imdb_votes, genres, audience_score, critic_score, critics_reviews, audience_reviews, streaming_platforms])
        print(f"Completed: {title}")
