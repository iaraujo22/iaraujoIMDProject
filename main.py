# Ivanildo Araujo (Ivan)
# COMP 490-001
import unittest.result
# comment to test workflow
import requests
import secrets


def get_250_televisionShows():
    location1 = f"https://imdb-api.com/api/{secrets.secre_key}/tt7462410"
    result = requests.get(location1)
    if result.status_code != 200:
        print("Help!")
        return
    data = result.json()
    with open('data.txt', 'w') as f:
        f.write(data)


def user_ratings():
    location2 = f"https://imdb-api.com/api#UserRatings-header/{secrets.secre_key}/tt7462410"
    results = requests.get(location2)
    if results.status_code != 200:
        print("Help!")
        return
    data = results.json()
    with open('data.txt', 'w') as f:
        f.write(data)


if __name__ == '__main__':
    get_250_televisionShows()
    user_ratings()
