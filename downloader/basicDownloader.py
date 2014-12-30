#!/usr/bin/env python 3
# -*- coding: utf-8 -*-


import urllib.request
import urllib.parse


def main():
    url = 'http://www.mangatown.com/search.php'
    searchedValues = {'name': input('Wich manga do you want to download? ')}
    Downloader = EncodedDownloader(url, searchedValues)
    Downloader.downloadAsString()
    arq = open('arq.html', 'w')
    arq.write(Downloader.contents)
    arq.close()


class Downloader():
    '''
    Basic Downloader class to download from a given URL.
    '''
    def __init__(self, url, textEncoding='utf-8'):
        self.url = url
        self.textEncoding = textEncoding
        self.contents = ''

    def requestData(self):
        '''

        '''
        req = urllib.request.Request(self.url)
        resp = urllib.request.urlopen(req)
        return(resp)

    def download(self):
        resp = self.requestData()
        is_downloaded = (resp.getcode() == 200)
        if not is_downloaded:
            print('ERROR: Could not request the data!')
        else:
            respData = resp.read()
            self.contents = respData
            return(respData)

    def downloadAsString(self):
        respData = self.download()
        respData = respData.decode(self.textEncoding, 'ignore')
        self.contents = respData
        return(respData)


class EncodedDownloader(Downloader):
    '''
    Class for encoding values to Downloaders and download the result.
    '''
    def __init__(self, url, encodingValues={}, textEncoding='utf-8'):
        self.encodingValues = encodingValues
        self.contents = ''
        super().__init__(url, textEncoding='utf-8')

    def requestData(self):
        encodingData = urllib.parse.urlencode(self.encodingValues)
        encodingData = encodingData.encode('utf-8')
        req = urllib.request.Request(self.url, encodingData)
        resp = urllib.request.urlopen(req)
        return(resp)


if __name__ == '__main__':
    main()
