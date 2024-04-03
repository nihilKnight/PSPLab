import jieba

from docx import Document


# source: https://github.com/fwwdn/sensitive-stop-words/
sensitive_wordlist_path = "./sensitive_wordlist.txt"

class Marker:
    def __init__(self) -> None:
        self.wordlist = set()
        with open(sensitive_wordlist_path, "r", encoding="UTF-8") as txtfile:
            self.wordlist = set([line.strip() for line in txtfile.readlines()])

    def search(self, word: str) -> bool:
        return word in self.wordlist


def mark(wordmarking_path: str):
    doc = Document(wordmarking_path)
    marker = Marker()
    for para in doc.paragraphs:
        for word in jieba.cut(para.text):
            if marker.search(word):
                print(word)
