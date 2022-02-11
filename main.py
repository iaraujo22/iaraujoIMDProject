# Ivanildo Araujo (Ivan)
# COMP 490-001
# comment to test workflow
import unittest.result

import sys
import requests
import secrets
import sqlite3
from typing import Tuple


def setup_tables(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_tv_show(
    imdbId TEXT PRIMARY KEY, 
    title TEXT NOT NULL, 
    full_title TEXT NOT NULL,
    the_year TEXT NOT NULL,
    crew TEXT NOT NULL,
    imdb_rating TEXT NOT NULL,
    imdb_rating_counting TEXT NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings(
    imdbId INTEGER NOT NULL,
    total_raring INTEGER DEFAULT 0,
    total_rating_votes INTEGER NOT NULL,
    rating_10_percent REAL NOT NULL,
    rating_10_votes INTEGER NOT NULL,
    rating_9_percents REAL NOT NULL,
    rating_9_votes INTEGER NOT NULL,
    rating_8_percents REAL NOT NULL,
    rating_8_votes INTEGER NOT NULL,
    rating_7_percents REAL NOT NULL,
    rating_7_votes INTEGER NOT NULL,
    rating_6_percents REAL NOT NULL,
    rating_6_votes INTEGER NOT NULL,
    rating_5_percents REAL NOT NULL,
    rating_5_votes INTEGER NOT NULL,
    rating_4_percents REAL NOT NULL,
    rating_4_votes INTEGER NOT NULL,
    rating_3_percents REAL NOT NULL,
    rating_3_votes INTEGER NOT NULL,
    rating_2_percents REAL NOT NULL,
    rating_2_votes INTEGER NOT NULL,
    rating_1_percents REAL NOT NULL,
    rating_1_votes INTEGER NOT NULL,
    FOREIGN KEY (imdbId) REFERENCES top_tv_show (imdbId) ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def populate_top_tv_show(show_list, cursor: sqlite3.Cursor):
    for data in show_list:
        cursor.execute('''INSERT INTO top_tv_show(imdbID, title, full_title, the_year, crew,  imdb_rating, imdb_rating_counting) 
        VALUES (?,?,?,?,?,?,?);
        ''', (data['id'], data['title'], data['fullTitle'], data['year'], data['crew'], data['imDbRating'], data['imDbRatingCount']))


def populate_rating(results, cursor: sqlite3.Cursor):
    for rate_data in results:
        cursor.execute('''INSERT INTO rating(imdbId, total_raring, total_rating_votes, rating_10_percent, rating_10_votes, rating_9_percents, rating_9_votes, rating_8_percents,
            rating_8_votes, rating_7_percents, rating_7_votes, rating_6_percents, rating_6_votes, rating_5_percents, rating_5_votes, rating_4_percents, rating_4_votes,
              rating_3_percents, rating_3_votes, rating_2_percents, rating_2_votes,rating_1_percents, rating_1_votes)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
              ''', (rate_data['imDbId'], rate_data['totalRating'], rate_data['totalRatingVotes'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'],
                    rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId'],
                    rate_data['imDbId'], rate_data['imDbId'], rate_data['imDbId']))

def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()

def get_250_televisionShows() -> list[dict]:
    location = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secrets_key}"
    result = requests.get(location)
    if result.status_code != 200:
        print("Failed to get data!")
        sys.exit(-1)
    data = result.json()
    show_list = data["items"]
    return show_list


def report_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)

def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.secrets_key}/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundered)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:  # if we don't get an ok response we have trouble, skip it
            print(f"Failed to get data!")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results

def main():
    conn, cursor = open_db("project1_sprint2.sqlite")
    print(type(conn))
    setup_tables(cursor)
    show_list = get_250_televisionShows()
    populate_top_tv_show(show_list, cursor)
    close_db(conn)

    top_show = get_250_televisionShows()
    rating_data = get_ratings(top_show)
    report_results(rating_data)
    report_results(top_show)

if __name__ == '__main__':
    main()

