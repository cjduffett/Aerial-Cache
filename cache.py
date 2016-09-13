import requests
import getpass
import shutil
import os
import sys

METADATA_URL = "http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json"
CACHE_DIR = "/Users/:uname/Library/Caches/Aerial/"

def cachePhotos():

    """
        Caches all of the photos that the Aerial screen saver uses in
        /Users/YOURUSERNAME/Library/Caches/Aerial
    """
    print "Fetching Aerial metadata..."

    metadata = requests.get(METADATA_URL).json()
    cachedir = getCacheDir(getUsername())

    print "Aerial cache directory: " + cachedir
    print "Cleaning up directory..."
    makeCacheDir(cachedir)
    cleanCacheDir(cachedir)

    for collection in metadata:
        for asset in collection["assets"]:
            sys.stdout.write("Downloading " + asset["id"] + ": " + asset["accessibilityLabel"] + " " + asset["timeOfDay"] + " ... ")
            sys.stdout.flush()
            
            path = cachedir + asset["id"] + ".mov"
            r = requests.get(asset["url"], stream=True)

            if r.status_code == 200:
                with open(path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

                sys.stdout.write("done\n")
                sys.stdout.flush()

            else:
                sys.stdout.write("failed\n")
                sys.stdout.flush()


def getCacheDir(username):
    return CACHE_DIR.replace(":uname", username)


def makeCacheDir(cachedir):
    if not os.path.exists(cachedir):
        os.mkdir(cachedir, 0755)


def cleanCacheDir(cachedir):
    contents = os.listdir(cachedir)
    for content in contents:
        os.remove(cachedir + content)


def getUsername():
    return getpass.getuser()


if __name__ == "__main__":
    cachePhotos()
