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
    self.score = 0.
    self.leaf_count = 0
    self.children = []


class CommentTree(object):

  def __init__(self, comments):
    self._comments = deepcopy(comments)
    self._tree = {}
    self._root_id = self._comments[-1].id
    self.populate()
      
     
  def populate(self, prompt=False):
    comments = deepcopy(self._comments)
    
    root = comments.pop()
    self._tree[root.id] = Node(root)  # set thread root
  
    while len(comments)>0:
      # clear terminal
      if prompt: os.system('cls' if os.name == 'nt' else 'clear')
      
      com = comments.pop()
      node = Node(com)
      
      self._tree[com.id] = node
      self._tree[com.parent_id].children.append(node)
      
      # percolate leaf count if more than a comment chain
      parent_id = com.parent_id
      if self._tree[parent_id].leaf_count > 0:
        while parent_id != None:
          self._tree[parent_id].leaf_count += 1
          parent_id = self._tree[parent_id].comment.parent_id
      else:
        self._tree[parent_id].leaf_count = 1
      
      self._calc_scores(com.created_utc)
      
      if prompt:
        self.show()
        raw_input("\n\n\n\n\nEnter to continue...")
  
  
  def _calc_scores(self, current_utc):
    for _id, node in self._tree.items():
      if node.leaf_count == 0: continue
      
      dt = (current_utc - node.comment.created_utc) / 3600
      node.score = np.exp( np.log( node.leaf_count ) / dt )
  
  
  def show(self, hide_low=False):
    node_fmt_str = "({}, {})"
    node_fmt = lambda n: node_fmt_str.format(n.comment.id, n.score)
    
    def _helper(indent_level, root):
      for child in root.children:
        if hide_low and child.score>0: continue
        
        print indent_level*"\t" + node_fmt(child)
        _helper(indent_level+1, child)
    
    if len(self._tree)>0: _helper(0, self._tree[self._root_id])
    
      



if __name__=="__main__":
  thread_id = argv[1]
  pklfile = "{}.pkl".format(thread_id)
  
  comments = pickle.load( open(pklfile,'rb') )
  
  
  tree = CommentTree(comments)
  tree.populate(prompt=True)
  
    
    
  
  




