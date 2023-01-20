import urllib.request
import re
import random


def getReferenceUrlsOfPage(domain, url):
    webpage = urllib.request.urlopen(url)
    alreadyScrapedURLs = set()
    websiteMediaExtensions = ["jpg", "png", "mp3", "mp4", "pdf", "mov"]
    mediaURLs = set()
    for line in webpage:
            line = line.decode().strip()
            if domain in line:
                regexPattern = "href=\"(.*?)\""
                referencedUrls = re.findall(regexPattern, line)
                for scrapedURL in referencedUrls:
                    # handles potential regex mistake of an empty string being found
                    if len(scrapedURL) == 0:
                        continue
                    # Skips scanning the same website
                    if scrapedURL == url or scrapedURL == url + "/":
                        continue
                    #goes to the page associated with the domain (i.e. /events leads to www.rit.edu/events)
                    if scrapedURL[0] == "/":
                        scrapedURL = "https://" + domain + scrapedURL
                    # since we handled the backslash only cases (/events), we can get rid of any URLs/strings that don't have the domain that snuck past
                    if domain not in scrapedURL:
                        continue
                    # You should record, but do not need to search, files that are likely to be media (.jpg, .png, .mp4, etc.)
                    # Achieve this by splitting on periods and getting the potential file extension (which should be the last index of the list)
                    mediaTest = scrapedURL.split(".")
                    if mediaTest[len(mediaTest)-1] in websiteMediaExtensions:
                        mediaURLs.add(scrapedURL)
                        continue 
                    alreadyScrapedURLs.add(scrapedURL)

    return alreadyScrapedURLs, mediaURLs

def main():
    allUrlsScraped = set()
    allMediaScraped = set()
    # "This web scraper will take three pieces of input:  a domain, a URL, and a depth."
    print("Please enter a domain, a URL including https://, and a depth all separated by spaces. i.e. www.rit.edu https://www.rit.edu 2")
    inputParams = input("Enter here: ")
    scraperParams = inputParams.split(" ")
    domain, url, depth = scraperParams[0], scraperParams[1], scraperParams[2]
    depth = int(depth)
    while depth >= 0:
        pageURLs, pageMedia = getReferenceUrlsOfPage(domain, url)
        for url in pageURLs:
            allUrlsScraped.add(url)
        for media in pageMedia:
            allMediaScraped.add(media)
        print(url + " " + str(depth))
        url = random.sample(allUrlsScraped, 1)[0]
        depth -= 1
    # print(len(allUrlsScraped))
    # print(len(allMediaScraped))
    print(allUrlsScraped)
    
if __name__ == "__main__":
    main()