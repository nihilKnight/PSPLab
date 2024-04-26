
from urllib.parse import urljoin
from crawler import SubDirCrawler


if __name__ == "__main__":
    gen = SubDirCrawler(3).recursive_parse("https://www.cnki.net/")
    try:
        while True:
            url = next(gen)
            print(url)
    except StopIteration:
        pass

    # print(urljoin("http://hello.com/", "some/", "word.txt"))
