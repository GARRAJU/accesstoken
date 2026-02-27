# # import os
# # import requests
# # from fastapi import APIRouter, Request, HTTPException, Body
# # from app.config import POWERBI_API

# # router = APIRouter()

# # # --- CONFIGURATION ---
# # # IMPORTANT: This must be the "Object ID" found in 'Enterprise Applications' 
# # # in Azure, NOT the 'Application (client) ID'.
# # SP_OBJECT_ID = os.getenv("SP_OBJECT_ID", "36d789fd-926b-4106-93dc-e3928b36913e")


# # @router.get("/workspaces")
# # def get_workspaces(request: Request):
# #     access_token = request.session.get("access_token")
# #     if not access_token:
# #         raise HTTPException(status_code=401, detail="Not logged in")

# #     headers = {"Authorization": f"Bearer {access_token}"}

# #     # Fetch groups
# #     ws_resp = requests.get(f"{POWERBI_API}/groups", headers=headers)
# #     if ws_resp.status_code != 200:
# #         raise HTTPException(status_code=ws_resp.status_code, detail=ws_resp.text)

# #     workspaces = ws_resp.json().get("value", [])

# #     # Enrich workspaces with reports and datasets
# #     for ws in workspaces:
# #         workspace_id = ws["id"]
        
# #         # Reports
# #         r_resp = requests.get(f"{POWERBI_API}/groups/{workspace_id}/reports", headers=headers)
# #         ws["reports"] = r_resp.json().get("value", []) if r_resp.status_code == 200 else []
        
# #         # Datasets
# #         d_resp = requests.get(f"{POWERBI_API}/groups/{workspace_id}/datasets", headers=headers)
# #         ws["datasets"] = d_resp.json().get("value", []) if d_resp.status_code == 200 else []

# #     return {
# #         "count": len(workspaces),
# #         "workspaces": workspaces
# #     }


# # @router.post("/workspaces")
# # def create_workspace(request: Request, payload: dict = Body(...)):
# #     access_token = request.session.get("access_token")
# #     if not access_token:
# #         raise HTTPException(status_code=401, detail="Not logged in")

# #     workspace_name = payload.get("workspace_name")
# #     if not workspace_name:
# #         raise HTTPException(status_code=400, detail="workspace_name is required")

# #     headers = {
# #         "Authorization": f"Bearer {access_token}",
# #         "Content-Type": "application/json"
# #     }

# #     response = requests.post(
# #         f"{POWERBI_API}/groups?workspaceV2=true",
# #         headers=headers,
# #         json={"name": workspace_name},
# #         timeout=30
# #     )

# #     if response.status_code not in (200, 201):
# #         raise HTTPException(status_code=response.status_code, detail=response.text)

# #     data = response.json()
# #     return {
# #         "message": "Workspace created successfully",
# #         "workspaceId": data["id"],
# #         "workspaceName": data["name"]
# #     }



# # @router.post("/workspaces/add-sp")
# # def add_service_principal_to_workspace(request: Request, payload: dict = Body(...)):
# #     """
# #     Adds the Service Principal to the workspace.
# #     Requires the user to have 'Admin' rights on the target workspace.
# #     """
# #     access_token = request.session.get("access_token")
# #     workspace_id = payload.get("workspace_id")
    
# #     if not access_token:
# #         raise HTTPException(status_code=401, detail="Not logged in")
    
# #     if not workspace_id:
# #         raise HTTPException(status_code=400, detail="workspace_id is required")

# #     headers = {
# #         "Authorization": f"Bearer {access_token}",
# #         "Content-Type": "application/json"
# #     }

# #     # API Endpoint for adding users/principals to a workspace
# #     users_url = f"{POWERBI_API}/groups/{workspace_id}/users"
    
# #     # PAYLOAD: Ensure 'identifier' is the Object ID of the Service Principal
# #     add_payload = {
# #         "identifier": SP_OBJECT_ID,
# #         "principalType": "App",
# #         "groupUserAccessRight": "Admin"
# #     }

# #     # Execute request
# #     resp = requests.post(users_url, headers=headers, json=add_payload)

# #     # 200, 201 (Created), or 204 (No Content) are all successes for this API
# #     if resp.status_code in (200, 201, 204):
# #         return {"status": "success", "message": "Service Principal added to workspace"}
    
