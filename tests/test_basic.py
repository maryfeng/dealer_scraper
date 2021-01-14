from dealer_scraper.dealer_scraper import get_reviews, add_sentiment
from calendar import month_name


def test_get_reviews():
    URL = "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page"
    reviews = get_reviews(URL, 1, 1)
    months = set([month_name[m] for m in range(1, 13)])

    assert len(reviews) == 10
    for i, review_info in enumerate(reviews):
        # check authors exist
        assert len(review_info[0]) > 0

        # check dates
        date = review_info[1].split()
        assert date[0] in months
        assert int(date[1][:-1]) in range(1, 32)
        # apparently dealerrater.com was founded in 2002
        assert int(date[2]) in range(2002, 2022)

        assert len(review_info[2]) > 0
    return reviews


def test_add_sentiment():
    URL = "https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page"
    reviews = get_reviews(URL, 1, 1)
    ratings_before = sum(reviews.values())
    add_sentiment(reviews)
    ratings_after = sum(reviews.values())
    assert ratings_after > ratings_before
