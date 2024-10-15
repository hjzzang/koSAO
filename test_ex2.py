import pandas as pd

from konlpy.tag import Mecab

test_dir = r'D:\OneDrive\2.working paper\koSAO_ddonae'
test_df = pd.read_excel(test_dir+'//특허_한국에너지연구원_ㅎㅈ_20240722.xlsx',sheet_name='Sheet2', header=1)
mecab = Mecab()
pos_list = []
for hj in range(len(test_df)):
    this_abs = test_df.iloc[hj]['PHRASES']
    this_pos = mecab.pos(this_abs)
    pos_list.append(this_pos)

test_df['Mecab'] = pos_list
test_df.to_excel(test_dir+'//특허_한국에너지연구원_wPOS_ㅎㅈ_20240722.xlsx')

