#!/usr/bin/env python

from __future__ import with_statement
from operator import itemgetter
import sys

# hash on user number, value is movie,rating
usersInfo = {}

for line in sys.stdin:
  line = line.strip()

  # parse the input we get from mapper.py
  user, movie, rating = line.split('\t')

  # leave movie/rating as string, change user to int
  try:
    #user = int(user)
    value = movie + "," + rating
    # get the previous userValues
    userVals = usersInfo.get(user)
    if userVals is None:
      usersInfo[user] = [value]
    else:
      usersInfo[user] = userVals.append(value)
  except ValueError:
    pass

# write the results to one file per user
for user in usersInfo:
  # print out user with all sets of values
  # file is in format:   u1.txt for user 1, u101.txt for user 101
  # movie,rating
  filename = 'u%s.txt' % user
  with file(filename, 'a') as f:
    for v in usersInfo[user]:
      f.write("%s\n" % v)
  # end writing to file, with does the close for us
# end for loop


  
  
