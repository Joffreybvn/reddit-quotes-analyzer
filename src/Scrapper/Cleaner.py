
from src.Scrapper import Saver

import re
import pandas as pd
from datetime import datetime
from pandas import DataFrame
from typing import Union


class Cleaner:

    def __init__(self, raw_data: DataFrame):
        """Format the raw data to clean and useful quotes."""

        self.df: DataFrame = raw_data

    def clean(self):
        self.__create_quote_author()
        self.__transform_date()

        self.__sanitize_dataframe()
        Saver(self.df).save()

    def __sanitize_dataframe(self):

        # Drop the row with missing quote
        self.df.dropna(how='any', subset=['quote'], inplace=True)

        # Fill the missing author with 'Unknown'
        self.df['author'] = self.df['author'].fillna(value='Unknown')

        # Reset the index and re-arrange the columns
        self.df = self.df.reset_index(drop=True)
        self.df = self.df[['date', 'quote', 'author', 'id', 'comments', 'up_votes', 'post_author']]

    def __create_quote_author(self):
        """
        Retrieve the quote text and author from the dataframe, and
        update the dataframe with theses new data.
        """

        formatted = self.df['title'].apply(lambda title: pd.Series({

            # Apply the following function to the 'title' Series,
            # save the result in a new dataframe with "quote" and "author"
            # columns.
            'quote': self.__retrieve_quote(title),
            'author': self.__retrieve_author(title)
        }))

        # Append the formatted quote to the dataframe, and remove the 'title'.
        self.df = pd.concat([self.df, formatted], axis=1)
        self.df.drop(columns=['title'], inplace=True)

    def __retrieve_author(self, title) -> Union[str, None]:
        """Retrieve and return the author from a given post title."""

        author = self.__regex_search(title, r'[-―—](?P<value>.*)$')

        if author:
            return self.sanitize_author(author)

        return None

    @staticmethod
    def sanitize_author(text: str) -> Union[str, None]:
        text = text.capitalize().strip()

        if len(text) < 45:
            return text

        return None

    def __retrieve_quote(self, title) -> Union[str, None]:
        """Retrieve and return the quote from a given post title."""

        quote = self.__regex_search(title, r'[“”"\'](?P<value>.*)[“”"\']')

        if quote:
            return self.sanitize_quote(quote)

        return None

    @staticmethod
    def sanitize_quote(text: str) -> str:
        return re.sub(r'[“”"\']+', '', text).strip()

    @staticmethod
    def __regex_search(text, regex) -> Union[str, None]:
        """Apply a given regex to search value in a given text."""

        # Search in the text.
        result = re.search(regex, text, re.DOTALL)

        # Return the result.
        if result:
            return result.group('value')

        return None

    def __transform_date(self):
        self.df['date'] = self.df['date'].apply(lambda date: datetime.fromtimestamp(date))
