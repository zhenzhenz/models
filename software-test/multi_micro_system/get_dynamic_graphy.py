import csv
import pickle
import itertools
from multi_micro_system.data_processing import data_clean
neighbor_dict = dict()

reaction_dict = dict()

visited_nodes = dict()
enzyme_dict = dict()
compound_dict = dict()
gibbs_dict = dict()
full_path = []

micro_enzyme = {}
E_R = {}
with open('data//short_enzyme.csv', 'r') as f:
    for line in f:
        line = line.strip().split(',')
        micro_enzyme[line[0]] = line[1:]

with open('data//R_E.csv', 'r') as f:
    for line in f:
        line = line.strip().split(',')
        R = line[0]
        E_list = line[1].strip()
        if E_list != '':
            E_list = E_list.split(' ')
            for E in E_list:
                E_R[E] = R.replace('*', '')

with open("data//nodes3.csv") as nodes_file:
    node_reader = csv.reader(nodes_file)
    for node in node_reader:
        visited_nodes.update({node[0]: False})

with open('data//ECO.pkl', 'rb') as f:
    eco = pickle.load(f)

with open("data//reaction_enzyme_pair.csv") as enzyme_file:
    emzyme_reader = csv.reader(enzyme_file)
    for e in emzyme_reader:
        enzyme_dict.update({e[0]: e[1:]})

with open("data//compound_name_pair.csv") as c_file:
    c_reader = csv.reader(c_file)
    for c in c_reader:
        compound_dict.update({c[0]: c[1:]})
    compound_dict.update({'':''})

with open('data//Gibbs.pkl', 'rb') as g_f:
    gibbs_dict = pickle.load(g_f)


def union_set(micro_list):
    micro_list = micro_list.strip().split(',')
    # print(micro_list)
    result = []
    for micro in micro_list:
        result = list(set(result).union(set(micro_enzyme[micro])))
    # print(result)
    for i in range(len(result)):
        result[i] = E_R[result[i]]
    return result


def extract_info(reaction_set):
    with open("data//reaction.csv", "r") as f:
        r = csv.reader(f)
        for row in r:
            re_name = row[0]
            # print(re_name)
            if str(re_name) in reaction_set:
                for item in row[2:]:
                    # print(item)
                    if len(item) > 1 and item[0] == 'C':
                        pair = item[0:].split("_")
                        # print(pair)
                        #generate compoundpair-reaction dictionary
                        global reaction_dict
                        if (str(pair[0]) + '_' + str(pair[1])) in reaction_dict.keys():
                            reaction_dict[str(pair[0]) + '_' + str(pair[1])].add(re_name)
                        else:
                            reaction_dict.update({str(pair[0]) + '_' + str(pair[1]): {re_name}})
                        if (str(pair[1]) + '_' + str(pair[0])) in reaction_dict.keys():
                            reaction_dict[str(pair[1]) + '_' + str(pair[0])].add(re_name)
                        else:
                            reaction_dict.update({str(pair[1]) + '_' + str(pair[0]): {re_name}})
                        #generate neighbor map dictionary
                        global neighbor_dict
                        if str(pair[0]) in neighbor_dict.keys():
                            neighbor_dict[str(pair[0])].add(pair[1])
                        else:
                            neighbor_dict.update({str(pair[0]): {pair[1]}})
                        if str(pair[1]) in neighbor_dict.keys():
                            neighbor_dict[str(pair[1])].add(pair[0])
                        else:
                            neighbor_dict.update({str(pair[1]): {pair[0]}})

    for item in reaction_dict.keys():
        reaction_dict[item] = sorted(list(reaction_dict[item]))
    for item in neighbor_dict.keys():
        neighbor_dict[item] = sorted(list(neighbor_dict[item]))


