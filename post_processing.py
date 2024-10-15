import pandas as pd
from ast import literal_eval
import re

sao_df = pd.read_excel('SAO_df_240810.xlsx')


patent_df = pd.read_csv('특허_한국에너지연구원_20240722.csv', header = 4)
patent_abs_list = patent_df["요약(원문)"].tolist()

raw_split_txt = []
for hj in range(len(sao_df)):
    if hj % 1000==0: print(hj,"/",len(sao_df))
    this_pos = literal_eval(sao_df['txt'][hj])
    this_pos_txt = [i[0] for i in this_pos]
    this_patent_id = sao_df["id"][hj]

    text = patent_abs_list[this_patent_id-1]
    delimiters ="." , "," , ";"
    regex_pattern = '|'.join(map(re.escape, delimiters))

    pos_info_splitted = [i.strip() for i in re.split(regex_pattern , text) if len(i)>0]
    chk_len = 0

    for split_txt in pos_info_splitted:
        #print("/////////////////////////////////")
        #print("split_txt: ", split_txt)
        this_chk = [i for i in this_pos_txt if i in split_txt]
        #print("this_chk len:",len(this_chk))
        if len(this_chk) > chk_len:
            chk_len = len(this_chk)
            this_split_raw = split_txt
            #print("this_split_raw is changed to -->", split_txt)
    raw_split_txt.append(this_split_raw)

sao_df["split_raw"] = raw_split_txt
sao_df.to_excel('SAO_df_240810_w_rawtxt.xlsx')