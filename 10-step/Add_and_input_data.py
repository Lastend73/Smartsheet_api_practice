import requests
import pprint
import smartsheet

headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41",
    "Content-Type": "application/json",
}

params = {"page": 1, "pageSize": 10}

base_url = "https://api.smartsheet.com/2.0/workspaces"
workspace_id = "950257455523716"

date_control_ld_list = []  # 일정관리 시트 아이디 List


smartsheet_client = smartsheet.Smartsheet("jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41")


def get_sheet_ids(base_url, folder_id):

    url = f"{base_url}/{folder_id}"
    print(url)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        if "sheets" in data:
            for sheet in data["sheets"]:
                if "전체 프로젝트 상태" in sheet["name"]:

                    column1 = smartsheet.models.Column(
                        {
                            "title": "진행상태",
                            "type": "TEXT_NUMBER",
                            "index": 100,
                            "hidden": True,
                        }
                    )

                    column2 = smartsheet.models.Column(
                        {
                            "title": "주담당자",
                            "type": "TEXT_NUMBER",
                            "index": 100,
                            "hidden": True,
                        }
                    )

                    column3 = smartsheet.models.Column(
                        {
                            "title": "부담당자",
                            "type": "TEXT_NUMBER",
                            "index": 100,
                            "hidden": True,
                        }
                    )

                    new_columns = smartsheet_client.Sheets.add_columns(
                        sheet["id"], [column2]  # sheet_id
                    )

                    date_control_ld_list.append(sheet["id"])
                    print(sheet["name"])

    if "folders" in data:
        for folder in data["folders"]:
            print(folder["name"])
            get_sheet_ids(
                "https://api.smartsheet.com/2.0/folders", folder["id"]
            )  # 하위 폴더에 대해 재귀 호출
