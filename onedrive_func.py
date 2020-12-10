


# Import libraries
import requests
import msal
import atexit
import os
import pandas as pd
import pprint as pp
from tabulate import tabulate
from pathlib import Path
import config

def get_authentication_service():
    # Token caching
    # Each time you run the minimal example above, you will have to click on the link and log in with your web browser. 
    # We can avoid having to do this every time by adding a serializable token cache to the MSAL app when it is created
    cache = msal.SerializableTokenCache()

    if os.path.exists('token_cache.bin'):
        cache.deserialize(open('token_cache.bin', 'r').read())

    # Serialization
    # In order for the cache to useful in a command-line app, we need to serialize it to a file or some other form of storage so it can be accessed the next time you run the command. For example, to serialize to a file:
    # This writes the cache out to the file when your script terminates.
    atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

    # Create the MSAL Device Code flow application.
    # The app can run as a Python Console Application. It gets the list of users in an Azure AD tenant by using Microsoft Authentication Library (MSAL) for Python to acquire a token
    # PublicClientApplication - Class to be used to acquire tokens in desktop or mobile applications
    # https://docs.microsoft.com/en-us/java/api/com.microsoft.identity.client.publicclientapplication?view=azure-java-stable
    app = msal.PublicClientApplication(config.CLIENT_ID, authority = config.AUTHORITY, token_cache = cache)

    # Acquire the token
    # Firstly, looks up a token from cache
    # If that fails, attempt the device code flow
    accounts = app.get_accounts()
    result = None
    if len(accounts) > 0:
        result = app.acquire_token_silent(config.SCOPES, account=accounts[0])


    # Skipping account iteration and cache lookup
    if result is None:
        flow = app.initiate_device_flow(scopes=config.SCOPES)
        if 'user_code' not in flow:
            raise Exception('Failed to create device flow')

        print(flow['message'])

        result = app.acquire_token_by_device_flow(flow)

    return result


