@ECHO off

set server_id=%1

if "%server_id%" == "" (
    echo Error: Provide server_id argument
    exit /b 1
)

set addon_name=TrainSignals
set addon_sw_path=%appdata%/Stormworks/data/missions/%addon_name%

echo Publishing to server ID #%server_id%

: Publish addon
py publish.py --type "addon" --name %addon_name% --directory "%addon_sw_path%" --server_id %server_id%