def dfs(start_compound, target_compound, depth=10):

    path_list = []

    cur_depth = 0
    path_stack = []

    visited_nodes[start_compound] = True
    path_stack.append([start_compound, 0])
    while len(path_stack) > 0:
        if cur_depth >= depth:
            temp_top = path_stack.pop()
            cur_depth -= 1
            visited_nodes[temp_top[0]] = False
            continue
        cur_compound = path_stack[-1]
        temp_adj = neighbor_dict[cur_compound[0]]
        # for i in graph.neighbors(cur_compound[0]):
        #     temp_adj.append(i)

        length = len(temp_adj)
        if cur_compound[1] >= length:
            temp_top = path_stack.pop()
            visited_nodes[temp_top[0]] = False
            cur_depth -= 1
            continue
        else:
            next_compound = temp_adj[cur_compound[1]]
            path_stack[-1][1] += 1

            if next_compound == target_compound:
                path_stack.append([next_compound, 0])
                path_list.append(path_stack[:])
                path_stack.pop()
            else:
                if not visited_nodes[next_compound]:
                    visited_nodes[next_compound] = True
                    path_stack.append([next_compound, 0])
                    cur_depth += 1

    return path_list

def get_compound_pair_list(path_list):

    # path_list :  C1 C2 C3...
    for path in path_list:
        temp = []
        num = len(path)
        for i in range(0, num - 1):
            temp.append(str(path[i][0]) + '_' + str(path[i + 1][0]))
        # temp: C1_C2 C2_C3....
        rea_set = []
        for item in temp:
            rea_set.append(reaction_dict[item])
        first, *second = rea_set
        temp_rea = itertools.product(first, *second)
        global full_path
        full_path.append([temp, list(temp_rea)])
        # temp_full = []
        # for item in full_path:
        #     if not item in temp_full:
        #         temp_full.append(item)
        # full_path = temp_full

    return full_path

def all_dfs(start_compound, depth=3):

    path_list = []

    cur_depth = 0
    path_stack = []

    visited_nodes[start_compound] = True
    path_stack.append([start_compound, 0])
    while len(path_stack) > 0:

        if cur_depth >= depth:
            temp_top = path_stack.pop()
            cur_depth -= 1
            visited_nodes[temp_top[0]] = False
            continue
        cur_compound = path_stack[-1]
        temp_adj = neighbor_dict[cur_compound[0]]

        length = len(temp_adj)
        if cur_compound[1] >= length:
            temp_top = path_stack.pop()
            visited_nodes[temp_top[0]] = False
            cur_depth -= 1
            continue
        else:
            next_compound = temp_adj[cur_compound[1]]
            path_stack[-1][1] += 1

            if not visited_nodes[next_compound]:
                visited_nodes[next_compound] = True
                path_stack.append([next_compound, 0])
                path_list.append(path_stack[:])
                cur_depth += 1

    return path_list

def rank_list(conservation, w_gibbs = 0, w_in_ex = 0, w_posion = 0):
    #[['C00002_C00008', 'C00008_C00020'], [('R00002', 'R00122'), ('R00002', 'R00127'), ('R00002', 'R00157')
    rank_result = []
    global full_path
    for com_list in full_path:
        for rec_list in com_list[1]:  #('R00002', 'R00122'
            weight = 0
            gb = 0.0
            for i in range(len(rec_list)): # R00002
                weight += float(eco[(rec_list[i], com_list[0][i])])
                gb += gibbs_dict[(rec_list[i], com_list[0][i])]
            rank_result.append((rec_list,com_list[0],weight, gb))

    sort_result = sorted(rank_result, key=lambda w: w[3], reverse=True)
    # if conservation >= len(rank_result):
    return sort_result
    # else
    #     return sort_result[:conservation]


def re_rank_list(conservation, w_gibbs = 0, w_in_ex = 0, w_posion = 0):
    #[['C00002_C00008', 'C00008_C00020'], [('R00002', 'R00122'), ('R00002', 'R00127'), ('R00002', 'R00157')
    rank_result = []
    global full_path
    for com_list in full_path:
        for rec_list in com_list[1]:  #('R00002', 'R00122'
            weight = 0.0
            gb = 0.0
            for i in range(len(rec_list)):  # R00002
                temp_c = com_list[0][i].split('_')
                temp_r = temp_c[1] + '_' + temp_c[0]
                weight += float(eco[(rec_list[i], temp_r)])
                gb += gibbs_dict[(rec_list[i], temp_r)]
            rank_result.append((rec_list,com_list[0],weight, gb))

    sort_result = sorted(rank_result,key=lambda w: w[3], reverse=True)
    # if conservation >= len(rank_result):
    return sort_result
    # else:
    #     return sort_result[:conservation]


