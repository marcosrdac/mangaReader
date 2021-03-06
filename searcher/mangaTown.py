#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import basicDownloader as bd


def _test():
    manga = input('Wich manga do you want to search for? ')
    print('\n')
    try:
        search = mangaTownBrowser(manga)
        search.getResults()
        manga = search.getChosenManga(1)
        for i in ['title',
                  'alternative titles',
                  'style',
                  'genres',
                  'author',
                  'artist',
                  'status',
                  'rank',
                  'summary']:
            print(i.capitalize() + ': ' + manga[i])

    except mangaNotFound:
        print('Could not find the manga you typed.')


class mangaTownBrowser:
    '''
    A basic class to search in a manga reader site.
    '''
    def __init__(self, search=''):
        self.search = search
        self.searchUrl = 'http://www.mangatown.com/search.php'
        self.textEncoding = 'utf-8'
        self.results = []
        self.manga = {}

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
        except IndexError:
            raise mangaNotFound('Could not find the searched manga!')

    def getMangaInfo(self, htmlResult):
        urlAndTitle = re.findall(r'<a class="manga_cover" href="(.*?)" '
                                 r'title="(.*?)">',
                                 htmlResult,
                                 re.S | re.I)[0]
        url = urlAndTitle[0]
        title = urlAndTitle[1]
        coverLink = re.findall(r'<img src="(.*?)\?v=".* />',
                               htmlResult,
                               re.S | re.I)[0]
        mangaInfo = {'uploader': 'mangaTown',
                     'title': title,
                     'url': url,
                     'cover link': coverLink}
        return(mangaInfo)

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
            numberOfPages = self.getNumberOfPages(searchPage)
            for page in range(2, (numberOfPages + 1)):
                searchPage = self.getSearchPage(page)
                htmlResults = self.getHtmlResults(searchPage)
                for htmlResult in htmlResults:
                    mangaInfo = self.getMangaInfo(htmlResult)
                    mangas.append(mangaInfo)
        self.results = mangas
        return(mangas)

    # --------------------------------------------------------------------------
    def getChosenManga(self, mangaNumber):
        manga = self.results[mangaNumber-1]
        url = manga['url']

        page = bd.Downloader(url)
        page = page.downloadAsString()

        infoList = re.findall(r'<ul>(.*?)</ul>',
                              page,
                              re.S | re.I)[0]
        alternativeTitles = re.findall(r'<li><b>Alternative Name:</b>'
                                       r'(.*?)</li>',
                                       infoList,
                                       re.S | re.I)[0]
        manga['alternative titles'] = alternativeTitles

        style = re.findall(r'<li><b>Demographic:</b><.*?>(.*?)</a></li>',
                           infoList,
                           re.S | re.I)[0]
        manga['style'] = style

        genresElement = re.findall(r'<li><b>Genre\(s\):</b>(.*?)</li>',
                                   infoList,
                                   re.S | re.I)[0]
        genres = re.findall(r'<a.*?>(.*?)</a>',
                            genresElement,
                            re.S | re.I)
        genres = '; '.join(genres) + '.'
        manga['genres'] = genres

        author = re.findall(r'<li><b>Author\(s\):</b><.*?>(.*?)</a></li>',
                            infoList,
                            re.S | re.I)[0]
        manga['author'] = author

        artist = re.findall(r'<li><b>Artist\(s\):</b><.*?>(.*?)</a></li>',
                            infoList,
                            re.S | re.I)[0]
        manga['artist'] = artist

        status = re.findall(r'<li><b>Status\(s\):</b>(.*?)</li>',
                            infoList,
                            re.S | re.I)[0]
        if status != 'Completed':
            if re.findall('(Released)', status) != []:
                status = 'In Release'
            else:
                status = 'Incompleted'
        manga['status'] = status

        rank = re.findall(r'<li><b>Rank:</b>(.*?)</li>',
                          infoList,
                          re.S | re.I)[0]
        manga['rank'] = rank

        summary = re.findall(r'<b>Summary:</b>.*?<span id="show" style='
                             r'"display: none;">(.*?)&nbsp;<a.*?>',
                             infoList,
                             re.S | re.I)[0]
        manga['summary'] = summary

        chapterListBox = re.findall(r'<ul class="chapter_list">(.*?)</ul>',
                                    page,
                                    re.S | re.I)[0]

        listElements = re.findall(r'<li>(.*?)</li>',
                                  chapterListBox,
                                  re.S | re.I)
        chapters = {}
        for element in listElements:
            url = re.findall(r'<a href="(.*?)".*>',
                             element,
                             re.S | re.I)[0]
            number = re.findall(r'/c(\d*)',
                                url,
                                re.S | re.I)[0]
            chapter = {number: url}
            chapters = dict(list(chapters.items()) +
                            list(chapter.items()))

        manga['chapters'] = chapters

        self.manga = manga
        return(manga)


class mangaNotFound(Exception):
    pass


if __name__ == '__main__':
    _test()
