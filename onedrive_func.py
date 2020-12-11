'''
1. Microsoft Graph exposes two resource types for working with files:

    Drive - Represents a logical container of files, like a document library or a user's OneDrive.
    DriveItem - Represents an item within a drive, like a document, photo, video, or folder.

OneDrive's REST API provides a few top-level types that represent addressable resources in the API:

    drive (top-level object)
    driveItem (files and folders)

Drive and DriveItem resources expose data in three different ways:

    Properties (like id and name) expose simple values (strings, numbers, Booleans).
    Facets (like file and photo) expose complex values. The presence of file or folder facets indicates behaviors and properties of a DriveItem.
    References (like children and thumbnails) point to collections of other resources.

How to authenticate and authorize Python apps on Azure
https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate?tabs=cmd

https://docs.microsoft.com/en-us/graph/api/resources/onedrive?view=graph-rest-1.0
https://docs.microsoft.com/en-us/onedrive/developer/rest-api/concepts/addressing-driveitems?view=odsp-graph-online
https://docs.microsoft.com/en-us/graph/api/driveitem-get?view=graph-rest-1.0&tabs=http
https://docs.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http

https://cloud-right.com/2020/06/microsoft-graph-python
https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-configure-app-access-web-apis#add-permissions-to-access-web-apis

Erro Response
https://docs.microsoft.com/en-us/graph/errors

2. Addressing resources in a drive on OneDrive

    The OneDrive API allows a single URL to address two aspects of a resource:

    The driveItem resource
    A property, facet, or relationship of the Item
    An Item facet represents an element of the resource, like the image metadata, folder metadata, and so on.

    https://graph.microsoft.com/v1.0 - The version of the Microsoft Graph being used.
    /me - A top-level Microsoft Graph resource being addressed, in this case the current user.
    /drive - The default drive for the previous resource, in this case the user's OneDrive.
    /root - The root folder for the drive.

    :/Documents/MyFile.xlsx: - The : : around /Documents/MyFile.xlsx represents a switch to the path-based addressing syntax. Everything between the two colons is treated as a path relative to the item before the path (in this case, the root).
    /content - Represents the default binary stream for the file. You can also address other properties or relationships on the item.

    GET /drives/{drive-id}/items/{item-id}
    GET /drives/{drive-id}/root:/{item-path}
    GET /groups/{group-id}/drive/items/{item-id}
    GET /groups/{group-id}/drive/root:/{item-path}
    GET /me/drive/items/{item-id}
    GET /me/drive/root:/{item-path}
    GET /sites/{site-id}/drive/items/{item-id}
    GET /sites/{site-id}/drive/root:/{item-path}
    GET /sites/{site-id}/lists/{list-id}/items/{item-id}/driveItem
    GET /users/{user-id}/drive/items/{item-id}
    GET /users/{user-id}/drive/root:/{item-path}


        print("=============== Onedrive Menu ======================")
        print()
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

'''


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
	
# Get my profile of signed-in user
def onedrive_get_my_profile(authen):
	pass

# List all files and folders on my drive
def onedrive_listFilesAtRoot_on_myDrive(authen):
	pass

# List all subfolders and files
def onedrive_get_children_on_myDrive(authen, itemID):
	pass

def onedrive_get_myRecentFile_on_myDrive(authen):
	pass

def onedrive_get_item_by_itemID_on_myDrive(authen, itemid):
	pass

# Provide the itemId and return its name
def onedrive_convert_Id_to_Name(authen, itemid):
	pass

'''
Move item to new folder
    To move a DriveItem to a new parent item, your app requests to update the parentReference of the DriveItem to move
    This is a special case of the Update method
    Items cannot be moved between Drives using this request.

'''

def onedrive_move_item_to_new_folder(anthen, item_id, new_folder_id):
	pass

# Check if item belongs to a folder or not. If Yes, return True and its id, otherwise return False and None
def onedrive_item_id_belongs_parent_id(authen, item_id, parent_id):
	pass

# Get item location
def onedrive_get_item_location(authen, item_id):
	pass

# Copy a driveitem
# https://docs.microsoft.com/en-us/graph/api/driveitem-copy?view=graph-rest-1.0&tabs=http
# Copy item (via itemId) to the new destimation

def onedrive_copy_item(authen, item_id, parent_id):
	pass

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
    pass
# Folder
# Create a folder 
# https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
# https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
# https://stackoverflow.com/questions/44379557/error-creating-folder-with-onedrive-api-javascript


def onedrive_create_folder_on_myDrive(authen, parent_id, folder_name):
	pass

# Rename folder
def ondrive_rename_folder(authen, itemID, new_name):
	pass

# Delete item by itemId
def onedrive_delete_item_by_itemID_on_myDrive(authen, itemid):
	pass

# Restore item that has been deleted before
def onedrive_restore_item_by_itemID_on_myDrive(authen, itemid):
	pass


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
	pass

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
	pass

# Does not work
def onedrive_upload_file_less_than_4Mb_replace(authen, full_file_name, item_id):
	pass

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
	pass

# Get the list of versions of itemId
# https://docs.microsoft.com/en-us/graph/api/driveitem-list-versions?view=graph-rest-1.0&tabs=http

def onedrive_list_version_of_item(authen, item_id):
	pass

def menu():
	pass
	
def main():
    menu()