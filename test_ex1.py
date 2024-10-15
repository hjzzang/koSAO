#https://konlpy.org/ko/latest/install/#id2

#https://github.com/byungjooyoo/Text_Bigdata_Book/blob/main/06%EC%9E%A5_%ED%95%9C%EA%B8%80%ED%98%95%ED%83%9C%EC%86%8C%EB%B6%84%EC%84%9D%EA%B8%B0_%ED%99%9C%EC%9A%A9.ipynb

# 한국어 폰트 세팅 (출력용)
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.font_manager.fontManager.addfont('C://Windows/Fonts/NanumGothic.ttf')
mpl.rc('font', family='NanumGothic')
plt.rc("axes", unicode_minus=False)

import pandas as pd
pd.Series([0,2,-4,6]).plot(title="한글", figsize=(12, 2))

"""
# 한글형태소분석 라이브러리 설치 (윈도우)
ref.
https://joyhong.tistory.com/127
# mecab_python-0.996_ko_0.9.2_msvc-cp37-cp37m-win_amd64.whl

!pip install konlpy
!git clone https://github.com/SOMJANG/Mecab-ko-for-Google-Colab.git
cd Mecab-ko-for-Google-Colab
.\install_mecab-ko_on_colab_light_220429.sh


"""


import MeCab
mecab = MeCab.Tagger()

out = mecab.parse("오늘은 맑은 날씨이다.")

print(out)

import konlpy
from konlpy.tag import Kkma, Komoran, Okt, Hannanum, Mecab


text = '코드잇에 오신 걸 환영합니다'

okt = Okt()
print(okt.morphs(text))
okt.pos(text)

mecab = Mecab()
mecab.pos(text)

print(mecab.pos(text))

mecab.morphs(text)

text = '대형 기판의 양산 공정에 더욱 적합하고, 고정세의 패터닝이 가능하도록 하는 박막 증착 장치, 이를 이용한 유기 발광 디스플레이 장치의 제조방법 및 이에 따라 제조된 유기 발광 디스플레이 장치를 제공하기 위하여, 본 발명은 기판상에 박막을 형성하기 위한 박막 증착 장치에 있어서, 진공으로 유지되는 제2 챔버; 상기 제2 챔버 내에 서로 나란하게 구비되며, 그 상부에 기판이 고정되는 두 개의 스테이지들; 상기 각각의 스테이지 상에 고정된 기판에 결합하는 마스크들; 및 상기 스테이지 상부에 이동가능하도록 형성되어, 상기 기판측으로 증착 물질을 방사하는 제1 증착원 및 제2 증착원;을 포함하는 박막 증착 장치를 제공한다.'
mecab.pos(text)
mecab.morphs(text)

print(mecab.tagset)