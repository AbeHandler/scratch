from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm as tqdm
from typing import List
import json
import glob
import re

class HTMLFileExtractor(object):

    def __init__(self, filename: str="html/20.html") -> None:
        
        self.filename = filename
        with open(filename, "r") as inf:
            html_doc = inf.read()
            self.soup = BeautifulSoup(html_doc, 'lxml')
            
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

    def filter_out_tags_by_class(self, tags: List[Tag], _class='ipsItemControls'):
        '''exclude tags with a given class from a list of tags'''
        return [o for o in tags if _class not in o.attrs["class"]]

    def extract(self, html_element="div", html_class="message-userContent"):

        messages = self.select_by_class(html_element, html_class)

        output = []
        
        for i, message in enumerate(messages):
            tags = [c for c in message.children if type(c) == Tag]
            tags = self.filter_out_tags_by_class(tags, _class='ipsItemControls')
            for c in tags:
                message = self.strip_tag_from_html_string(str(c), "abbr")
                message = BeautifulSoup(message, 'lxml').text
                message = message.replace("\n", " ").strip()
                output.append({"body": message,
                               "id": self.filename.replace("html", "").replace(".", "").replace("/", "") + "_" + str(i)})

        return output
    
extractor = HTMLFileExtractor("index.html")
print(extractor.extract("div", "cPost_contentWrap"))