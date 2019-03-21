'''
inf558 project
wrapper
Ruotian
template:
{
Name:
logo:
Address:
Phone:
Inf:
Open hours:
Type:
Special-Notes: [s1,s2,s3]
Menu : [{
	Date:
	Items:
	ItemName:
    Allergy:
	},
	{}
	...
	]
},
...
{
}
...

'''



import os
import lxml.etree
from lxml import html
import json
import glob


def cat(context, elements):
    return [''.join(e.xpath('.//text()')) for e in elements]


if not os.path.exists("results_MIT"):
    os.makedirs("results_MIT")

#  wrapper for MIT dining
output = []
for file in glob.glob('MIT_dining/*.html'):
    res = {}
    res['name'] = str(file).split('.')[0].split('/')[1]
    print(res)


for directory in os.listdir('MIT_dining'):
    cur_Type = directory
    for file in glob.glob('MIT_dining/' + directory + '/*.html'):
        ns = lxml.etree.FunctionNamespace(None)
        ns['concat-texts'] = cat
        res = {}
        res['name'] = str(file).split('.')[0].split('/')[2]
        context = open(file, "r")
        webpage = html.fromstring(context.read())
        logo = webpage.xpath('//img[@typeof="foaf:Image"]//@src')
        res['logo'] = 'Not Found' if not logo else logo[0]
        contact = repr(webpage.xpath('concat-texts(//div[@class="col-sm-9 col-md-8"]/div)')).replace('\\t','').split('\\n')
        contact = [i for i in contact if i!='' and i != "['"]
        for i in range(len(contact)-1):
            if contact[i] == 'Cuisine':
                res['Cuisine'] = contact[i+1]
            if contact[i] == 'Location' and contact[i+1] == 'Campus':
                res['Address'] = contact[i+2]
            if contact[i] == 'Location' and contact[i+1] != 'Campus':
                res['Address'] = contact[i + 1] + ', '  + contact[i +3]
            if contact[i] == 'Hours of Operation:':
                res['hours'] = contact[i+1].replace('Accepted Methods of Payment:','')


        res['menu'] = webpage.xpath('//div[@class="contact-btn"]/a[text()="Website "]/@href')
        if res['menu'] == []:
            res['menu'] = 'Not Found'
        else:
            res['menu'] = res['menu'][0]
        res['type'] = cur_Type
        inf = []
        if webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-4"]/p/strong'):
            for i in webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-4"]/p/strong'):
                inf.append(i.text)
        if webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-4"]/p/strong/p'):
            for i in webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-4"]/p/strong/p'):
                inf.append(i.text)
        if webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-8"]/p'):
            for i in webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-8"]/p'):
                inf.append(i.text)
        inf = ''.join(filter(None, inf))
        if inf:
            res['inf'] = inf
        else:
            res['inf'] = repr(webpage.xpath('//div[@class="dining-menu"]//div[@class="col-sm-4"]/p/strong//text()'))\
                .strip('[\']\"').strip('\\n')
        res['type'] = cur_Type
        print (res)
