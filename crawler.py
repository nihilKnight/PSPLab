import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from constant import constant


class SubDirCrawler:
    def __init__(self, depth=3) -> None:
        self.dirs = set()
        self.depth = depth
        self.count = 1

    def renew(self):
        self.dirs = set()
        self.count = 1

    def parse(self, url: str, depth: int):
        domain = urlparse(url).netloc
        req = requests.get(url, headers={"User-Agent": constant.USER_AGENT})
        suburls = [url_tag["href"] for url_tag in BeautifulSoup(req.content, "html.parser").find_all("a", href=True)]
        for suburl in suburls:
            parsed_suburl = urlparse(suburl)
            if (parsed_suburl.netloc == domain and parsed_suburl.path.lstrip("/").count("/") >= depth) \
                or (parsed_suburl.netloc == "" and parsed_suburl.path.lstrip("/").count("/") >= depth):
                # the `dir` should be in the format of `dir_1/dir_2/.../dir_x/.../dir_n/` in depth n.
                dir = "/".join(parsed_suburl.path.lstrip("/").split("/")[:-1]) + "/"
                if not dir in self.dirs:
                    self.dirs.add(dir)
                    yield dir
                    
                
    def recursive_parse(self, url: str):
        if self.count == self.depth:
            # return an empty generator.
            yield from ()
            return 
        dir_gen = self.parse(url, self.count)
        for dir in dir_gen:
            yield dir
            self.count += 1
            next_dir_gen = self.recursive_parse(urljoin(url, dir))
            self.count -= 1
            yield from next_dir_gen

