import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def get_web_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def get_movie_data(movie_element):
    title = movie_element.find("h3").text.strip()
    title = re.sub(r'(^\d+\.\s)', '', title)

    year = int(movie_element.select_one("div.cli-title-metadata > span").text)

    rating = movie_element.select_one("div.cli-ratings-container > span").text
    rating = float(rating.split("\xa0")[0])

    return {"title": title, "year": year, "rating": rating}


def main():
    url = "https://www.imdb.com/chart/top"
    content = get_web_content(url)
    if content is None:
        print('Failed to retrieve web content')
        return

    soup = BeautifulSoup(content, "html.parser")
    movies_list = soup.find_all("li", {"class": "cli-parent"})
    movies = [get_movie_data(movie) for movie in movies_list]

    df = pd.DataFrame(movies)

    high_rated_movies = df[df["rating"] >= 9.0]
    sorted_movies = high_rated_movies.sort_values(by="rating", ascending=False)
    print(sorted_movies)

    df.to_csv("imdb_movies.csv", index=False)


if __name__ == "__main__":
    main()
