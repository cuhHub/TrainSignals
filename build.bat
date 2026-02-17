@ECHO off

set addon_dir=src
set addon_name=TrainSignals
set addon_build_file=_build/script.lua
set addon_sw_path=%appdata%/Stormworks/data/missions/%addon_name%

: Build addon into single .lua file
py combine.py --directory "%addon_dir%" --destination "%addon_build_file%" --allow_file_extension ".lua"

: Sync to game (for testing)
py sync.py --directory "%addon_build_file%" --destination "%addon_sw_path%"

: Sync game to here (in-case addon editor was used and locations were manipulated)
py sync.py --directory "%addon_sw_path%" --destination "%addon_dir%" --ignore "script.lua"