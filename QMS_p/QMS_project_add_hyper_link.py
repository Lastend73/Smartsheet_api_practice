import requests
import pprint

# 헤더 설정
headers = {
    "Authorization": "Bearer jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41",
    "Content-Type": "application/json"
}


params = {
    "page": 1,
    "pageSize": 15
}

fail_count = 0
success_count = 0

folder_Id_lst = ['998115009423236','8122950357411716','8867519982266244','2385964971648900']
folder_name_list =[]

sheet_count = len(folder_name_list)

for folder_Id in folder_Id_lst:
    folder_url = f"https://api.smartsheet.com/2.0/folders/{folder_Id}"
    folder_response = requests.get(folder_url, headers=headers, params=params)
    folder_result = folder_response.json()
    folder_datas= folder_result['sheets']
    
    for folder_data in folder_datas :
        folder_name_list.append(folder_data['id'])


# GET 요청 보내기
for sheet_id in folder_name_list :
    main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}"
    response = requests.get(main_sheet_url, headers=headers, params=params)

    # 응답 확인 
    if response.status_code == 200:
        print("요청 성공!")
        # 응답 데이터 처리 (JSON 형식으로 반환되는 경우)
        datas = response.json()
        sheet_url = datas["permalink"]
        print(sheet_url)
        
        sheet_col_info = {}
        for col_info in datas['columns']:
            if col_info["title"] == "부적합" :
                sheet_col_info= {"id":col_info["id"],"title" : col_info["title"]}
                break
        
        row_id_lst = []
        link_add_value = ""
        for row_info in datas['rows']:
            for check in row_info["cells"]:
                if (check['columnId'] == sheet_col_info['id']) &("value" in check):
                    link_add_value = check["value"]
                    row_id_lst.append(row_info['id'])


        for row_id in row_id_lst :
            main_sheet_url = f"https://api.smartsheet.com/2.0/sheets/{sheet_id}/rows"

            data = {
            'id': row_id,
            'cells': [
                    {
                        'columnId': sheet_col_info["id"],
                        "value" : link_add_value,
                        'hyperlink': sheet_url  
                    }
                ]
            }

            update_response = requests.put(main_sheet_url, headers=headers, json=data)
            pprint.pprint(update_response.json()['message'])
            if update_response.status_code == 200:
                success_count += 1
            else :
                fail_count +=1
                print(update_response.json())
        

    else:
        print("요청 실패:", response.text)

    print("Fin")
    print("success : ",success_count)
    print("fail : ",success_count)