# Author: Francisco Lopez
#
# Purpose: Web scrape tool: This script searches accepts the name of a song
#   that is input and returns the genre of the song using url.lib
#   requests to the website "www.allmusic.com"
#
# Side Note: This is a practice program and is not perfect
#   you're free to edit it as you wish
#
# Date: 6/8/17

import urllib.request as ur
import re
import random

class Scrape:

    global url
    url = "http://www.allmusic.com/search/song/"

    global hold
    hold = 0

    global hold2
    hold2 = 0

    global j
    j = random.randint(1, 3)

    global comp
    comp = []

    global temp
    temp = []

    global songDict
    songDict = {}

    global fullLink
    fullLink = []

    global composerComplete
    composerComplete = []

    global linkList
    linkList = []

    global song
    song = ''

    global songTitle
    songTitle = []

    def scrape(self):
        self.getinitdata()
        self.composersearch()
        self.linksearch()
        self.genresearch()

    def getinitdata(self):
        song = input('What song would you like to search?\n')
        songTitle = song.split(" ")
        title = ''.join(songTitle)
        url = "http://www.allmusic.com/search/song/"
        url = url + title

        global headers
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

        req = ur.Request(url, headers=headers)
        gate = ur.urlopen(req)

        global parsedData
        parsedData = gate.read()

        global strData
        strData = str(parsedData)

    def composersearch(self):
        global searchList
        searchList = strData.split("<li class=\"song\"")
        del searchList[0]

        for i in searchList:
            songData = i.split("           ")

            compFilter = re.compile('.by*')
            filterItems = filter(compFilter.match, songData)
            comp.append(list(filterItems))

            linkFilter = re.compile('.*a href="http://www.allmusic.com/song/.*')
            linkFilteredItems = filter(linkFilter.match, songData)
            linkList.append(list(linkFilteredItems))

    def linksearch(self):
        for i in linkList:
            temp.append(i[0].split("\""))


        for i in temp:
            fullLink.append(i[1])

        for i in comp:
            if len(i) == 0:
                continue
            indComp = str(i).split('>')
            composer = indComp[1][0:-3]
            composerComplete.append(composer)

        hold = 0
        for i in composerComplete:
            songDict.setdefault(i, '')
            if j == 2:
                continue
            else:
                songDict[i] = fullLink[hold]
            hold += 1

        for i in composerComplete:
            if songDict[i] == '':
                songDict[i] = fullLink[hold2]
            hold += 1

    def genresearch(self):
        for i in songDict:
            print()
            print("Is the artist of the song:", song, i)
            responce = input()
            responce.lower()
            if responce == 'y':
                req = ur.Request(songDict[i], headers=headers)
                gate = ur.urlopen(req)
                parsedData = gate.read()
                strData = str(parsedData)
                searchList = strData.split('<a href=\"http://www.allmusic.com/genre')
                if len(searchList) == 1:
                    print("Sorry I couldn't find the genre this time. Ask again and I might find it on that search.")
                    break
                searchList = searchList[1]
                searchList = searchList.split('>')
                searchList = searchList[1]
                genre = searchList[0:-3]

                print('\nThe genre of ', song, " is", genre)
                break