def onedrive_get_my_profile(authen):
    resp = requests.get(f'{config.ENDPOINT}/me', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    print(data.keys())
    pp.pprint(data)

# List all files and folders on my drive
def onedrive_listFilesAtRoot_on_myDrive(authen):

    rows = []
    resp = requests.get(f'{config.ENDPOINT}/me/drive/root/children', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    count = data.get("@odata.count", [])
    items = data.get("value")
    print(data.keys()) # dict_keys(['@odata.context', '@odata.count', 'value'])
    print(f"There are {count} items")

    # save the items into a list
    for item in items:
        # pp.pprint(item)
        id = item.get("id", [])
        name = item.get("name", [])
        folder = item.get("folder", "N/A")
        if folder == "N/A":
            chichildCount = 0
            type_item = "File"
        else:
            chichildCount = folder.get("childCount")
            type_item = "Folder"
        url = item.get("webUrl", [])

        rows.append((id, name, type_item, chichildCount, url))

    headers = ['Id' , 'Name' , 'Type', 'Sub folders' , 'Url']
    print(tabulate(rows, headers = headers))

# List all subfolders and files
def onedrive_get_children_on_myDrive(authen, itemID):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{itemID}/children', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    count = data.get("@odata.count", [])
    items = data.get("value")
    print(data.keys()) # dict_keys(['@odata.context', '@odata.count', 'value'])
    print(f"There are {count} items")
    # for item in items:
    #     print("==============================================================================================================")
    #     pp.pprint(item)
        # print(item.get("id", []))
        # print(item.get("name", []))
        # pp.pprint(item.get("folder", []))
        # print(item.get("webUrl", []))

    rows = []
    for item in items:
        # pp.pprint(item)
        id = item.get("id", [])
        name = item.get("name", [])
        parentReference = item.get("parentReference", []).get("name", [])
        folder = item.get("folder", "N/A")

        if folder == "N/A":
            chichildCount = 0
            type_item = "File"
        else:
            chichildCount = folder.get("childCount")
            type_item = "Folder"
        url = item.get("webUrl", [])

        rows.append((id, name, parentReference, type_item, chichildCount, url))

    headers = ['Id' , 'Name' , 'Parent Folder' , 'Type', 'Sub folders' , 'Url']
    print(tabulate(rows, headers = headers))


def onedrive_get_myRecentFile_on_myDrive(authen):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/recent', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    print(data.keys())
    pp.pprint(data)


def onedrive_get_item_by_itemID_on_myDrive(authen, itemid):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{itemid}', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    print(data.keys())
    pp.pprint(data)

# Provide the itemId and return its name
def onedrive_convert_Id_to_Name(authen, itemid):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{itemid}', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    name = data.get("name", [])
    return name
'''
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_move?view=odsp-graph-online
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_update?view=odsp-graph-online

Move item to new folder
    To move a DriveItem to a new parent item, your app requests to update the parentReference of the DriveItem to move
    This is a special case of the Update method
    Items cannot be moved between Drives using this request.

'''

def onedrive_move_item_to_new_folder(anthen, item_id, new_folder_id):
  
    # Calling the onedrive_item_id_belongs_parent_id() to check the item name belongs to new destination or not
    # It returns True and itemId. Otherwise, return False and None
    is_existing, itemID = onedrive_item_id_belongs_parent_id(anthen, item_id, new_folder_id)
    
    
    if is_existing:
        print("You already have a file or folder with the same name !")
    else:

        DriveItem = {
        "parentReference": {
            "id": new_folder_id
        }
        # "name": "new-item-name.txt"
        }

        resp = requests.patch(f'{config.ENDPOINT}/me/drive/items/{item_id}', 
                            headers={'Authorization': 'Bearer ' + anthen['access_token'],
                                    'Content-Type': 'application/json'},
                            json = DriveItem)


        # data = resp.json()
        # print(data.keys())
        pp.pprint(resp.status_code)


# Check if item belongs to a folder or not. If Yes, return True and its id, otherwise return False and None
def onedrive_item_id_belongs_parent_id(authen, item_id, parent_id):
    # Get the list of subfolder in the parent
    
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{parent_id}/children', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    count = data.get("@odata.count", [])
    items = data.get("value")
    # print(data.keys()) # dict_keys(['@odata.context', '@odata.count', 'value'])
    # print(f"There are {count} items")

    # Get the item name from itemId
    item_name = onedrive_convert_Id_to_Name(authen, item_id)

    for item in items:
        name = item.get("name", [])
        if name == item_name:
            # Return the True and its id
            return (True, item.get("id", []))
    
    return False, None

# Get item location
def onedrive_get_item_location(authen, item_id):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{item_id}', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()

    location = data.get("parentReference" , []).get("path" , [])
    url = data.get("webUrl" , [])

    # print(location)
    # print(url)
    return location, url


# Copy a driveitem
# https://docs.microsoft.com/en-us/graph/api/driveitem-copy?view=graph-rest-1.0&tabs=http
# Copy item (via itemId) to the new destimation

def onedrive_copy_item(authen, item_id, parent_id):

    # Calling the onedrive_item_id_belongs_parent_id() to check the item name belongs to new destination or not
    # It returns True and itemId. Otherwise, return False and None
    is_existing, itemID = onedrive_item_id_belongs_parent_id(authen, item_id, parent_id)
    
    
    if is_existing:
        print("You already have a file or folder with the same name !")
    else:

        # Copying a file identified by {item-id} into a folder identified with a driveId and id value. 
        # The new copy of the file will be named contoso plan (copy).txt
        DriveItem = {
                        "parentReference": {
                                            # "driveId": "6F7D00BF-FC4D-4E62-9769-6AEA81F3A21B",
                                            "id": parent_id
                                            },
                        # "name": "contoso plan (copy).txt"
         }

        resp = requests.post(f'{config.ENDPOINT}/me/drive/items/{item_id}/copy', 
                            headers={'Authorization': 'Bearer ' + authen['access_token'],
                                    'Content-Type': 'application/json'},
                            json = DriveItem)

    
# def onedrive_copy_item_temp(authen, item_id, new_location_id):

#     # Copying a file identified by {item-id} into a folder identified with a driveId and id value. The new copy of the file will be named contoso plan (copy).txt

#     DriveItem = {
#     "parentReference": {
#                         # "driveId": "6F7D00BF-FC4D-4E62-9769-6AEA81F3A21B",
#                         "id": new_location_id
#                         },
#     # "name": "contoso plan (copy).txt"
#     }

#     resp = requests.post(f'{config.ENDPOINT}/me/drive/items/{item_id}/copy', 
#                         headers={'Authorization': 'Bearer ' + authen['access_token'],
#                                  'Content-Type': 'application/json'},
#                         json = DriveItem)

#     print(resp.status_code)

# Search items by keywork
# https://docs.microsoft.com/en-us/graph/api/driveitem-search?view=graph-rest-1.0&tabs=http
# https://docs.microsoft.com/en-us/graph/query-parameters

'''

This method returns an object containing an collection of DriveItems that match the search criteria. If no items were found, an empty collection is returned

    Parameters:
        option: False  - item name contains keyword
                True  = item name equals keyword (not including extension)

    Cut the the beginning and ending spaces of keyword by calling strip()
    The query returns a list of result that contains the keyword. 
    We will go through the list and check each item (name field) ensure it matches condition (case) :
    Case 1: Name item contains keyword 
    Case 2: Name item (not including extion) equals keyword



'''
def onedrive_search_items_by_keyword_on_myDrive(authen, keyword, option):
    
    result_list = []

    keyword = keyword.strip()

    resp = requests.get(f"{config.ENDPOINT}/me/drive/root/search(q='{keyword}')", headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    print(data.keys()) # dict_keys(['@odata.context', '@odata.nextLink', 'value'])
    
    result = data.get("value", [])

    if option == False: # item name contains keyword
        for item in result:
            name = item.get("name" , [])
            if (str.lower(keyword) in str.lower(name)): # file or folder name contairns keyword
                id = item.get("id" , [])
                name = item.get("name" , [])
                path = item.get("parentReference" , []).get("path", [])
                location = item.get("webUrl" , [])

                result_list.append((id, name, path, location))

    if option == True: # item name equals keyword (not including extension)
        for item in result:
            name = item.get("name" , [])
            if (str.lower(keyword) == str.lower(name)): # file name equal keyword (including extension)
            
                id = item.get("id" , [])
                name = item.get("name" , [])
                path = item.get("parentReference" , []).get("path", [])
                location = item.get("webUrl" , [])

                result_list.append((id, name, path, location))


    if (len(result_list) == 0):
        print("No Found !")

    else:
        print(f"There are {len(result_list)} item(s)")
        print("===========================================================")
        for item in result_list:
            print(item)

# def onedrive_search_items_by_keyword_on_myDrive_temp2(authen, keyword):
    
#     result_list = []

#     keyword = keyword.strip()

#     resp = requests.get(f"{config.ENDPOINT}/me/drive/root/search(q='{keyword}')", headers={'Authorization': 'Bearer ' + authen['access_token']})
#     data = resp.json()
#     print(data.keys()) # dict_keys(['@odata.context', '@odata.nextLink', 'value'])
    
#     result = data.get("value", [])

  
#     for item in result:

#         # pp.pprint(result[item])
#         name = item.get("name" , [])
#         if keyword == name: # file name equal keyword (including extension)
#         # if (str.lower(keyword) in str.lower(name)): # file or folder name contairns keyword
#             id = item.get("id" , [])
#             name = item.get("name" , [])
#             path = item.get("parentReference" , []).get("path", [])
#             location = item.get("webUrl" , [])

#             result_list.append((id, name, path, location))


#     if (len(result_list) == 0):
#         print("No Found !")

#     else:
#         print(f"There are {len(result_list)} item(s)")
#         print("===========================================================")
#         for item in result_list:
#             print(item)

# def onedrive_search_items_by_keyword_on_myDrive_temp1(authen, keyword):
#     resp = requests.get(f"{config.ENDPOINT}/me/drive/root/search(q='{keyword}')", headers={'Authorization': 'Bearer ' + authen['access_token']})
#     data = resp.json()
#     print(data.keys()) # dict_keys(['@odata.context', '@odata.nextLink', 'value'])
    
#     result = data.get("value", [])
#     if (len(result) == 0):
#         print("No Found !")
#     else:
#         for i in range(0, 10):
#             pp.pprint(result[i])

# Folder
# Create a folder 
# https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
# https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
# https://stackoverflow.com/questions/44379557/error-creating-folder-with-onedrive-api-javascript


def onedrive_create_folder_on_myDrive(authen, parent_id, folder_name):
    DriveItem = {
        "name": folder_name,
        "folder": { },
        "@microsoft.graph.conflictBehavior": "rename" # Value is fail, replace, or rename. It is used indicates that if an item already exists with the same name, the service should choose a new name for the folder while creating it
    }

    # If successful, this method returns 201 Created response code and a Driveitem resource in the response body.
    resp = requests.post(f'{config.ENDPOINT}/me/drive/items/{parent_id}/children', 
                        headers={'Authorization': 'Bearer ' + authen['access_token'],
                                 'Content-Type': 'application/json'},
                        json = DriveItem)


    data = resp.json()
    # print(data.keys())
    # pp.pprint(data)

    # Return the id of new created folder
    return data.get("id", [])

# Rename folder
def ondrive_rename_folder(authen, itemID, new_name):
    
    DriveItem = {
        "name" : new_name
    }

    resp = requests.patch(f'{config.ENDPOINT}//me/drive/items/{itemID}',
                          headers={'Authorization': 'Bearer ' + authen['access_token'],
                                 'Content-Type': 'application/json'},
                          json = DriveItem)

    
    print(resp.status_code)

# Delete item by itemId
def onedrive_delete_item_by_itemID_on_myDrive(authen, itemid):
    resp = requests.delete(f'{config.ENDPOINT}/me/drive/items/{itemid}', headers={'Authorization': 'Bearer ' + authen['access_token']})
    print(resp.status_code)

    # print(data.keys())
    # pp.pprint(data)

# Restore item that has been deleted before
def onedrive_restore_item_by_itemID_on_myDrive(authen, itemid):
    resp = requests.post(f'{config.ENDPOINT}/me/drive/items/{itemid}/restore', headers={'Authorization': 'Bearer ' + authen['access_token']})
    print(resp.status_code)
# Download a file by provding itemid
'''
https://keathmilligan.net/automate-your-work-with-msgraph-and-python
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get_content?view=odsp-graph-online
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get_content_format?view=odsp-graph-online

Download a file by provding itemid
   Provide itemID and the file_path where file wil be placed
   From itemID, convert to file_name by using onedrive_convert_Id_to_Name()

Work well with:
 - pdf
 - txt
Should check with:


'''

def ondrive_download_file(authen, itemid, file_path):
    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{itemid}/content', headers={'Authorization': 'Bearer ' + authen['access_token']})

    # Get the file name from itemID
    file_name = onedrive_convert_Id_to_Name(authen, itemid)
    full_file_path = Path(file_path, file_name) 
    # Write the content
    open(full_file_path, 'wb').write(resp.content)

'''

https://docs.microsoft.com/en-us/graph/api/driveitem-put-content?view=graph-rest-1.0&tabs=http
https://docs.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
https://keathmilligan.net/automate-your-work-with-msgraph-and-python
https://gist.github.com/keathmilligan/590a981cc629a8ea9b7c3bb64bfcb417


To upload a small file, you first need to check to see if the file already exists, in which case you will replace its contents
This method only supports files up to 4MB in size.
To upload large files see Upload large files with an upload session


For small files (4MB or less), you can upload them directly using a single request.
For larger files, Graph documentation directs you to use a resumable upload session where you can upload the file in chunks

'''
def onedrive_upload_file_less_than_4Mb_new(authen, full_file_name, parent_id):
    # Full name is splitted by path (location) and file_name
    path, file_name = os.path.split(full_file_name)

    # PUT /me/drive/items/{parent-id}:/{filename}:/content
    resp = requests.put(f'{config.ENDPOINT}/me/drive/items/{parent_id}:/{file_name}:/content', 
                        headers={'Authorization': 'Bearer ' + authen['access_token'],
                                  'Content-type': 'application/binary'
                        }, data=open(full_file_name, 'rb').read())
    # pp.pprint(resp)
    # print(path)
    # print(file_name)

# Does not work
def onedrive_upload_file_less_than_4Mb_replace(authen, full_file_name, item_id):
    # Full name is splitted by path (location) and file_name
    path, file_name = os.path.split(full_file_name)

    # PUT /me/drive/items/{item-id}/content
    resp = requests.put(f'{config.ENDPOINT}/me/drive/items/{item_id}:/content', 
                        headers={'Authorization': 'Bearer ' + authen['access_token'],
                                  'Content-type': 'application/binary'
                        }, data=open(full_file_name, 'rb').read())

'''
To upload a file using an upload session, there are two steps:

    1.Create an upload session
    2.Upload bytes to the upload session

To begin a large file upload, your app must first request a new upload session. 
This creates a temporary storage location where the bytes of the file will be saved until the complete file is uploaded. 
Once the last byte of the file has been uploaded the upload session is completed and the final file is shown in the destination folder. 
Alternatively, you can defer final creation of the file in the destination until you explicitly make a request to complete the upload, by setting the deferCommit property in the request arguments.

https://gist.github.com/keathmilligan/590a981cc629a8ea9b7c3bb64bfcb417
https://docs.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0

'''
def onedrive_upload_file_more_than_4Mb(authen, full_file_name, parent_id):
    # Full name is splitted by path (location) and file_name
    path, file_name = os.path.split(full_file_name)

    # PUT /me/drive/items/{parent-id}:/{filename}:/content
    resp = requests.post(f'{config.ENDPOINT}/me/drive/items/{parent_id}:/{file_name}:/createUploadSession', 
                        headers = {
                                'Authorization': 'Bearer ' + authen['access_token'],
                                'Content-type': 'application/json'},

                        json =   {
                                '@microsoft.graph.conflictBehavior': 'replace',
                                'description': 'A large test file',
                                'fileSystemInfo': {'@odata.type': 'microsoft.graph.fileSystemInfo'},
                                'name': file_name
                        })
    upload_session = resp.json()
    upload_url  = upload_session['uploadUrl']
    pp.pprint(upload_session.keys())
    # pp.pprint(upload_session["@odata.context"])

    # Calculate the number of chunks you will need to send
    st = os.stat(full_file_name)
    size = st.st_size
    CHUNK_SIZE = 10485760
    chunks = int(size / CHUNK_SIZE) + 1 if size % CHUNK_SIZE > 0 else 0
    with open(full_file_name, 'rb') as fd:
        start = 0
        for chunk_num in range(chunks):
            chunk = fd.read(CHUNK_SIZE)
            bytes_read = len(chunk)
            upload_range = f'bytes {start}-{start + bytes_read - 1}/{size}'
            print(f'chunk: {chunk_num} bytes read: {bytes_read} upload range: {upload_range}')
            result = requests.put(
                upload_url,
                headers={
                    'Content-Length': str(bytes_read),
                    'Content-Range': upload_range
                },
                data=chunk
            )
            result.raise_for_status()
            start += bytes_read

# Get the list of versions of itemId
# https://docs.microsoft.com/en-us/graph/api/driveitem-list-versions?view=graph-rest-1.0&tabs=http

def onedrive_list_version_of_item(authen, item_id):
    rows = []

    resp = requests.get(f'{config.ENDPOINT}/me/drive/items/{item_id}/versions', headers={'Authorization': 'Bearer ' + authen['access_token']})
    data = resp.json()
    print(data.keys())
    items = data.get("value", [])
    
    print(f"There are {len(items)} items")

    for item in items:
        id = item.get("id", [])
        url = item.get("@microsoft.graph.downloadUrl", [])
        modified = item.get("lastModifiedDateTime", [])
        size = item.get("size", [])
        # folder = item.get("folder", "N/A")
     

        rows.append((id, url, modified, size))

    headers = ['Id' , 'url' , 'modified', 'size folders']
    print(tabulate(rows, headers = headers))


def menu():
    while True:
        print()
        print("================== Onedrive Menu ======================")
        print("Note: An item may be a file or folder")
        print()
        print("      1. Show my profile ")
        print("      2. List all files and folders at root")
        print("      3. List all subfolders and files")
        print("      4. View file or folder name basing on ID")
        print("      5. Get file or folder location")
        print("      6. Get my recent files")
        print("      7. Search an item")
        print("      8. Rename an item")
        print("      9. Create a folder")
        print("      10. Delete a item")
        print("      11. Restore a item")
        print("      12. Copy a item")
        print("      13. Move a item")
        print("      14. Download a file")
        print("      15. Upload a file")
        print("      16. List all version of an item")
        print("      17. Exit")
        print()
        your_answer = int(input("Please enter your choice:  "))
        print("Your selection is: ", your_answer)

        print("=======================================================")
        client = get_authentication_service()

        if your_answer == 1: # Show my profile
            onedrive_get_my_profile(client)

        elif your_answer == 2: # List all files and folders at root
            onedrive_listFilesAtRoot_on_myDrive(client)
        
        elif your_answer == 3: # List all subfolders and files
            parentID = input("Enter folder ID: ")
            onedrive_get_children_on_myDrive(client, parentID)
        
        elif your_answer == 4: # View file or folder name basing on ID
            item_id = input("Enter item ID: ")
            location, url = onedrive_get_item_location(client, item_id)
            print(f"The location is  {location}")
            print(f"You can access {url}")

        elif your_answer == 5: # Get file or folder location
            item_id = input("Enter folder or file ID: ")
            item_name = onedrive_convert_Id_to_Name(client, item_id)
            location, url = onedrive_get_item_location(client, item_id)
            print(f"It is {item_name}")
            print(f"The location is  {location}")
            print(f"You can access {url}")

        elif your_answer == 6: # Get my recent files
            onedrive_get_myRecentFile_on_myDrive(client)

        elif your_answer == 7: # Search a file
            type_search = input("A part or full text search: (y/n) ? ")
            full_text = False

            if type_search.lower() == 'n':
                full_text = False
            else:
                full_text = True

            some_words = input("Enter some words: ")
            onedrive_search_items_by_keyword_on_myDrive(client, some_words, full_text)

        elif your_answer == 8: # Rename a item:

            # itemId = "88621E8311BA434!105676"
            # new_name = "My_New_Folder"
            itemId = input("Enter item Ids: ")
            new_name = input("Enter new name: ")
            ondrive_rename_folder(client, itemId, new_name)
     

        elif your_answer == 9:
            folder_name = input("Enter a name for folder: ")
            parent_id = input("Enter the folder Id where a new folder will be created: ")
            # folder_name = "Test 1"
            # parent_id = "88621E8311BA434!105676"
            print(onedrive_create_folder_on_myDrive(client, parent_id, folder_name))
      

        elif your_answer == 10: # Delete a item (file or folder)
            itemId = input("Enter item Id that you need to delete: ")
            onedrive_delete_item_by_itemID_on_myDrive(client, itemId)

        elif your_answer == 11: # Restore a item (file or folder)
            itemId = input("Enter item Id that you need to restore: ")
            onedrive_restore_item_by_itemID_on_myDrive(client, itemId)

        elif your_answer == 12: # Copy an item (file or folder)
            itemId = input("Enter item Id that you need to be copied: ")
            parent_id = input("Enter the folder Id where a new folder will be copied: ")
            onedrive_copy_item(client, itemId, parent_id)

        elif your_answer == 13: # Move an item (file or folder)
            itemId = input("Enter item Id that you need to be moved: ")
            parent_id = input("Enter the folder Id where a new folder will be moved to: ")
            onedrive_move_item_to_new_folder(client, itemId, parent_id)

        elif your_answer == 14: # Download file
            file_path = input("Enter the location where you want to put the downloaded file: ")
            itemId = input("Enter itemId you want to download: ")
            ondrive_download_file(client, itemId, file_path)

        elif your_answer == 15: # Upload a file
            parent_id = input("Enter the location where you want to put the uploaded file: ")
            full_file_name = input("Enter file you want to upload: ")
       
            # full_file_name = r"D:\temp\football_data.csv"
            # parent_id = "88621E8311BA434!77160" # Where file will be uploaded
            onedrive_upload_file_more_than_4Mb(client, full_file_name, parent_id)

        elif your_answer == 16: # List all version of an item
            itemId = input("Enter item Id that you want to view: ")
            # itemId = "88621E8311BA434!105815" # sach 1 2.txt
            onedrive_list_version_of_item(client, itemId)

        elif your_answer == 17:
            print("Goodbye !")
            break


def main():
    menu()