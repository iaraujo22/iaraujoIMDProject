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
    imdbId INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    full_title TEXT NOT NULL,
    the_year INTEGER NOT NULL,
    crew TEXT NOT NULL,
    imdb_rating float NOT NULL,
    imdb_rating_counting INTEGER NOT NULL
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings(
    imdbId INTEGER NOT NULL,
    total_raring INTEGER DEFAULT 0,
    total_rating_votes INTEGER NOT NULL,
    10_rating_percents float NOT NULL,
    10_rating_votes INTEGER NOT NULL,
    9_rating_percents float NOT NULL,
    9_rating_votes INTEGER NOT NULL,
    8_rating_percents float NOT NULL,
    8_rating_votes INTEGER NOT NULL,
    7_rating_percents float NOT NULL,
    7_rating_votes INTEGER NOT NULL,
    6_rating_percents float NOT NULL,
    6_rating_votes INTEGER NOT NULL,
    5_rating_percents float NOT NULL,
    5_rating_votes INTEGER NOT NULL,
    4_rating_percents float NOT NULL,
    4_rating_votes INTEGER NOT NULL,
    3_rating_percents float NOT NULL,
    3_rating_votes INTEGER NOT NULL,
    2_rating_percents float NOT NULL,
    2_rating_votes INTEGER NOT NULL,
    1_rating_percents float NOT NULL,
    1_rating_votes INTEGER NOT NULL,
    FOREIGN KEY (imdbId) REFERENCES top_tv_show (imdbId) ON DELETE CASCADE ON UPDATE NO ACTION,
    );''')


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_db(connection: sqlite3.Connection):
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
    close_db(conn)

    #top_show = get_250_televisionShows()
    #rating_data = get_ratings(top_show)
    #report_results(rating_data)
    #report_results(top_show)

if __name__ == '__main__':
    main()

