import pandas as pd
from konlpy.tag import Mecab
mecab = Mecab()

patent_df = pd.read_csv('특허_한국에너지연구원_20240722.csv', header = 4)
patent_abs_list = patent_df["요약(원문)"].tolist()

abs_pos_list = []
all_xsv_df = pd.DataFrame()
for hj in range(len(patent_abs_list)):
    pos_tuple = mecab.pos(patent_abs_list[hj])
    abs_pos_list.append(pos_tuple)
    ind_list = []
    pos_list = []
    for pos_id in range(len(pos_tuple)):
        if "JKO" in pos_tuple[pos_id][1]:
            ind_list.append(pos_id)
            pos_list.append(pos_tuple[pos_id-2:pos_id+2])
    this_df = pd.DataFrame({"id":patent_df.iloc[hj]['일련번호'],"patent_id":patent_df.iloc[hj]['번호'],"a":ind_list,"words":pos_list})
    all_xsv_df = all_xsv_df.append(this_df).reset_index(drop=True)

#patent_df['POS'] = abs_pos_list
#patent_df.to_excel('특허_한국에너지연구원_POS_20240801.xlsx')
all_xsv_df.to_excel('POS_w_JKO.xlsx')