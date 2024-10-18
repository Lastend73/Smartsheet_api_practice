import requests
import pprint
import smartsheet

# 헤더 설정
headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41"
}

params = {
    "page": 1,
    "pageSize": 10
}

# API 엔드포인트
url = "https://api.smartsheet.com/2.0/sheets/5749026821459844/crosssheetreferences"

# GET 요청 보내기
response = requests.get(url, headers=headers, params=params)

date_control_ld_list=[] #일정관리 시트 아이디 List
folder_num = 5 #최하단 폴더 갯수
# 응답 확인 
if response.status_code == 200:
    print("요청 성공!")
    # 응답 데이터 처리 (JSON 형식으로 반환되는 경우)
    data = response.json()

    pprint.pprint(data['data'][0])

    results = data


else:
    print("요청 실패:", response.text)