import pickle
import csv
import itertools

visited_nodes = dict()
neighbor_dict = dict()
full_path = []

with open('data//nodes3.csv') as nodes_file:
    node_reader = csv.reader(nodes_file)
    for node in node_reader:
        visited_nodes.update({node[0]: False})

with open('data//adj_map2.pk', 'rb') as f:
    neighbor_dict = pickle.load(f)

with open('data//reaction_dictionary.pk', 'rb') as f:
    reaction_dict = pickle.load(f)

with open('data//ECO.pkl', 'rb') as f:
    eco = pickle.load(f)


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

        full_path.append([temp, list(temp_rea)])

    return full_path


def rank_list(conservation, w_gibbs = 0, w_in_ex = 0, w_posion = 0):
    #[['C00002_C00008', 'C00008_C00020'], [('R00002', 'R00122'), ('R00002', 'R00127'), ('R00002', 'R00157')
    rank_result = []
    for com_list in full_path:
        for rec_list in com_list[1]:  #('R00002', 'R00122'
            weight = 0
            for i in range(len(rec_list)): # R00002
                weight += float(eco[(rec_list[i], com_list[0][i])])
            weight=round(weight,4)
            rank_result.append((rec_list,com_list[0],weight))

    sort_result = sorted(rank_result,key=lambda weight: weight[2], reverse=True)
    if conservation >= len(rank_result):
        return sort_result
    else:
        return sort_result[:conservation]



def main(condon,condon1):

    start_compound = condon['Input']
    target_compound = condon['Output']
    depth = condon['MaxLength']
    conservation = 50

    #路径搜索
    if start_compound=='':
        compound_result =all_dfs(target_compound,int(depth))
    if target_compound=='':
        compound_result =all_dfs(start_compound,int(depth))
    if start_compound!='' and target_compound!='':
        compound_result = dfs(start_compound, target_compound,int(depth))
    #print('search done!')
    #路径格式转换
    get_compound_pair_list(compound_result)
    #搜索排序
    result = rank_list(int(conservation))
    #result=list(result)
    return result
    #print('sort done!')
    #for item in result:
    #   print(item)


if __name__ == '__main__':
    main()
