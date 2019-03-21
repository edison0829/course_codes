


import os
from lxml import html
import json
import glob

if not os.path.exists("results"):
    os.makedirs("results")
for file in glob.glob('data/*.html'):
    name = str(file).split('.')[0].split('/')[1]
    context = open(file, "r")
    webpage = html.fromstring(context.read())
    courses = [x.text if x.text else '' for x in webpage.xpath('//div[@class="media-body"]/h3')]
    infs = [x.text if x.text else '' for x in webpage.xpath('//div[@class="media-body"]/p')]
    sub_out = []
    print (name)
    print (len(courses))
    print (len(infs))
    for i in range(0,len(infs),2):
        details = {"course number & title":courses[int(i/2)],"Number of units": infs[i], "Course description": infs[i+1]}
        sub_out.append(details)
    output = {"subject": name, "courses":sub_out}
    # output = json.dumps(output, indent=4)
        # for course in webpage.xpath('//div[@class="media-body"]/h3'):
    #     # print(ElementTree.tostring(course.xpath('/h3'), encoding='utf8', method='xml'))
    #     details = {}
    #     values = [e.text_content() for e in course]
    #     print  (course.xpath('//h3/text()'))
    #     # print (ElementTree.tostring(course.xpath('//h3'), encoding='utf8', method='xml'))
    #     # print (course.text_content().tostring())
    with open("results/" + name + ".json", 'w') as outfile:
        json.dump(output, outfile, indent=4)