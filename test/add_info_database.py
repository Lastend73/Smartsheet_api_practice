# workspace 정보 테이블
# Folder 정보 -> 상위 폴더 여부(최상위 폴더는 0), workspace 위치 ID, 폴더 이름
# sheet 정보 -> sheet 이름, sheet ID , sheet 폴더
# report -> report 이름, report ID, report 폴더

import requests
import pprint

headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41"
}

params = {
    "page": 1,
    "pageSize": 10
}

workspace_url = "https://api.smartsheet.com/2.0/workspaces"

# GET 요청 보내기
workspace_response = requests.get(workspace_url, headers=headers, params=params)

Workspace_info_list=[]

if workspace_response.status_code == 200:
    print("요청 성공!")
    # 응답 데이터 처리 (JSON 형식으로 반환되는 경우)
    data = workspace_response.json()

    pprint.pprint(data['data'][0])

    results = data

