# import os
# from dotenv import load_dotenv

# load_dotenv()

# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# TENANT_ID = os.getenv("TENANT_ID")
# REDIRECT_URI = os.getenv("REDIRECT_URI")

# AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
# EMPTY_PBIX_NAME = os.getenv("EMPTY_PBIX_NAME")

# POWERBI_SCOPE = [
#     "https://analysis.windows.net/powerbi/api/.default"
# ]

# POWERBI_API = "https://api.powerbi.com/v1.0/myorg"


import os

from dotenv import load_dotenv
 
load_dotenv()
 
CLIENT_ID = os.getenv("CLIENT_ID")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TENANT_ID = os.getenv("TENANT_ID")

REDIRECT_URI = os.getenv("REDIRECT_URI")
 
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")

EMPTY_PBIX_NAME = os.getenv("EMPTY_PBIX_NAME")
 
# ────────────────────────────────────────────────────────────────

# FIXED: Specific scopes only – NO .default to avoid AADSTS70011

# These match your app registration + required for capacity assignment

# ────────────────────────────────────────────────────────────────

POWERBI_SCOPE = [

    "Capacity.ReadWrite.All",           # Required for assignToCapacity

    "Workspace.ReadWrite.All",          # Required for workspace create/read/write

    "Capacity.Read.All",                # View capacities list

    "Dataset.ReadWrite.All",

    "Report.ReadWrite.All",

    "Dashboard.ReadWrite.All",

    "Content.Create",

    "Item.ReadWrite.All",

    "Connection.Read.All",

    "Workspace.GitCommit.All",

    "Workspace.GitUpdate.All",

    # Add more only if your app actually uses them

]
 
# API bases

POWERBI_API = "https://api.powerbi.com/v1.0/myorg"

FABRIC_API  = "https://api.fabric.microsoft.com/v1"
 