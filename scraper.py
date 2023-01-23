import urllib.request
import urllib.error
import queue
import threading
from bs4 import BeautifulSoup


allUrlsScraped = set()

def getReferenceUrlsOfPage(domain, url):
    try:
        webpage = urllib.request.urlopen(url)
        htmlURLs = set()
        javaScriptURLs = set()
        cssURLs = set()
        urlList = []
        # We want the urls to be on the same domain, so we check for the keyword.
        splitDomain = domain.split(".")

        soupify = BeautifulSoup(webpage, 'html.parser')

        # Handles hyperlinks in HTML
        hyperlinks = soupify.findAll("a")
        for hyperlink in hyperlinks:
            hyperlinkURL = hyperlink.get('href')
            # A link should have an href tag and not be empty to be included 
            if hyperlinkURL != None and len(hyperlinkURL) != 0:
                # We want the urls to be on the same domain, so we check for the keyword.
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in hyperlinkURL and splitDomain[0] == "www":
                # Check to see if result is unique to the domain (i.e. /event)
                    if hyperlinkURL[0] == "/" or hyperlinkURL[0] == "#":
                        #add domain to make a full url
                        hyperlinkURL = "https://" + domain + hyperlinkURL
                    htmlURLs.add(hyperlinkURL)

        # Handles JavaScript.
        srcs = soupify.findAll("script")
        for src in srcs:
            srcURL = src.get('src')
            # A script should have an src tag and not be empty to be included.
            if srcURL != None and len(srcURL) != 0:
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in srcURL and splitDomain[0] == "www":
                    if srcURL[0] == "/" or srcURL[0] == "#":
                        #add domain to make a full url
                        srcURL = "https://" + domain + srcURL
                    # don't add to javaScript set if its in HTML set already. No need for duplicates.
                    if srcURL in htmlURLs:
                        continue
                    javaScriptURLs.add(srcURL)

        # Handles CSS
        links = soupify.findAll("link")
        for link in links:
            linkURL = link.get("href")
            # A link should have an href tag and not be empty to be included.
            if linkURL != None and len(linkURL) != 0:
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in linkURL and splitDomain[0] == "www":
                    if linkURL[0] == "/" or linkURL[0] == "#":
                        #add domain to make a full url
                        linkURL = "https://" + domain + linkURL
                    # don't add to CSS set if its in HTML/javasScript. No need for duplicates.
                    if linkURL in htmlURLs or linkURL in javaScriptURLs:
                        continue
                    cssURLs.add(linkURL)

        # adding all the sets into a list to make return value easier to handle
        urlList.append(htmlURLs)
        urlList.append(javaScriptURLs)
        urlList.append(cssURLs)

        return urlList

    except urllib.error.HTTPError as e:
        print(url, "gave an http error", e)
        pass

    
def execute_queue(domain, url_queue):
    q_full = True
    while q_full:
        try:
            url = url_queue.get(False)
            urlLists = getReferenceUrlsOfPage(domain, url)
            # If it = None this indicates some HTTP error most likely happened. The thread/site crawl will not be ran.
            # Should NOT affect the program from running.
            # Right now there is a bug with creating urls with the first character starting with /
            # Lots of webpages scraped are also old and don't exist anymore. NOT BUG RELATED
            if urlLists == None:
                pass
            else:
                for urlList in urlLists:
                    for url in urlList:
                        allUrlsScraped.add(url)
        except queue.Empty:
            q_full = False

def write_to_file(urlList):
    file = open("URLs Scraped.txt", "a")
    for url in urlList:
        file.write(url + "\n")

def main():
    # "This web scraper will take three pieces of input:  a domain, a URL, and a depth."
    print("Please enter a domain, a URL including https://, and a depth all separated by spaces. i.e. www.rit.edu https://www.rit.edu 2")
    inputParams = input("Enter here: ")
    scraperParams = inputParams.split(" ")
    domain, url, depth = scraperParams[0], scraperParams[1], scraperParams[2]
    castDepth = int(depth)
    counter = 0

    while castDepth >= 0:
        # if its the first iteration we want to gather all the future urls from our initial input url
        if castDepth == int(depth):
            urlLists = getReferenceUrlsOfPage(domain, url)
            for urlList in urlLists:
                for url in urlList:
                    allUrlsScraped.add(url)
            print("Total Amount of URLs Scraped at depth " + str(counter) + " is " + str(len(allUrlsScraped)))
        else:
            # A queue handles all the locking and stuff in threading, easy to use
            q = queue.Queue()
            # Then we use the urls we scraped from the first url and then scrape those.
            iterableScapedUrls = list(allUrlsScraped)
            for url in iterableScapedUrls:
                # If the start of the spliced URL does not match the domain then it should be ignored.
                domainWithHttps = "https://" + domain
                splicedUrl = url[0:len(domainWithHttps)]
                if splicedUrl != domainWithHttps:
                    continue
                q.put(url)
                t = threading.Thread(target=execute_queue, args=(domain,q,))
                t.start()
                t.join()
            print("Total Amount of URLs Scraped at depth " + str(counter) + " is " + str(len(allUrlsScraped)))
        castDepth -= 1
        counter += 1
        write_to_file(allUrlsScraped)
    
    
if __name__ == "__main__":
    main()