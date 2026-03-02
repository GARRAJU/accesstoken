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
 
# Updated scopes – includes legacy Power BI + required Fabric Core scopes for capacity assignment

# POWERBI_SCOPE = [

#     "https://analysis.windows.net/powerbi/api/.default",  # Legacy Power BI REST API (keep for other calls)

#     "Capacity.ReadWrite.All",                             # Required for assign workspace to capacity

#     "Workspace.ReadWrite.All"                             # Required for workspace read/write operations

# ]
# --- FIXED SCOPES ---
# We remove ".default" and use the full URL for the specific scopes.
# This ensures the token is valid for both Power BI and Fabric assignment.

POWERBI_SCOPE = [
    "https://analysis.windows.net/powerbi/api/Capacity.ReadWrite.All",
    "https://analysis.windows.net/powerbi/api/Workspace.ReadWrite.All",
    "https://analysis.windows.net/powerbi/api/Report.ReadWrite.All", # Added for your /workspaces GET call
    "https://analysis.windows.net/powerbi/api/Dataset.ReadWrite.All", # Added for your /workspaces GET call
    "openid",
    "profile",
    "offline_access"
]
 
# Legacy Power BI API base (used for create workspace, list capacities, etc.)

POWERBI_API = "https://api.powerbi.com/v1.0/myorg"
 
# Modern Fabric Core API base (used specifically for assignToCapacity)

FABRIC_API = "https://api.fabric.microsoft.com/v1"
 
