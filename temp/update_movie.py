from datetime import datetime, timedelta
import requests
import json
import urllib.request
from bs4 import BeautifulSoup

# 오늘 날짜 import
today = datetime.today()

# base url
daily_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

### key값 따로 저장 필요 ###
key = '660f73acbf0225280f5db341b9f4e840'

# movie.json 불러오기
with open('fixtures/movie.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# print(data)
len_data = len(data)

# director.json 불러오기
with open('fixtures/director.json', 'r', encoding='utf-8') as f:
    director_data = json.load(f)
# print(director_data)


movie_name_list = []
for i in range(len_data):
    movie_name_list.append(data[i].get('fields').get('title'))
# print(movie_name_list)

# 관람 등급 dictionary
watchgrade_dict = {1: '전체관람가', 2: '12세이상관람가', 3: '15세이상관람가', 4: '청소년관람불가', 5: '제한상영가', 6: '등급보류'}

# 업데이트 할 targetDt 가져오기 (어제 날짜)
targetDt = (today + timedelta(days=-1)).strftime('%Y%m%d')

daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}'

res = requests.get(daily_movie_url).json()

new_movieNm_list = []
new_audiAcc_list = []
new_movieNmEn_list = []
new_directors_list = []
new_watchGradeNm_list = []

for k in range(10):
    # 영화 제목으로 업데이트할 지 추가할 지 결정
    movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')
    movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieNm')
    audiAcc = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('audiAcc')
    # print(movieNm)
    if movieNm in movie_name_list:
        # 기존에 있는 데이터이기 때문에 update 해준다. (audience)
        for i in range(len_data):
            if data[i].get('fields').get('title') == movieNm:
                temp_data = data[i].get('fields')
                temp_data.update(audience = audiAcc)
                data[i].update(fields = temp_data)
    else:
        # 기존에 없는 데이터이므로 추가해준다.
        new_movieNm_list.append(movieNm)
        new_audiAcc_list.append(audiAcc)

        detail_movie_url = f'{detail_url}?key={key}&movieCd={movieCd}'
        detail_res = requests.get(detail_movie_url).json()

        # engligh title
        movieNmEn = detail_res.get('movieInfoResult').get('movieInfo').get('movieNmEn')
        new_movieNmEn_list.append(movieNmEn)

        # director list
        peopleNms = detail_res.get('movieInfoResult').get('movieInfo').get('directors')
        peopleNm_list = []
        for dd in range(len(director_data)):
            for p in range(len(peopleNms)):
                peopleNm = peopleNms[p].get('peopleNm')
                if peopleNm == director_data[dd].get('fields').get('name'):
                    peopleNm_list.append(director_data[dd].get('id'))
        new_directors_list.append(peopleNm_list)

        # watch grade list
        watchGradeNms = detail_res.get('movieInfoResult').get('movieInfo').get('audits')
        if len(watchGradeNms) == 0:
            new_watchGradeNm_list.append(6)
        else:
            watchGradeNm = watchGradeNms[0].get('watchGradeNm')
            for dict_id, val in watchgrade_dict.items():
                if val == watchGradeNm:
                    new_watchGradeNm_list.append(dict_id)
                    break
            else:
                new_watchGradeNm_list.append(6)

# print(new_watchGradeNm_list)


### id, secret값 따로 저장 필요 ###
#애플리케이션 클라이언트 id 및 secret
client_id = "hG6O_G7PA_2DCtQbUri0" 
client_secret = "fsSh41QFYc"

len_new_movie = len(new_movieNm_list)
poster_image_url = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="
genre_dict = {1: '드라마', 2: '판타지', 3: '서부', 4: '공포', 5: '로맨스', 6: '모험', 7: '스릴러', 8: '느와르', 9: '컬트', 10: '다큐멘터리', 11: '코미디', 12: '가족', 13: '미스터리', 14: '전쟁', 15: '애니메이션', 16: '범죄', 17: '뮤지컬', 18: 'SF', 19: '액션', 20: '무협', 21: '에로', 22: '서스펜스', 23: '서사', 24: '블랙코미디', 25: '실험', 26: '영화카툰', 27: '영화음악', 28: '영화패러디포스터'}
cnt_id = len_data

# print(data)

for i in range(len_new_movie):
    new_movie_data = {}
    fields = {}

    #영화검색 url
    url = "https://openapi.naver.com/v1/search/movie.json"
    option = "&display=1"
    query = "?query="+urllib.parse.quote(new_movieNm_list[i]) # movieNm
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

        if dict_info.get('items') != []:
            cnt_id += 1

            # score
            score = dict_info.get('items')[0].get('userRating') # string type
            score = float(score)
            # print(score)

            # link
            movie_link = dict_info.get('items')[0].get('link') # poster_url, summary, video_url, ost_url

            # poster_url
            temp_link = movie_link
            for t in range(len(temp_link)):
                if temp_link[t] == "=":
                    naver_movie_code = temp_link[t+1:]
                    break
            poster_url = poster_image_url + naver_movie_code
            # print(poster_url)

            # soup
            response = requests.get(movie_link).text
            soup = BeautifulSoup(response, 'html.parser')

            # summary
            contents = soup.select('div.story_area > p.con_tx')

            summary = ''
            if len(contents) == 0:
                summary = "줄거리 없음"
            else:
                for c in contents:
                    temp = c.text
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\xa0', '')
                    temp = temp.replace('   ', ' ')
                    temp = temp.replace('  ', ' ')
                    summary = temp
            # print(summary)
        
            # genres
            genre_list = soup.select('dl.info_spec > dd:nth-child(2) > p')
            temp_genres = genre_list[0].text.replace(',', '').replace('/', ' ')
            temp_genre_list = temp_genres.split()

            genres = []
            for dict_id, val in genre_dict.items():
                for temp_genre in temp_genre_list:
                    if val == temp_genre:
                        genres.append(dict_id)
            # print(genres)

            # video_url
            #content > div.article > div.section_group.section_group_frst > div:nth-child(4) > div > ul > li:nth-child(1) > a
            #content > div.article > div.section_group.section_group_frst > div:nth-child(4) > div > ul > li:nth-child(1)
            # video_html = soup.select('div.section_group.section_group_frst > div:nth-child(4) > div > ul > li:nth-child(1)')[0]
            # video_url = 'https://movie.naver.com' + video_html.find_all('a')[0].get('href')
            # print(video_url)
    else:
        print("Error code:"+rescode)

    fields["title"] = new_movieNm_list[i]
    fields["title_en"] = new_movieNmEn_list[i]
    fields["summary"] = summary
    fields["score"] = score
    fields["audience"] = new_audiAcc_list[i]
    fields["poster_url"] = poster_url
    fields["video_url"] = ''
    fields["ost_url"] = ''

    fields["movie_directors"] = new_directors_list[i]
    fields["movie_genres"] = genres
    fields["grade_id"] = new_watchGradeNm_list[i]


    new_movie_data["id"] = cnt_id
    new_movie_data["model"] = "movies.movie"
    new_movie_data["fields"] = fields
    data.append(new_movie_data)
print(data)

with open('fixtures/movie.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)