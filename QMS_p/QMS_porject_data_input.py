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
    folder_result = folder_response.json()['sheets']
    # folder_datas= folder_result['sheets']
    
    for folder_data in folder_result :
        folder_name_list.append(folder_data['id'])

count_input_num = 0

# 입력할 연결할 시트 정보 
for input_sheetId in folder_name_list :
    #50 개 단위로 끊기
    if count_input_num%50 == 0 :
        main_sheetId =['5461036178034564','5668977019670404','8695696307736452','3630521116479364']
        main_sheetId = main_sheetId[int(count_input_num/50)]
        main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}"
        pprint.pprint(main_sheet_url)
        main_sheet_response = requests.get(main_sheet_url, headers=headers, params=params)
        main_sheet_results = main_sheet_response.json()["columns"]
        print("sheet change")

    main_sheet_colunm_info = []
    #input_sheetId = folder_name_list[0]    

    updata_data_cells_lst = [] # 업데이트(연결)될 cells 리스트
    input_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{input_sheetId}"
    input_sheet_response = requests.get(input_sheet_url, headers=headers, params=params)
    input_sheet_result = input_sheet_response.json()
    link_row_id = input_sheet_result['rows'][2]['id']

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

    get_row_number = str(response.json()["result"]["rowNumber"])

    added_row_id = response.json()["result"]["id"]
        

    colunm_title_lst = [] #입력될 컬럼의 제목 ID
    for a in main_sheet_colunm_info:
        colunm_title_lst.append(a['title'])

    linked_sheet_column_info = [] #링크 해야할 시트의 콜럼 ID

    for b in input_sheet_result['columns']:
        if b["title"] in colunm_title_lst:
            linked_sheet_column_info.append({"id" :b['id'], "title" : b['title']})


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
                last_row_id = data['id']
                final_goal_update = {
                        "columnId": main_sheet_goal_id, #수정 될 페이지의 컬럼 아이디
                        "value": "",
                        "linkInFromCell":{
                            "rowId" : last_row_id,
                            "columnId" : value["columnId"],
                            'sheetId' : input_sheetId # 연결되 시트아이디
                        }
                    }
    updata_data_cells_lst.append(final_goal_update)

    # reference 생성 및 추가{RAG1...}
    for data in input_sheet_result['columns']:
        if data['title'] == "RAG":
            linked_rag_id = data['id']
            break

    rag_data ={
        "sourceSheetId" :input_sheetId ,
        "name" : "RAG"+get_row_number,
        "endColumnId" : linked_rag_id,
        "startColumnId" : linked_rag_id
    }

    rag_ref_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}/crosssheetreferences"
    rag_ref_response = requests.post(rag_ref_url, headers=headers, json=rag_data)
    if rag_ref_response.status_code == 200:
        print()
    else :
        print(rag_ref_response.json())
    
    if rag_ref_response.status_code != 200 :
        print("50개 초과 정지")
        break

    #reference 생성 및 추가{시정완료}
    for data in input_sheet_result['columns']:

        if data['title'] == "실제 완료일":
            finish_check_id = data['id']
            break

                
    finsh_check_data ={
        "sourceSheetId" :input_sheetId ,
        "name" : "시정완료"+get_row_number,
        "endColumnId" : finish_check_id,
        "startColumnId" : finish_check_id,
        "endRowId" : last_row_id,
        "startRowId" : last_row_id
    }
                    
    finish_check_url = f"https://api.smartsheet.com/2.0/sheets/{main_sheetId}/crosssheetreferences"
    finish_check_response = requests.post(finish_check_url, headers=headers, json=finsh_check_data)
    if finish_check_response.status_code == 200:
        print()
    else :
        print(update_response.json())
    
    #pprint.pprint(finish_check_response.json())
    #COUNTR

    RAG_value = "{RAG"+get_row_number+"}"
    fixed_complete_value = "{시정완료"+get_row_number+"}"
    for i in main_sheet_colunm_info :

        if i['title'] == "COUNTR" :
            updata_data_cells_lst.append(
                    {
                    "columnId": i['id'], #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "formula": f'=COUNTIF({RAG_value}, "RED")'
                }
                )

        #COUNTY
        if i['title'] == "COUNTY" :
            updata_data_cells_lst.append(
                    {
                    "columnId": i['id'], #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "formula": f'=COUNTIF({RAG_value}, "YELLOW")'
                    }
                )

        #시정완료 여부
        if i['title'] == "시정완료 여부" :
            updata_data_cells_lst.append(
                    {
                    "columnId": i['id'], #수정 될 페이지의 컬럼 아이디
                    "value": "",
                    "formula": f'=IFERROR(COUNTIF(YEAR({fixed_complete_value}), ">0"), 0)'
                    }
                )

    cell_update_data = {
            "id" : added_row_id,
            "cells": updata_data_cells_lst
        }
    
    update_response = requests.put(main_sheet_url, headers=headers, json=cell_update_data)
    if update_response.status_code == 200:
        print()
    else :
        print(update_response.json())
    count_input_num +=1
    

#    pprint.pprint(cell_update_data)




# pprint.pprint(input_sheet_result['columns'])