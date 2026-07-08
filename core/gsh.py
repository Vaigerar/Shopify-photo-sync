from db.models import *
import httplib2, apiclient
from settings import GSH_ID, GSH_ACCOUNT
from oauth2client.service_account import ServiceAccountCredentials

'''
async def check_updates(service):
    get_data = service.spreadsheets().values().get(spreadsheetId=GSH_ID, range='A2:M100', majorDimension='ROWS').execute()

    new_i_data_list = []
    for value in get_data['values']:
        get_id = value[0]
        get_title = value[1]
        get_description = value[2]
        get_reserve = value[6]
        get_genres = value[12]

        i_data = Inventory.select().where(Inventory.number == get_id)
        if i_data.count() == 0:
            i_data = Inventory.create(number=get_id, title=get_title, description=get_description,
                                        reserve=get_reserve, genres=get_genres)

            new_i_data_list.append(i_data)

    if len(new_i_data_list) > 0:
        return [True, new_i_data_list]
    else:
        return [False]
'''


async def check_updates(service, get_list_sheets, select_choise_sheets):
    sheets_titles_dict = {'Lot Number': None, 'SKU': None, 'Width': None, 'Height': None,
                          'Materials': None, 'Basis': None, 'Product Type': None,
                          'Subject': None, 'Lot Title': None, 'Lot Description': None, 'Reserve': None,
                          'iteration_number': 0}
    alphabet_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']

    get_choise_sheets = get_list_sheets[select_choise_sheets]
    get_name_sheet = get_choise_sheets['properties']['title']
    get_row_count = get_choise_sheets['properties']['gridProperties']['rowCount']
    get_column_count = get_choise_sheets['properties']['gridProperties']['columnCount']
    get_alphabet_first_letter = alphabet_list[0]
    delta = (get_column_count - (25))
    get_alphabet_second_letter = alphabet_list[get_column_count - delta]


    # Получение заголовком таблицы
    get_data_sheets_tltle = service.spreadsheets().values().get(spreadsheetId=GSH_ID,
                                                                range=f'{get_name_sheet}!{get_alphabet_first_letter}1:{get_alphabet_second_letter}{1}').execute()
    print(get_data_sheets_tltle)
    for title in get_data_sheets_tltle['values'][0]:
        get_sheets_titles_dict = sheets_titles_dict.get(title, False)
        if get_sheets_titles_dict != False:
            sheets_titles_dict[title] = sheets_titles_dict['iteration_number']

        sheets_titles_dict['iteration_number'] += 1

    new_i_data_list = []

    get_data_sheet = service.spreadsheets().values().get(spreadsheetId=GSH_ID,
                                                             range=f'{get_name_sheet}!{get_alphabet_first_letter}2:{get_alphabet_second_letter}{get_row_count}',
                                                             majorDimension='ROWS').execute()

    for sheet_data in get_data_sheet['values']:

        try:
            # print(sheet_data[sheets_titles_dict.get('Lot Number', '')])
            get_id = sheet_data[sheets_titles_dict.get('Lot Number', '')]
            # print(sheet_data[sheets_titles_dict.get('SKU', '')])
            get_SKU = sheet_data[sheets_titles_dict.get('SKU', '')]

            if ',' in sheet_data[sheets_titles_dict.get('Width', '')]:
                get_Width = sheet_data[sheets_titles_dict.get('Width', '')].replace(",", ".")
            else:
                get_Width = sheet_data[sheets_titles_dict.get('Width', '')]
            # print(sheet_data[sheets_titles_dict.get('Width', '')])
            if ',' in sheet_data[sheets_titles_dict.get('Height', '')]:
                get_Height = sheet_data[sheets_titles_dict.get('Height', '')].replace(",", ".")
            else:
                get_Height = sheet_data[sheets_titles_dict.get('Height', '')]
            # print(sheet_data[sheets_titles_dict.get('Height', '')])
            # print(sheet_data[sheets_titles_dict.get('Materials', '')])
            get_Materials = sheet_data[sheets_titles_dict.get('Materials', '')]
            # print(sheet_data[sheets_titles_dict.get('Basis', '')])
            get_Basis = sheet_data[sheets_titles_dict.get('Basis', '')]
            # print(sheet_data[sheets_titles_dict.get('Product Type', '')])
            get_Product_Type = sheet_data[sheets_titles_dict.get('Product Type', '')]
            # print(sheet_data[sheets_titles_dict.get('Subject', '')])
            get_Subject = sheet_data[sheets_titles_dict.get('Subject', '')]
            # print(sheet_data[sheets_titles_dict.get('Lot Title', '')])
            get_Lot_Title = sheet_data[sheets_titles_dict.get('Lot Title', '')]
            # print(sheet_data[sheets_titles_dict.get('Lot Description', '')])
            get_Lot_Description = sheet_data[sheets_titles_dict.get('Lot Description', '')]
            # print(sheet_data[sheets_titles_dict.get('Reserve', '')])
            get_Reserve = sheet_data[sheets_titles_dict.get('Reserve', '')]

            i_data = Inventory.select().where(Inventory.number == get_id, Inventory.Lot_Title == get_Lot_Title)

            if i_data.count() == 0:
                i_data = Inventory.create(number=get_id, SKU=get_SKU, Width=get_Width, Height=get_Height,
                                          Materials=get_Materials,
                                          Basis=get_Basis, Product_Type=get_Product_Type, Subject=get_Subject,
                                          Lot_Title=get_Lot_Title, description=get_Lot_Description, Reserve=get_Reserve,
                                          sheet_name=get_name_sheet)
                new_i_data_list.append(i_data)
        except:
            pass

    # Устанавливаем значение словаря по умолчанию
    for sheets_titles in sheets_titles_dict:
        if sheets_titles != 'iteration_number':
            sheets_titles_dict[sheets_titles] = None
        else:
            sheets_titles_dict['iteration_number'] = 0

    if len(new_i_data_list) > 0:
        return [True, new_i_data_list]
    else:
        return [False]


async def gsh_auth():
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GSH_ACCOUNT,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])

        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
        return [True, service]
    except Exception as error:
        return [False, error]
