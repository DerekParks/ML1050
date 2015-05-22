# CalculateRating.py
#
# Estimates what a given user will rate a given movie

import urllib


class CalculateRating:
    """A Netflix movie rating estimator
    
    This classifier will take in a the ID of a movie and the ID of
    a user and estimate what the given user will rate the given movie.
    """
    
    def __init__(self):
        pass
    
    def getUsersViewed(self, movieID):
        """getUsersViewed(self, movieID)
        
        Method takes in a movie ID and will return a dictionary of
        users who have viewed the movie as keys, and their specific
        rating as values.
        """
        #declare dictionary
        movieDict = {}
        
        #convert movieID to string format
        movieString = "mv_"
        tempString = str(movieID)
        for i in range(7 - len(tempString)):
            movieString += "0"
        movieString += tempString
        
        #fetch movie from network
        # 'http://netflix.mines.edu.s3.amazonaws.com/training_set/'+movieString
        movieFile = urllib.urlopen("network_address_to_movie_directory" + movieString)
        
        #move past first line "movie ID)
        movieFile.next()
        
        #move iteratively through file and map users to ratings
        for line in f:
            tokens = string.split(",")
            movieDict[tokens[0]] = tokens[1]
            
        #return dictionary
        return movieDict
        
    
    def getMoviesViewed(self, userID):
        """getMoviesViewed(self, movieID)
        
        Method takes in a user ID and will return a dictionary of
        movies which the user has viewed as keys, and their specific
        rating as values
        """
        #declare dictionary
        usersMovieDict = {}

        # user file is in the form of uNum.txt: so for user 101 its u101.txt
        userString = "u%s.txt" % userID
        
        #fetch user file from network
        # 'http://netflix.mines.edu.s3.amazonaws.com/training_set/'+userString
        userFile = urllib.urlopen("network_address_to_user_file")
        
        #move iteratively through file and grab movie:rating pair
        for line in f:
            tokens = line.split(",")
            userMovieDict[tokens[0]] = tokens[1]
            
        #return dictionary
        return userMovieDict
    
    
    def calculateCorrelation(self, rating1, rating2):
        """calculateCorrelation(self, rating1, rating2)
        
        Method takes in two floats and calculates the correlation between the
        two users.  Right now it is based on the following formula:
        
        <difference in rating> ** 2
        """
        weight = (rating1 - rating2) ** 2
        return weight
    
    
    def getRatingOffset(self, User):
        """getRatingOffset(self, User)
        
        This method may or may not get used depending on the implementation.
        If it is implemented, all it will do is average the movie reviews of
        the user and return how much, numerically, that number differs from the
        value 3.
        """
        return 0
    
    
    
    def compareMovieTastes(self, primaryUserMoviesViewed, userMoviesViewed, primaryOffset, userOffset):
        """compareMovieTastes(self, primaryUserMoviesViewed, userMoviesViewed)
        
        Method takes in two dictionaries.  Each dictionary contains the movies
        viewed by an individual user (keys) and what the individual rated said
        movie (value).  The method returns a float which specifies how similar
        the two users movie tastes are.
        """
        #check each movie the primary user has viewed against each
        #movie the current user has viewed
        weight = 0
        for primaryMovie in primaryUserMoviesViewed.keys():
            for userMovie in userMoviesViewed.keys():
                #If both users have watched the same movie, find how much their votes correlate
                if(primaryMovie == userMovie):
                    primaryRating = primaryUserMoviesViewed[primaryMovie] + primaryOffset
                    userRating = userMoviesViewed[userMovie] + userOffset
                    weight += calculateCorrelation(primaryRating, userRating)
        return weight
    
    
    def rateMovie(self, primaryUserID, primaryMovieID):
        """getMoviesViewed(self, movieID)
        
        This is the actual method that needs to be called when a user
        desires to estimate a movie rating.  Method takes a user ID and
        a movie ID as its two parameters, respectively.
        """
        #declare variables - dictionary of userIDs mapped to weights, and
        #the estimated rating
        weights{}
        rating = 0;
        totalWeight = 0;
        
        #get all the users who have viewed this movie
        usersViewed = getUsersViewed(primaryMovieID)
        
        #get all the movies viewed by the primary user and their rating offset
        primaryUserMoviesViewed = getMoviesViewed(primaryUserID)
        primaryRatingOffset = getRatingOffset(primaryUserID)
        
        #find how much each user correlates to the primary user
        for userID in usersViewed.keys():
            userMoviesViewed = getMoviesViewed(userID)
            userRatingOffset = getRatingOffset(userID)
            userWeight = compareMovieTastes(primaryUserMoviesViewed, userMoviesViewed, primaryRatingOffset, userRatingOffset)
            weights[userID] = userWeight
            totalWeight += userWeight
        
        #Normalize each weight and add it to the final rating
        for userID in usersViewed.keys():
            rating += (weights[userID] / totalWeight) * usersViewed[userID]
        
        #normalize and discretize rating
        rating /= len(usersViewed)
        intRating = int(rating + .5)
        
        #print result
        print("Estimated rating of movie %d by user %d: %d (%f)",primaryMovieID, primaryUserID, intRating, rating)
        
    def __call__(self, primaryUserID, primaryMovieID):
        rateMovie(primaryUserID, primaryMovieID)
