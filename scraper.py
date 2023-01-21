import urllib.request
import re
import random
from bs4 import BeautifulSoup


def getReferenceUrlsOfPage(domain, url):
    webpage = urllib.request.urlopen(url)
    # for line in webpage:
    #     print(line.decode().strip())
    htmlURLs = set()
    javaScriptURLs = set()
    cssURLs = set()
    urlList = []

    soupify = BeautifulSoup(webpage)

    # Handles hyperlinks in HTML
    hyperlinks = soupify.findAll("a")
    for hyperlink in hyperlinks:
        hyperlinkURL = hyperlink.get('href')
        # A link should have an href tag and not be empty to be included 
        if hyperlinkURL != None and len(hyperlinkURL) != 0:
            # Check to see if result is unique to the domain
            if hyperlinkURL[0] == "/":
                #add domain to make a full url
                hyperlinkURL = "https://" + domain + hyperlinkURL
                #Scrape this website as well
            htmlURLs.add(hyperlinkURL)

    # Handles JavaScript.
    srcs = soupify.findAll("script")
    for src in srcs:
        srcURL = src.get('src')
        # A script should have an src tag and not be empty to be included.
        if srcURL != None and len(srcURL) != 0:
            # We want the urls to be on the same domain, so we check for the keyword.
            splitDomain = domain.split(".")
            #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
            if splitDomain[1] not in srcURL:
                print(srcURL)
                continue
            javaScriptURLs.add(srcURL)

    # Handles CSS
    links = soupify.findAll("link")
    for link in links:
        linkURL = link.get("href")
        # We want the urls to be on the same domain, so we check for the keyword.
        splitDomain = domain.split(".")
        #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
        if splitDomain[1] in linkURL:
            if linkURL in htmlURLs:
                continue
            cssURLs.add(linkURL)

    # adding all the sets into a list to make return value easier to handle
    urlList.append(htmlURLs)
    urlList.append(javaScriptURLs)
    urlList.append(cssURLs)

    return urlList



def main():
    allUrlsScraped = set()
    # "This web scraper will take three pieces of input:  a domain, a URL, and a depth."
    print("Please enter a domain, a URL including https://, and a depth all separated by spaces. i.e. https://www.rit.edu https://www.rit.edu 2")
    inputParams = input("Enter here: ")
    scraperParams = inputParams.split(" ")
    domain, url, depth = scraperParams[0], scraperParams[1], scraperParams[2]
    castDepth = int(depth)
    counter = 0
    while castDepth >= 0:
        # if its the first iteration we want to gather all the urls from our initial input url
        if castDepth == int(depth):
            urlList = getReferenceUrlsOfPage(domain, url)
            for urlList in urlList:
                for url in urlList:
                    allUrlsScraped.add(url)
        else:
            # Then we use the urls we scraped from the first url and then scrape those.
            iterableScapedUrls = list(allUrlsScraped)
            for url in iterableScapedUrls:
                newUrlList = getReferenceUrlsOfPage(domain, url)
                for urlList in newUrlList:
                    for url in urlList:
                        allUrlsScraped.add(url)
        print(depth)
        print("Total Amount of URLs Scraped at depth " + str(counter) + " is " + str(len(allUrlsScraped)))
        castDepth -= 1
        counter += 1
    
    # print(allUrlsScraped)
    
if __name__ == "__main__":
    main()