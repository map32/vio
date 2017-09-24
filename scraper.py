from bs4 import BeautifulSoup
import re, urllib2, time

def scrape(d, n): # d is a date format
    soup = BeautifulSoup(link(d,1),'html.parser')
    pages = int(soup.find(string=re.compile('\d of')).split()[-1])
    count = (pages-1)*14+1
    vios = []
    i = 0
    f = open('vios','w+')
    while len(vios) < n or count < 1:
        time.sleep(0.3)
        html = link(d,count)
        if html=='error':
            continue
        soup = BeautifulSoup(html,'html.parser')
        ns = soup.find_all(string=re.compile('\A\d{8}[A-Z]\Z'))
        ds = soup.find_all(string=re.compile('\A\d\d/\d\d/\d\d\d\d\Z'))
        for i in range(0,min(len(ds),len(ns))):
            #print ns[i]+' '+ds[i]
            print 'checking violation '+ns[i]+' from '+ds[i]+'...'
            info = scrapeone(ns[i],ds[i])
            if 'error' not in info:
                print ns[i]+' is a valid violation, adding to the list.'
                f.write(info['name']+'<|>')
                f.write(info['address']+'<|>')
                f.write(info['desc']+'<|>')
                f.write(info['vid']+'<|>')
                f.write(info['date']+'<|>')
                f.write(info['data']+'<|>')
                with open('dat/'+ds[i].replace('/','-'),'a+') as g:
                    g.write(ns[i]+'\n')
                vios.append(info)
                print str(len(vios))+' violations added so far.'
                if len(vios)>=n:
                    break
            else:
                if info['error'] == 'irrelevant':
                    print ns[i]+' is not relevant to our search, skipping.'
                elif info['error'] == 'duplicate':
                    print ns[i]+' was already found before, skipping.'
                elif info['error'] == 'html error':
                    print ns[i]+' unknown html error was found, skipping.'
        count -= 14
    f.close()
    return vios

def scrapeone(num, date):
    error= {'error':'irrelevant'}
    info = {}
    date = date.replace('/','-')
    with open('dat/'+date,'a+') as f:
        f.seek(0)
        for n in f:
            #print 'file: '+n[:-1]+' '+num
            if num == n[:-1]:
                #print 'vio id already found'
                error['error'] = 'duplicate'
                return error
    time.sleep(0.3)
    html = linki(num)
    if html=='error':
        return {'error':'html error'}
    soup = BeautifulSoup(html,'html.parser')
    name = soup.find_all(name='td',class_='content',colspan=3)[0].get_text()
    address = soup.find_all(name='td',class_='content',colspan=5)[0].get_text()
    desc = soup.find_all(name='td',class_='content',colspan=6)[1].get_text()
    code = soup.find_all(name='td',class_='content',bgcolor='#eoeoeo')[0].get_text()
    division = soup.find_all(name='td',class_='content',colspan=2)[4].get_text()
    certstatus = soup.find_all(name='td',class_='content',colspan=2)[0].get_text()
    hearstatus = soup.find_all(name='td',class_='content',colspan=2)[1].get_text()
    #print '\n'
    #print name
    #print address
    #print desc
    #print code
    #print division
    #print certstatus
    #print hearstatus
    
    if code not in ['28-301.1','28-302.1','28-105.1'] or division == 'ELECTRICAL DIVISION' or certstatus != 'NO COMPLIANCE RECORDED' or hearstatus != 'PENDING':
        #print '\n'+'error wrong type of thing'+'\n'
        info = error
        with open('dat/'+date,'a+') as f:
            f.write(num+'\n')
    else:
        info['name'] = name
        info['address'] = address
        info['desc'] = desc
        info['vid'] = num
        info['date'] = date
        info['data'] = html.strip()
        #print '\n'+num+'successfully added to vios'
    return info

#scrape one -> name, address, desc, id or error



def link(d, c):
    s = 'http://a810-bisweb.nyc.gov/bisweb/ECBBrowseByDateTypeServlet?allcount='+str(c).zfill(4)+'&allviolationtype=CN&allstartdate_month='+str(d.month).zfill(2)+'&allstartdate_year='+str(d.year)+'&allstartdate_day='+str(d.day).zfill(2)+'&allenddate_month=99&allenddate_year=9999&allenddate_day=99'
    try:
        req = urllib2.Request(s)
        res = urllib2.urlopen(req)
    except HTTPError:
        return 'error'
    a = res.info()
    #print a
    if a.get('Pragma') == 'no-cache':
        #print 'redirect'
        time.sleep(5)
        s = link(d,c)
        return s
    s = res.read()
    #print s
    return s

def linki(n):
    try:
        req = urllib2.Request('http://a810-bisweb.nyc.gov/bisweb/ECBQueryByNumberServlet?ecbin='+str(n))
        res = urllib2.urlopen(req)
    except urllib2.HTTPError:
        return 'error'
    a = res.info()
    #print a
    if a.get('Pragma') == 'no-cache':
        #print 'redirect'
        time.sleep(5)
        return linki(n)
    s = res.read()
    #print s
    return s
