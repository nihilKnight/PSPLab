import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from docx import Document


# utilize np, pd to conduct word counting; then draw a word cloud from the result.
def count(wordcounting_path: str):
    doc = Document(wordcounting_path)
    for para in doc.paragraphs:
        pass