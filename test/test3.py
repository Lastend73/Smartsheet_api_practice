import smartsheet
import pprint
import json
# API 액세스 토큰 설정
smartsheet_client = smartsheet.Smartsheet('jq7j4cRjxemFCK9klZ90M7cTYkHyv3qH0El41')

# 시트 ID로 시트 가져오기
response = smartsheet_client.Sheets.get_columns(
  6344154669862788,       # sheet_id
  include_all=True)
columns = response.data

for columns in columns:
    print(columns.title)


# 추가
column2 = smartsheet.models.Column({
  'title': '갱신용4',
  'type': 'DATE',
  'index': 100,
  'hidden' : True
})

# Add columns to the sheet
new_columns = smartsheet_client.Sheets.add_columns(
  6344154669862788,       # sheet_id
[column2])
# 행 추가
