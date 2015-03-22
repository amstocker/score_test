"""
Parse comment trees from all pickled threads in cwd
"""
import os
import numpy as np
from scorer import tree_from_id

# get file name/extension
file_ext = lambda f: f.split('.')


def score_all(submission_ids):
  return [tree_from_id(t_id) for t_id in submission_ids]
  


def corr_all(trees):
  from scipy.stats import pearsonr as corr
  
  tscores_all = np.array([])
  rscores_all = np.array([])
  
  for tree in trees:
    tscores, rscores = tree.scores()
    
    # mask out bigtree leaf nodes (which will have a score of zero),
    #  because leaves don't take into account upvotes in bigtree model
    mask = tscores>0
    tscores = tscores[mask]
    rscores = rscores[mask]
    
    # normalize by max score
    tscores /= np.max(tscores)
    rscores /= np.max(rscores)
    
    tscores_all = np.concatenate(( tscores_all, tscores ))
    rscores_all = np.concatenate(( rscores_all, rscores ))
  
  return corr(tscores_all, rscores_all)
  
  

if __name__=="__main__":
  
  # get pickle files from current directory
  pkls = filter(
    lambda f: file_ext(f)[1] == 'pkl',
    [f for f in os.listdir('.') if os.path.isfile(f)]
  )
  
  submission_ids = [file_ext(pkl)[0] for pkl in pkls]
  
  
  trees = score_all(submission_ids)
  
  # average correlation of each scoring methods per thread
  print np.average([t.score_correlation() for t in trees])
  
  # correlation of scoring methods for all scraped threads
  print corr_all(trees)
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
