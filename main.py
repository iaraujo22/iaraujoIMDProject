# Ivanildo Araujo (Ivan)
# COMP 490-001
# comment to test workflow

import sqlite3
from typing import Tuple

import Window as Window
import requests
import secrets
import guiWindow
import  pandas as pd
from PySide6.QtWidgets import QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QMessageBox
import pyqtgraph as pg
import sys


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()

def get_250_TV() -> list[dict]:
    location = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}"
    result = requests.get(location)
    if result.status_code != 200:
        print("Failed to get 250 TV show!")
        sys.exit(-1)
    data = result.json()
    show_list = data["items"]
    return show_list

def get_most_popular_movies() -> list[tuple]:
    location = f"https://imdb-api.com/en/API/MostPopularMovies/{secrets.secret_key}"
    result = requests.get(location)
    if result.status_code != 200:
        print("Failed to get Most popular Movie!")
        sys.exit(-1)
    data = result.json()
    movie_list = data["items"]
    most_pop_ready = prepare_most_popular(movie_list)
    return most_pop_ready

def get_most_popular_TV() -> list[tuple]:
    location = f"https://imdb-api.com/en/API/MostPopularTVs/{secrets.secret_key}"
    result = requests.get(location)
    if result.status_code != 200:
        print("Failed to get Most popular TV show")
        sys.exit(-1)
    data = result.json()
    show_list = data["items"]
    most_pop_ready = prepare_most_popular(show_list)
    return most_pop_ready

def get_top_250_Movies() -> list[dict]:
    location = f"https://imdb-api.com/en/API/Top250Movies/{secrets.secret_key}"
    result = requests.get(location)
    if result.status_code != 200:
        print("Failed to get TOP 250 Movie!")
        sys.exit(-1)
    data = result.json()
    top_movie_list = data["items"]
    return top_movie_list

def report_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)

def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/"
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
            print(f"Failed to get  ratings data!")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def prepare_top_250_data(most_popular_json: list[dict]) -> list[tuple]:
    data_for_database = []
    for show_data in most_popular_json:
        show_values = list(show_data.values())  # dict values is now an object that is almost a list, lets make it one
        # now we have the values, but several of them are strings and I would like them to be numbers
        # since python 3.7 dictionaries are guaranteed to be in insertion order
        show_values[1] = int(show_values[1])  # convert rank to int
        show_values[4] = int(show_values[4])  # convert year to int
        show_values[7] = float(show_values[7])  # convert rating to float
        show_values[8] = int(show_values[8])  # convert rating count to int
        # now covert the list of values to a tuple to easy insertion into the database
        show_values = tuple(show_values)
        data_for_database.append(show_values)
    return data_for_database


def prepare_most_popular(top_show_data: list[dict]) -> list[tuple]:
    data_for_database = []
    for show_data in top_show_data:
        show_values = list(show_data.values())  # dict values is now an object that is almost a list, lets make it one
        # now we have the values, but several of them are strings and I would like them to be numbers
        # since python 3.7 dictionaries are guaranteed to be in insertion order
        show_values[1] = int(show_values[1])  # convert rank to int
        show_values[2] = rank_to_int(show_values[2])  # rank up down sometimes has bad data so handle it specially
        show_values[4] = int(show_values[5])  # convert year to int
        show_values[7] = rating_to_float(show_values[8])  # convert rating to float, some are '' and need to become 0
        show_values[8] = int(show_values[9])  # convert rating count to int
        # now covert the list of values to a tuple to easy insertion into the database
        show_values = tuple(show_values)
        data_for_database.append(show_values)
    return data_for_database

def rank_to_int(rank_val: str) -> int:
    try:
        real_rank = int(rank_val)
        return real_rank
    except ValueError:
        return 0


def rating_to_float(rating: str) -> float:
    try:
        real_rank = float(rating)
        return real_rank
    except ValueError:
        return 0


