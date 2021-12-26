# Curseforge-Modpack-Downloader
 <h2 align="center"> <i> <b> A Python script which automatically download mods from a Curseforge modpack. </b> </i> </h2>
## Installing Dependencies 
⚠ Make sure you have Python 3 installed. ⚠

```bash
pip install pretty-downloader
```
## Steps
1. Find your desired modpack file. (Depending on your minecraft version and/or mod loader etc.)
2. Click on download (if there is no download button and theres only install from the Curseforge app, erase `?client=y` from the button url.)
![mods.list](https://github.com/Rayrsn/Curseforge-Modpack-Downloader/raw/main/images/example1.png?raw=true)
3. After downloading the .zip file, unpack it. There should be a `manifest.json` file inside it.
4. You can either upload the file somewhere or copy the local path to it and paste it inside the `config.json` file from the script
## Running
You can simply run the script by running `python main.py`
