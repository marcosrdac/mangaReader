#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse


def download(url, encodingValues={}):
    data = urllib.parse.urlencode(encodingValues)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    isDownloaded = resp.getcode() == 200
    if isDownloaded:
        respData = str(resp.read(), 'cp1251')
        return(respData)
    else:
        print('ERROR: Could not request the data!')


if __name__ == '__main__':
    arq = open('arq.html', 'w')
    arq.write(download(input('Type the URL: ')))
    arq.close()
