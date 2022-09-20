import urllib.request, json, tempfile, pretty_downloader, os
from sys import platform
config = json.load(open("config.json"))

debug_mode = config["debug_mode"] # true or false
load_from_file = config["load_from_file"] # true or talse
manifest = config["manifest_location"] # URL or file path to manifest
if load_from_file == "true":
    try:
        manifest = json.load(open(manifest))
    except FileNotFoundError:
        print("The manifest file path does not exist. Check if the provided location isn't a url.")
        exit()
_count = 0
mod_dict=dict()
if debug_mode == "true":
    print('Downloading manifest')
if os.path.exists(tempfile.gettempdir()+"/manifest.json"):
    print('Manifest already exists, Skipping...')
else:
    print('Downloading manifest')
    urllib.request.urlretrieve(manifest, tempfile.gettempdir()+"/manifest.json")
manifest_json = json.loads(open(tempfile.gettempdir()+"/manifest.json").read())
if debug_mode == "true":
    print('loaded url')
print(str(len(manifest_json['files']))+' Mods')
for i in manifest_json['files']:
    projectID = i['projectID']
    fileID = i['fileID']
    mod_json = json.loads((urllib.request.urlopen("https://addons-ecs.forgesvc.net/api/v2/addon/{}/files".format(projectID))).read().decode())
    if debug_mode == "true":
        print('loaded json')
    for i in mod_json:
        _count+=1
        if i['id'] == fileID:
            if debug_mode == "True":
                print(i['downloadUrl'])
            if platform == "linux" or platform == "linux2":
                pretty_downloader.download(i['downloadUrl'],name="Downloading mod: " + i['downloadUrl'],file_path=os.path.expanduser("~/.minecraft/mods/"))
            elif platform == "win32":
                pretty_downloader.download(i['downloadUrl'],name="Downloading mod: " + i['downloadUrl'],file_path=os.getenv('APPDATA')+'/.minecraft/mods')
