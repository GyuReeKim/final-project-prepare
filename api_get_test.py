from datetime import datetime, timedelta
import requests
import urllib.request
import json
from bs4 import BeautifulSoup

today = datetime.today()
genre_dict = {1: '드라마', 2: '판타지', 3: '서부', 4: '공포', 5: '로맨스', 6: '모험', 7: '스릴러', 8: '느와르', 9: '컬트', 10: '다큐멘터리', 11: '코미디', 12: '가족', 13: '미스터리', 14: '전쟁', 15: '애니메이션', 16: '범죄', 17: '뮤지컬', 18: 'SF', 19: '액션', 20: '무협', 21: '에로', 22: '서스펜스', 23: '서사', 24: '블랙코미디', 25: '실험', 26: '영화카툰', 27: '영화음악', 28: '영화패러디포스터'}

movieNm_list = []
for i in range(1):
    targetDt = (today + timedelta(days=-(i+2)*7)).strftime('%Y%m%d')
    print(targetDt)
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    key = '660f73acbf0225280f5db341b9f4e840'
    movie_url = f'{url}?key={key}&targetDt={targetDt}'

    res = requests.get(movie_url).json()

    for i in range(10):
        movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[i].get('movieNm')
        if movieNm not in movieNm_list:
            movieNm_list.append(movieNm)
print(len(movieNm_list))

#애플리케이션 클라이언트 id 및 secret
client_id = "hG6O_G7PA_2DCtQbUri0" 
client_secret = "fsSh41QFYc"


#영화검색 url
url = "https://openapi.naver.com/v1/search/movie.json"
option = "&display=1"


data = []

movie_info = []
cnt = 0
for movie_name in movieNm_list:
    temp_data = {}

    query = "?query="+urllib.parse.quote(movie_name) # movieNm
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
        # print(type(temp))
        dict_info = json.loads(str_info)
        if dict_info.get('items') != []:
            # print(movie_name)
            cnt += 1
            title = dict_info.get('items')[0].get('title').replace('<b>', '').replace('</b>', '')
            title_en = dict_info.get('items')[0].get('subtitle').replace('<b>', '').replace('</b>', '')
            score = dict_info.get('items')[0].get('userRating') # string type
            score = float(score)
            poster_url = dict_info.get('items')[0].get('image')
            video_url = dict_info.get('items')[0].get('image')
            ost_url = dict_info.get('items')[0].get('image')
    #         print(dict_info.get('items')[0].get('link')) # 줄거리 크롤링에 필요
    #         print(dict_info.get('items')[0].get('director'))
    #         print()
    
            # 크롤링
            link = dict_info.get('items')[0].get('link')
            
            response = requests.get(link).text
            soup = BeautifulSoup(response, 'html.parser')


            # 줄거리
            contents = soup.select('div.story_area > p.con_tx')
            # print(contents)

            temp_content = []
            if len(contents) == 0:
                movie_info.append("줄거리 없음")
            else:
                for c in contents:
                    temp = c.text
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\xa0', '')
                    temp = temp.replace('   ', ' ')
                    temp = temp.replace('  ', ' ')
                    temp_content = temp
            movie_info.append(temp_content)
            # print(temp_content)

            # 관객수
            audiences = soup.select('div.step9_cont > p.count')

            audience = 0
            audience_str = ''
            for a in audiences:
                for temp in a.text:
                    if temp == '명':
                        break
                    if temp != ',':
                        audience_str += temp
            audience = int(audience_str)
            # print(audience)

            # 장르
            genres = soup.select('dl.info_spec > dd:nth-child(2) > p')
            temp_genres = genres[0].text.replace(',', '')
            temp_genres = genres[0].text.replace('/', ' ')

            #content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p

            temp_genre_list = temp_genres.split()

            genre = []
            for key, val in genre_dict.items():
                for temp_genre in temp_genre_list:
                    if temp_genre == val:
                        genre.append(key)
                        break
            # print(genre)

    else:
        print("Error code:"+rescode)

    if dict_info.get('items') != []:
        temp_data["id"] = cnt
        temp_data["title"] = title
        temp_data["title_en"] = title_en
        temp_data["score"] = score
        temp_data["audience"] = audience
        temp_data["poster_url"] = poster_url
        temp_data["summary"] = temp_content
        # temp_data[]
        # print(temp_data)
        data.append(temp_data)
# print(len(movie_info))
# print(movie_info)
# print(data)

with open('movie.json', 'w', encoding='UTF-8-sig') as json_file:
    json.dump(data, json_file, ensure_ascii=False)