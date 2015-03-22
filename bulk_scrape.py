"""
Scrape all threads from a given subreddit (first arg)
"""
import praw
from scraper import get_reddit_client, pkl_thread

from sys import argv


def bulk_scrape(submissions):
  [pkl_thread(t) for t in submissions]


if __name__=="__main__":
  R = get_reddit_client()
  
  subreddit_id = argv[1]
  
  submissions = [s for s in R.get_subreddit(subreddit_id).get_hot(limit=200)]
  
  bulk_scrape(submissions)
  
