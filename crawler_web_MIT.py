import scrapy
import urllib.request
import os

class QuotesSpider(scrapy.Spider):
    if not os.path.exists('MIT_dining'):
        os.makedirs('MIT_dining')
    name = "MIT_Dining"
    start_urls = ['https://studentlife.mit.edu/dining/residential-dining']
    def parse(self, response):
        print (response.request.url)
        if 'residential-dining' in str(response.request.url):
            urllib.request.urlretrieve(response.request.url, "MIT_dining/"+"residential-dining.html")

        elif 'retail-dining' in str(response.request.url):
            if not os.path.exists('MIT_dining/retail-dining'):
                os.makedirs('MIT_dining/retail-dining')
            for store in response.xpath('.//li[contains(@class, "leaf menu-mlid-") and contains(@class ,"level-4")]/a'):
                print (store.xpath('@href').extract()[0])
                print (store.xpath('text()').extract()[0])
                urllib.request.urlretrieve('https://studentlife.mit.edu'+ store.xpath('@href').extract()[0], "MIT_dining/retail-dining/"
                                           + store.xpath('text()').extract()[0]+'.html')
        elif 'catering' in str(response.request.url):
            keys = ['Alpine Catering (Dunkin\' Donuts and Cambridge Grill)', 'Anna\'s Taqueria', 'Bon Appétit',
                     'LaVerde\'s Market', 'Pacific St. Café']
            if not os.path.exists('MIT_dining/catering'):
                os.makedirs('MIT_dining/catering')
            for store in response.xpath('//ul/li[not(@id) and not(@class)]/a'):
                if store.xpath('@href').extract() and store.xpath('text()').extract() and store.xpath('text()').extract()[0] in keys:
                    print(store.xpath('@href').extract()[0])
                    print(store.xpath('text()').extract()[0])
                    urllib.request.urlretrieve(store.xpath('@href').extract()[0], "MIT_dining/catering/"
                                               + store.xpath('text()').extract()[0]+'.html')
        next_page = response.xpath('.//li[@class="collapsed menu-mlid-1822 level-3"]/a/@href').extract()
        if not next_page:
            next_page = response.xpath('.//li[@class="last leaf menu-mlid-1823 level-3"]/a/@href').extract()
        print (next_page)
        if next_page:
            print ('aaa')
            next_page_url = 'https://studentlife.mit.edu' + next_page[0]
            yield response.follow(next_page_url, self.parse)
