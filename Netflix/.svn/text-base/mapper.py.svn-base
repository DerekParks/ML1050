#!/usr/bin/env python

import sys

# input is file of a movie, loop over to do all movies
# grab movie number...

movie = 0

# input comes from STDIN
for line in sys.stdin:
  # remove leading and trailing whitespace
  line = line.strip()
  
  entry = line.split(',')

  # beginning of the file, grab the movie number
  if len(entry) != 3:
    movie = line.split(':')[0]
    continue

  user = entry[0]
  rating = entry[1]
  
  # want to print out user\t movie\t rating
  print '%s\t%s\t%s' %(user, movie, rating)
