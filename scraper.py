import urllib.request
import urllib.error
import queue
import threading
from bs4 import BeautifulSoup


allUrlsScraped = set()

def getReferenceUrlsOfPage(domain, url):
    try:
        webpage = urllib.request.urlopen(url)
        # We want the urls to be on the same domain, so we check for the keyword.
        splitDomain = domain.split(".")
        httpsDomain = "https://" + domain

        soupify = BeautifulSoup(webpage, 'html.parser')

        # Handles hyperlinks in HTML
        hyperlinks = soupify.findAll("a")
        for hyperlink in hyperlinks:
            hyperlinkURL = hyperlink.get('href')
            if hyperlinkURL == "//www.rit.edu/photonics/":
                print()
            # A link should have an href tag and not be empty to be included 
            if hyperlinkURL != None and len(hyperlinkURL) != 0:
                # We want the urls to be on the same domain, so we check for the keyword.
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in hyperlinkURL:
                # Check to see if result is unique to the domain (i.e. /event)
                    if hyperlinkURL[0] == "/" or hyperlinkURL[0] == "#":
                        # There was a bug where the domain would repeat twice since some urls started with a // making them /domain.
                        # This fixes it
                        if hyperlinkURL[:2] == "//":
                            #If this is the case, only need to add HTTPS. Not domain too.
                            hyperlinkURL = "https://" + hyperlinkURL[2:len(hyperlinkURL)]
                        #gets rid of potential duplicates. i.e. https://www.rit.edu/ vs https://www.rit.edu
                        elif hyperlinkURL[len(hyperlinkURL)-1] == "/":
                            hyperlinkURL = hyperlinkURL[:len(hyperlinkURL)-1]
                        else:
                            #add domain and https to make a full url
                            hyperlinkURL = httpsDomain + hyperlinkURL
                    # If the start of the spliced URL does not match the domain then it should be ignored.
                    if hyperlinkURL[:len(httpsDomain)] == httpsDomain:
                        allUrlsScraped.add(hyperlinkURL.strip())

        # Handles JavaScript.
        srcs = soupify.findAll("script")
        for src in srcs:
            srcURL = src.get('src')
            # A script should have an src tag and not be empty to be included.
            if srcURL != None and len(srcURL) != 0:
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in srcURL:
                    if srcURL[0] == "/" or srcURL[0] == "#":
                        # There was a bug where the domain would repeat twice since some urls started with a / making them /domain.
                        # This fixes
                        if srcURL[:2] == "//":
                            #If this is the case, only need to add HTTPS. Not domain too.
                            srcURL = "https://" + srcURL[2:len(srcURL)]
                        #gets rid of potential duplicates. i.e. https://www.rit.edu/ vs https://www.rit.edu
                        elif srcURL[len(srcURL)-1] == "/":
                            srcURL = srcURL[:len(srcURL)]
                        else:
                            #add domain and https to make a full url
                            srcURL = httpsDomain + srcURL
                    # No need for duplicates. Failsafe
                    if srcURL in allUrlsScraped:
                        continue
                    # If the start of the spliced URL does not match the domain then it should be ignored.
                    if srcURL[:len(httpsDomain)] == httpsDomain:
                        allUrlsScraped.add(srcURL.strip())

        # Handles CSS
        links = soupify.findAll("link")
        for link in links:
            linkURL = link.get("href")
            # A link should have an href tag and not be empty to be included.
            if linkURL != None and len(linkURL) != 0:
                #In theory it should always be in the 1st spot since www (DOT) domainName (DOT) com
                if splitDomain[1] in linkURL:
                    if linkURL[0] == "/" or linkURL[0] == "#":
                        # There was a bug where the domain would repeat twice since some urls started with a / making them /domain.
                        # This fixes
                        if linkURL[:2] == "//":
                            #If this is the case, only need to add HTTPS. Not domain too.
                            linkURL = "https://" + linkURL[2:len(linkURL)]
                        #gets rid of potential duplicates. i.e. https://www.rit.edu/ vs https://www.rit.edu
                        elif linkURL[len(linkURL)-1] == "/":
                            linkURL = linkURL[:len(linkURL)]
                        else:
                            #add domain and https to make a full url
                            linkURL = httpsDomain + linkURL
                    # No need for duplicates. Failsafe
                    if linkURL in allUrlsScraped:
                        continue
                    # If the start of the spliced URL does not match the domain then it should be ignored.
                    if linkURL[:len(httpsDomain)] == httpsDomain:
                        allUrlsScraped.add(linkURL.strip())

    except urllib.error.HTTPError as e:
        print(url, "gave an http error", e)
        pass

    
def execute_queue(domain, url_queue):
    q_full = True
    while q_full:
        try:
            url = url_queue.get(False)
            getReferenceUrlsOfPage(domain, url)
        except queue.Empty:
            q_full = False

def write_to_file(urlList):
    #I keep getting a duplicate https://www.rit.edu/ so this is a last resort method of fixing it.
    urlsUsed = set()
    file = open("URLs Scraped.txt", "a")
    for url in urlList:
        if url not in urlsUsed:
            file.write(url + "\n")
            urlsUsed.add(url)

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
            getReferenceUrlsOfPage(domain, url)
            print("Total Amount of URLs Scraped at depth " + str(counter) + " is " + str(len(allUrlsScraped)))
        else:
            # A queue handles all the locking and stuff in threading, easy to use
            q = queue.Queue()
            # Then we use the urls we scraped from the first url and then scrape those.
            iterableScapedUrls = list(allUrlsScraped)
            for url in iterableScapedUrls:
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