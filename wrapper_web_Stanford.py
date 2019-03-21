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


if not os.path.exists("results_Stanford"):
    os.makedirs("results_Stanford")

#  wrapper for Stanford dining
output = []


for directory in os.listdir('Stanford_dining'):
    cur_Type = directory
    for file in glob.glob('Stanford_dining/' + directory + '/*.html'):
        ns = lxml.etree.FunctionNamespace(None)
        ns['concat-texts'] = cat
        res = {}
        res['name'] = str(file).split('.')[0].split('/')[2]
        context = open(file, "r")
        webpage = html.fromstring(context.read())
        logo = webpage.xpath('//div[@class="field-items"]//img//@src')
        res['logo'] = 'Not Found' if not logo else logo[0]
        res['type'] = cur_Type
        contact = repr(webpage.xpath('concat-texts(//div[@class="panel"]//p[@class="rtecenter"])')).replace('\\t', '').split(
            '\\n')
        print (contact)
        contact = repr(webpage.xpath('concat-texts(//div[@class="node-content"]//p)')).replace('\\t', '').split(
            '\\n')
        print(contact)
        print(res['name'])
        # print (res)
