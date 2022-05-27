from html import entities
from nis import cat

catalog_dic = {}
entities_dic = {}
entities_list = []
dim_num = 5

def calc_dis(a, b):
    dis = len(a)
    for i in a:
        if i in b:
            dis -= 1
    return dis / (len(a))

def Distribute_cluster(KPoint, N, M, K):
    for k1 in KPoint:
        for k2 in KPoint:
            if k2 != [len(catalog_dic) - 1] and k1 != k2 and len(k1) > 0 and len(k2) > 0:
                if calc_dis(k1, k2) <= 0.5:
                    print("remove")
                    k2.clear()
    cluster_id = [0] * N
    cluster_list = set([])
    for i in range(len(entities_list)):
        cluster_list.add(cluster_id[i])
    new_cluster = []
    for i in range(K):
        if not i in cluster_list:
            new_cluster.append(i)
    for i in range(N):
        id = 0
        min_dis = M
        for k in range(K):
            if len(KPoint[k]) == 0:
                continue
            k_dis = calc_dis(KPoint[k], entities_list[i])
            if k_dis < min_dis:
                min_dis = k_dis
                id = k
        if min_dis > 0.8 and len(new_cluster) > 0:
            cluster_id[i] = new_cluster[0]
            new_cluster.remove(new_cluster[0])
        else:
            cluster_id[i] = id
    return cluster_id

def Calc_center(cluster_id, N, K):
    centers = [[len(catalog_dic) - 1]]
    # print(cluster_id)
    for k in range(1, K):
        cnt = [0] * len(catalog_dic)
        # tot_cnt = 0
        center = []
        for i in range(N):
            if cluster_id[i] == k:
                # tot_cnt += 1
                for c in entities_list[i]:
                    cnt[c] += 1
        # threshold = int(tot_cnt / 2)
        # print(cnt)
        num = list(range(len(catalog_dic)))
        # print(len(cnt), len(num))
        st = zip(cnt, num)
        st = sorted(st, key = lambda st:len(catalog_dic) - st[0])
        # print(st)
        stl, stl2 = zip(*st)
        # print(stl2)
        for i in range(min(len(catalog_dic), dim_num)):
            if stl[i] > 0:
                center.append(stl2[i])
        # while len(center) < 5 and tot_cnt > 0:
        #     for i in range(len(catalog_dic)):
        #         if not i in center and cnt[i] > 0 and cnt[i] > threshold:
        #             tot_cnt -= cnt[i]
        #             center.append(i)
        #     threshold = (threshold / 2)
        centers.append(center)
    return centers
    
def KMeans(KPoint, N, M, K):
    for i in range(50):
        cluster_id = Distribute_cluster(KPoint, N, M, K)
        KPoint = Calc_center(cluster_id, N, K)
        print(KPoint)
    
    fw = open("1.txt", "w")
    for k in KPoint:
        for ki in k:
            fw.write(catalog_list[ki] + ' ')
        fw.write('\n')
    return Distribute_cluster(KPoint, N, M, K)

def InitCenter(entities_list, K, M):
    KPoint = []
    KPoint.append([len(catalog_dic) - 1])
    while(len(KPoint) < K):
        min_dis_k = -1
        min_dis_num = M
        for i in range(N):
            if entities_list[i][0:dim_num] in KPoint:
                continue
            min_dis = M
            for k in KPoint:
                if len(k) == 0:
                    continue
                min_dis = min(min_dis, calc_dis(k, entities_list[i]))
            if min_dis < min_dis_num:
                min_dis_num = min_dis
                min_dis_k = i
        print("K Point select: ", min_dis_k)
        KPoint.append(entities_list[min_dis_k][0:dim_num])
    return KPoint

