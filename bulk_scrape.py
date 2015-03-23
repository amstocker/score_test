"""
Scrape all threads from a given subreddit (first arg)
"""
import praw
from scraper import get_reddit_client, pkl_thread

from sys import argv


def bulk_scrape(submissions):
  for t in submissions:
    pkl_thread(t)


if __name__=="__main__":
  R = get_reddit_client()
  
  subreddit_id = argv[1]
  limit = int(argv[2])
  
  submissions = R.get_subreddit(subreddit_id).get_hot(limit=limit)
  
  bulk_scrape(submissions)
  
