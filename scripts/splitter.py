from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg
import os

def split():
    
    cwd = os.getcwd()
    
    video_path = os.path.join(cwd, "videos")
    
    files = os.listdir(video_path)
    
    os.chdir(video_path)
    
    for file in files:
        
        scene_list = detect(file, AdaptiveDetector())
        new_list = []
        
        for scene in scene_list:
            numFrames = 16
            
            if scene[1].get_frames() - scene[0].get_frames() >= numFrames:
                new_list.append(scene)
            
        split_video_ffmpeg(file, new_list)
        
        os.remove(file)
        
    os.chdir(cwd)

if __name__ == '__main__':
    split()