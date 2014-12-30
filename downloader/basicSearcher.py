class basicSearcher:
	'''
	A basic class to search in a manga reader site.
	'''

	def __init__(self, search=''):
		self.search = search
		self.textEncoding = 'utf-8'

	def getSearchPage(self, page=1):
		pass

	def getSearchBox(self, searchPage):
		pass

	def getHtmlResults(self, searchBox):
		pass

	def getMangaInfo(self, htmlResult):
		pass

	def getResults(self, mode='partial'):
		if mode == 'partial':
			searchPage = self.getSearchBox(searchPage)
			resultsBox = self.getSearchBox(searchpage)
			htmlResults = self.getHtmlResults(resultsBox)

			for htmlResult in range(len(htmlResults)):
				mangaInfo = self.getMangaInfo(htmlResult)

		elif mode == 'full':
			pass
