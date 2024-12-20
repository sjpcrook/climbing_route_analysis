import pandas as pd
import sweetviz as sv
from matplotlib import pyplot as plt, colors
import numpy as np


df = pd.read_csv("mp_routes.csv")
# df.info() #*Amounts and type of each variable


#* SIMPLE CLEANING - Dropping null rows, renaming columns for ease, dropping unused index column
df = df.dropna(how="any")
df = df.rename(columns={"Avg Stars":"Avg_Stars", "Route Type":"Route_Type", "Area Latitude":"Area_Latitude", "Area Longitude": "Area_Longitude", " desc":"Desc", " protection": "Protection", " num_votes":"Num_Votes"})
df = df.drop(columns=["Unnamed: 0"])

#* Makes our plots look nicer
plt.style.use("ggplot")

#! AS TAKEN FROM KAGGLE:
#? Route: The name of the route
#? Location: The location and sub-location of the route
#? URL: Link to the Mountain Project page about this route
#? Avg Stars: The average rating of a route
#? Route Type: Only sport and trad routes were scraped
#? Rating: How difficult the route is
#? Pitches: How many pitches the route is
#? Length: How tall/long the route is
#? Area Latitude/Longitude: GPS coordinates of the route
#? desc: Description of the route
#? protection: What gear is needed to climb the route
#? num_votes: How many people have voted on the quality of a route

# print(df.describe()) #*Means, medians of floats/ints


# print(df[df.duplicated()]) #*There are 0 duplicates in this dataset
df = df.query("Pitches >= 0")
df = df.query("Length >= 0")
df = df.drop(columns=["URL", "Desc"])

def first_word(string):
    '''
    Returns the first word of a string

    Parameters
    --------
    string : string
        The string you want to find the first word of
    Returns
    --------
    first : string
        The first word of the string
    '''
    first = string.split()[0]
    return(first)

df["Rating"] = df["Rating"].apply(first_word) #*Isolates the grade of the climb to 5.11a, 5.9 etc
boolean_list = df["Rating"].isin(["3rd", "4th", "5th", "6th", "Easy", "Medium", "Hard"]) #*Removes grades of a different scale
boolean_list = [not elem for elem in boolean_list]
df = df[boolean_list]

# df.info()
# df = df.query("Pitches > 1")

# report = sv.analyze(df)
# report.show_html()
# print(df.describe())
rating_conversion = {"a":0, "b": 2/7, "c": 4/7, "d": 6/7, "+": 1/3, "-":-1/3} #* Converts the sub-grades into numerics


def grade_conversion(grade):
    '''
    Converts the grade into a decimal for comparison
    
    Parameters
    --------
    grade : string
        The grade of the climb by the USA scale (eg. 5.9+))
    Returns
    --------
    grade : float
        The grade of the climb as a float (eg. 5.933)
    '''
    grade = grade[2:]
    decimal = 0
    if len(grade.split("/"))>1:
        decimal = rating_conversion[(grade[-1])] - 1/8
        grade = 500.0 + float(grade[:2]) + decimal
    elif len(grade) == 3:
        decimal = rating_conversion[((grade[-1]))]
        grade = 500.0 + float(grade[:2]) + decimal
    elif len(grade) == 2:
        if grade[-1] in rating_conversion:
            decimal = rating_conversion[((grade[-1]))]
        grade = 500.0 + float(grade[0]) + decimal
    else:
        grade = 500.0 + float(grade)    
    # print(grade)
    return(grade)

def outlier_remover(df, column):
    '''
    A function to remove outliers according to the interquartile range
    
    Parameters
    --------
    df : pd.DataFrame
        The dataframe you wish to modify
    column : string
        The name of the column you wish to remove outliers from 
    Returns
    --------
    df : pd.DataFrame
        A modified dataframe
    '''
    print(f"Before : The maximum {column} is {df[column].max()} and the minimum is {df[column].min()}")
    series = df[column]
    length = len(series)
    iqr = series[round(length*0.75)]-series[round(length*0.25)]
    lb = series[round(length*0.25)] - (1.5*iqr)
    print(f"lb = {lb}")
    ub = series[round(length*0.75)] + (1.5*iqr)
    print(f"ub = {ub}")
    df = df[lb<=df[column]]
    df = df[ub>=df[column]]
    print(f"After : The maximum {column} is {df[column].max()} and the minimum is {df[column].min()}")
    return(df)

df["Rating"] = df["Rating"].apply(grade_conversion)
# print(df["Rating"].value_counts())
# # #* A scatter plot showing the locations of all climbing routes. Would be good to overlay this with a map of the world. You can clearly see the outline of some continents.
# cmap = plt.cm.RdYlGn
# norm = colors.Normalize()
# plt.scatter(df["Area_Longitude"], df["Area_Latitude"], s=0.05, color = cmap(norm(df["Avg_Stars"].values)))
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Where Climbing Routes Can Be Found Across The World")
# plt.show()

df = outlier_remover(df, "Length")
# df = outlier_remover(df, "Pitches")



plt.scatter(df["Rating"], df["Avg_Stars"], s=0.3, color="blue")
plt.xlabel("Difficulty")
plt.ylabel("Stars")
plt.title("Comparing difficulty and stars")
m,c = np.polyfit(df["Rating"], df["Avg_Stars"], 1)
print(f"The equation for line of best fit is y = {m} x + {c}")
plt.plot(df["Rating"], m*df["Rating"]+c, color = "red")
plt.show()

plt.scatter(df["Length"], df["Avg_Stars"], s=0.3, color="blue")
plt.xlabel("Length")
plt.ylabel("Stars")
plt.title("Comparing length and stars")
m,c = np.polyfit(df["Length"], df["Avg_Stars"], 1)
print(f"The equation for line of best fit is y = {m} x + {c}")
plt.plot(df["Length"], m*df["Length"]+c, color = "red")
plt.show()


plt.scatter(df["Pitches"], df["Avg_Stars"], s=0.3, color="blue")
plt.xlabel("Pitches")
plt.ylabel("Stars")
plt.title("Comparing pitches and stars")
m,c = np.polyfit(df["Pitches"], df["Avg_Stars"], 1)
print(f"The equation for line of best fit is y = {m} x + {c}")
plt.plot(df["Pitches"], m*df["Pitches"]+c, color = "red")
plt.show()







