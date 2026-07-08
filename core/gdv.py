import os
from db.models import *
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from settings import GDV_ACCOUNT, GDV_FOLDER_ID


async def gdv_save_images():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(GDV_ACCOUNT)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(GDV_ACCOUNT)
    drive = GoogleDrive(gauth)
    print(drive)

    files_list = []
    folder_list = drive.ListFile({"q": f"mimeType='application/vnd.google-apps.folder' and '{GDV_FOLDER_ID}' in parents and trashed=false"}).GetList()

    if len(folder_list) > 0:
        for folder in folder_list:
            get_folder_id = folder['id']
            get_folder_title = folder['title']
            if get_folder_title.isdigit():
                if not os.path.isdir(f'drive_photo/{get_folder_title}'):
                    os.mkdir(f'drive_photo/{get_folder_title}')

                get_files = drive.ListFile({'q': f"'{get_folder_id}' in parents and trashed=false"}).GetList()
                if len(get_files) > 0:
                    for file in get_files:
                        get_file_name = file['title']
                        get_suffix_path = Path(get_file_name).suffix
                        get_file_name_without_suffix = get_file_name.replace(get_suffix_path, '')

                        #if get_file_name_without_suffix.isdigit():
                        if Image.select().where(Image.folder == get_folder_title, Image.name == get_file_name_without_suffix).count() == 0:
                            new_image = Image.create(name=get_file_name_without_suffix, folder=get_folder_title,
                                                     expansion=get_suffix_path, gdrive=True)

                            file.GetContentFile(f'drive_photo/{get_folder_title}/{get_file_name}')
                            files_list.append(new_image.id)

        if len(files_list) > 0:
            return [True, 1, files_list]
        else:
            return [True, 2, files_list]
    else:
        return [False]