import subprocess
import time
import json
import sys


def format_news_piece(piece: dict):
    return "\n".join([
        piece['title'][0],
        piece['date'][0],
        "\n".join(piece['content'])
    ])

def convert_json_to_txt(path: str, json_file_name: str):
    txt_file_name = json_file_name[:-4] + "txt"
    with open(path + json_file_name, encoding="UTF-8") as json_file:
        news = json.load(json_file)
    if news == []:
        return
    with open(path + txt_file_name, "w", encoding="UTF-8") as txt_file:
        [txt_file.write(format_news_piece(piece) + "\n\n") for piece in news]

if __name__ == "__main__":
    ticks = str(time.time())[:10]
    path = "results/"
    json_file_name = f"sina_news_{ticks}.json"
    spider_name = "sina_spider" if len(sys.argv) <= 1 else sys.argv[1]

    subprocess.run(["scrapy", "crawl", spider_name, "-o", path + json_file_name])

    convert_json_to_txt(path, json_file_name)
