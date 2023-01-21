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
    mediaURLs = set()

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
            javaScriptURLs.add(srcURL)

    # Handles CSS
    links = soupify.findAll("link")
    for link in links:
        linkURL = link.get("href")
        # We want the sites to be on the same domain, so we check for the keyword.
        splitDomain = domain.split(".")
        #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
        if splitDomain[1] in linkURL:
            #print(linkURL)
            if linkURL in htmlURLs:
                continue
            print(linkURL)
            cssURLs.add(linkURL)

    return htmlURLs, javaScriptURLs, cssURLs



def main():
    allUrlsScraped = set()
    allMediaScraped = set()
    # "This web scraper will take three pieces of input:  a domain, a URL, and a depth."
    print("Please enter a domain, a URL including https://, and a depth all separated by spaces. i.e. https://www.rit.edu https://www.rit.edu 2")
    inputParams = input("Enter here: ")
    scraperParams = inputParams.split(" ")
    domain, url, depth = scraperParams[0], scraperParams[1], scraperParams[2]
    depth = int(depth)
    pageURLs, pageMedia = getReferenceUrlsOfPage(domain, url)
    # while depth >= 0:
    #     pageURLs, pageMedia = getReferenceUrlsOfPage(domain, url)
    #     for url in pageURLs:
    #         allUrlsScraped.add(url)
    #     for media in pageMedia:
    #         allMediaScraped.add(media)
    #     # print(url + " " + str(depth))
    #     # url = random.sample(allUrlsScraped, 1)[0]
    #     depth -= 1
    # # # print(len(allUrlsScraped))
    # # print(len(allMediaScraped))
    # print(allUrlsScraped)
    print("Total Amount of URLs Scraped: " + str(len(pageURLs)))
    # print(pageURLs)
    
if __name__ == "__main__":
    main()