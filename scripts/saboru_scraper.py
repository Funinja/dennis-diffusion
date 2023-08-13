
import requests
import json
import cv2
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from content_splitter import c_split
from sequence_splitter import split_sequences
import os

from skimage.metrics import structural_similarity as ssim

base_url = 'https://sakugabooru.com/post.json'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

cwd = os.getcwd()
    
video_path = os.path.join(cwd, "videos")

limit = 100000

ssim_limit = 0.55

def jprint(obj):
    
    text = json.dumps(obj, sort_keys=True, indent=4)
    
    print(text)

# download url as mp4
def download_mp4(file_url, page, entry, mp4_dir, dim, lseq=24):
    # f = Path("scene_" + str(page) + "_" + str(entry) + ".mp4")
    name_mp4 = mp4_dir + "/scene_" + str(page) + "_" + str(entry) + ".mp4"
    cap = cv2.VideoCapture(file_url)
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    if frame is not None:
        # dim = (int(width), int(height))
        
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blur the image for better edge detection
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

        # Canny Edge Detection
        edges = cv2.Canny(image=img_blur, threshold1=75, threshold2=100) 
        
        img_resized = cv2.resize(edges, dim, interpolation=cv2.INTER_AREA)
        
        prev_frame = img_resized
        ret, frame = cap.read()
    
        frame_list = [prev_frame]
        counter = 1
        cut_no = 1
        
        while(frame is not None):
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Blur the image for better edge detection
            img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

            # Canny Edge Detection
            edges = cv2.Canny(image=img_blur, threshold1=75, threshold2=100) 
            
            img_resized = cv2.resize(edges, dim, interpolation=cv2.INTER_AREA)
            
            ssim_img = ssim(prev_frame, img_resized, data_range=img_resized.max() - img_resized.min())
            
            if counter >= lseq:
                out = cv2.VideoWriter(name_mp4[:-4] + "_" + str(cut_no) + ".mp4", fourcc, fps, dim, isColor=False)
                
                cut_no += 1
                
                for f in frame_list:
                    out.write(f)
                
                out.release()
                            
                
                frame_list = [img_resized]
                counter = 1
            elif ssim_img < ssim_limit and counter < lseq:
                
                counter = 1
                prev_frame = img_resized
                frame_list = [img_resized]
                
            else:
            
                frame_list.append(img_resized)
                counter += 1
            
            prev_frame = img_resized
            ret, frame = cap.read()
            
        cap.release()
    
            
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
    
    page = 1555
    
    num_entries = get_page(page, entry_limit, mp4_dir)
    
    cwd = os.getcwd()
    
    print("First Page Complete")
    
    while(num_entries != 0):
        if page_limit != -1 and page_limit <= page:
            break
        page += 1
        num_entries = get_page(page, entry_limit, mp4_dir)
        print("Getting next page: " + str(page))
        
        
        
    # c_split(l_seq)
    # split_sequences(l_seq)
    

if __name__ == '__main__':
    scrape(3000, -1)