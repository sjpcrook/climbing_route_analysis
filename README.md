# A python script to analyse a dataframe of climbing routes across the world and return plots depicting their location. It can also find trends in the grade and rating.



### Discussing the Dataset

# Our dataset 

## Route

# Bikini Amber
# The name of the route, stored as a string. Since these names are submitted by users and the routes are found worldwide, multiple routes can share the same name, so if you wanted to specify a certain route you may also have to refer to its location

## Location

# Upper Tier > Nameless Bay > Cheddar Gorge North > Cheddar Gorge > South West > England > United Kingdom > Europe > International
# The location of the route described by which city, country etc. it is found in. 

## URL

# https://www.mountainproject.com/route/109264385/bikini-amber
# A link to the Mountain Project page about this route, stored as a string. Whilst this uniquely identifies each route, it is not ideal to use for filtering. Its primary use is to find additional information about a given route if desired.

## Description

# A little gem of a route~ hidden out of the way of the crowds far below. The rock is immaculate~ the moves are a perfect balance of delicate and dynamic; the only problem is the indistinct line at the top. The crux is negotiating the slight groove around bolt 3~ and has several solutions making various use of a good hold on the left and a good pocket to the right.
# A description of the route submitted by a user, stored as a string. It uses "~" in place of ",". This may be useful to generate a wordcloud seeing what words appear the most in descriptions and whether these words imply the route is good/bad or easy/hard.

## Avg_Stars
# 2.0
# The average number of stars the route has recieved, ranging from 0 to 4, stored as a float.

## Route_Type
# Sport
#

## Rating
# 5.12a
#

## Pitches
# 1
# 

## Length
# 50.0

## Area_Latitude
# 51.28513

## Area_Longitude
# -2.76345

## Protection
# 5 bolts~ 2-bolt lower-off with rings.

## Num_Votes
# 1

