# cuhHub - Train Signals

## 📚 Overview
An addon providing train signals around the map. Ripped from base-game train signals addon.

## ⚙️ Setup
1) Run `git clone https://github.com/cuhHub/TrainSignals`.
2) `cd` into the created directory and run `pip install -r requirements.txt` to install needed Python packages for building the project.
3) Create an addon called "TrainSignals" (exactly) in Stormworks, then run `setup.bat`.
4) Run `build.bat`. This will update the addon in `%appdata%/Stormworks/data/missions` into the required location for the game. Do this for every change to the code you make in order to test in-game or to publish new changes to cuhHub.
5) Run the addon in a save and all should work.

## ✈️ Publishing
To publish the addon to a cuhHub server, run `publish.bat`.

Before doing so, rename `example.env` to `.env` and add missing env variables.

If the addon is already on the server, publishing again will simply update the addon.

## ✨ Credit
- [Cuh4](https://github.com/Cuh4)