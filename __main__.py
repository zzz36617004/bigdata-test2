from collect import crawler
from analysis import analizer
from visualize import visualizer
pagename = "chosun"
from_date = "2018-05-01"
to_date = "2018-05-24"

if __name__=="__main__":
    #수집
    result=crawler.fb_get_post_list(pagename,from_date,to_date)
    print(result)
    #분석
    dataString = analizer.json_to_str("d:/" + pagename + ".json", 'message_str')
    data = analizer.count_wordfreq(dataString)
    dictWords = dict(data.most_common(20))
    print(data)
    #그래프
    visualizer.show_graph_bar(dictWords,pagename)
    #워드클라우드
    visualizer.wordcloud(dictWords, pagename)