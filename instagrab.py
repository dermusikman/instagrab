import urllib.request as urlreq
from pathlib import Path
import re
import json

class Instagrab():
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __is_good_url(self, url):
        url_regex = '(https?://)?(www\.)?instagram.com/\w(/)?'
        if re.match(url_regex, url):
            return True
        else:
            return False

    def __is_good_username(self, username):
        username_regex = '^[A-Za-z0-9_-]*$'
        if re.match(username_regex, username):
            return True
        else:
            return False

    def __get_binary(self, url):
        """Download raw file from URL"""
        return urlreq.urlopen(url).read()

    def __get_json(self, url):
        """Download file as string from URL"""
        raw = urlreq.urlopen(url).read()
        treated = raw.decode("utf-8")
        return treated

    def __url_from_username(self, username):
        """Translate username into base url for scraping"""
        return "https://www.instagram.com/" + username + "/media"

    def __clean_name(self, url):
        """Strips cruft from URL and provides basename"""
        file_re = '.*(png|jpg|gif|mp4)'
        clean_url = re.search(file_re, url).group()
        return Path(clean_url).name

    def download(self, target):
        """Download media from instagram account"""
        if type(target).__name__ == 'str':
            if self.__is_good_username(target):
                # Target is a username
                url = self.__url_from_username(target)
            elif self.__is_good_url(str(target)):
                url = target
            else:
                raise("Invalid URL or Instagram username: " + target)
        else:
            raise("In download(t), 't' must be a 'str'")

        media = json.loads(self.__get_json(url))

        while True:
            for item in media['items']:
                if 'videos' in item:
                    medium = 'videos'
                else:
                    medium = 'images'

                item_url = item[medium]['standard_resolution']['url']
                item_name = self.__clean_name(item_url)

                # Let's default to no clobber
                if not Path(item_name).exists():
                    if self.verbose == True:
                        print("Downloading... " + item_name)
                    f = open(item_name, "wb")
                    f.write(self.__get_binary(item_url))
                    f.close()

            next_url = url + "?max_id=" + media['items'][-1]['id']
            media = json.loads(self.__get_json(next_url))

            if not media or not media['items']:
                break
