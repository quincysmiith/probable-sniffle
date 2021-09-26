# from .extensions import db
from urllib import parse
import re

# class MyModel(db.Model):
# pass

class Html_Location:
    'file path to html documents stored on digital ocean'

    def __init__(self, string_path: str) -> None:
        self.string_path = string_path
        self.friendly_path = parse.quote_plus(string_path)
        self.base = "https://marquin-space-object-storage-01.sgp1.cdn.digitaloceanspaces.com/"
        self.link = self.base + self.friendly_path

        # create name string
        self.name = string_path.replace("web-resources/htmls/", "")
        self.name = self.name.replace(".html", "")
        self.name = re.sub('\(\d{4}-\d{2}-\d{2}.*M\)', "", self.name)

        
