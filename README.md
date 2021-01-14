# Scraping top reviews for McKaig Chevrolet Buick from DealerRater.com
This simple script 
1. scrapes the first five pages of reviews for the [McKaig Chevrolet Buick](https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685) dealership on [DealerRater.com](https://www.dealerrater.com/)
2. creates a dictionary of reviews with keys (author, review date, review text) with sum of review stars as values
3. adds an overall sentiment score using [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment) to break ties
4. displays the top three most positive reviews in descending order

## Usage
Assuming you're using Python 3,

`python dealer_scraper/dealer_scraper.py`

and for the simple tests,

`pytest`