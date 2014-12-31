#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import basicDownloader as bd


def _test():
    manga = input('Wich manga do you want to search for? ')
    print('\n')
    try:
        search = mangaTownBrowser(manga)
        results = search.getResults('full')
        for i in results:
            for j in ['title',
                      'style',
                      'cover link',
                      'url']:
                print(j.capitalize() + ': ' + i[j])
            print('\n')
        print('Number of results: %i' % len(results))
    except mangaNotFound:
        pass

class mangaTownBrowser:
    '''
    A basic class to search in a manga reader site.
    '''
    def __init__(self, search=''):
        self.search = search
        self.searchUrl = ''
        self.textEncoding = 'utf-8'
        self.results = []

    def getSearchPage(self, page=1):
        searchValues = {'name': self.search,
                        'page': page}
        search = bd.EncodedDownloader(self.searchUrl,
                                      searchValues,
                                      self.textEncoding)
        search.downloadAsString()
        return(search.contents)

    def getHtmlResults(self, searchPage):
        try:
            resultsBox = re.findall(r'<ul attrs >(.*?)</ul>',
                                    searchPage,
                                    re.S | re.I)[0]
            htmlResults = re.findall(r'<li>(.*?)</li>',
                                     resultsBox,
                                     re.S | re.I)
            return(htmlResults)
        except IndexError:
            raise mangaNotFound('Could not find the searched manga!')

    def getMangaInfo(self, htmlResult):
        url = re.findall(r'',
                         htmlResult,
                         re.S | re.I)[0]
        title = re.findall(r'',
                           htmlResult,
                           re.S | re.I)[0]
        coverLink = re.findall(r'',
                               htmlResult,
                               re.S | re.I)[0]
        style = re.findall(r'',
                           keywordsTag,
                           re.S | re.I)
        style = ', '.join(style)
        mangaDict = {'uploader': 'basicBrowser',
                     'title': title,
                     'style': style,
                     'cover link': coverLink,
                     'url': url}
        return(mangaDict)

    def getNumberOfPages(self, searchPage):
        numberOfPages = re.findall(r'<option.*>1/(\d*?)</option>',
                                       searchPage,
                                       re.S | re.I)[0]
        numberOfPages = int(numberOfPages)
        return(numberOfPages)


    def getResults(self, mode='partial'):
        mangas = []

        searchPage = self.getSearchPage()
        htmlResults = self.getHtmlResults(searchPage)
        for htmlResult in htmlResults:
            mangaInfo = self.getMangaInfo(htmlResult)
            mangas.append(mangaInfo)

        if mode == 'full':
            numberOfPages = getNumberOfPages
            for page in range(2, (numberOfPages + 1)):
                searchPage = self.getSearchPage(page)
                htmlResults = self.getHtmlResults(searchPage)
                for htmlResult in htmlResults:
                    mangaInfo = self.getMangaInfo(htmlResult)
                    mangas.append(mangaInfo)
        self.mangas = mangas
        return(mangas)


class mangaNotFound(Exception):
    print('Could not find the manga you typed.')


if __name__ == '__main__':
    _test()