def get_big_movers(popular_movies: list[tuple]) -> list[tuple]:
    popular_movies.sort(key=get_sort_key, reverse=True)  # order the list by rankupdown with positive moves first
    big_movers = []
    big_movers.extend(popular_movies[:3])  # put the first three items from the sorted list into the final list
    big_movers.append(popular_movies[-1])  # put the last item from the sorted list into the final list
    return big_movers


def get_big_mover_ratings(big_movers: list[tuple]) -> list[tuple]:
    big_mover_rating_data = []
    for mover in big_movers:
        url = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{mover[0]}"  # the ttid is in position 0
        response = requests.get(url)
        if response.status_code != 200:
            print(f"response code for {mover[3]} came back : {response.status_code}")
            continue
        big_mover_rating_data.append(response.json())
    big_mover_rating_data = prepare_ratings_for_db(big_mover_rating_data)
    return big_mover_rating_data


def get_sort_key(item):
    if len(item) < 3:
        raise ValueError
    return item[2]  # rank up down is in index 2 of the tuple

def make_zero_values() -> list[dict]:
    '''this is a kludge to deal with the fact that one record has no ratings data'''
    zero_rating = []
    for rating_value in range(10, 0, -1):
        rating = {}
        rating['rating'] = rating_value
        rating['percent'] = '0%'
        rating['votes'] = 0
        zero_rating.append(rating)
    return zero_rating

def _flatten_and_tuplize(ratings_entry: dict) -> tuple:
    db_ready_list = []
    db_ready_list.append(ratings_entry['imDbId'])
    db_ready_list.append(ratings_entry['title'])
    db_ready_list.append(ratings_entry['fullTitle'])
    db_ready_list.append(int(ratings_entry['year']))
    db_ready_list.append(int(ratings_entry['totalRating']))
    db_ready_list.append(int(ratings_entry['totalRatingVotes']))
    if not ratings_entry['ratings']:  # deal with #200 missing ratings
        ratings_entry['ratings'] = make_zero_values()
    for rating in ratings_entry['ratings']:
        # the first data is a percent and we need to remove the % then conver it to a float
        str_percent = rating['percent']
        str_percent = str_percent[:-1]  # slice with all but the last character
        db_ready_list.append(float(str_percent))
        db_ready_list.append(int(rating['votes']))
    return tuple(db_ready_list)


def prepare_ratings_for_db(ratings: list[dict]) -> list[tuple]:
    data_for_database = []
    for ratings_entry in ratings:
        db_redy_entry = _flatten_and_tuplize(ratings_entry)
        data_for_database.append(db_redy_entry)
    return data_for_database

def setup_top250_TV_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_show_data(
    ttid TEXT PRIMARY KEY,
    rank INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    imdb_rating REAL,
    imdb_rating_count INTEGER);''')

def setup_Most_popular_TV_show_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS most_popular_shows(
    ttid TEXT PRIMARY KEY,
    rank INTEGER,
    rankUpDown INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    imdb_rating REAL,
    imdb_rating_count INTEGER);''')

def setup_most_popular_movie_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS most_popular_movie(
    ttid TEXT PRIMARY KEY,
    rank INTEGER,
    rankUpDown INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    imdb_rating REAL,
    imdb_rating_count INTEGER);''')

def setup_top250movie_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_250_movie(
        ttid TEXT PRIMARY KEY,
        rank INTEGER DEFAULT 0,
        title TEXT,
        fulltitle TEXT,
        year INTEGER,
        image_url TEXT,
        crew TEXT,
        imdb_rating REAL,
        imdb_rating_count INTEGER);''')


