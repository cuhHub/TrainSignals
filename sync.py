# // ---------------------------------------------------------------------
# // ------- [cuhHub] Sync
# // ---------------------------------------------------------------------

"""
A tool for syncing all files in a directory from one place to the other.
Repo: https://github.com/cuhHub/cuhHub

Copyright (C) 2026 cuhHub - All Rights Reserved
    - Unauthorized copying of this file, via any medium is strictly prohibited
    - Proprietary and confidential
"""

# ---- // Imports
import os
import click
import shutil

# ---- // Classes
def sync(directory: str, destination: str, ignore: list[str]) -> str:
    """
    Clones all files and directories in a directory to a destination directory.

    Args:
        directory (str): The directory containing files/directories to synchronize.
        destination (str): The destination that all of the synced files/directories will be cloned to.
        ignore (list[str]): The files/directories to ignore when synchronizing (patterns supported, e.g. '*.py').
    
    Returns:
        str: The destination which may have been changed.
    """
    
    if os.path.isfile(directory):
        if not os.path.isfile(destination):
            destination = os.path.join(destination, os.path.basename(directory))
        
        shutil.copyfile(
            src = directory,
            dst = destination
        )
        
        return destination
    
    shutil.copytree(
        src = directory,
        dst = destination,
        ignore = shutil.ignore_patterns(*ignore),
        dirs_exist_ok = True
    )
    
    return destination

# ---- // Main
@click.command()
@click.option("--directory", "-d", "-p", "--path", type = str, required = True, help = "The directory containing files/directories to sync.")
@click.option("--destination", "-de", type = str, required = True, help = "The destination that all of the synced files/directories will be cloned to.")
@click.option("--ignore", "-ip", type = str, required = False, multiple = True, help = "The files/directories to ignore when synchronizing.")
def sync_tool(directory: str, destination: str, ignore: tuple[int, ...]):
    """
    Clones all files and directories in a directory to a destination directory.

    Args:
        directory (str): The directory containing files/directories to synchronize.
        destination (str): The destination that all of the synced files/directories will be cloned to.
        ignore (tuple[int, ...]): The files/directories to ignore when synchronizing.
    """    
    
    ignore = list(ignore) # `ignore` is a tuple for some reason
    ignore.extend([__file__])

    destination = sync(
        directory = directory,
        destination = destination,
        ignore = ignore
    )

    click.secho(f"[Done] Sucessfully synced `{directory}` to `{destination}`.", fg = "green", underline = True, bold = True)
    
if __name__ == "__main__":
    sync_tool()