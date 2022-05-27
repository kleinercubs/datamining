from operator import concat
from tkinter import N
import csv

min_sup = 0.01
min_conf = 0.5
dic = {}
dic_cnt = 0
dic_word = []

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
    global dic_cnt
    count = [0] * dic_cnt
    L1 = []
    for d in D:
        for i in d:
            count[i] += 1
    for i in range(0, dic_cnt):
        if count[i] / len(D) >= min_sup:
            L1.append([i])
    return L1

def to_string(cl):
    c = ""
    cl.sort()
    for ci in cl:
        c += str(ci)
    # print("to string", c)
    return c

def GetInput(path):
    global dic_cnt
    f = open(path)
    out = []
    for l in f.readlines():
        l = l[:-1]
        concept = l.split(' ')
        # print(concept)
        trans = []
        for c in concept:
            if not c in dic:
                dic[c] = dic_cnt
                dic_cnt += 1
                dic_word.append(c)
            trans.append(dic[c])
        out.append(trans)
    return out

def calc_sup(l, D):
    sup = 0
    for d in D:
        if set(l).issubset(set(d)):
            sup += 1
    return sup / len(D)

def calc_sup_2(l, l2, D):
    sup = 0
    for d in D:
        if set(l).issubset(set(d)) and not set(l2).issubset(set(d)):
            sup += 1
    return sup

rulelist = []
def gen_rule(l, l1, i, D):
    if i == len(l):
        conf = calc_sup(l, D) / calc_sup(l1, D)
        if len(l1) > 0 and len(l1) != len(l) and conf >= min_conf:
            rulelist.append([l1, list(set(l) - set(l1)), conf])
        return 
    gen_rule(l, l1 + [l[i]], i + 1, D)
    gen_rule(l, l1, i + 1, D)

def calcLift(a, b, D):
    n = len(D)
    # print(a + b, a, b)
    return (calc_sup(a + b, D)) / ((calc_sup(a, D)) * (calc_sup(b, D)))

def calcAllConf(a, b, D):
    return calc_sup(a + b, D) / max(calc_sup(a, D), calc_sup(b, D))

def calcKulc(a, b, D):
    n = calc_sup(a + b, D)
    return 0.5 * (n / calc_sup(a, D) + n / calc_sup(b, D))

def calcChi(a, b):
    return (b - a) ** 2 / a

def calcChiSquared(a, b, D):
    n = len(D)
    pa = calc_sup(a, D)
    pb = calc_sup(b, D)
    # print(a,   b)
    nab = calc_sup(a + b, D) * n
    eab = n * pa * pb
    enab = (n * (1 - pa) * pb)
    eanb = (n * (1 - pb) * pa)
    enanb = (n * (1 - pa) * (1 - pb))
    # print(eab, enab, eanb, enanb)
    return calcChi(eab, nab) + calcChi(enab, calc_sup_2(b, a, D)) \
        +  calcChi(eanb, calc_sup_2(a, b, D)) + calcChi(enanb, n - nab)

def calcIR(a, b, D):
    na = calc_sup(a, D)
    nb = calc_sup(b, D)
    return abs(na - nb) / (na + nb - calc_sup(a + b, D))

# [[I1, I2, I5], [I2, I4], [I2, I3], [I1, I2, I4], [I1, I3], [I2, I3], [I1, I3], [I1, I2, I3, I5], [I1, I2, I3]]
D = GetInput('./concept_records.txt')
L1 = find_frequent_1_itemsets(D)
# print("find_frequent", 1, L1)
Lk = L1
L = []
k = 1
min_sup_count = int(min_sup * len(D))
while len(Lk) != 0:
    Ck = apriori_gen(Lk, k)
    Lk = []
    # print("apriori gen ", Ck)
    count = {}
    candidate = []
    all_cand = []
    for t in D:
        candidate = subset(Ck, t)
        all_cand += candidate
    for c in all_cand:
        cs = to_string(c)
        if not cs in count:
            count[cs] = 0
        count[cs] += 1
        if count[cs] == min_sup_count:
            L.append(c)
            Lk.append(c)
    k += 1
    # print("find_frequent", k, Lk)
# for l in L:
#     for l2 in L:
#         if l != l2 and set(l).issubset(set(l2)):
#             L.remove(l)
#             break
for l in L:
    for li in l:
        print(dic_word[li], end=" ")
    print('')

for l in L:
    gen_rule(l, [], 0, D)

f = open("out.csv", "w")
writer = csv.writer(f)
writer.writerow(['', 'Left', 'Right', 'Conf', 'Lift', 'ChiSquared', 'AllConf', 'Kulc', 'IR'])
cnt = 0
for rule in rulelist:
    sa = ''
    for r in rule[0]:
        # print(dic_word[r], end=' ')
        sa += dic_word[r] + ' '
    # print("  ===>  ", end='')
    sb = ''
    for r in rule[1]:
        # print(dic_word[r], end=' ')
        sb += dic_word[r] + ' '
    # print("    conf = ", rule[2], end=' ')
    # print("    lift = ", calcLift(rule[0], rule[1], D), end=' ')
    # print("    chis = ", calcChiSquared(rule[0], rule[1], D), end=' ')
    # print("    allconf = ", calcAllConf(rule[0], rule[1], D), end=' ')
    # print("    kulc = ", calcKulc(rule[0], rule[1], D), end=' ')
    # print("    IR = ", calcIR(rule[0], rule[1], D))
    writer.writerow([cnt, sa, sb, rule[2], calcLift(rule[0], rule[1], D), calcChiSquared(rule[0], rule[1], D), \
        calcAllConf(rule[0], rule[1], D), calcKulc(rule[0], rule[1], D), calcIR(rule[0], rule[1], D)])
    cnt += 1
for l1 in L[0:30]:
    for l2 in L[0:30]:
        sa = ''
        for r in l1:
            # print(dic_word[r], end=' ')
            sa += dic_word[r] + ' '
        # print("  ===>  ", end='')
        sb = ''
        for r in l2:
            # print(dic_word[r], end=' ')
            sb += dic_word[r] + ' '
        if l1 != l2:
            writer.writerow([cnt, sa, sb, calc_sup(l1+l2, D) / calc_sup(l1, D), calcLift(l1, l2, D), calcChiSquared(l1, l2, D), \
                calcAllConf(l1, l2, D), calcKulc(l1, l2, D), calcIR(l1, l2, D)]) 
            cnt += 1