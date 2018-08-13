# -*- coding: utf-8 -*-



    
def data_clean(data,need_list,not_need_list):
    result=[]
    #print(need_list)
    for item in data:
        rout=item[1]
        new_rout=[]
        for c_pair in rout:
            c_list=c_pair.split('_')
            for c in c_list:
                if c not in new_rout:
                    new_rout.append(c)
        
        compound_name=item[5]
        new_compound_name=''
        for name_list in compound_name:
            for name in name_list:
                if name not in new_compound_name:
                    new_compound_name+=name+' | '
        item[5]=new_compound_name.strip()[0:-1].strip()
        
        if need_list==['']:
            for c in new_rout:
                if c in not_need_list:
                    break
                if c==new_rout[-1]:
                    item[1]=new_rout
                    result.append(item)
        elif need_list!='':
            exist=False
            for c in new_rout:
                if c in not_need_list:
                    break
                if c in need_list:
                    exist=True
                if c==new_rout[-1] and exist:
                    item[1]=new_rout
                    result.append(item)
    data=[]
    for item in result:
        reaction=''
        for i in item[0]:
            reaction+=i+' '
            
        route=''
        for i in item[1]:
            route+=i+'→'
        
        data.append([reaction.strip(),route[0:-1],item[2],item[3],item[4],item[5]])
        
            
    return data

def trans_compound(com_list):
    result=[]
    for c_pair in com_list:
        c_list=c_pair.split('_')
        for c in c_list:
            if c not in result:
                result.append(c)
    return result
if __name__=='__main__':
    data=[['R',['C1_C2','C2_C3','C3_C4']]]
    print(data_clean(data,'','C2'))