from scenedetect import detect, ContentDetector, split_video_ffmpeg
import os

def c_split(l_seq):
    
    cwd = os.getcwd()
    
    video_path = os.path.join(cwd, "videos")
    
    files = os.listdir(video_path)
    
    os.chdir(video_path)
    
    for file in files:
        
        scene_list = detect(file, ContentDetector())
        new_list = []
        
        for scene in scene_list:
            
            if scene[1].get_frames() - scene[0].get_frames() >= l_seq:
                new_list.append(scene)
            
        split_video_ffmpeg(file, new_list)
        if len(scene_list) != 0:
            os.remove(file)
        
    os.chdir(cwd)

if __name__ == '__main__':
    c_split(20)