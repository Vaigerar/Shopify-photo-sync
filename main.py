from db.models import *
from pathlib import Path
import asyncio, shopify, os
from core.functions import get_date
from core.gdv import gdv_save_images
from PIL import Image as pillow_images
from core.gsh import check_updates, gsh_auth
from settings import GSH_ID, api_key, api_version, password, shop_name
from module import metafield


loop = asyncio.get_event_loop()

tags = {
	'still_life': ['still_life_painting', 'still_life', 'signed_artwork', 'original_painting', 'oil_still_life', 'oil_painting', 'oil_flowers', 'kitchen_decor', 'flowers_painting', 'art_collectibles'],
	'landscape': ['ukrainian_art', 'signed_artwork', 'original_painting', 'oil_painting', 'oil_landscape', 'nature_painting', 'landscape_painting', 'landscape_art', 'kitchen_decor', 'art_collectibles'],
	'social_realism': ['ukrainian_art', 'socrealism', 'signed_artwork', 'portrait_painting', 'portrait_art', 'original_painting', 'oil_socrealism', 'oil_portrait', 'oil_painting', 'kitchen_decor', 'art_socrealism', 'art_collectibles'],
	'portraits_with_girls': ['signed_artwork', 'portrait_painting', 'portrait_art', 'original_painting', 'oil_portrait', 'oil_painting', 'oil_girl', 'kitchen_decor', 'girl_painitng', 'girl_art', 'art_collectibles'],
	'portraits_with_men': ['signed_artwork', 'portrait_painting', 'portrait_art', 'original_painting', 'oil_portrait', 'oil_painting', 'oil_man', 'kitchen_decor', 'man_painitng', 'man_art', 'art_collectibles'],
	'naked_portraits': ['signed_artwork', 'portrait_painting', 'portrait_art', 'original_painting', 'oil_portrait', 'oil_painting', 'oil_naked', 'kitchen_decor', 'naked_painitng', 'naked_art', 'art_collectibles'],
	'abstract': ['signed_artwork', 'original_painting', 'oil_painting', 'oil_abstract', 'kitchen_decor', 'art_collectibles', 'abstract_painting', 'abstract_art'],
    'portrait': ['art_collectibles', 'original_painting', 'kitchen_decor', 'portrait_painting', 'portrait_art', 'oil_portrait', 'oil_painting']
}


async def choise_sheets(get_list_sheets):
    async def select_sheets(max):
        get_session_id = input(f'\n* Используйте числа от 1 до {max}! › ')

        if get_session_id.isdigit():
            max = int(max)
            get_session_id = int(get_session_id)
            if get_session_id > 0 and get_session_id <= max:
                return get_session_id - 1
            else:
                print(f'[{await get_date()}] [SSYNC] Номер таблицы должен быть больше 0 и не больше {max}! Повторите попытку..')
                return await select_sheets(max=max)
        else:
            print(f'[{await get_date()}] [SSYNC] Номер таблицы должен быть целым числом! Повторите попытку..')
            return await select_sheets(max=max)

    max_list_sheets = len(get_list_sheets)
    print(f'\n[{await get_date()}] [SSYNC] Укажите номер таблицы для запуска работы!')
    for num, sheet_data in zip(range(1, max_list_sheets + 1), get_list_sheets):
        get_title_sheet = sheet_data['properties']['title']
        print(f'⠀{num}. {get_title_sheet}')

    get_select_session = await select_sheets(max=max_list_sheets)
    get_name_sheets = get_list_sheets[get_select_session]['properties']['title']
    print(f'\n* Выбрана таблица с именем ({get_name_sheets})!')
    return get_select_session


async def load_local_photo():
    files_list = []
    folders = os.listdir(os.path.abspath(path='local_photo'))
    if len(folders) > 0:
        for folder in folders:
            if folder.isdigit():
                get_suffix_path = Path(folder).suffix
                if len(get_suffix_path) == 0:
                    files = os.listdir(os.path.abspath(path=f'local_photo/{folder}'))
                    if len(files) > 0:
                        for file in files:
                            get_suffix_path = Path(file).suffix
                            get_file_name = file.replace(get_suffix_path, '')
                            #if get_file_name.isdigit():
                            files_list.append([folder, get_file_name, get_suffix_path])


        if len(files_list) > 0:
            return [True, files_list]
        else:
            return [False, 2]
    else:
        return [False, 1]


