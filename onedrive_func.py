


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
def onedrive_get_children_on_myDrive(client, itemID):
    pass

def onedrive_get_myRecentFile_on_myDrive(client):
    pass

def onedrive_get_item_by_itemID_on_myDrive(client, itemid):
    pass

# Provide the itemId and return its name
def onedrive_convert_Id_to_Name(client, itemid):
    pass

def onedrive_move_item_to_new_folder(client, item_id, new_folder_id):
    pass

# Check if item belongs to a folder or not. If Yes, return True and its id, otherwise return False and None
def onedrive_item_id_belongs_parent_id(client, item_id, parent_id):
    pass

# Get item location
def onedrive_get_item_location(client, item_id):
    pass

# Copy a driveitem
# https://docs.microsoft.com/en-us/graph/api/driveitem-copy?view=graph-rest-1.0&tabs=http
# Copy item (via itemId) to the new destimation

def onedrive_copy_item(client, item_id, parent_id):
    pass

def onedrive_search_items_by_keyword_on_myDrive(client, keyword, option):
    pass

# Create a folder
def onedrive_create_folder_on_myDrive(client, parent_id, folder_name):
    pass

# Rename folder
def ondrive_rename_folder(client, itemID, new_name):
    pass

# Delete item by itemId
def onedrive_delete_item_by_itemID_on_myDrive(client, itemid):
    pass

# Restore item that has been deleted before
def onedrive_restore_item_by_itemID_on_myDrive(client, itemid):
    pass

# Download a file by provding itemid
def ondrive_download_file(client, itemid, file_path):
    pass

def onedrive_upload_file_less_than_4Mb_new(client, full_file_name, parent_id):
    pass

def onedrive_upload_file_more_than_4Mb(client, full_file_name, parent_id):
    pass

# Get the list of versions of itemId
# https://docs.microsoft.com/en-us/graph/api/driveitem-list-versions?view=graph-rest-1.0&tabs=http

def onedrive_list_version_of_item(client, item_id):
    pass

def menu():
    pass