from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm as tqdm
from typing import List
import json
import glob
import re

class HTMLExtractor(object):

    def __init__(self, html_str: str) -> None:
        
        self.soup = BeautifulSoup(html_str, 'lxml')
            
    def select_by_class(self, html_element="div", 
                              html_class="bbWrapper"):
        return self.soup.find_all(html_element, {"class": html_class})

    def strip_tag_from_html_string(self, html_str: str, html_tag: str) -> str:
        '''
        Sample input: <p>I\'m in the same spot as you. <abbr title="Licensed Practice Nurse">LPN</abbr>, needing to work from home </p>
        Sample output: <p>I\'m in the same spot as you, needing to work from home </p>
        '''
        regex = "<{}(.|\n)*?</{}>".format(html_tag, html_tag)
        return re.sub(regex, "", str(html_str))

    def exclude_tags_by_class(self, tags: List[Tag], _class='ipsItemControls'):
        '''exclude tags with a given class from a list of bs4 tags'''
        return [o for o in tags if _class not in o.attrs["class"]]

    def extract(self, html_element="div", html_class="message-userContent"):

        items = self.select_by_class(html_element, html_class)

        output = []
        
        for i, item in enumerate(items):
            tags = [c for c in item.children if type(c) == Tag]
            tags = self.exclude_tags_by_class(tags, _class='ipsItemControls')
            for c in tags:
                item = self.strip_tag_from_html_string(str(c), "abbr")
                item = BeautifulSoup(item, 'lxml')
                item = item.text
                item = item.replace("\n", " ").strip()
                output.append(item)

        return output


if __name__ == "__main__":
    with open("index.html", "r") as inf:
        html_doc = inf.read()
        extractor = HTMLExtractor(html_doc)
        messages = extractor.extract(html_element="div", html_class="cPost_contentWrap")
        for i, message in enumerate(messages):
            print(i, message)
