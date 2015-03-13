import praw
import cPickle as pickle

from sys import argv



# only keep necessary info for pickling
class CommentLite(object):

  def __init__(self, praw_comment_obj=None):
    c = praw_comment_obj
    
    if c:
      if c.author:      
        self.author = c.author.name
      else:
        self.author = "[deleted]"
      self.body = c.body
      self.id = c.name
      self.created_utc = c.created_utc
      self.parent_id = c.parent_id
    else:
      self.author = None
      self.body = None
      self.id = None
      self.created_utc = None
      self.parent_id = None
      
    
  def as_dict(self):
    return self.__dict__
  
  @staticmethod
  def fromthread(thread):
    com = CommentLite()
    com.author = 'THREAD_ROOT'
    com.body = thread.title
    com.id = thread.name
    com.created_utc = thread.created_utc
    return com


### comment preparation pipeline ###

# flatten comment tree
flat = lambda comments: praw.helpers.flatten_tree(comments)

# filter out MoreComments objects
filt = lambda comments: [c for c in comments if c.__class__.__name__ != 'MoreComments']

# convert praw comment objects to CommentLite objects
lite = lambda comments: [CommentLite(c) for c in comments]

# sort by time created (newest first)
sort = lambda comments: sorted(comments, key=lambda c: -c.created_utc)

# all of the above
prep = lambda comments: sort(lite(filt(flat(comments))))



if __name__=="__main__":
  R = praw.Reddit('Testing for comment ranking algorithm research -- amstocker@dons.usfca.edu')
  
  thread_id = argv[1]
  thread = R.get_submission(submission_id=thread_id)
  
  comments = prep(thread.comments)
  comments = sort(comments + [CommentLite.fromthread(thread)])  # add thread root as comment
  
  pklfile = "{}.pkl".format(thread_id)
  
  print "dumping comments into {} ...".format(pklfile)
  pickle.dump( comments, open(pklfile,'wb') )
  
  
