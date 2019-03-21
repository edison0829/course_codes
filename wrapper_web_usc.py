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


if not os.path.exists("results_usc"):
    os.makedirs("results_usc")
# wrapper for usc dining
output = []
for directory in os.listdir('usc_dining'):
    cur_Type = directory
    for file in glob.glob('usc_dining/' + directory + '/*.html'):
        ns = lxml.etree.FunctionNamespace(None)
        ns['concat-texts'] = cat
        print(file)
        res = {}
        res['name'] = str(file).split('.')[0].split('/')[2]
        context = open(file, "r")
        webpage = html.fromstring(context.read())
        res['logo'] = webpage.xpath('//img[@class="logo-image center-block"]//@src')[0]
        # res['address'] = [x.text if x.text else None for x in webpage.xpath('//div[@class="fw-tile-content"]/p')]
        contact = repr(webpage.xpath('concat-texts(//div[@class="fw-tile-content"]/p)'))
        if len(contact) == 2:
            contact = repr(webpage.xpath('concat-texts(//p[@class="contact-info"])'))
            opentime = repr(webpage.xpath('concat-texts(//p/span[@class="dining-details-hours"])'))
            res['phone'] = contact.split(':')[1].strip('\'] ')
            res['address'] = 'Not Found'
            res['menu'] = 'Not Found'
            res['hours'] = opentime
        else:
            menu = webpage.xpath('//div[@class="fw-tile-content"]/form/@action')
            if len(menu) == 0:
                res['menu'] = 'Not Found'
            else:
                res['menu'] = menu[0]
            contact = contact.split('\', \'')
            res['phone'] = contact[0].split('Phone:')[1].replace('\\n',' ').replace('\\t','')
            res['address'] = contact[0].split('Phone:')[0].strip('[\'').replace('\\n',' ').replace('\\t\\t\\t\\t',' ').replace('\\t','')
            res['hours'] = contact[2].strip(']\'')
        res['type'] = cur_Type
        res['inf'] = webpage.xpath('//div[@class="fw-col-xs-12 fw-col-sm-8"]/p')[0].text
        output.append(res)
        print (res)
with open("results_usc/usc_dining.json", 'w') as outfile:
    json.dump(output, outfile, indent=4)
outfile.close()