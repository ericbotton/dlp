from io import StringIO
from html.parser import HTMLParser
import re

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return_string = s.get_data()
    return re.sub(r'\n\s*\n','\n', return_string, re.MULTILINE)

#print(re.sub(r'\n\s*\n','\n',a,re.MULTILINE))
