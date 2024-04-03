import os
import argparse
import json
import csv
import re

from make import make_docx, make_pdf
from count import count
from excep import InputTypeMismatchException, OutputTypeMismatchException


default_output_dir = "outputs/"

if __name__ == "__main__":

    # parse the command line arguments.
    parser = argparse.ArgumentParser("doc-collector-parser", add_help=False)
    parser.add_argument("-h", "--help", action="help", help=
                        "The input file should at least contains 3 fields: `title`, `date` and `content`.")
    parser.add_argument("-i", "--input_path", action="store", help=
                        "The path where the input document(.json, .csv or .txt) stored.")
    parser.add_argument("-o", "--output_path", action="store", nargs="?", help=
                        "The path where the output document(.docx or .pdf) stored. Default to output a .docx with the same name as input in the `outputs/` dir.")
    parser.add_argument("-c", "--wordcounting_path", action="store", help=
                        "The path where the file(.docx) to conduct word counting. Output a .png with the same name as input in the `figs/` dir.")
    parser.add_argument("-m", "--wordmarking_path", action="store", help=
                        "The path where the file to conduct word marking.")
    args = parser.parse_args()

    # input_path = args.input_path
    # input_name = os.path.split(input_path)[-1].split(".")[0]
    # input_type = os.path.split(input_path)[-1].split(".")[1]
    # output_path = os.path.join(default_output_dir, input_name + ".docx") if not args.output_path else args.output_path
    # output_name = input_name if not args.output_path else os.path.split(output_path)[-1].split(".")[0]
    # output_type = "docx" if not args.output_path else os.path.split(output_path)[-1].split(".")[1]

    # # check whether the input/output type is matched.
    # if input_type not in ["json", "csv", "txt"]:
    #     raise InputTypeMismatchException()
    # if output_type not in ["docx", "pdf"]:
    #     raise OutputTypeMismatchException()

    # # init the `articles`, whose element is a *dict* with field `title`, `date` and `content`.
    # articles = []
    # if input_type == "json":
    #     with open(input_path, encoding="UTF-8") as jsonfile:
    #         # load the json file to objects.
    #         articles = json.load(jsonfile)
    # elif input_type == "csv":
    #     with open(input_path, encoding="UTF-8") as csvfile:
    #         # load the csv file to objects.
    #         articles = [row for row in csv.DictReader(csvfile)]
    #     for arti in articles:
    #         # split the `arti["content"]` into list[str].
    #         arti["content"] = arti["content"].split(",")
    # else:
    #     with open(input_path, "r", encoding="UTF-8") as txtfile:
    #         lines = txtfile.read().splitlines()
    #     article = {}
    #     article["title"] = lines[0].strip()
    #     article["date"] = lines[1].strip()
    #     last_date_line = 1
    #     # start with pattern "xxxx年xx(/x)月xx(/x)日".
    #     date_pattern = re.compile(r"^\d{4}年\d{1,2}月\d{1,2}日")
    #     # recognize and split articles throught date pattern.
    #     for i in range(2, len(lines)):
    #         if date_pattern.search(lines[i]) != None:
    #             article["content"] = [line.strip() for line in lines[last_date_line+1:i-1]]
    #             # avoiding shallow copy.
    #             articles.append(article.copy())
    #             article["title"] = lines[i-1].strip()
    #             article["date"] = lines[i].strip()
    #             last_date_line = i
    #     article["content"] = [line.strip() for line in lines[last_date_line+1:]]
    #     articles.append(article.copy())

    # # output
    # if output_type == "docx":
    #     make_docx(output_path, articles)
    # else:
    #     make_pdf(output_path, articles)

    wordcounting_path = args.wordcounting_path
    count(wordcounting_path)