def setup_ratings_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS show_ratings(
        ratings_key INTEGER PRIMARY KEY,
        imdb_ttcode TEXT NOT NULL,
        title TEXT,
        fulltitle TEXT,
        year INTEGER,
        total_rating INT DEFAULT 0,
        total_votes INTEGER,
        rating10_percent REAL,
        rating10_votes INTEGER,
        rating9_percent REAL,
        rating9_votes INTEGER,
        rating8_percent REAL,
        rating8_votes INTEGER,
        rating7_percent REAL,
        rating7_votes INTEGER,
        rating6_percent REAL,
        rating6_votes INTEGER,
        rating5_percent REAL,
        rating5_votes INTEGER,
        rating4_percent REAL,
        rating4_votes INTEGER,
        rating3_percent REAL,
        rating3_votes INTEGER,
        rating2_percent REAL,
        rating2_votes INTEGER,
        rating1_percent REAL,
        rating1_votes INTEGER,
        FOREIGN KEY (imdb_ttcode) REFERENCES top_show_data (ttid)
        ON DELETE CASCADE ON UPDATE NO ACTION
        );''')


def populate_top_250tv_show(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO top_show_data(ttid, rank, title, fulltitle, year, image_url, crew, imdb_rating,
        imdb_rating_count)
        VALUES(?,?,?,?,?,?,?,?,?)""", data_to_add)

def populate_top_250_movie(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO top_250_movie(ttid, rank, title, fulltitle, year, image_url, crew, imdb_rating,
        imdb_rating_count)
        VALUES(?,?,?,?,?,?,?,?,?)""", data_to_add)

def put_in_wheel_of_time(db_cursor: sqlite3.Cursor):
    """this is just a total kludge. I need a Wheel of time Entry for the foreign key to work, so I'm just adding it"""
    db_cursor.execute("""INSERT INTO top_show_data(ttid, rank, title, fulltitle, year, image_url, crew, imdb_rating, imdb_rating_count)
    VALUES('tt7462410',0,'The Wheel of Time','The Wheel of Time (TV Series 2021– )',2021,'','Rosamund Pike, Daniel Henney',
    7.2,85286)""")


def populate_rating(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO show_ratings(imdb_ttcode, title, fulltitle, year, total_rating, total_votes,
        rating10_percent,
        rating10_votes, rating9_percent, rating9_votes, rating8_percent, rating8_votes, rating7_percent, rating7_votes,
        rating6_percent, rating6_votes, rating5_percent, rating5_votes, rating4_percent, rating4_votes, rating3_percent,
        rating3_votes, rating2_percent, rating2_votes, rating1_percent, rating1_votes)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data_to_add)

def populate_most_popular_Movie_table(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO most_popular_movie(ttid, rank, rankUpDown, title, fulltitle, year, image_url, crew, imdb_rating,
        imdb_rating_count)
        VALUES(?,?,?,?,?,?,?,?,?,?)""", data_to_add)

def populate_most_popular_show_table(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO most_popular_shows(ttid, rank, rankUpDown, title, fulltitle, year, image_url, crew, imdb_rating,
        imdb_rating_count)
        VALUES(?,?,?,?,?,?,?,?,?,?)""", data_to_add)

def main():

    conn, cursor = open_db("project1_sprint2.sqlite")
    print(type(conn))
    setup_Most_popular_TV_show_table(cursor)
    setup_top250_TV_table(cursor)
    setup_most_popular_movie_table(cursor)
    setup_top250movie_table(cursor)
    setup_ratings_table(cursor)

    top_show_data = get_250_TV()
    top_250_movies = get_top_250_Movies()
    top_show_data_for_db = prepare_top_250_data(top_show_data)
    top_250_movies_for_db = prepare_top_250_data(top_250_movies)

    most_Popular_Movies = get_most_popular_movies()
    most_popular_tv = get_most_popular_TV()

    populate_top_250tv_show(top_show_data_for_db, cursor)
    populate_top_250_movie(top_250_movies_for_db, cursor)
    populate_most_popular_show_table(most_popular_tv, cursor)
    populate_most_popular_Movie_table(most_Popular_Movies, cursor)
    put_in_wheel_of_time(cursor)
    big_mover_records = get_big_movers(most_Popular_Movies)
    big_mover_ratings = get_big_mover_ratings(big_mover_records)
    ratings_data = get_ratings(top_show_data)
    db_ready_ratings_data = prepare_ratings_for_db(ratings_data)
    populate_rating(db_ready_ratings_data, cursor)
    populate_rating(big_mover_ratings, cursor)
    close_db(conn)


    app = guiWindow.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

