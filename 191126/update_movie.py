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
with open('movie.json', 'r', encoding='utf-8') as f:
    movie_data = json.load(f)
print(movie_data)

# 관람 등급 dictionary
watchgrade_dict = {1: '전체관람가', 2: '12세이상관람가', 3: '15세이상관람가', 4: '청소년관람불가', 5: '제한상영가', 6: '등급보류'}

# 업데이트 할 targetDt 가져오기 (어제 날짜)
targetDt = (today + timedelta(days=-1)).strftime('%Y%m%d')

daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}'

res = requests.get(daily_movie_url).json()

for k in range(10):
    movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')
    movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieNm')
    audiAcc = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('audiAcc')
    
