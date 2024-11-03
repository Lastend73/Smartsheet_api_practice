import requests
import pprint
import smartsheet

# 헤더 설정
headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41",
    "Content-Type": "application/json",
}


params = {"page": 1, "pageSize": 70}

# data ={
#     "sourceSheetId" : 6374450563862404,
#     "name" : "TEST2",
#     "endColumnId" : 5736227184791428,
#     "startColumnId" : 5736227184791428
# }

# API 엔드포인트
main_sheetId = "5755279152992132"
smartsheetUrl = "https://api.smartsheet.com/2.0/sheets"

smartsheet_client = smartsheet.Smartsheet("jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41")
# GET 요청 보내기
response = requests.get(
    f"{smartsheetUrl}/{main_sheetId}", headers=headers, params=params
)

# 응답 확인
if response.status_code == 200:

    data = response.json()
    pprint.pprint(data["rows"][0])
    main_person_column_id = data["columns"][8]['id'] #주 담당자 ID (모든 컬럼 추가된다음)
    link_data_list = []

    input_column1 = smartsheet.models.Column(
        {
            "title": "요청부서",
            "type": "TEXT_NUMBER",
            "index": 4,
        }
    )
    input_column_result = smartsheet_client.Sheets.add_columns(
        main_sheetId, [input_column1]  # sheet_id
    )
    
    #요청부서 ID
    input_column1_id = input_column_result.to_dict()["data"][0]["id"]

    input_column2 = smartsheet.models.Column(
        {
            "title": "진행상태",
            "type": "TEXT_NUMBER",
            "index": 9,
        }
    )
    input_column_result = smartsheet_client.Sheets.add_columns(
        main_sheetId, [input_column2]  # sheet_id
    )
    #진행상태 ID
    input_column2_id = input_column_result.to_dict()["data"][0]["id"]


    input_column3 = smartsheet.models.Column(
        {
            "title": "부담당자",
            "type": "TEXT_NUMBER",
            "index": 11,
        }
    )
    input_column_result = smartsheet_client.Sheets.add_columns(
        main_sheetId, [input_column3]  # sheet_id
    )

    #부담당자 ID
    input_column3_id = input_column_result.to_dict()["data"][0]["id"]
 
    update_column = smartsheet.models.Column(
        {
            "width" : 150,
            "hidden" : False,
        }
    )

    response = smartsheet_client.Sheets.update_column(
        main_sheetId,       # sheet_id
        main_person_column_id,       # column_id
        update_column)
    # 주담당자 ID
    update_col_id = response.to_dict()["data"]["id"]
    
    

    for link_data in data["rows"]:
        # 기존에 링크된 시트들의 정보
        update_url = f"{smartsheetUrl}/{main_sheetId}/rows"
        update_cell_list =[]

        cell_info = {}
        cell_info["rowId"] = link_data["cells"][3]["linkInFromCell"]["rowId"]
        cell_info["sheetId"] = link_data["cells"][3]["linkInFromCell"]["sheetId"]
        cell_info["sheetName"] = link_data["cells"][3]["linkInFromCell"]["sheetName"]

        # 링크 추가할 데이터들의 컬럼 ID 모음 [요청부서, 진행상태, 주담당자,부담당자]
        new_cell_response = requests.get(
            f"{smartsheetUrl}/{cell_info["sheetId"]}", headers=headers, params=params).json()
        new_cell_response = new_cell_response["columns"]

        new_cell_id = {}



        for new_data in new_cell_response:
            if "요청부서" in new_data["title"]:
                new_cell_id["요청부서"] = new_data["id"]
            elif "진행상태" in new_data["title"]:
                new_cell_id["진행상태"] = new_data["id"]
            elif "주담당자" in new_data["title"]:
                new_cell_id["주담당자"] = new_data["id"]
            elif "부담당자" in new_data["title"]:
                new_cell_id["부담당자"] = new_data["id"]
        print(new_cell_id)
        
        
        cell_update_data = {
                "id": link_data['id'],
                "cells": [
                    #요청부서
                    {
                    "columnId": input_column1_id, #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell":{
                        "rowId" :  cell_info["rowId"],
                        "columnId" : new_cell_id["요청부서"],
                        'sheetId' : cell_info["sheetId"] # 연결되 시트아이디
                    }
                },
                #진행상태
                    {
                    "columnId": input_column2_id, #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell":{
                        "rowId" :  cell_info["rowId"],
                        "columnId" : new_cell_id["진행상태"],
                        'sheetId' : cell_info["sheetId"] # 연결되 시트아이디
                    }
                },
                #주담당자
                    {
                    "columnId": update_col_id, #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell":{
                        "rowId" :  cell_info["rowId"],
                        "columnId" : new_cell_id["주담당자"],
                        'sheetId' : cell_info["sheetId"] # 연결되 시트아이디
                    }
                },
                #부담당자
                    {
                    "columnId": input_column3_id, #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell":{
                        "rowId" :  cell_info["rowId"],
                        "columnId" : new_cell_id["부담당자"],
                        'sheetId' : cell_info["sheetId"] # 연결되 시트아이디
                    }
                }
                ]
            }
        
        pprint.pprint(cell_update_data)
        response = requests.put(
            update_url, headers=headers, json=cell_update_data
        )
        pprint.pprint(response.json())
            
    
    # pprint.pprint(response.json())

    
# else:
    # print("요청 실패:", response.text)
