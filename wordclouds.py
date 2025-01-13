import pandas as pd
import sweetviz as sv
from matplotlib import pyplot as plt, colors
import numpy as np
import nltk
#from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')
from wordcloud import WordCloud
from PIL import Image

nltk.download("stopwords")
# print(stopwords.words("english"))

df = pd.read_csv("outputted_df.csv")
names = ""
for i in df["Route"]:
    names = names + " " + i
# print(names)


# j = 0
# temp_descs = ""
# with open("descriptions.txt", "w", encoding="utf-8") as f:
#     f.write("")
# for i in df["Description"]:
#     print(j)
#     j = j+1
#     with open("descriptions.txt", "a", encoding="utf-8") as f:
#         f.write(i+"\n")
# # print(descs_ts)



with open("descriptions.txt", 'r', encoding="utf-8") as file:
    descs = file.read()

mount_mask = np.array(Image.open("mountain_trans.png"))
# print(mount_mask)

wc = WordCloud(background_color="black", mask = mount_mask, colormap = "Pastel1", width = 800, height = 500).generate(names)
plt.imshow(wc)
plt.axis("off")
plt.savefig("Route Name Wordcloud")
plt.show()

wc = WordCloud(background_color="black", mask = mount_mask, colormap = "Pastel1", width = 800, height = 500, stopwords= stopwords).generate(descs)
plt.imshow(wc)
plt.axis("off")
plt.savefig("Route Description Wordcloud")
plt.show()