f_triple = "CN_Cluster26_triples.txt"
f_triple2 = "CN_Classify20_triples.txt"
f_entities = "CN_Cluster26_entities.txt"
ft = open(f_triple)
name = []
catalog_list = []
for l in ft.readlines():
    words = l.split('\t')
    words[2] = words[2][:-1]
    # print(words)
    if not words[0] in entities_dic:
        entities_dic[words[0]] = len(entities_dic)
        entities_list.append([])
        name.append(words[0])
    # if words[1] == "外文名称" or words[1] == "中文名" or words[1] == "类型":
    #     continue
    if not words[1] in catalog_dic:
        catalog_dic[words[1]] = len(catalog_dic)
        catalog_list.append(words[1])
    entities_list[entities_dic[words[0]]].append(catalog_dic[words[1]])
ft = open(f_triple2)
for l in ft.readlines():
    words = l.split('\t')
    words[2] = words[2][:-1]
    # print(words)
    if not words[0] in entities_dic:
        entities_dic[words[0]] = len(entities_dic)
        entities_list.append([])
        name.append(words[0])
    # if words[1] == "外文名称" or words[1] == "中文名" or words[1] == "类型":
    #     continue
    if not words[1] in catalog_dic:
        catalog_dic[words[1]] = len(catalog_dic)
        catalog_list.append(words[1])
    entities_list[entities_dic[words[0]]].append(catalog_dic[words[1]])
catalog_list.append("无用信息")
catalog_dic["无用信息"] = len(catalog_dic)
print(entities_list)
print(len(catalog_dic), len(entities_list))
for entities in entities_list:
    entities.sort()
    while catalog_dic["外文名称"] in entities:
        entities.remove(catalog_dic["外文名称"])
    while catalog_dic["别名"] in entities:
        entities.remove(catalog_dic["别名"])
    while catalog_dic["中文名称"] in entities:
        entities.remove(catalog_dic["中文名称"])
    while catalog_dic["中文名"] in entities:
        entities.remove(catalog_dic["中文名"])
    while catalog_dic["英文名称"] in entities:
        entities.remove(catalog_dic["英文名称"])
    while catalog_dic["简称"] in entities:
        entities.remove(catalog_dic["简称"])
    if len(entities) == 0:
        # print(b)
        entities.append(catalog_dic["无用信息"])
K = 26
N = len(entities_list)
M = len(catalog_dic)
KPoint = InitCenter(entities_list, K, M)
cluster_id = KMeans(KPoint, N, M, K)
fw2 = open("2.txt", "w")
ei = open("CN_Cluster26_entities.txt")
for l in ei.readlines():
    name = l[:-1]
    if not name in entities_dic:
        fw2.write("{}\t{}\n".format(name, 0))
    else:
        fw2.write("{}\t{}\n".format(name, cluster_id[entities_dic[name]]))
# cluster_set = set([])
# mark = [0] * K
# for i in range(N):
#     # if(cluster_id[i] == 0):
#         # continue
# #     # mark[cluster_id[i]] = 1
# #     fw2.write("{}\t{}\n".format(name[i], cluster_id[i]))
#     fw.write(name[i] + ' ' + str(cluster_id[i]) + '   ')
#     # cluster_set.add(cluster_id[i])
#     for c in entities_list[i]:
#         fw.write(catalog_list[c] + ' ')
#     fw.write('\n')
# print(len(cluster_set), cluster_set)
# new_K = K - len(cluster_set)
# new_list = []
# new_entities = []
# mp = [0] * N
# for i in range(N):
#     if cluster_id[i] == 0:
#         mp[i] = len(new_list)
#         new_list.append(i)
#         new_entities.append(entities_list[i])
#         new_entities[mp[i]].remove()
# entities_list = new_entities
# # print(entities_list)
# KPoint = InitCenter(new_entities, new_K)
# new_cluster_id = KMeans(KPoint, len(entities_list), M, new_K)
# nK = 0
# new_id = [0] * (K+1)
# for i in range(new_K):
#     new_id[i] = nK
#     nK += 1
#     while mark[nK] == 1:
#         nK += 1
# for i in range(N):
#     clusterid = cluster_id[i]
#     if clusterid == 0:
#         clusterid = new_cluster_id[mp[i]]
#     fw.write(name[i] + ' ' + str(new_id[cluster_id[i]]) + '   ')
#     # cluster_set.add(cluster_id[i])