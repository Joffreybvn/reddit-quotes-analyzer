
import praw
from praw.models import Subreddit
from os import environ


class Reddit:

    def __init__(self):
        """Create a Reddit API Wrapper (PRAW)."""

        # Create the API wrapper.
        self.agent = praw.Reddit(
            client_id=environ.get('REDDIT_ID'),
            client_secret=environ.get('REDDIT_SECRET'),
            user_agent="Reddit Quotes Analyzer 1.0 by /u/Joffreybvn github.com/Damgaard/Reddit-Bots/"
        )

    def get_subreddit(self, subreddit_name: str) -> Subreddit:
        """Assign a given subreddit as the subreddit to connect."""

        return self.agent.subreddit(subreddit_name)
