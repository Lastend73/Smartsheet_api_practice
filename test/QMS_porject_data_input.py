import requests
import pprint

headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41"
}

params = {
    "page": 1,
    "pageSize": 100
}

#붙혀 넣을 시트가 모여있는 폴더
folder_Id_lst = ['998115009423236','8122950357411716','8867519982266244','2385964971648900']
folder_name_list =[]

for folder_Id in folder_Id_lst:
    folder_url = f"https://api.smartsheet.com/2.0/folders/{folder_Id}"
    folder_response = requests.get(folder_url, headers=headers, params=params)
    folder_result = folder_response.json()
    folder_datas= folder_result['sheets']
    
    for folder_data in folder_datas :
        folder_name_list.append(folder_data['id'])

# 입력될 시트 정보 
main_sheetId ='3277342667394948'
main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}"
main_sheet_response = requests.get(main_sheet_url, headers=headers, params=params)
main_sheet_results = main_sheet_response.json()["columns"]

main_sheet_colunm_info = []

for main_sheet_result in main_sheet_results :
    main_sheet_colunm_info.append({'id': main_sheet_result['id'],'title':main_sheet_result['title']})
    if main_sheet_result['title'] == '시정조치 목표일':
        main_sheet_goal_id = main_sheet_result['id']

#입력 식
data ={
    "cells" : [

    ]
}
for input_data in main_sheet_colunm_info :
    if input_data['title'] not in ['RAG','프로젝트 상태']:
        data["cells"].append({"columnId" : input_data["id"],"value" : "Test"})
        break

main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}/rows"
response = requests.post(main_sheet_url, headers=headers, json=data)

# added_row_id = response.json()
added_row_id = response.json()["result"]["id"]
    
# 입력할 연결할 시트 정보 
input_sheetId = folder_name_list[0]
input_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{input_sheetId}"
input_sheet_response = requests.get(input_sheet_url, headers=headers, params=params)
input_sheet_result = input_sheet_response.json()
link_row_id = input_sheet_result['rows'][2]['id']

colunm_title_lst = [] #입력될 컬럼의 제목 ID
for a in main_sheet_colunm_info:
    colunm_title_lst.append(a['title'])

linked_sheet_column_info = [] #링크 해야할 시트의 콜럼 ID

for b in input_sheet_result['columns']:
    if b["title"] in colunm_title_lst:
        linked_sheet_column_info.append({"id" :b['id'], "title" : b['title']})

updata_data_cells_lst = [] # 업데이트(연결)될 cells 리스트

for i in main_sheet_colunm_info :
    if i['title'] not in ['RAG','프로젝트 상태']:
        for j in linked_sheet_column_info :
            if i['title'] == j['title'] :
                updata_data_cells_lst.append(
                    {
                    "columnId": i['id'], #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell": {
                        'sheetId' : input_sheetId, # 연결되 시트아이디
                        'columnId' : j['id'], #연결된 시트의 컬럼 ID
                        'rowId' :link_row_id, # 연결된 시트의 열 ID
                    }
                }
                )
                continue
# 완료 목표일 링크

for data in input_sheet_result['columns']:
    if data['title'] == "목표 완료일":
        goal_date_id = data['id']

for data in input_sheet_result['rows']:
    for value in data['cells']:
        if (value['columnId'] == goal_date_id) & ("value" in value):
            final_goal_update = {
                    "columnId": main_sheet_goal_id, #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "linkInFromCell":{
                        "rowId" : data['id'],
                        "columnId" : value["columnId"],
                        'sheetId' : input_sheetId # 연결되 시트아이디
                    }
                }
updata_data_cells_lst.append(final_goal_update)


cell_update_data = {
        "id" : added_row_id,
        "cells": updata_data_cells_lst
    }
update_response = requests.put(main_sheet_url, headers=headers, json=cell_update_data)

print(update_response.json())

# pprint.pprint(input_sheet_result['columns'])