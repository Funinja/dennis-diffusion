
import requests
import json
from pathlib import Path
import os

base_url = 'https://sakugabooru.com/post.json'

def jprint(obj):
    
    text = json.dumps(obj, sort_keys=True, indent=4)
    
    print(text)

# download url as mp4
def download_mp4(file_url, page, entry, mp4_dir):
    f = Path("scene_" + str(page) + "_" + str(entry) + ".mp4")
    
    cwd = os.getcwd()
    
    if mp4_dir == "":
        new_path = os.path.join(cwd, "videos")
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        
        os.chdir(new_path)
        
    else:
        os.chdir(mp4_dir)
            
    f.write_bytes(requests.get(file_url).content)
    
    os.chdir(cwd)
            
# inspect all entries of the page
def get_page(page, entry_limit, mp4_dir):
    
    parameters = {
        "page":page,
        "tags":"animated -effects",
    }
    
    response = requests.get(base_url, params=parameters)
    
    response_json = response.json()
    
    num_entries = len(response_json)
    
    if num_entries <= 0:
        return 0
    else:
        for index, entry in enumerate(response_json):
            if entry_limit != -1 and entry_limit <= index:
                break
            
            download_mp4(entry['file_url'], page, index, mp4_dir=mp4_dir)
            
        
        return num_entries

# page limit == -1 causes all pages to be read
def scrape(page_limit=-1,entry_limit=-1, mp4_dir=""):
    
    page = 0
    
    num_entries = get_page(page, entry_limit, mp4_dir)
    
    while(num_entries != 0):
        if page_limit != -1 and page_limit <= page:
            break
        page += 1
        num_entries = get_page(page, entry_limit, mp4_dir)
    

if __name__ == '__main__':
    scrape(0, -1, "")