# #     # Detailed error handling
# #     try:
# #         error_detail = resp.json()
# #     except:
# #         error_detail = resp.text

# #     # Log specific reasons for 403
# #     if resp.status_code == 403:
# #         # Possible reasons: 
# #         # 1. User calling the API isn't an Admin of the Workspace.
# #         # 2. The SP_OBJECT_ID is actually a Client ID.
# #         # 3. Tenant settings haven't propagated yet.
# #         raise HTTPException(
# #             status_code=403,
# #             detail={
# #                 "error": "Forbidden",
# #                 "reason": "Ensure the current user is a Workspace Admin and SP_OBJECT_ID is correct.",
# #                 "ms_response": error_detail
# #             }
# #         )

# #     raise HTTPException(status_code=resp.status_code, detail=error_detail)


# import os
# import requests
# from fastapi import APIRouter, Request, HTTPException, Body
# from app.config import POWERBI_API

# router = APIRouter()

# # --- CONFIGURATION ---
# SP_OBJECT_ID = os.getenv(
#     "SP_OBJECT_ID",
#     "36d789fd-926b-4106-93dc-e3928b36913e"
# )

# # ------------------------------------------------------------
# # 1️⃣ GET USER CAPACITIES
# # ------------------------------------------------------------
# @router.get("/user-capacities")
# def get_user_capacities(request: Request):
#     access_token = request.session.get("access_token")

#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not logged in")

#     response = requests.get(
#         f"{POWERBI_API}/capacities",
#         headers={"Authorization": f"Bearer {access_token}"},
#         timeout=30
#     )

#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail=response.text)

#     return response.json()


# # ------------------------------------------------------------
# # 2️⃣ GET WORKSPACES (WITH REPORTS & DATASETS)
# # ------------------------------------------------------------
# @router.get("/workspaces")
# def get_workspaces(request: Request):
#     access_token = request.session.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not logged in")

#     headers = {"Authorization": f"Bearer {access_token}"}

#     ws_resp = requests.get(f"{POWERBI_API}/groups", headers=headers, timeout=30)

#     if ws_resp.status_code != 200:
#         raise HTTPException(status_code=ws_resp.status_code, detail=ws_resp.text)

#     workspaces = ws_resp.json().get("value", [])

#     for ws in workspaces:
#         workspace_id = ws["id"]

#         # Reports
#         r_resp = requests.get(
#             f"{POWERBI_API}/groups/{workspace_id}/reports",
#             headers=headers,
#             timeout=30
#         )
#         ws["reports"] = r_resp.json().get("value", []) if r_resp.status_code == 200 else []

#         # Datasets
#         d_resp = requests.get(
#             f"{POWERBI_API}/groups/{workspace_id}/datasets",
#             headers=headers,
#             timeout=30
#         )
#         ws["datasets"] = d_resp.json().get("value", []) if d_resp.status_code == 200 else []

#     return {
#         "count": len(workspaces),
#         "workspaces": workspaces
#     }


# # ------------------------------------------------------------
# # 3️⃣ CREATE WORKSPACE ONLY
# # ------------------------------------------------------------
# # @router.post("/workspaces")
# # def create_workspace(request: Request, payload: dict = Body(...)):
# #     access_token = request.session.get("access_token")
# #     if not access_token:
# #         raise HTTPException(status_code=401, detail="Not logged in")

# #     workspace_name = payload.get("workspace_name")
# #     if not workspace_name:
# #         raise HTTPException(status_code=400, detail="workspace_name is required")

# #     headers = {
# #         "Authorization": f"Bearer {access_token}",
# #         "Content-Type": "application/json"
# #     }

# #     response = requests.post(
# #         f"{POWERBI_API}/groups?workspaceV2=true",
# #         headers=headers,
# #         json={"name": workspace_name},
# #         timeout=30
# #     )

# #     if response.status_code not in (200, 201):
# #         raise HTTPException(status_code=response.status_code, detail=response.text)

# #     data = response.json()

# #     return {
# #         "message": "Workspace created successfully",
# #         "workspaceId": data["id"],
# #         "workspaceName": data["name"]
# #     }


