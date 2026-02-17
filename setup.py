# // ---------------------------------------------------------------------
# // ------- [cuhHub] Setup
# // ---------------------------------------------------------------------

"""
A tool for setting up everything on first-time install.
Repo: https://github.com/cuhHub/cuhHub

Copyright (C) 2026 cuhHub - All Rights Reserved
    - Unauthorized copying of this file, via any medium is strictly prohibited
    - Proprietary and confidential
"""

# ---- // Imports
import os
import subprocess
import sys
import shutil

# ---- // Main
ADDON_NAME = sys.argv[1]
ADDON_PATH = sys.argv[2]
SW_ADDON_PATH = os.path.expandvars(f"%appdata%/Stormworks/data/missions/{ADDON_NAME}")

def copy_over_playlist():
    """
    Copies over playlist.xml from addon to Stormworks.
    """
    
    shutil.copyfile(
        os.path.join(ADDON_PATH, "playlist.xml"),
        os.path.join(SW_ADDON_PATH, "playlist.xml")    
    )
    
def copy_over_vehicles():
    """
    Copies over vehicles from addon to Stormworks.
    """
    
    for file in os.listdir(ADDON_PATH):
        if not file.endswith(".xml"):
            continue
        
        if not file.startswith("vehicle_"):
            continue
        
        shutil.copyfile(
            os.path.join(ADDON_PATH, file),
            os.path.join(SW_ADDON_PATH, file)
        )
        
def first_build():
    """
    Builds the addon for (what should be) the first time.
    """
    
    subprocess.call("build.bat")

def main():
    """
    Main logic.
    """
    
    if not os.path.exists(SW_ADDON_PATH):
        print(f"Create addon with name \"{ADDON_NAME}\" via Stormworks first!")
        return
    
    copy_over_playlist()
    copy_over_vehicles()
    first_build()
        
if __name__ == "__main__":
    main()