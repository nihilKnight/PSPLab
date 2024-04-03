import os
import jieba
import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from docx import Document


font_path = "fonts/SourceHanSansCN-Normal.otf"
fig_dir = "figs/"

def count(wordcounting_path: str):
    doc = Document(wordcounting_path)
    wordlist = {}
    for para in doc.paragraphs:
        for word in jieba.cut(para.text):
            # skip short words.
            if len(word) <= 2:
                continue
            if word in wordlist:
                wordlist[word] += 1
            else:
                wordlist[word] = 1
    df = pd.DataFrame({
        "word": [item[0] for item in wordlist.items()],
        "frequency": [item[1] for item in wordlist.items()]
    })
    df.sort_values("frequency", inplace=True, ascending=False)
    wordcloud = WordCloud(max_font_size=80, max_words=300, font_path=font_path, background_color="white").generate(' '.join(list(df["word"])))
    wordcloud.to_file(fig_dir + os.path.split(wordcounting_path)[-1].split(".")[0] + ".png")
