import urllib.request
import re
import random
from bs4 import BeautifulSoup


def getReferenceUrlsOfPage(domain, url):
    webpage = urllib.request.urlopen(url)
    # for line in webpage:
    #     print(line.decode().strip())
    alreadyScrapedURLs = set()
    mediaURLs = set()

    soupify = BeautifulSoup(webpage)

    # Handles HTML and CSS
    links = soupify.findAll("a")
    for link in links:
        linkURL = link.get('href')
        # A link should have an href tag and not be empty to be included 
        if linkURL != None and len(linkURL) != 0:
            # Check to see if result is unique to the domain
            if linkURL[0] == "/":
                #If it it is we request the websites for these as well.
            alreadyScrapedURLs.add(linkURL)

    # Handles JavaScript.
    srcs = soupify.findAll("script")
    for src in srcs:
        srcURL = src.get('src')
        # A script should have an src tag and not be empty to be included.
        if srcURL != None and len(srcURL) != 0:
            alreadyScrapedURLs.add(srcURL)

    
    # for line in webpage:
    #         line = line.decode().strip()
    #         # if domain in line:
    #         regexPattern = "href=\"(.*?)\""
    #         referencedUrls = re.findall(regexPattern, line)
    #         for scrapedURL in referencedUrls:
    #             # handles potential regex mistake of an empty string being found
    #             
    #             
    #             # since we handled the backslash only cases (/events), we can get rid of any URLs/strings that don't have the domain that snuck past
    #             if domain not in scrapedURL:
    #                 continue
    #             # You should record, but do not need to search, files that are likely to be media (.jpg, .png, .mp4, etc.)
    #             # Achieve this by splitting on periods and getting the potential file extension (which should be the last index of the list)
    #             mediaTest = scrapedURL.split(".")
    #             if mediaTest[len(mediaTest)-1] in websiteMediaExtensions:
    #                 mediaURLs.add(scrapedURL)
    #                 continue 
    #             alreadyScrapedURLs.add(scrapedURL)

    return alreadyScrapedURLs, mediaURLs



def main():
    allUrlsScraped = set()
    allMediaScraped = set()
    # "This web scraper will take three pieces of input:  a domain, a URL, and a depth."
    print("Please enter a domain and URL both including https://, and a depth all separated by spaces. i.e. https://www.rit.edu https://www.rit.edu 2")
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
    print(pageURLs)
    
if __name__ == "__main__":
    main()