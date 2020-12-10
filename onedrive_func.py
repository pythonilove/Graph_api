


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
    pass

def onedrive_get_my_profile(authen):
    pass

# List all files and folders on my drive
def onedrive_listFilesAtRoot_on_myDrive(client):
    pass

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