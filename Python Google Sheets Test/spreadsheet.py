import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

worksheet = client.open("test").get_worksheet(0)

cell_list = worksheet.range('A1:C7')

for cell in cell_list:
    cell.value = 'O_o'
    
worksheet.update_cells(cell_list)