def attach_inform(sort_result):
    inform_result = []
    for row in sort_result:  # (('R01417', 'R02421'), ['C00002_C00008', 'C00008_C00498'], 0.0)
        enzymes = []
        for rection in row[0]:
            enzymes.append(enzyme_dict[rection])
        cnames = []
        for com in row[1]:
            temp = com.split('_')
            cnames.append([compound_dict[temp[0]][0],compound_dict[temp[1]][0]])

        # gb = 0.0
        # for i in range(0,len(row[0])):
        #     gb += gibbs_dict[row[0][i],row[1][i]]

        row = list(row)
        row.append(enzymes)
        row.append(cnames)
        # row.append(gb)
        inform_result.append(row)

    return inform_result



def reverse_info(inform):
    #[('R01417', 'R02421'), ['C00002_C00008', 'C00008_C00498'], 0.0, [['2.7.3.10'], ['2.4.1.21', '2.4.1.242']], [['ATP', 'ADP'], ['ADP', 'ADP-glucose']]]
    reversed = []
    for row in inform:
        temp_re = []
        for i in range(len(row[0])-1,-1,-1):
            # print(len(row[0]))
            temp_re.append(row[0][i])
        temp_comp = []
        for i in range(len(row[1])-1,-1,-1):
            s = row[1][i].split('_')
            temp_comp.append(s[1] + "_" + s[0])
        temp_enzyme = []
        for i in range(len(row[4])-1,-1,-1):
            temp_enzyme.append(row[4][i])
        temp_name = []
        for i in range(len(row[5])-1,-1,-1):
            temp_name.append([row[5][i][1],row[5][i][0]])
        reversed.append([temp_re,temp_comp,row[2],row[3],temp_enzyme,temp_name])

    return reversed;



def all_path(comp, depth, conserv, ogan):

    reaction_set = union_set(ogan)
    extract_info(reaction_set)

    compound_result = all_dfs(comp, int(depth))

    print('search done!')
    #路径格式转换
    temp_ans = get_compound_pair_list(compound_result)

    print('convert done!')
    #搜索排序
    result = rank_list(int(conserv))
    print('sort done!')
    result = attach_inform(result)

    return result


def reverse_all_path(comp, depth, conserv, ogan):

    reaction_set = union_set(ogan)
    extract_info(reaction_set)

    compound_result = all_dfs(comp, int(depth))

    print('search done!')
    # 路径格式转换
    temp_ans = get_compound_pair_list(compound_result)

    print('convert done!')
    # 搜索排序
    result = re_rank_list(int(conserv))
    print('sort done!')
    result = attach_inform(result)
    result = reverse_info(result)

    return result

def trans_C(c):
    #转中文名为编号
    for key,val in compound_dict.items():
        if key==c:
            return c
        elif c in val:
            return key
        
def trans_list(l):
    for i in range(len(l)):
        l[i]=trans_C(l[i])
    return l


def main(condon):
    global reaction_dict
    reaction_dict = dict()
    global full_path
    full_path = []
    global neighbor_dict
    neighbor_dict = dict()
    start_compound = trans_C(condon['Input'])
    target_compound = trans_C(condon['Output'])
    depth = condon['MaxLength']
    conservation = condon['result_conservation']
    multi_micro=condon['Microorganism']
    
    required_compound=trans_list(condon['requrired'].strip().split(','))
    not_required_compound=trans_list(condon['not_requrired'].strip().split(','))

    #正向全路径
    # result = all_path(start_compound,depth, conservation, 'ACO,ECO')

    #逆向全路径
    #result = reverse_all_path(target_compound, depth, conservation, 'ACO,ECO')
    result = ''
    if start_compound!='' and target_compound=='':
        result = all_path(start_compound,depth, conservation, multi_micro)
    elif start_compound=='' and target_compound!='':
        result = reverse_all_path(target_compound, depth, conservation, multi_micro)

    result=data_clean(result,required_compound,not_required_compound)
    
    if conservation < len(result):
        result = result[:conservation]

    return result

if __name__ == '__main__':
    main()
