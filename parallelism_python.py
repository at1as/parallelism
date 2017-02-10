import datetime
import time
import threading
from   multiprocessing import Pool
import os


def long_function(id):
  print "Starting Job ID : {}. OS Process PID : {}".format(id, os.getpid())
  time.sleep(4)
  print "Done Job ID : {}. OS Process PID : {}".format(id, os.getpid())


def synchronous():
  """
  The base iterative solution in which 
  """
  start = datetime.datetime.now()
  print ">> Starting loop (process id {})".format(os.getpid())

  for x in range(10):
    long_function(x)

  stop = datetime.datetime.now()
  print ">> Loop complete (process id {})".format(os.getpid())
  print ">> Runtime: {}".format(stop - start)


def threaded():
  """
  Run with threads. Due to Python's Global Interpreter lock, the below does not happen in parallel,
  but rather each function is rapidly switched into and out of, even before they have returned

  Why does the printed output look so poorly formatted? The 'print' method is not thread safe.
  Should surround print statements by a lock

    Starting Job ID : 0. OS Process PID : 23783Starting Job ID : 1. OS Process PID : 23783

    Starting Job ID : 3. OS Process PID : 23783
    Starting Job ID : 2. OS Process PID : 23783
  """
  start = datetime.datetime.now()
  print ">> Starting threads... (process id {})".format(os.getpid())

  threads = []
  for x in range(10):
    t = threading.Thread(target=long_function, args=(x,))
    threads.append(t)

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()

  stop = datetime.datetime.now()
  print ">> All threads complete (process id {})".format(os.getpid())
  print ">> Runtime: {}".format(stop - start)


def multiprocess_with_limit():
  """
  Run each function call in a separate system process
  Will spawn set number of processes below and reuse them as 
  """ 
  start = datetime.datetime.now()
  print ">> Starting processes (process id {})".format(os.getpid())

  processes = 4
  pool = Pool(processes=processes)
  pool.map(long_function, range(10))
  
  stop = datetime.datetime.now()
  print ">> All processes complete (process id {})".format(os.getpid())
  print ">> Runtime: {}".format(stop - start)


def multiprocess_high_limit():
  """
  Run each function call in a separate system process
  Will spawn set number of processes below and reuse them as 
  """ 
  start = datetime.datetime.now()
  print ">> Starting processes (process id {})".format(os.getpid())

  processes = 10
  pool = Pool(processes=processes)
  pool.map(long_function, range(10))
  
  stop = datetime.datetime.now()
  print ">> All processes complete (process id {})".format(os.getpid())
  print ">> Runtime: {}".format(stop - start)

if __name__ == "__main__":
  synchronous()
  print "\n\n\n\n"
  threaded()
  print "\n\n\n\n"
  multiprocess_with_limit()
  print "\n\n\n\n"
  multiprocess_high_limit()