# # ------------------------------------------------------------
# # 4️⃣ CREATE WORKSPACE + ASSIGN TO CAPACITY
# # ------------------------------------------------------------
# @router.post("/workspaces/with-capacity")
# def create_workspace_with_capacity(request: Request, payload: dict = Body(...)):
#     access_token = request.session.get("access_token")

#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not logged in")

#     workspace_name = payload.get("workspace_name")
#     capacity_id = payload.get("capacity_id")

#     if not workspace_name or not capacity_id:
#         raise HTTPException(
#             status_code=400,
#             detail="workspace_name and capacity_id are required"
#         )

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     # STEP 1 — Create Workspace
#     create_res = requests.post(
#         f"{POWERBI_API}/groups?workspaceV2=true",
#         headers=headers,
#         json={"name": workspace_name},
#         timeout=30
#     )

#     if create_res.status_code not in (200, 201):
#         raise HTTPException(
#             status_code=create_res.status_code,
#             detail=create_res.text
#         )

#     workspace_data = create_res.json()
#     workspace_id = workspace_data["id"]

#     # STEP 2 — Assign to Capacity (PATCH METHOD)
#     assign_res = requests.patch(
#         f"{POWERBI_API}/groups/{workspace_id}",
#         headers=headers,
#         json={"capacityId": capacity_id},
#         timeout=30
#     )

#     print("Assign Status:", assign_res.status_code)
#     print("Assign Response:", assign_res.text)

#     if assign_res.status_code not in (200, 202):
#         raise HTTPException(
#             status_code=assign_res.status_code,
#             detail=f"Workspace created but capacity assignment failed: {assign_res.text}"
#         )

#     return {
#         "message": "Workspace created and assigned to capacity successfully",
#         "workspaceId": workspace_id,
#         "workspaceName": workspace_data["name"],
#         "capacityId": capacity_id
#     }


# # ------------------------------------------------------------
# # 5️⃣ ADD SERVICE PRINCIPAL TO WORKSPACE
# # ------------------------------------------------------------
# @router.post("/workspaces/add-sp")
# def add_service_principal_to_workspace(request: Request, payload: dict = Body(...)):
#     access_token = request.session.get("access_token")
#     workspace_id = payload.get("workspace_id")

#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not logged in")

#     if not workspace_id:
#         raise HTTPException(status_code=400, detail="workspace_id is required")

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     users_url = f"{POWERBI_API}/groups/{workspace_id}/users"

#     add_payload = {
#         "identifier": SP_OBJECT_ID,
#         "principalType": "App",
#         "groupUserAccessRight": "Admin"
#     }

#     resp = requests.post(users_url, headers=headers, json=add_payload, timeout=30)

#     if resp.status_code in (200, 201, 204):
#         return {
#             "status": "success",
#             "message": "Service Principal added to workspace"
#         }

#     try:
#         error_detail = resp.json()
#     except:
#         error_detail = resp.text

#     if resp.status_code == 403:
#         raise HTTPException(
#             status_code=403,
#             detail={
#                 "error": "Forbidden",
#                 "reason": "Ensure user is Workspace Admin and SP_OBJECT_ID is correct.",
#                 "ms_response": error_detail
#             }
#         )

#     raise HTTPException(status_code=resp.status_code, detail=error_detail)


import os
import time
import requests
from fastapi import APIRouter, Request, HTTPException, Body
from app.config import POWERBI_API

router = APIRouter()

# --- CONFIGURATION ---
SP_OBJECT_ID = os.getenv(
    "SP_OBJECT_ID", 
    "36d789fd-926b-4106-93dc-e3928b36913e"
)

