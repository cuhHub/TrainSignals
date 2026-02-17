# // ---------------------------------------------------------------------
# // ------- [cuhHub] Publish
# // ---------------------------------------------------------------------

"""
A tool for publishing mods and addons to cuhHub.
Repo: https://github.com/cuhHub/cuhHub

Copyright (C) 2026 cuhHub - All Rights Reserved
    - Unauthorized copying of this file, via any medium is strictly prohibited
    - Proprietary and confidential
"""

# ---- // Imports
import click
import os
import requests
import shutil
from functools import cache
from dotenv import load_dotenv

# ---- // Main
API_URL = "https://api.cuhhub.com"

def send_api_request(
    method: str,
    endpoint: str,
    params: dict = None,
    body: dict = None,
    files: dict|list[tuple] = None,
    *,
    api_token: str,
) -> requests.Response:
    """
    Sends a request to the cuhHub API.

    Args:
        method (str): The method to use.
        endpoint (str): The endpoint to send a request to.
        api_token (str): The API token.
        params (dict, optional): The URL parameters to provide. Defaults to None.
        body (dict, optional): The body to provide. Defaults to None.
        files (dict, optional): The files to provide. Defaults to None.

    Returns:
        requests.Response: _description_
    """    
    
    response = requests.request(
        method = method,
        url = f"{API_URL}/{endpoint}",
        params = params,
        json = body,
        files = files,
        headers = {
            "x-authorization": f"Bearer {api_token}"
        }
    )
    
    if not response.ok:
        click.secho(f"API request failed with status code {response.status_code}.\nResponse: {response.text}", fg = "red", underline = True, bold = True)
        exit(1)
        
    return response
    
@cache
def get_all_servers(api_token: str) -> list[dict]:
    """
    Returns a list of all servers.

    Args:
        api_token (str): The API token

    Returns:
        list[dict]: A list of all servers
    """

    return send_api_request("GET", "servers", api_token = api_token).json()

@cache
def get_all_server_ids(api_token: str) -> list[int]:
    """
    Returns a list of all server IDs.

    Args:
        api_token (str): The API token

    Returns:
        list[int]: A list of all server IDs
    """

    return [server["id"] for server in get_all_servers(api_token)]

def get_server_info(server_id: int, api_token: str) -> dict:
    """
    Returns information about a server.

    Args:
        server_id (int): The ID of the server
        api_token (str): The API token

    Returns:
        dict: Information about the server
    """

    return send_api_request("GET", f"servers/{server_id}", api_token = api_token).json()

def refresh_server(server_id: int, api_token: str):
    """
    Refreshes a server.

    Args:
        server_id (int): The ID of the server
        api_token (str): The API token
    """

    send_api_request("POST", f"servers/{server_id}/refresh", api_token = api_token)

def get_uploaded_addons(api_token: str) -> list[str]:
    """
    Returns a list of all uploaded addons.

    Args:
        api_token (str): The API token

    Returns:
        list[str]: A list of all uploaded addons
    """

    return send_api_request("GET", "storage/addons", api_token = api_token).json()

def is_addon_uploaded(addon_name: str, api_token: str) -> bool:
    """
    Returns whether or not the provided addon is uploaded already.

    Args:
        addon_name (str): The name of the addon
        api_token (str): The API token

    Returns:
        bool: Whether or not the addon is uploaded
    """

    return addon_name in get_uploaded_addons(api_token)

def add_addon_to_server(addon_name: str, server_id: int, api_token: str):
    """
    Adds an addon to a server.

    Args:
        addon_name (str): The name of the addon
        server_id (int): The ID of the server
        api_token (str): The API token
    """
    
    if addon_name in get_server_info(server_id, api_token)["addons"]:
        return

    send_api_request(
        "PATCH",
        f"servers/{server_id}/addons",
        body = {
            "addon_name" : addon_name
        },
        api_token = api_token
    )

