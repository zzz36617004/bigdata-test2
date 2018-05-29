import json
import re
from konlpy.tag import Twitter
from collections import Counter
#json 파일명, key값을 주면 문자열을 리턴한다.
def json_to_str(filename,key):
    jsonfile= open(filename ,'r',encoding='utf-8')
    json_string=jsonfile.read()
    jsondata=json.loads(json_string)

    # print(type(json_string))
    # print(json_string)
    # print(type(jsondata))
    # print(jsondata)

    data = ''
    for item in jsondata:
        value = item.get(key)
        if value is None:
            continue
        data += re.sub(r'[^\w]','',value) #한글만 계속 붙여 나간다.
    return data

#명사 추출해서 빈도수를 알려줌
def count_wordfreq(data):
    twitter = Twitter()
    nouns = twitter.nouns(data)             #명사를 리스트로 쭉 뽑아낸다.
    count = Counter(nouns)
    print(type(count))
    return count

