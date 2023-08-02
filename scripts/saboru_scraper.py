
import requests
import json
import cv2

from content_splitter import c_split
from sequence_splitter import split_sequences
import os

base_url = 'https://sakugabooru.com/post.json'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

cwd = os.getcwd()
    
video_path = os.path.join(cwd, "videos")

limit = 100000

def jprint(obj):
    
    text = json.dumps(obj, sort_keys=True, indent=4)
    
    print(text)

# download url as mp4
def download_mp4(file_url, page, entry, mp4_dir, dim):
    # f = Path("scene_" + str(page) + "_" + str(entry) + ".mp4")
    name_mp4 = mp4_dir + "/scene_" + str(page) + "_" + str(entry) + ".mp4"
    cap = cv2.VideoCapture(file_url)
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    if frame is not None:
        # dim = (int(width), int(height))
        out = cv2.VideoWriter(name_mp4, fourcc, fps, dim)
        
        
        while(frame is not None):
            resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            out.write(resized)
            
        #     cv2.imshow('frame',resized)
        # # Press q to close the video windows before it ends if you want
        #     if cv2.waitKey(22) & 0xFF == ord('q'):
        #         break
            ret, frame = cap.read()
        cap.release()
        out.release()
    
            
# inspect all entries of the page
def get_page(page, entry_limit, mp4_dir):
    
    parameters = {
        "page":page,
        "tags":"animated -effects -production_materials -genga_comparison",
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

            download_mp4(entry['file_url'], page, index, mp4_dir=mp4_dir, dim=(128,128))
            
        
        return num_entries

# page limit == -1 causes all pages to be read
def scrape(page_limit=-1,entry_limit=-1, mp4_dir="videos", l_seq=30):
    
    page = 0
    
    num_entries = get_page(page, entry_limit, mp4_dir)
    
    cwd = os.getcwd()
    
    print("First Page Complete")
    
    while(num_entries != 0):
        if page_limit != -1 and page_limit <= page:
            break
        page += 1
        num_entries = get_page(page, entry_limit, mp4_dir)
        
        print("Getting next page: " + str(page))
        
        
    c_split(l_seq)
    split_sequences(l_seq)
    

if __name__ == '__main__':
    scrape(0, -1)