def publish_addon(addon_name: str, path: str, server_id: int, api_token: str):
    """
    Uploads or updates an addon.

    Args:
        addon_name (str): The name of the addon
        path (str): The path to the addon
        server_id (int): The ID of the server to publish the addon to, or -1 for all
        api_token (str): The API token
    """
    
    vehicle_files = []
    
    for vehicle in os.listdir(path):
        if vehicle.startswith("vehicle_") and os.path.splitext(vehicle)[1] == ".xml":
            vehicle_files.append(
                ("vehicle_files", open(os.path.join(path, vehicle), "rb"))
            )

    send_api_request(
        "PATCH" if is_addon_uploaded(addon_name, api_token = api_token) else "POST",
        f"storage/addons/{addon_name}",
        files = [
            ("script_file", open(os.path.join(path, "script.lua"), "rb")),
            ("playlist_file", open(os.path.join(path, "playlist.xml"), "rb")),
            *vehicle_files
        ],
        api_token = api_token   
    )

    if server_id != -1:
        add_addon_to_server(addon_name, server_id, api_token)
    else:
        for server_id in get_all_server_ids(api_token):
            add_addon_to_server(addon_name, server_id, api_token)
            
    refresh_server(server_id, api_token)

def get_uploaded_mods(api_token: str) -> list[str]:
    """
    Returns a list of all uploaded mods.

    Args:
        api_token (str): The API token

    Returns:
        list[str]: A list of all uploaded mods
    """

    return send_api_request("GET", "storage/mods", api_token = api_token).json()

def is_mod_uploaded(mod_name: str, api_token: str) -> bool:
    """
    Returns whether or not the provided mod is uploaded already.

    Args:
        mod_name (str): The name of the mod
        api_token (str): The API token

    Returns:
        bool: Whether or not the mod is uploaded
    """

    return mod_name in get_uploaded_mods(api_token)

def add_mod_to_server(mod_name: str, server_id: int, api_token: str):
    """
    Adds a mod to a server.

    Args:
        mod_name (str): The name of the mod
        server_id (int): The ID of the server
        api_token (str): The API token
    """
    
    if mod_name in get_server_info(server_id, api_token)["mods"]:
        return

    send_api_request(
        "PATCH",
        f"servers/{server_id}/mods",
        body = {
            "mod_name" : mod_name
        },
        api_token = api_token
    )

def publish_mod(path: str, server_id: int, api_token: str):
    """
    Uploads or updates a mod.

    Args:
        path (str): The path to the mod
        server_id (int): The ID of the server to publish the mod to, or -1 for all
        api_token (str): The API token
    """

    mod_name = os.path.basename(path)
    _archive_path = shutil.make_archive(mod_name, "zip", path)
    archive_path = os.path.join("_build", mod_name + ".zip")
    shutil.move(_archive_path, archive_path)
    
    with open(archive_path, "rb") as archive_file:
        send_api_request(
            "PATCH" if is_mod_uploaded(mod_name, api_token = api_token) else "POST",
            f"storage/mods/{mod_name}",
            files = {
                "mod_zip": archive_file
            },  
            api_token = api_token
        )
    
    os.remove(archive_path)
    
    if server_id != -1:
        add_mod_to_server(mod_name, server_id, api_token)
    else:
        for server_id in get_all_server_ids(api_token):
            add_mod_to_server(mod_name, server_id, api_token)

    refresh_server(server_id, api_token)

@click.command()
@click.option("--type", "-t", type = click.Choice(["addon", "mod"]), required = True, help = "Whether to publish an addon or mod.")
@click.option("--name", "-n", type = str, help = "The name of the addon to publish (if addon!).")
@click.option("--directory", "-d", "-p", "--path", type = str, required = True, help = "The directory of the addon/mod to publish.")
@click.option("--server_id", "-s", type = int, required = True, help = "The ID of the server to publish the addon to. -1 = all")
@click.option("--api_token", "-k", type = str, required = False, help = "Your API key for the cuhHub API. Uses the environment variable `CUHHUB_API_TOKEN` if not provided.")
def publish_tool(type: str, name: str, directory: str, server_id: int, api_token: str):
    """
    Publishes an addon or mod to cuhHub.
    """    
    
    load_dotenv()
    api_token = os.getenv("CUHHUB_API_TOKEN") if api_token is None else api_token
    
    if type == "addon":
        publish_addon(name, directory, server_id, api_token)
        click.secho(f"Published addon successfully.", fg = "blue", underline = True, bold = True)
    elif type == "mod":
        publish_mod(directory, server_id, api_token)
        click.secho(f"Published mod successfully.", fg = "blue", underline = True, bold = True)
    else:
        click.secho("Invalid type provided.", fg = "red", underline = True, bold = True)

if __name__ == "__main__":
    publish_tool()