import urllib.request as urlreq
from pathlib import Path
import re
import json

class Instagrab():
    def __init__(self, target=None):
        self.verbose = True
        # Should I scrap this and force target in download()?
        if self.__is_good_target(target):
            if re.match('^\w$', target):
                self.__target = __url_from_username(target)
            else:
                self.__target = target
        else:
            self.__target = None

    def __is_good_target(self, target):
        if target and type(target).__name__ == 'str':
            if re.match('\w', target):
                # username
                return True
            elif self.__is_good_url(target):
                return True
        else:
            return False

    def __is_good_url(self, url):
        url_regex = '(https?://)?(www\.)?instagram.com/\w(/)?'
        if re.match(url_regex, url):
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

    def download(self, target=None):
        """Download media from instagram account"""
        #XXX A lot of this is duplicated in __init__()
        #  Should probably isolate the logic better
        #  Maybe strip a default target?
        if not target and self.__target:
            # Use initialized target
            url = self.__target
        elif re.match('\w', str(target)):
            # Target is a username
            url = self.__url_from_username(target)
        elif self.__is_good_url(str(target)):
            url = target
        else:
            raise("Invalid URL or Instagram username: " + str(target))

        media = json.loads(self.__get_json(url))

        while True:
            for item in media['items']:
                if item['videos']:
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
