#!/usr/bin/env python 3
# -*- coding: utf-8 -*-


import urllib.request
import urllib.parse
import re


class Downloader():
    '''
    Basic Downloader class to download URL contents.
    '''
    def __init__(self, url, textEncoding='utf-8'):
        self.url = url
        self.content = ''
        self.textEncoding = textEncoding

    def download(self):
        req = urllib.request.Request(self.url)
        resp = urllib.request.urlopen(req)
        return(resp)

    def getAsString(self):
        resp = self.download()
        is_downloaded = (resp.getcode() == 200)
        if not is_downloaded:
            print('ERROR: Could not request the data!')
        else:
            respData = resp.read()
            respData = respData.decode(self.textEncoding, 'ignore')
            self.content = respData


class EncodedDownloader(Downloader):
    '''
    Class for encoding values to Downloaders and download the result.
    '''
    def __init__(self, url, encodingValues={}, textEncoding='utf-8'):
        self.encodingValues = encodingValues
        super().__init__(url, textEncoding='utf-8')

    def download(self):
        encodingData = urllib.parse.urlencode(self.encodingValues)
        encodingData = encodingData.encode('utf-8')
        req = urllib.request.Request(self.url, encodingData)
        resp = urllib.request.urlopen(req)
        return(resp)


def main():
    url = 'http://www.mangatown.com/search.php'
    searchedValues = {'name': input('Wich manga do you want to download? ')}
    Downloader = EncodedDownloader(url, searchedValues)
    Downloader.getAsString()
    arq = open('arq.html', 'w')
    arq.write(Downloader.content)
    arq.close()

if __name__ == '__main__':
    main()
