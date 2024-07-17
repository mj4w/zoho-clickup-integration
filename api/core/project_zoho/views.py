import requests


def list_project_data(zoho_token, organization_id):
    url = f"https://projectsapi.zoho.com/restapi/portal/{organization_id}/projects/"
    headers = {
        # "orgId": organization_id,
        "Authorization": f"Zoho-oauthtoken {zoho_token}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # data = response.json().get("data", [])
        # print(data)
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as e:
        return {"error": str(e)}, 500
    
    
# def create_task_data(zoho_token, organization_id, data):
#     url = "https://desk.zoho.com/api/v1/tasks"
#     headers = {
#         "orgId": organization_id,
#         "Authorization": f"Zoho-oauthtoken {zoho_token}",
#         "Content-Type": "application/json"
#     }
    
#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         return response.json(), response.status_code
#     except requests.exceptions.HTTPError as e:
#         return {"error": str(e), "response": response.text}, 422
        

    
    