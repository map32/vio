import scraper, cui, makeprint
from datetime import date, timedelta

def main():
    #sdate = date.today()-timedelta(days=30)
    #vios = scraper.scrape(sdate, 60)
    vios = []
    while True:
        s = raw_input('start searching or check saved violations? 1 for search, 2 for checking out (type q to quit)\n')
        if s=='2':
            try:
                i=0
                f = open('vios','r')
                line = f.read()
                line = line.split('<|>')[:-1]
                print line
                while i < len(line):
                    v = {}
                    v['name']=line[0+i]
                    v['address']=line[1+i]
                    v['desc']=line[2+i]
                    v['vid']=line[3+i]
                    v['date']=line[4+i]
                    v['data']=line[5+i]
                    vios.append(v)
                    i+=6
                f.close()
            except IOError:
                print('no saved file.')
                s = raw_input('how much violations should be found\n')
                sdate = date.today()-timedelta(days=30)
                vios = scraper.scrape(sdate, int(s))
            break
        elif s=='1':
            s = raw_input('how much violations should be found\n')
            sdate = date.today()-timedelta(days=30)
            vios = scraper.scrape(sdate, int(s))
            break
        elif s=='q':
            return
        else:
            print 'invalid input.'
    vios = cui.initialize(vios)
    print('creating address labels..')
    makeprint.addressLabels(vios)
    print('address labels created.\ncreating violation pdfs...')
    makeprint.violationPdfs(vios)
    print('violation pdfs created. Done!')
    #with open('vios','w+') as f:
    #    for v in vios:
    #        f.write(v.name)
    #        f.write(v.address)
    #        f.write(v.desc)
    #        f.write(v.vid)
    #        f.write(v.date)
    

if __name__ == '__main__':
    main()
