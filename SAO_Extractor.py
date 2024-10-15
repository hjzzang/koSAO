from SAO_base import *

rule_df = pd.read_excel(r'D:\OneDrive\2.working paper\koSAO_ddonae'+'//koSAO_rule_240730.xlsx')
rule_list = rule_df['A_POS_re'].tolist()
s_rule_list = rule_df['S'].tolist()
s_add_rule_list = rule_df['S_'].tolist()
o_rule_list = rule_df['O'].tolist()
overlap_chk = rule_df['overlap']

patent_df = pd.read_csv('특허_한국에너지연구원_20240722.csv', header = 4)
patent_abs_list = patent_df["요약(원문)"].tolist()

sao_df = pd.DataFrame()
for hj in range(len(patent_abs_list)):
    this_abs = patent_abs_list[hj]
    this_split_abs_pos_list = getPOS(this_abs)
    for split_id in range(len(this_split_abs_pos_list)):
        text_w_pos = this_split_abs_pos_list[split_id]
        for rule_id in range(len(rule_list)):
            if rule_id != 15:
                this_rule = literal_eval(rule_list[rule_id])
                so_rule = [s_rule_list[rule_id], s_add_rule_list[rule_id],o_rule_list[rule_id]]
                this_sao_df = getSAO(text_w_pos, getA(text_w_pos, this_rule), so_rule)
                if len(this_sao_df)>0:
                    this_sao_df["overlap"] = overlap_chk[rule_id]
                    this_sao_df["rule"] = str(this_rule)
                    this_sao_df["txt"] = str(text_w_pos)
                    this_sao_df["id"] = patent_df.iloc[hj]["일련번호"]
                    this_sao_df["patent_id"] = patent_df.iloc[hj]["번호"]
                    this_sao_df = this_sao_df.reset_index(drop=True)
                    sao_df = sao_df.append(this_sao_df).reset_index(drop=True)
                    sao_df = sao_df.drop_duplicates(subset= ['a_id','overlap', 'txt']).reset_index(drop=True)
sao_df.to_excel("SAO_df_240810.xlsx")