async def choise_photo_path():
    async def select_photo_path():
        get_photo_path_type = input('\n* Укажите откуда будем брать фотографии?\n* Из GDrive - 1 | Локально - 2 › ')

        if get_photo_path_type.isdigit():
            get_photo_path_type = int(get_photo_path_type)
            if get_photo_path_type > 0 and get_photo_path_type < 3:
                return get_photo_path_type
            else:
                print(f'[{await get_date()}] [SSYNC] Тип откуда берём фотографии должен 1 или 2, повторите попытку..')
                return await select_photo_path()
        else:
            print(f'[{await get_date()}] [SSYNC] Тип откуда берём фотографии должен быть целым числом, повторите попытку..')
            return await select_photo_path()

    get_select_photo_path = await select_photo_path()
    return get_select_photo_path


async def main():
    print(f'[{await get_date()}] [SSYNC] Запускаюсь..')
    get_choise_photo_path = await choise_photo_path()
    if get_choise_photo_path == 1:
        print(f'\n[{await get_date()}] [SSYNC / Google Drive] Попытка синхронизации фотографий из Google Диска!')
        get_gdv_save_images = await gdv_save_images()
        if get_gdv_save_images[0]:
            files_list = get_gdv_save_images[2]
            if get_gdv_save_images[1] == 1:
                print(f'[{await get_date()}] [SSYNC / Google Drive] Успешная синхронизация, обработано {len(files_list)} файлов!')
            else:
                print(f'[{await get_date()}] [SSYNC / Google Drive] Синхронизация не требуется!')
        else:
            files_list = None
            print(f'[{await get_date()}] [SSYNC / Google Drive] Что-то пошло не так, работа остановлена!\n* Папка указана в настройках пуста.')
    else:
        print(f'\n[{await get_date()}] [SSYNC / Local Drive] Попытка синхронизации фотографий из локальной папки!')
        get_load_local_photo = await load_local_photo()
        if get_load_local_photo[0]:
            files_list = []
            get_files = get_load_local_photo[1]
            for file in get_files:
                if file[0].isdigit():
                    if Image.select().where(Image.name == file[1], Image.folder == file[0]).count() == 0:
                        new_image = Image.create(folder=file[0], name=file[1], expansion=file[2], local=True)
                        files_list.append(new_image.id)

            if len(files_list) > 0:
                print(f'[{await get_date()}] [SSYNC / Local Drive] Успешная синхронизация, обработано {len(files_list)} файлов!')
            else:
                files_list = None
                print(f'[{await get_date()}] [SSYNC / Local Drive] Что-то пошло не так, работа остановлена!\n* Папка пуста!')
        else:
            files_list = None
            if get_load_local_photo[1] == 1:
                print(f'[{await get_date()}] [SSYNC / Local Drive] Что-то пошло не так, работа остановлена!\n* В папке нет папок!')
            else:
                print(f'[{await get_date()}] [SSYNC / Local Drive] Что-то пошло не так, работа остановлена!\n* В папках нет файлов!')


    if files_list is not None:
        get_gsh_auth = await gsh_auth()
        if get_gsh_auth[0]:
            service = get_gsh_auth[1]
            get_data = service.spreadsheets().get(spreadsheetId=GSH_ID).execute()
            get_list_sheets = get_data.get('sheets')

            if len(get_list_sheets) > 0:
                get_choise_sheets = await choise_sheets(get_list_sheets=get_list_sheets)
                print(f'[{await get_date()}] [SSYNC] Начинаю синхронизацию..')
                cu = await check_updates(service=service, get_list_sheets=get_list_sheets, select_choise_sheets=get_choise_sheets)

                if cu[0]:
                    print(f'\n[{await get_date()}] [SSYNC] Новые {len(cu[1])} записи(-ей) записаны!')

                    sfy_url = f"https://{api_key}:{password}@{shop_name}.myshopify.com/admin/api/{api_version}"
                    shopify.ShopifyResource.set_site(sfy_url)

                    i_data = Inventory.select().where(Inventory.processed == False)
                    if i_data.count() > 0:
                        print(f'\n[{await get_date()}] [SSYNC] Синхронизуюсь..')
                        for inventory in i_data:
                            if get_choise_photo_path == 1:
                                image_data = Image.select().where(Image.folder == str(inventory.number),
                                                                  Image.local == False, Image.gdrive == True)
                                folder_drive = 'drive_photo'
                            else:
                                image_data = Image.select().where(Image.folder == str(inventory.number),
                                                                  Image.local == True, Image.gdrive == False)
                                folder_drive = 'local_photo'


                            if image_data.count() > 0:
                                sfy_product = shopify.Product()
                                sfy_product.title = inventory.Lot_Title
                                sfy_product.product_type = inventory.Product_Type

                                inventory_description = inventory.description.split('\r\n')[0].replace('\n', '<br>')
                                sfy_product.body_html = f"{inventory_description}"
                                sfy_product.vendor = "Ukrainianvintage"

                                variant = shopify.Variant({
                                                "sku": inventory.SKU,
                                                "price": inventory.Reserve,
                                                "inventory_policy": 'continue',
                                                "inventory_management": 'shopify',
                                                "barcode": '',
                                                "inventory_quantity":1,
                                                "old_inventory_quantity":1,


                                        })
                                print(variant)
                                sfy_product.variants = [variant]
                                sfy_product.collections = ["Artwork"]


                                list_images = []
                                for get_i_data in image_data:
                                    #Полный путь до картинки
                                    get_image_full_path = f'{folder_drive}/{get_i_data.folder}/{get_i_data.name}{get_i_data.expansion}'

                                    #Получаем размер картинки в байтах
                                    new_getsize = os.path.getsize(get_image_full_path)
                                    if new_getsize >= 1048576:
                                        #Открытие картинки
                                        c_image = pillow_images.open(get_image_full_path)

                                        #Получение размеров (высота/ширина)
                                        c_image_width, c_image_height = c_image.size

                                        #Сжимаем картинку в 2 раза
                                        c_image_resize = c_image.resize((int(c_image_width / 2), int(c_image_height / 2)))

                                        #Сохраняем результат
                                        c_image_resize.save(get_image_full_path)

                                    image = shopify.Image()
                                    with open(get_image_full_path, "rb") as f:
                                        load_image = f.read()
                                        image.attach_image(load_image, filename=f'{get_i_data.name}{get_i_data.expansion}')
                                        list_images.append(image)

                                sfy_product.images = list_images

                                tag_text = ''
                                number = 0
                                tag_type = inventory.Product_Type.replace(' ', '_').lower()

                                get_tags = tags.get(tag_type, None)
                                if get_tags is not None:
                                    count_tags = len(get_tags)
                                    for tag in get_tags:
                                        number += 1
                                        if number < count_tags:
                                            tag_text += f'{tag}, '
                                        else:
                                            tag_text += tag

                                    sfy_product.tags = tag_text
                                    print(f'[{await get_date()}] [SSYNC] Теги к товару №{inventory.id} успешно установлены!')

                                sfy_product.save()
                                
                                metafield.add_metafields(sfy_product.id, inventory)


                                print(f'\n[{await get_date()}] [SSYNC] Товар №{inventory.id} успешно добавлен!')

                                inventory.processed = True
                                inventory.save()

                            else:
                                print(f'\n[{await get_date()}] [SSYNC] Товар №{inventory.id} не был добавлен!\n* Картинка не найдена!')
                    else:
                        print(f'\n[{await get_date()}] [SSYNC] Синхронизация не нужна!')
                else:
                    print(f'\n[{await get_date()}] [SSYNC] Новых данных для обработки нет!')
            else:
                print(f'\n[{await get_date()}] [SSYNC] Листов в таблице нет, завершаю работу!')
        else:
            print(f'\n[{await get_date()}] [SSYNC] Не могу авторизовать аккант для работы с Google Таблицами!\n{get_gsh_auth[1]}')
    else:
        print('* Исправьте ошибку и перезапустите программу.')


loop.run_until_complete(main())
