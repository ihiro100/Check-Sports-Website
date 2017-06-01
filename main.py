import re
import urllib2
from bs4 import BeautifulSoup
from threading import Thread
import requests

def add_http(sites):
    i = 0
    for site in sites:
        if site[:4] != 'http':
            sites[i] = 'http://' + str(site)
        i += 1
    return sites
def download(url):
    print 'Downloading:', url
    #request = urllib2.Request(url, headers={'User-Agent': 'my-app/0.0.1'})
    try:
        print 'iam doing'
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
    html = None

def downloadd(url):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        html = None
        if e.reason:
            html = requests.get(url, headers={'User-Agent': 'my-app/0.0.1'}).text
    return html

def S_meta(soup,sports):
    title = soup.title.string.lower()
    for sport in sports:
        if title.find(sport) > -1:
            return sport
    L_tags = soup.find_all('meta')
    print L_tags
    for tag in L_tags:
        tag = tag.__str__().lower()
        for sport in sports:
            if tag.find(sport) > -1:
                return sport
    return None

def start_crawl(site,sports,data):
    html = download(site)
    if html == None:
        return 0
    flg = 0
    for s in sports:
        if site.lower().find(s) > -1:
            flg = s
            break
    if flg == 0:
        soup = BeautifulSoup(html)
        flg = S_meta(soup, sports)
    if flg != None:
        a = str(site) + ' --> ' + flg + '\n'
        print a
        data.append(a)
    else:
        a = str(site) + ' --> ' + 'NA' + '\n'
        print a
        data.append(a)


if __name__ == '__main__':
    file = open(raw_input('enter filename :'))
    sites = file.read().split()
    file.close()
    file = open('sports.txt')
    sports = file.read().split('\n')
    file.close()
    data = []
    t_list = []
    sites = add_http(sites)
    file = open('op.txt', 'w')
    for u in sites:
        start_crawl(u,sports,data)


    for site in sites:
        t = Thread(target=start_crawl, name=site, args=(site ,sports, data,))
        t.start()
        t_list.append(t)
    for b in t_list:
        b.join()
    for d in data:
        file.write(d)
    print 'output file has been saved in op.txt'
    file.close()
