import cPickle as pickle
from copy import deepcopy
from pprint import pprint

import os
import numpy as np
from sys import argv
from scraper import CommentLite


# represents a comment (node) on the comment tree
class Node(object):
  def __init__(self, comment):
    self.comment = comment
    self.depth = 0
    self.score = 0.
    self.tree_size = 0
    self.children = []
    
  def __repr__(self):
    return "[{:.3f},\t{},\t{},\t{},\t{}]".format(self.score, self.comment.created_utc, self.depth, self.comment.author, self.comment.body[:30])


class CommentTree(object):

  def __init__(self, comments):
    self._comments = deepcopy(comments)
    self._tree = {}
    self._root_id = self._comments[-1].id  # last "comment" is actually thread root
    self._root_created_utc = self._comments[-1].created_utc
    self.populate()
      
     
  def populate(self, prompt=False):
    comments = deepcopy(self._comments)
    
    root = comments.pop()
    self._tree = {}
    self._tree[root.id] = Node(root)  # set thread root
    
    # loop through the timeline of the thread
    while len(comments)>0:
    
      # clear terminal
      if prompt: os.system('cls' if os.name == 'nt' else 'clear')
      
      com = comments.pop()
      node = Node(com)
      
      self._tree[com.id] = node
      self._tree[com.parent_id].children.append(node)
      
      # trace depth of comment relative to thread root
      depth = 0
      
      # traverse up tree and increment tree size counts
      parent_id = com.parent_id
      while parent_id != None:
        depth += 1
        parent = self._tree[parent_id]
        parent.tree_size += 1
        parent_id = parent.comment.parent_id
      
      node.depth = depth
      
      # update all scores
      self._calc_scores(com.created_utc)
      
      if prompt:
        self.show()
        raw_input("\n\n\n\n\nEnter to continue...")
  
  
  def _calc_scores(self, current_utc):
    for _id, node in self._tree.items():
      if node.tree_size == 0: continue
      
      dt = (current_utc - node.comment.created_utc) / 3600
      node.score = node.tree_size / dt
  
  
  def show(self, hide_low=False):
    dt_min = lambda n: int((n.comment.created_utc-self._root_created_utc)/60)
    node_fmt = lambda n: "-->[{:.3f}, {}, {}]".format(n.score, dt_min(n), n.comment.author)
    
    def _helper(indent_level, root):
      for child in root.children:
        if hide_low and child.score>0: continue
        
        print indent_level*"\t" + node_fmt(child)
        print indent_level*"\t" + "   " + child.comment.body[:30]
        _helper(indent_level+1, child)
    
    if len(self._tree)>0: _helper(0, self._tree[self._root_id])
    
  
  def get_top(self, n = -1):
    top = sorted(self._tree.values(), key = lambda n: -n.score)
    return top[:n]
    
      



if __name__=="__main__":
  thread_id = argv[1]
  pklfile = "{}.pkl".format(thread_id)
  
  comments = pickle.load( open(pklfile,'rb') )
  
  
  tree = CommentTree(comments)
  tree.show()
  #tree.populate(prompt=True)
  
  print
  pprint( tree.get_top(20) )
  
    
    
  
  




