#import
import json
import requests
import urllib.request
from bs4 import BeautifulSoup
 
genre_dict = {1: '드라마', 2: '판타지', 3: '서부', 4: '공포', 5: '로맨스', 6: '모험', 7: '스릴러', 8: '느와르', 9: '컬트', 10: '다큐멘터리', 11: '코미디', 12: '가족', 13: '미스터리', 14: '전쟁', 15: '애니메이션', 16: '범죄', 17: '뮤지컬', 18: 'SF', 19: '액션', 20: '무협', 21: '에로', 22: '서스펜스', 23: '서사', 24: '블랙코미디', 25: '실험', 26: '영화카툰', 27: '영화음악', 28: '영화패러디포스터'}


#애플리케이션 클라이언트 id 및 secret
client_id = "hG6O_G7PA_2DCtQbUri0" 
client_secret = "fsSh41QFYc"
 
#영화검색 url
url = "https://openapi.naver.com/v1/search/movie.json"
option = "&display=1"
query = "?query="+urllib.parse.quote('윤희에게') # movieNm
url_query = url + query + option
 
#Open API 검색 요청 개체 설정
request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
 
#검색 요청 및 처리
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode == 200):
    response_body = response.read()
    str_info = response_body.decode('utf-8')
    dict_info = json.loads(str_info)
    link = dict_info.get('items')[0].get('link') # 줄거리 크롤링에 필요
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'html.parser')
    # video_html = soup.select('div.section_group.section_group_frst > div:nth-child(4) > div > ul > li:nth-child(1)')[0]
    # video_url = 'https://movie.naver.com' + video_html.find_all('a')[0].get('href')
    # print(video_url)
    genres = soup.select('dl.info_spec > dd:nth-child(2) > p')
    temp_genres = genres[0].text.replace(',', '').replace('/', ' ')
    # temp_genres = genres[0].text.replace('/', ' ')

    # #content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p

    temp_genre_list = temp_genres.split()
    print(temp_genre_list)

    genre = []
    for key, val in genre_dict.items():
        for temp_genre in temp_genre_list:
            if val == temp_genre:
                genre.append(key)
    print(genre)
else:
    print("Error code:"+rescode)