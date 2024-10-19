import requests
import pprint

# 헤더 설정
headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41",
    "Content-Type": "application/json"
}


params = {
    "page": 1,
    "pageSize": 5
}
# API 엔드포인트
main_sheetId ='6374450563862404'
main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}"

# GET 요청 보내기
response = requests.get(main_sheet_url, headers=headers, params=params)

# 응답 확인 
if response.status_code == 200:
    print("요청 성공!")
    # 응답 데이터 처리 (JSON 형식으로 반환되는 경우)
    datas = response.json()
    for data in datas['columns']:
        if data['title'] == "목표 완료일":
            goal_date_id = data['id']
    
    # pprint.pprint(datas['rows'][0])
    for data in datas['rows']:
        for value in data['cells']:
            if (value['columnId'] == goal_date_id) & ("value" in value):
                last_date = {
                    "rowId" : data['id'],
                    "columnId" : value["columnId"]
                    }
    
    print(last_date)

else:
    print("요청 실패:", response.text)