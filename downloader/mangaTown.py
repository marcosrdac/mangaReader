#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import basicDownloader as bD


def main():
    test = mangaTownSearch('naruto')
    test.getHtmlSearchList()


class mangaTownSearch():
    '''
    Class for getting Manga Town searchings.
    '''
    def __init__(self, search=''):
        self.baseUrl = 'http://www.mangatown.com/search.php'
        self.textEncoding = 'utf-8'
        self.search = search
        self.searchBoxHtml = ''
        self.results = {}

    def getHtmlSearchList(self, page=1):
        searchValues = {'name': self.search,
                        'page': page}
        htmlSearch = bD.EncodedDownloader(self.baseUrl,
                                          searchValues,
                                          self.textEncoding)
        htmlSearch.getAsString()
        htmlResultsBox = re.findall(r'<ul class="manga_pic_list">(.*?)</ul>',
                                htmlSearch.contents,
                                re.S | re.I)
        htmlResults = re.findall(r'<li>(.*?)</li>',
                                 htmlResultsBox,
                                 re.S | re.I)
        return(htmlResults)


    def


if __name__ == '__main__':
    main()
