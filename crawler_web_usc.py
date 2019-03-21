import scrapy
import urllib.request
import os

class QuotesSpider(scrapy.Spider):
    if not os.path.exists('usc_dining'):
        os.makedirs('usc_dining')
    name = "USC_Dining"
    start_urls = ['https://hospitality.usc.edu/dining-locations/']
    def parse(self, response):
        noisy = ['Hours','Farmers\' Market','Locations','Dining Map','Annenberg Cart','Soto St. Café' ]
        keys = ['Full Service Restaurants', 'Quick Service Restaurants (UPC)', 'Quick Service Restaurants (HSC)',
                'Residential Dining']
        d = {}
        for store in response.xpath('//ul[@class = "sub-menu"]/li[@id = "menu-item-225"]/ul[@class = "sub-menu"]'):
            urls = store.xpath('//li/a/@href').extract()[5:-50]
            # print (course.xpath('//tr//a/text()').extract())
            labels = store.xpath('//li/a/text()').extract()[5:-50]
            # print (cur.xpath('text()').extract()[0])
            # print ("https://www.registrar.ucla.edu"+course.xpath("@href").extract()[0])
            cur = []
            k = ''
            for i in range(len(labels)):
                if labels[i] not in noisy:
                    if keys and labels[i] == keys[0]:
                        if k != '':
                            d[k] = cur
                        cur = []
                        k = keys.pop(0)
                        continue
                    cur.append([urls[i],labels[i]])
            d[k] = cur
            for key, value in d.items():
                if not os.path.exists("usc_dining/"+key):
                    os.makedirs("usc_dining/"+key)
                for v in value:
                    print (v)
                    urllib.request.urlretrieve(v[0],"usc_dining/" +key + "/" + v[1]+".html")