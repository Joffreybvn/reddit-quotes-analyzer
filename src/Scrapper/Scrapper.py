
from src.Scrapper import Reddit
from typing import Iterator
import pandas as pd


class Scrapper:

    def __init__(self):
        """Scrape the Reddit API and return it's result to the Cleaner."""
        self.subreddit = Reddit().get_subreddit('quotes')
        self.quotes = pd.DataFrame(columns=['date', 'id', 'title', 'up_votes', 'comments', 'post_author'])

    def __get_submissions(self) -> Iterator:
        """Query the Reddit API and return a generator with the results."""

        # Query the API and return a generator.
        return self.subreddit.new(limit=1000)

    def __scrape(self):
        """Retrieve the data from the API and format it."""

        # Loop through all submission and format the data into a list.
        for post in self.__get_submissions():

            fields = [
                post.created_utc,
                post.id,
                post.title,
                post.upvote_ratio,
                post.num_comments,
                post.author
            ]

            # Append the data to the DataFrame.
            self.quotes.loc[len(self.quotes)] = fields

    def get_data(self):
        """Return the data scrapper from  Reddit."""

        # Scrape Reddit if it wasn't done yet.
        if not len(self.quotes):
            self.__scrape()

        return self.quotes
