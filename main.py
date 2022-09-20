import urllib.request, json, tempfile, pretty_downloader, os, requests
from sys import platform

config = json.load(open("config.json"))

debug_mode = config["debug_mode"] # true or false
load_from_file = config["load_from_file"] # true or false
manifest = config["manifest_location"] # URL or file path to manifest
apikey = config["api-key"] # API key for the API


if debug_mode == "true":
    print("Debug mode enabled")

if load_from_file == "true":
    try:
        manifest_json = json.loads(open(manifest).read())
    except FileNotFoundError:
        print("The manifest file path does not exist. Check if the provided location isn't a url.")
        exit()
else:
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

manifest_mod_count=str(len(manifest_json['files']))
print(manifest_mod_count+' Mods')
count=1
no_url_mods=[]

for i in manifest_json['files']:
    projectID = i['projectID']
    fileID = i['fileID']

    headers={"Accept": "application/json", "x-api-key": apikey}
    url = "https://api.curseforge.com/v1/mods/{}/files/{}".format(projectID, fileID)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        mod_json = json.loads(response.read().decode('utf-8'))

    if debug_mode == "true":
        print('loaded json')
        print(mod_json['data'])
        try:
            print(mod_json['data']['downloadUrl'])
        except TypeError:
            print("Download Url not found for mod: " + mod_json['data']['displayName'])

    if platform == "linux" or platform == "linux2":
        try:
            pretty_downloader.download(mod_json['data']['downloadUrl'],name=str(count) + ". Downloading mod: " + mod_json['data']['displayName'],file_path=os.path.expanduser("~/.minecraft/mods/"))
            count+=1
            print()

        except TypeError:
            print("Download Url not found for mod: " + mod_json['data']['displayName'])
            print()
            no_url_mods.append(mod_json['data']['displayName'])
        except requests.exceptions.MissingSchema:
            print("Download Url not found for mod: " + mod_json['data']['displayName'])
            print()
            no_url_mods.append(mod_json['data']['displayName'])

    elif platform == "win32":
        try:
            pretty_downloader.download(mod_json['data']['downloadUrl'],name=str(count) + ". Downloading mod: " + mod_json['data']['displayName'],file_path=os.getenv('APPDATA')+'/.minecraft/mods')
            count+=1
            print()
        except TypeError:
            print("Download Url not found for mod: " + mod_json['data']['displayName'])
            print()
            no_url_mods.append(mod_json['data']['displayName'])
        except requests.exceptions.MissingSchema:
            print("Download Url not found for mod: " + mod_json['data']['displayName'])
            print()
            no_url_mods.append(mod_json['data']['displayName'])

print('Done!, Downloaded '+str(count)+' of '+ manifest_mod_count + ' mods')
if len(no_url_mods) > 0:
    print('The following mods did not have a download url:')
    for i in no_url_mods:
        print(i.strip().replace('.jar', ''))