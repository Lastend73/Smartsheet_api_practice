import requests
import pprint

# 헤더 설정
headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41",
    "Content-Type": "application/json"
}


# params = {
#     "page": 1,
#     "pageSize": 100
# }

data ={
    "sourceSheetId" : 6374450563862404,
    "name" : "TEST2",
    "endColumnId" : 5736227184791428,
    "startColumnId" : 5736227184791428
}
# API 엔드포인트
main_sheetId ='3277342667394948'
main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}/crosssheetreferences"

# GET 요청 보내기
response = requests.post(main_sheet_url, headers=headers, json=data)

# 응답 확인 
if response.status_code == 200:
    print("요청 성공!")
    # 응답 데이터 처리 (JSON 형식으로 반환되는 경우)
    datas = response.json()
    pprint.pprint(datas)
   

else:
    print("요청 실패:", response.text)