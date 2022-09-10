import json
import os
import re
import name2code
import code2continent

author_dic = {}
trans = []
country_thesis = {}
name_list = []
file_list = []

def preprocess(f, file):
    jsonf = json.load(f)
    # print(jsonf['metadata']['authors'])
    authors = jsonf['metadata']['authors']
    tmp_tran = set()
    for author in authors:
        if 'affiliation' in author and 'location' in author['affiliation'] and 'country' in author['affiliation']['location']:
            # print(author['affiliation']['location']['country'])
            # print(author['affiliation']['location']['country'])
            countries = author['affiliation']['location']['country'].split(",")
            # # 特殊字符的过滤， 双国籍
            for country in countries:
                country = ''.join(re.findall(r"[A-Za-z ]", country)).strip()
                # print("|"+country+"|")
                code = name2code.name2code(country)
                if code == 'Unknown':
                    continue
                continent = code2continent.convert_country_alpha2_to_continent(code)
                if not continent in country_thesis:
                    country_thesis[continent] = []
                country_thesis[continent].append(file)
                # print(" ------------ ")
                # country_thesis[country_dic[country]].append([file])
        # print(name)
    return

path = "D:\\pdf_json"
files = os.listdir(path)
cnt = 0
for file in files:
    cnt += 1
    if cnt % 500 == 0:
        print(cnt)
    if cnt == 30000:
        break
    if not os.path.isdir(file):
        f = open(path + "/" + file)
        preprocess(f, file)
fw = open("preprogress2.out", "w")
for key in country_thesis:
    fw.write(key + '\n')
    for f in country_thesis[key]:
        fw.write(f + '\n')
    fw.write('\n\n')