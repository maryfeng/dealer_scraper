import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_reviews(URL, start_page, end_page):
    """
    Scrapes reviews from start_page to end_page

    :param URL: str
        base to scraping reviews from
    :param start_page: int
        page to start scraping reviews, inclusive
    :param end_page: int
        page to stop scraping reviews, inclusive

    :return: dict of reviews in which the
        keys are (reviewer, dates, review text)
        values are the sum of the star ratings
    """
    reviews = {}
    for page_index in range(start_page, end_page + 1):
        print(f"Scraping page {page_index}...")
        page = requests.get(f"{URL}{page_index}")
        results = BeautifulSoup(page.content, "html.parser").find(id="reviews")
        authors = results.find_all("span", class_="italic font-18 black notranslate")
        dates = results.find_all(
            "div", class_="italic col-xs-6 col-sm-12 pad-none margin-none font-20"
        )
        stars = results.find_all(
            "div",
            class_="table width-100 pad-left-none pad-right-none margin-bottom-md",
        )
        texts = results.find_all(
            "p", class_="font-16 review-content margin-bottom-none line-height-25"
        )
        for i, review in enumerate(stars):
            ratings = review.select('div[class*="rating"]')
            # for the rating, we simply take the sum of the star ratings
            rating_sum = sum(
                map(int, (elt["class"][1].split("-")[1][0] for elt in ratings))
            )
            reviews[
                (authors[i].get_text()[2:], dates[i].get_text(), texts[i].get_text())
            ] = rating_sum
    return reviews


def add_sentiment(reviews):
    """
    To break ties, adds a value for overall sentiment based on review text

    :param reviews: dict
        reviews dict in structure from get_reviews()
    """
    analyzer = SentimentIntensityAnalyzer()
    for review in reviews:
        reviews[review] += analyzer.polarity_scores(review)["compound"]


def display_top_reviews(reviews, num_reviews):
    """
    Sorts and displays the top reviews in descending order

    :param reviews: dict
        reviews dict in structure from get_reviews()
    :param num_reviews: int
        number of top reviews to display
    """
    print("\n-------------------------- \nTop Reviews\n")
    top_reviews = sorted(reviews.items(), key=itemgetter(1), reverse=True)[:num_reviews]
    for r, review in enumerate(top_reviews):
        print(
            f"Top review {r+1}\nScore {review[1]} | Submitted by {review[0][0]} on {review[0][1]}"
        )
        print(review[0][2])
        print()


if __name__ == "__main__":
    URL = "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page"
    reviews = get_reviews(URL, 1, 5)
    add_sentiment(reviews)
    display_top_reviews(reviews, 3)
