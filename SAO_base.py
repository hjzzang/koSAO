import re
from ast import literal_eval
from konlpy.tag import Mecab
import pandas as pd

def getPOS(text):
    mecab = Mecab()
    pos_info_str = str(mecab.pos(text))[1:][:-1]
    #Phase 끊기 규칙 - 구분자 기준
    delimiters = "('.', 'SF')" , "(',', 'SC')" , "(';', 'SY')"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    pos_info_splitted = re.split(regex_pattern, pos_info_str)
    pos_info_splitted_re = [i[2:] for i in pos_info_splitted if i.startswith(', ')]
    pos_info_splitted_re = [i[:-2] for i in pos_info_splitted_re if i.endswith(', ')]
    #Rule 0-2 [~화, ~의 등에 NNG에 대한 전처리]
    replace_dic = {"('화', 'XSN')":"('화', 'NNG')", "('의', 'JKG')":"('의', 'NNG')", 'NNBC':'NNG', 'NR':'NNG', "('및', 'MAJ')":"('및', 'NNG')"}
    regex_sub_pattern = re.compile("(%s)" % "|".join(map(re.escape, replace_dic.keys())))
    pos_replace_list = [regex_sub_pattern.sub(lambda mo: replace_dic[mo.string[mo.start():mo.end()]], text) for text in pos_info_splitted_re]
    pos_tuple_list = [literal_eval(i) for i in pos_replace_list]
    return pos_tuple_list

def getNP(tuple, id_start, id_end, bf):
    NP_list = []
    if bf == "forth":
        i = id_start
        while True:
            if i == id_end-1:
                break
            elif (tuple[i][1] != "NNG" and len(NP_list) == 0):
                i -= 1
            elif tuple[i][1] == "NNG":
                NP_list.append(tuple[i][0])
                i -= 1
            else:
                break
        NP_list.reverse()

    elif bf == "back":
        #for i in range(id_start, id_end):
        i = id_start
        while True:
            if i == id_end: break
            elif (tuple[i][1] != "NNG" and len(NP_list)==0):i += 1
            elif tuple[i][1] == "NNG":
                NP_list.append(tuple[i][0])
                i += 1
            else: break
    return ''.join(NP_list)

def getA(target_tuple, rules_tuple):
    #결과예시: # [(19, '발생'), (29, '최소화')]
    first_id_list = []
    this_rule = rules_tuple[0]
    all_start_index = [i for i,x in enumerate(target_tuple) if this_rule == x]
    first_id = ''
    if len(all_start_index)>0:
        for start_idx in all_start_index:
            if len(rules_tuple) == 1:
                first_id_list = [start_idx]
            elif len(rules_tuple) > 1:
                for rule_token_len in range(len(rules_tuple)):
                    try:
                        if rules_tuple[rule_token_len+1] == target_tuple[start_idx+rule_token_len+1]:
                            first_id = start_idx
                        else:
                            first_id = ''
                            break
                    except:break
                if first_id != '': first_id_list.append(first_id)
    a_word_list = []
    for this_a_id in first_id_list:
        if target_tuple[this_a_id-1][1] == 'NNG':
            this_a_word = getNP(target_tuple, this_a_id,0, 'forth')
        else: this_a_word = 'None'
        a_word_list.append(this_a_word)
    if len(first_id_list)>0: a_info = [(first_id_list[i], a_word_list[i]) for i in range(len(first_id_list))]
    else: a_info = []
    return a_info

def adjA(tuple,a_id, bf):
    prior_a_id = 0
    try:
        if bf == "forth":
            for i in range(a_id-1, -1, -1):
                if (tuple[i][1]=='XSV') or (tuple[i][1]=='XSA') or (tuple[i][1]=='VV'):
                    prior_a_id = i
                    if prior_a_id > 0: break
        elif bf == "back":
            for i in range(a_id, len(tuple)):
                if (tuple[i][1] == 'XSV') or (tuple[i][1] == 'XSA') or (tuple[i][1] == 'VV'):
                    prior_a_id = i
                    if prior_a_id > 0: break
            if prior_a_id == 0:
                prior_a_id = len(tuple)
    except:
        print("error",str(i))
        print(tuple)
    return prior_a_id

def getSOid(tuple, a_id, prior_a_id, type):
    id_list = []
    try:
        for i in range(min(a_id, prior_a_id), max(a_id, prior_a_id)):
            if type == 'o':
                if tuple[i][1] == 'JKO': id_list.append(i)
            if type == 's':
                if (tuple[i][1] == "JX") or (tuple[i][1] == "JKS"): id_list.append(i)
    except:
        print("error: len of tuple is ",len(tuple),"required ",i)
        print(tuple)

    return id_list

def getSAO(target_tuple, a_info, so_rule):
    s_word_list = []
    a_word_list = []
    o_word_list = []
    s_josa_list = []
    a_josa_list = []
    o_josa_list = []
    for a in range(len(a_info)):
        this_a_id = a_info[a][0]
        this_a_word = a_info[a][1]
        # 주어
        # 주어가 동사 바로 뒤에 나오는 명사구
        if so_rule[1] == 1:
            s_word = getNP(target_tuple, this_a_id, len(target_tuple),so_rule[0])
            s_josa_id = 'None'
        else:
            # 동사 앞에 나오는 주격조사를 찾아서
            if so_rule[0] == 'forth':
                prior_a_id = adjA(target_tuple, this_a_id, 'forth')
                s_josa_id = getSOid(target_tuple, this_a_id, prior_a_id, 's')
                s_josa_id.sort()
                if len(s_josa_id) > 0: s_word = getNP(target_tuple, s_josa_id[-1], 0,'forth')
                else:s_word = ''
            # 동사 뒤에 나오는 주격조사를 찾아서
            elif so_rule[0] == 'back':
                latter_a_id = adjA(target_tuple, this_a_id, 'back')
                s_josa_id = getSOid(target_tuple, this_a_id, latter_a_id, 's')
                s_josa_id.sort()
                if len(s_josa_id) > 0: s_word = getNP(target_tuple, s_josa_id[0], 0, 'forth')
                else:s_word = ''
            else:
                s_josa_id = 'None'
                s_word = ''

        # 목적어
        # 목적어가 동사 앞에
        if so_rule[2] == 'forth':
            prior_a_id = adjA(target_tuple, this_a_id, 'forth')
            o_josa_id = getSOid(target_tuple, this_a_id, prior_a_id, 'o')
            o_josa_id.sort()
            if len(o_josa_id) > 0: o_word = getNP(target_tuple, o_josa_id[-1], 0, 'forth')
            else: o_word = ''
        # 목적어가 동사 뒤에
        elif so_rule[2] == 'back':
            latter_a_id = adjA(target_tuple, this_a_id, 'back')
            o_josa_id = getSOid(target_tuple, this_a_id, latter_a_id, 'o')
            o_josa_id.sort()
            if len(o_josa_id) > 0: o_word = getNP(target_tuple, o_josa_id[0], 0, 'forth')
            else:o_word = ''
        else:
            o_word = ''
            o_josa_id = 'None'
        s_word_list.append(s_word)
        a_word_list.append(this_a_word)
        o_word_list.append(o_word)
        s_josa_list.append(s_josa_id)
        a_josa_list.append(this_a_id)
        o_josa_list.append(o_josa_id)
    sao_df = pd.DataFrame({"s":s_word_list, "a":a_word_list, "o":o_word_list, "s_id":s_josa_list, "a_id":a_josa_list, "o_id":o_josa_list})
    return sao_df