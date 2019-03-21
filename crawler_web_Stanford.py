import scrapy
import urllib.request
import os

class QuotesSpider(scrapy.Spider):
    if not os.path.exists('Stanford_dining'):
        os.makedirs('Stanford_dining')
    name = "USC_Dining"
    start_urls = ['https://rde.stanford.edu/dining/locations-hours']
    def parse(self, response):
        if not os.path.exists('Stanford_dining/Dining_Hall'):
            os.makedirs('Stanford_dining/Dining_Hall')
        if not os.path.exists('Stanford_dining/Retail_Cafés'):
            os.makedirs('Stanford_dining/Retail_Cafés')
        flag = 0
        for store in response.xpath('//ul/li[not(@id) and not(@class)]/a'):
            if store.xpath('text()').extract() == ['Arrillaga\xa0Family Dining Commons']:
                flag = 1
            elif store.xpath('text()').extract() == ['Forbes Cafe']:
                flag = 2
            elif store.xpath('text()').extract() == ['Catering Menu'] or store.xpath('text()').extract() == ['Latenight\xa0at Lakeside']:
                flag = 0
            if flag == 1:
                print(store.xpath('@href').extract())
                print(store.xpath('text()').extract())
                if store.xpath('@href').extract() and 'https' in store.xpath('@href').extract()[0]:
                    urllib.request.urlretrieve(store.xpath('@href').extract()[0], "Stanford_dining/Dining_Hall/"
                                               + store.xpath('text()').extract()[0] + '.html')
                elif store.xpath('@href').extract():
                    urllib.request.urlretrieve('https://rde.stanford.edu' + store.xpath('@href').extract()[0], "Stanford_dining/Dining_Hall/"
                                               + store.xpath('text()').extract()[0] + '.html')
            if flag == 2:
                print(store.xpath('@href').extract())
                print(store.xpath('text()').extract())
                if store.xpath('@href').extract() and 'https' in store.xpath('@href').extract()[0]:
                    urllib.request.urlretrieve(store.xpath('@href').extract()[0], "Stanford_dining/Retail_Cafés/"
                                               + store.xpath('text()').extract()[0] + '.html')
                elif store.xpath('@href').extract():
                    # exception error
                    if store.xpath('text()').extract() == ['Forbes Cafe']:
                        urllib.request.urlretrieve('https://rde.stanford.edu/hospitality/forbes-family-caf%C3%A9',
                                                   "Stanford_dining/Retail_Cafés/Forbes Cafe.html")
                    elif store.xpath('text()').extract() == ['Med Cafe at\xa0LKSC']:
                        urllib.request.urlretrieve('https://rde.stanford.edu/hospitality/med-caf%C3%A9',
                                                   "Stanford_dining/Retail_Cafés/Med Cafe at\xa0LKSC.html")
                    else:
                        urllib.request.urlretrieve('https://rde.stanford.edu' + store.xpath('@href').extract()[0], "Stanford_dining/Retail_Cafés/"
                                               + store.xpath('text()').extract()[0]+ '.html')


