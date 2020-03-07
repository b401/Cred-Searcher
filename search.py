import requests
from sys import argv
import re
import json

class github:
    def __init__(self, repo):
        self.api = "https://api.github.com"
        self.repo = repo
        pass

    def search(self,keyword):
        path = "/search/code?q={}+repo:{}".format(keyword,self.repo)
        return requests.get(self.api+path).json()


    def existing_repository(self):
        path = "/repos/{}".format(self.repo)
        r = requests.get(self.api+path)
        if r.status_code != 200:
            return False
        return True

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[91m'
    ENDC = '\033[0m'


def load_keywords():
    with open('keywords.txt') as words_file:
        keywords = words_file.read().splitlines()
    return keywords


def grab_file(files):
    for item in files:
        for f in files[item]:
            r = requests.get(f)
            if r.status_code == 200:
                pattern = re.compile(r".*"+item+".*")
                print("-----")
                print("File: {}".format(bcolors.WARNING+f+bcolors.ENDC))
                for findings in re.findall(pattern, r.text):
                    print("{}".format(findings.replace(item,bcolors.OKGREEN+item+bcolors.ENDC)))

if __name__ == '__main__':
    g = github(argv[1])
    if g.existing_repository():
        keywords = load_keywords()
        print("Found existing Repository")
        print("Looking for keywords: ")
        findings = dict()
        for i in keywords:
            search = g.search(i)
            if search["total_count"] != 0:
                urls = []
                for items in search["items"]:
                    urls.append(items['html_url'].replace("github.com","raw.githubusercontent.com").replace("/blob",""))

                findings.update({
                    i : urls
                })

        grab_file(findings)

    else:
        print("Repository {} does not exist".format(argv[1]))
