import pandas as pd
import sweetviz as sv
from matplotlib import pyplot as plt, colors
import numpy as np
import nltk
#from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')
from wordcloud import WordCloud
from PIL import Image
import string
import random

# nltk.download("stopwords")
# print(stopwords.words("english"))

df = pd.read_csv("outputted_df.csv")
names = ""
for i in df["Route"]:
    names = names + " " + i
# print(names)




# translator = str.maketrans('', '', string.punctuation)
# j = 0
# dictionary = {}
# temp_descs = ""
# with open("descriptions.txt", "w", encoding="utf-8") as f:
#     f.write("")
# for i in df["Description"]:
#     i = i.translate(translator)
#     # print(j)
#     with open("descriptions.txt", "a", encoding="utf-8") as f:
#         f.write(i+"\n")
#     for word in i.lower().strip().split() :
#         if dictionary.get(word) == None:
#             dictionary[word] = [1, df.iloc[j, 2]]
#         else:
#             dictionary[word] = [dictionary[word][0]+1, dictionary[word][1]+df.iloc[j, 2]]
#     j=j+1
# # print(descs_ts)
# # print(dictionary)

# def long_word(word):
#     if len(word)>2:
#         return True
#     else:
#         return False
# word_df = pd.DataFrame(dictionary).T
# # print(word_df)
# word_df = word_df.rename(columns={0: "Frequency", 1 : "Score"})
# # print(word_df)
# word_df = word_df[word_df["Frequency"] >= 50]
# word_df["Words"] = word_df.index
# word_df = word_df[word_df["Words"].apply(long_word)]
# word_df = word_df.drop(columns=["Words"])
# # print(word_df)
# word_df["Score"] = word_df["Score"]/word_df["Frequency"]
# word_df.to_csv("word_score_df.csv")


with open("descriptions.txt", 'r', encoding="utf-8") as file:
    descs = file.read()


word_df = pd.read_csv("word_score_df.csv")
word_df = word_df.set_index("Word")

# print(word_df)
word_df = word_df.sort_values(by="Score")
# print(word_df.head(10))
word_df = word_df.sort_values(by="Score", ascending=False)
# print(word_df.head(10))
all_words = list(word_df.index)

def word_checker(df, word):
    ind = list(df.index)
    if word in ind:
        return True
    else:
        return False
                       
steepness = ["slab", "vertical", ["overhang", "overhung"], "ceiling"]
stones = ["limestone", "granite", "sandstone", "slate", ["quartz", "quartzite"], "basalt"]
holds = [["jug", "bucket", "jugs", "buckets"], ["edge", "ledge", "edges", "ledges"], ["crimp", "crimps", "crimpy"],
        ["pinch", "pinches"], ["sloper", "slopers"], ["pocket", "pockets"], ["undercling", "underclings"],
        ["flake", "flakes"], ["horn", "horns"], ["crack", "cracks"]]
def word_search(df, words):
    new_df = pd.DataFrame(columns = ["Word", "Frequency", "Score"])
    for i in words:
        if isinstance(i, list):
            freq = 0
            score = 0
            for j in i:
                if j in all_words:
                    freq = freq + df["Frequency"].loc[j]
                    score = score + df["Frequency"].loc[j]*df["Score"].loc[j]
                else:
                    print(f"Warning: {j} not in dataframe")
            if freq != 0:
                score = score/freq
                new_df = pd.concat([new_df, pd.Series({"Word":i[0], "Frequency":freq, "Score":score}).to_frame().T], ignore_index=True)
        else:
            if i in all_words:
                freq = df["Frequency"].loc[i]
                score = df["Score"].loc[i]
                new_df = pd.concat([new_df, pd.Series({"Word":i, "Frequency":freq, "Score":score}).to_frame().T], ignore_index=True)
            else:
                print(f"Warning: {i} not in dataframe")
    new_df = new_df.set_index("Word")
    return(new_df.sort_values(by="Score", ascending=False))
# print(word_search(word_df, steepness))
# print(word_search(word_df, stones))
# print(word_search(word_df, holds))


mount_mask = np.array(Image.open("Images\mountain_trans.png"))
# print(mount_mask)

def star_colour_grade(word, font_size, position, orientation, random_state=None,**kwargs):
    # print(word)
    if word in all_words:
        return f"hsl({((word_df["Score"].loc[word]-2.07)*105)}, 100%, 50%)"
    else:
        return f"hsl(240, 100%, 50%)"

# wc = WordCloud(background_color="black", mask = mount_mask, colormap = "Pastel1", width = 1600, height = 1000).generate(names)
# plt.imshow(wc)
# plt.axis("off")
# plt.savefig("Graphs\Route Name Wordcloud")
# plt.show()

wc = WordCloud(background_color="black", mask = mount_mask, width = 1600, height = 1000, stopwords= stopwords).generate(descs)
default_colors = wc.to_array()

plt.imshow(wc.recolor(color_func = star_colour_grade), interpolation="bilinear")
wc.to_file("test.png")
plt.axis("off")
plt.savefig("Graphs\Route Description Wordcloud")


# plt.figure()
# plt.imshow(default_colors, interpolation="bilinear")
# plt.axis("off")

plt.show()