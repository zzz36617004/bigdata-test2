__all__=["visualizer"]
from . import visualizer
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pytagcloud
import webbrowser

# 워드크라우드

def wordcloud(dictWords, pagename):
    print(type(dictWords))
    print(dictWords)
    taglist = pytagcloud.make_tags(dictWords.items(), maxsize=80)
    save_filename = "D:/javaStudy/facebook/%s_wordcloud.jpg" % pagename
    pytagcloud.create_tag_image(
     taglist,
     save_filename,
     size=(800, 600),
     fontname='korean',
     rectangular=False
    )

    webbrowser.open(save_filename)

def show_graph_bar(dictWords,pagename):

    # 한글처리
    font_filename = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=font_filename).get_name()
    print(font_name)
    plt.rc('font', family=font_name)     #이 폰트를 쓰라고 준비시키는것
    #라벨처리
    plt.xlabel("주요단어")                 #X축 라벨처라
    plt.ylabel("빈도수")                   #Y축 라벨처리
    plt.grid(True)

    # 데이타 대입
    dict_keys = dictWords.keys()
    dict_values = dictWords.values()
    plt.bar(range(len(dictWords)), dict_values, align='center') #바그래프 그리고 옵션주는것(길이의 범위는 단어계수만큼 dictword)
    plt.xticks(range(len(dictWords)), list(dict_keys), rotation=70)
    plt.show()
    save_filename = "D:/javaStudy/facebook/%s_bar_graph.png" % pagename
    plt.savefig(save_filename, dpi=400, bbox_inches='tight')