__all__=["crawler"]
from . import crawler
import json
import requests
from datetime import datetime, timedelta

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAACEdEose0cBAPseCw09vNcZBD5ZBm1g0kEAgpYjqSwaxfEdyseHvwhjLCuf0E0HhTKZApujZARvLNxtHwrZCHzFCKw41i5xr0AqEo8c1ldfYimn44S0GmKlVtfp5hXgGZBtGZCJQQH1jyJex9cUSiqrSPsRkRWgDYv8ZB7lRFeTWJjO51Pb5HkZABewsL9mTb1gZD"
LIMIT_REQUEST = 5


def get_json_result(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()                                 #데이터 못받을 경우 ex)404면 리턴 none
        except Exception as e:
           return "%s :Error for request [%s]" % (datetime.now(), url)              #통신상의 오류




#페이스북 페이지 네임을 주면 페이지 id값을 리턴해주는 함수!~!!!!#@#!@#!@#!@#
def fb_name_to_id(pagename):
    base = BASE_URL_FB_API
    node = "/"+pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params
    json_result = get_json_result(url) # 딕션어리로 리턴된다
    return json_result["id"]  # id 값만 리턴한다

    # result=fb_name_to_id("jtbcnews")
    # print(result)

#페이스북 페이지 네임,시작날짜, 끝날짜를 주면 json-->List형태로 데이터를 리턴해준다.
def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)                           #페이지네임 받아서 페이지 아이디 뽑아옴
    base = BASE_URL_FB_API
    node = '/%s/posts' % page_id
    fields='/?fields=id,message,link,name,type,shares,'+\
    'created_time,comments.limit(0).summary(true),'+\
    'reactions.limit(0).summary(true)'
    duration='&since=%s&until=%s' % (from_date, to_date)
    parameters='&limit=%s&access_token=%s' %(LIMIT_REQUEST, ACCESS_TOKEN)
    url=base + node + fields + duration + parameters
    print(url)
    postList=[]
    isNext=True
    while isNext:
        tmpPostList = get_json_result(url)
        for post in tmpPostList["data"]:            #스무개로 돌린다.
            postVo = preprocess_post(post)
            postList.append(postVo)                 #단위는 post인데 그중에서 message를 담는다.
        paging = tmpPostList.get("paging").get("next")        #페이징이 다음 주소 json에서 next라는 이름으로 url을 넘겨줌
        if paging != None:
            url = paging
        else:
            isNext=False
    # save results to file

    with open("d:/" + pagename + ".json", 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(postList, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)
    return postList
    #jsonPosts = get_json_result(url) #포트스 정보를 딕션어리 형태로 리턴한다( data, paging)
    #return jsonPosts

def preprocess_post(post):
    # 작성일 +9시간(오차수정)
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

    #공유 수
    if "shares" not in post:
        shares_count=0
    else:
        shares_count = post["shares"]["count"]
    # 리액션 수
    if "reactions" not in post:
        reactions_count = 0
    else:
        reactions_count = post["reactions"]["summary"]["total_count"]
    # 댓글 수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]
    # 메세지
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]
    postVo = {
        "shares_count": shares_count,
        "reactions_count": reactions_count,
        "comments_count": comments_count,
        "message_str": message_str,
        "created_time": created_time
    }
    return postVo


# jsondata = fb_get_post_list(pagename, from_date, to_date)
# print(jsondata)