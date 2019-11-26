# movies model에 저장
# 업데이트 필요

from datetime import datetime, timedelta
import requests
import json

today = datetime.today()

daily_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

### key값 따로 저장 필요 ###
key = '660f73acbf0225280f5db341b9f4e840'
weekGb = '0'

# director.json 불러오기
with open('director.json', 'r', encoding='utf-8') as f:
    director_data = json.load(f)

movieNm_list = []
audiCnt_list = []
movieNmEn_list = []
directors_list = []
watchGradeNm_list = []
# for i in range(60):
for i in range(1):
    targetDt = (today + timedelta(days=-(i+1))).strftime('%Y%m%d')
    # print(targetDt)
    daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}&weekGb={weekGb}'

    res = requests.get(daily_movie_url).json()

    for k in range(10):
        movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')
        movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieNm')
        audiCnt = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('audiCnt')

        if movieNm not in movieNm_list:
            movieNm_list.append(movieNm)
            audiCnt_list.append(int(audiCnt))
            
            detail_movie_url = f'{detail_url}?key={key}&movieCd={movieCd}'
            detail_res = requests.get(detail_movie_url).json()

            movieNmEn = detail_res.get('movieInfoResult').get('movieInfo').get('movieNmEn')
            movieNmEn_list.append(movieNmEn)
            
            peopleNms = detail_res.get('movieInfoResult').get('movieInfo').get('directors')
            peopleNm_list = []
            for dd in range(len(director_data)):
                for p in range(len(peopleNms)):
                    peopleNm = peopleNms[p].get('peopleNm')
                    if peopleNm == director_data[dd].get('fields').get('name'):
                        peopleNm_list.append(director_data[dd].get('id'))
            directors_list.append(peopleNm_list)
            
            watchGradeNms = detail_res.get('movieInfoResult').get('movieInfo').get('audits')
            if len(watchGradeNms) == 0:
                watchGradeNm_list.append('-')
            else:
                watchGradeNm = watchGradeNms[0].get('watchGradeNm')
                watchGradeNm_list.append(watchGradeNm)
    # print(len(movieNm_list))
print(movieNm_list)
print(audiCnt_list)
print(movieNmEn_list)
print(directors_list)
print(watchGradeNm_list)