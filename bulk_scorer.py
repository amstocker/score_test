"""
Parse comment trees from all pickled threads in cwd
"""
import os
import numpy as np
from scorer import CommentTree

from time import time


def score_all(submission_ids):
  trees = [CommentTree.from_id(t_id) for t_id in submission_ids]
  
  # update scores to current time
  cur = time()
  [t._calc_scores(cur) for t in trees]
  
  return trees 
  


def correlation_all(trees):
  from scipy.stats import pearsonr as corr
  
  tscores_all = np.array([])
  rscores_all = np.array([])
  
  for tree in trees:
    tscores, rscores = tree.scores()
    
    tscores_all = np.concatenate(( tscores_all, tscores ))
    rscores_all = np.concatenate(( rscores_all, rscores ))
  
  return corr(tscores_all, rscores_all)
  
  

if __name__=="__main__":

  file_ext = lambda f: f.split('.')
  
  # get pickle files from current directory
  pkls = filter(
    lambda f: file_ext(f)[1] == 'pkl',
    [f for f in os.listdir('.') if os.path.isfile(f)]
  )
  
  submission_ids = [file_ext(pkl)[0] for pkl in pkls]
  
  
  trees = score_all(submission_ids)
  
  
  # individual correlation of each scoring methods per thread
  indiv = filter(lambda t: (not np.isnan(t[0])), [t.score_correlation() for t in trees])
  
  # correlation of scoring methods for all scraped threads
  print correlation_all(trees)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
