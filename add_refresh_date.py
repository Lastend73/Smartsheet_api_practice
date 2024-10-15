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

smartsheet_client = smartsheet.Smartsheet('jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41')

# API 엔드포인트
base_url = "https://api.smartsheet.com/2.0/workspaces"
workspace_id = "950257455523716"

date_control_ld_list = []  # 일정관리 시트 아이디 List


def get_sheet_ids(base_url,folder_id):
    """
    주어진 폴더 ID 아래의 모든 "일정관리" 시트 ID를 찾는 재귀 함수
    """
    url = f"{base_url}/{folder_id}"
    print(url)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if "sheets" in data:
            for sheet in data["sheets"]:
                if "일정관리" in sheet["name"]:
                    
                    column2 = smartsheet.models.Column({
                    'title': '갱신일',
                    'type': 'DATE',
                    'index': 100,
                    'hidden' : True
                    })

                    new_columns = smartsheet_client.Sheets.add_columns(
                    sheet["id"],       # sheet_id
                    [column2])

                    date_control_ld_list.append(sheet["id"])
                    print(sheet["name"])

        if "folders" in data:
            for folder in data["folders"]:
                print(folder["name"])
                get_sheet_ids("https://api.smartsheet.com/2.0/folders",folder["id"])  # 하위 폴더에 대해 재귀 호출
    else:
        print(f"폴더 요청 실패: {response.status_code}")


get_sheet_ids(base_url,workspace_id)

print("일정관리 시트 ID:", date_control_ld_list)
print("sheet 개수 : ",len(date_control_ld_list))