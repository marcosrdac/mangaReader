#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import basicDownloader as bd


def main():
    manga = input('Wich manga do you want to search for? ')
    print('\n')
    try:
        search = mangaTownBrowser(manga)
        results = search.getResults('full')
        for i in results:
            for j in ['title',
                      'keywords',
                      'cover link',
                      'link',
                      'views',
                      'score',
                      'new chapter title',
                      'new chapter link']:
                print(j.capitalize() + ': ' + i[j])
            print('\n')
        print('Number of results: %i' % len(results))
    except mangaTownBrowser().mangaNotFound:
        print('Could not find the manga you typed.')


class mangaTownBrowser:
    '''
    A basic class to search in a manga reader site.
    '''
    def __init__(self, search=''):
        self.search = search
        self.searchUrl = 'http://www.mangatown.com/search.php'
        self.textEncoding = 'utf-8'
        self.results = {}

    class mangaNotFound(Exception):
        pass

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
            resultsBox = re.findall(r'<ul class="manga_pic_list">(.*?)</ul>',
                                    searchPage,
                                    re.S | re.I)[0]
            htmlResults = re.findall(r'<li>(.*?)</li>',
                                     resultsBox,
                                     re.S | re.I)
            return(htmlResults)
        except:
            raise self.mangaNotFound('Could not find the searched manga!')

    def getMangaInfo(self, htmlResult):
        linkTitle = re.findall(r'<a class="manga_cover" href="(.*?)" '
                               r'title="(.*?)">',
                               htmlResult,
                               re.S | re.I)[0]
        link = linkTitle[0]
        title = linkTitle[1]
        coverLink = re.findall(r'<img src="(.*?)".* />',
                               htmlResult,
                               re.S | re.I)[0]
        score = re.findall(r'<span.*<b>(.*?)</b>',
                           htmlResult,
                           re.S | re.I)[0]
        keywordsTag = re.findall(r'<p class="keyWord">(.*?)</p>',
                                 htmlResult,
                                 re.S | re.I)[0]
        keywords = re.findall(r'<a href=".*">(.*?)</a>',
                              keywordsTag,
                              re.S | re.I)
        keywords = ', '.join(keywords)
        views = re.findall(r'<p class="view">Views:\s*(\d*?)\s*</p>',
                           htmlResult,
                           re.S | re.I)[0]
        newChapterTitleLink = re.findall(r'<p class="new_chapter"><a.*'
                                         r'title="(.*?)" href="(.*?)">.*'
                                         r'</a></p>',
                                         htmlResult,
                                         re.S | re.M | re.I)[0]
        newChapterTitle = newChapterTitleLink[0]
        newChapterLink = newChapterTitleLink[1]
        mangaDict = {'title': title,
                     'keywords': keywords,
                     'cover link': coverLink,
                     'link': link,
                     'views': views,
                     'score': score,
                     'new chapter title': newChapterTitle,
                     'new chapter link': newChapterLink}
        return(mangaDict)

    def getResults(self, mode='partial'):
        searchPage = self.getSearchPage()
        mangas = []

        htmlResults = self.getHtmlResults(searchPage)
        for htmlResult in htmlResults:
            mangaInfo = self.getMangaInfo(htmlResult)
            mangas.append(mangaInfo)

        if mode == 'full':
            numberOfPages = re.findall(r'1/(\d*?)</option>',
                                       searchPage,
                                       re.S | re.I)[0]
            numberOfPages = int(numberOfPages)
            for page in range(2, (numberOfPages + 1)):
                searchPage = self.getSearchPage(page)
                htmlResults = self.getHtmlResults(searchPage)
                for htmlResult in htmlResults:
                    mangaInfo = self.getMangaInfo(htmlResult)
                    mangas.append(mangaInfo)
        return(mangas)


if __name__ == '__main__':
    main()