# ------------------------------------------------------------
# 1️⃣ GET USER CAPACITIES
# ------------------------------------------------------------
@router.get("/user-capacities")
def get_user_capacities(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not logged in")

    response = requests.get(
        f"{POWERBI_API}/capacities",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

# ------------------------------------------------------------
# 2️⃣ GET WORKSPACES (WITH ENRICHED DATA)
# ------------------------------------------------------------
@router.get("/workspaces")
def get_workspaces(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not logged in")

    headers = {"Authorization": f"Bearer {access_token}"}
    ws_resp = requests.get(f"{POWERBI_API}/groups", headers=headers, timeout=30)

    if ws_resp.status_code != 200:
        raise HTTPException(status_code=ws_resp.status_code, detail=ws_resp.text)

    workspaces = ws_resp.json().get("value", [])
    for ws in workspaces:
        workspace_id = ws["id"]
        # Enrichment
        r_resp = requests.get(f"{POWERBI_API}/groups/{workspace_id}/reports", headers=headers, timeout=10)
        ws["reports"] = r_resp.json().get("value", []) if r_resp.status_code == 200 else []
        d_resp = requests.get(f"{POWERBI_API}/groups/{workspace_id}/datasets", headers=headers, timeout=10)
        ws["datasets"] = d_resp.json().get("value", []) if d_resp.status_code == 200 else []

    return {"count": len(workspaces), "workspaces": workspaces}

# ------------------------------------------------------------
# 3️⃣ CREATE WORKSPACE + GUARANTEED CAPACITY ASSIGNMENT
# ------------------------------------------------------------
@router.post("/workspaces/with-capacity")
def create_workspace_with_capacity(request: Request, payload: dict = Body(...)):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not logged in")

    workspace_name = payload.get("workspace_name")
    capacity_id = payload.get("capacity_id")

    if not workspace_name or not capacity_id:
        raise HTTPException(status_code=400, detail="workspace_name and capacity_id are required")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # --- STEP 1: Create Workspace ---
    create_res = requests.post(
        f"{POWERBI_API}/groups?workspaceV2=true",
        headers=headers,
        json={"name": workspace_name},
        timeout=30
    )
    if create_res.status_code not in (200, 201):
        raise HTTPException(status_code=create_res.status_code, detail=create_res.text)

    workspace_id = create_res.json()["id"]

    # --- STEP 2: Initiate Capacity Assignment ---
    # We use the specific AssignToCapacity endpoint for moving from Pro -> Premium
    assign_url = f"{POWERBI_API}/groups/{workspace_id}/AssignToCapacity"
    assign_res = requests.post(
        assign_url,
        headers=headers,
        json={"capacityId": capacity_id},
        timeout=30
    )

    # If POST fails, try the PATCH fallback as some tenants prefer it
    if assign_res.status_code not in (200, 201, 202):
        requests.patch(
            f"{POWERBI_API}/groups/{workspace_id}",
            headers=headers,
            json={"capacityId": capacity_id},
            timeout=30
        )

    # --- STEP 3: Verification Polling (Wait until it is actually updated) ---
    max_retries = 5
    is_verified = False
    
    for i in range(max_retries):
        time.sleep(3) # Wait 3 seconds per check
        verify_res = requests.get(
            f"{POWERBI_API}/groups?$filter=id eq '{workspace_id}'",
            headers=headers,
            timeout=20
        )
        
        if verify_res.status_code == 200:
            group_details = verify_res.json().get("value", [{}])[0]
            current_cap = group_details.get("capacityId", "").lower()
            
            if current_cap == capacity_id.lower():
                is_verified = True
                break
        
    if not is_verified:
        raise HTTPException(
            status_code=500, 
            detail="Workspace created, but capacity assignment verification timed out. Please check permissions."
        )

    return {
        "message": "Workspace created and capacity assignment verified",
        "workspaceId": workspace_id,
        "capacityId": capacity_id
    }

# ------------------------------------------------------------
# 4️⃣ ADD SERVICE PRINCIPAL TO WORKSPACE
# ------------------------------------------------------------
@router.post("/workspaces/add-sp")
def add_service_principal_to_workspace(request: Request, payload: dict = Body(...)):
    access_token = request.session.get("access_token")
    workspace_id = payload.get("workspace_id")

    if not access_token or not workspace_id:
        raise HTTPException(status_code=400, detail="Missing token or workspace_id")

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    add_payload = {
        "identifier": SP_OBJECT_ID,
        "principalType": "App",
        "groupUserAccessRight": "Admin"
    }

    resp = requests.post(
        f"{POWERBI_API}/groups/{workspace_id}/users", 
        headers=headers, 
        json=add_payload, 
        timeout=30
    )

    if resp.status_code in (200, 201, 204):
        return {"status": "success", "message": "Service Principal added as Admin"}

    raise HTTPException(status_code=resp.status_code, detail=resp.text)