import json
import os
import re

author_dic = {}
trans = []
country_dic = {}
country_list = []
country_thesis = []
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
            countries = author['affiliation']['location']['country'].split(' ')
            # 特殊字符的过滤， 双国籍
            for country in countries:
                country = ''.join(re.findall(r"[A-Za-z]", country))
                if not country in country_dic:
                    country_dic[country] = len(country_dic)
                    country_thesis.append([])
                country_thesis[country_dic[country]].append([file])
                # print(country, end=' ')
        if 'affiliation' in author and 'institution' in author['affiliation']:
            name = author['affiliation']['institution']
        else:
            name = 'Individual'
        name = ''.join(re.findall(r'[A-Za-z\ ]', name))
        name = name.strip()
        # print(name)
        if len(name) > 1:
            if not name in author_dic:
                author_dic[name] = len(author_dic)
                name_list.append(name)
            tmp_tran.add(author_dic[name])
    trans.append(list(tmp_tran))
    file_list.append(file)
    return
min_sup = 5

def subset(a, b):
    ret = []
    for ai in a:
        if is_subset(ai, b):
            ret.append(ai)
    return ret

def is_subset(a, b):
    f = 1
    for i in a:
        if not i in b:
            f = 0
    return f

def has_infrequent_subset(C, Lk, k):
    cnt = 0
    # print("has infrequent subset ", C, Lk)
    for l in Lk:
        if is_subset(l, C):
            cnt += 1
    # print("cnt ", cnt, k)
    if cnt != k:
        return 1
    return 0

def apriori_gen(Lk, k):
    Ck = []
    for l1 in Lk:
        for l2 in Lk:
            # print(l1, l2, k)
            if l1[0:k - 1] == l2[0:k - 1] and l1[k - 1] < l2[k - 1]:
                c = l1 + l2[k - 1: k]
                # print(c)
                if has_infrequent_subset(c, Lk, k + 1) == 0:
                    Ck.append(c)
    return Ck

def find_frequent_1_itemsets(D):
    count = [0] * len(name_list)
    L1 = []
    for d in D:
        for i in d:
            count[i] += 1
    for i in range(0, len(name_list)):
        if count[i] >= min_sup:
            L1.append([i])
    return L1

def to_string(cl):
    c = ""
    cl.sort()
    for ci in cl:
        c += str(ci)
    # print("to string", c)
    return c


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
# print(name_list)
# print(trans)
# [[I1, I2, I5], [I2, I4], [I2, I3], [I1, I2, I4], [I1, I3], [I2, I3], [I1, I3], [I1, I2, I3, I5], [I1, I2, I3]]
D = trans
L1 = find_frequent_1_itemsets(D)
print(L1)
print("D count is ", len(D))
# print("find_frequent", 1, L1)
Lk = L1
L = []
k = 1
while len(Lk) != 0:
    print("phase ", k)
    Ck = apriori_gen(Lk, k)
    print("    apriori generate finish")
    Lk = []
    # print("apriori gen ", Ck)
    count = {}
    candidate = []
    all_cand = []
    for t in D:
        candidate = subset(Ck, t)
        all_cand += candidate
    print("    subset find finish")
    cccc = 0
    for c in all_cand:
        cccc += 1
        if cccc % 10 == 0:
            print("    ", cccc)
        cs = to_string(c)
        if not cs in count:
            count[cs] = 0
        count[cs] += 1
        if count[cs] == min_sup:
            L.append(c)
            Lk.append(c)
    k += 1
    # print("find_frequent", k, Lk)
# print(L)
print(len(trans), len(file_list))
f = open("preprogress.out", "w")
for l in L:
    fl = 1
    for t in l:
        if name_list[t] == "Individual":
            fl = 0
            break
    if fl == 0:
        continue
    for t in l:
        f.write(name_list[t] + ' | ')
    f.write('\n')
    for i in range(len(file_list)):
        fl = 0
        for ti in trans[i]:
            if ti in l:
                fl = 1
                break
        if fl == 1:
            f.write(file_list[i] + ' ')
    f.write('\n')
    
f.close()