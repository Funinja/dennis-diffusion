import cv2
import os

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def split_sequences(l_seq=20):
    
    cwd = os.getcwd()
    
    video_path = os.path.join(cwd, "videos")
    
    files = os.listdir(video_path)
    
    os.chdir(video_path)
    for file in files:
        cap = cv2.VideoCapture(file)
        ret, frame = cap.read()
        fps = cap.get(cv2.CAP_PROP_FPS)
        dim = (64, 64)
        seq_count = 1
        
        if frame is not None:
            # dim = (int(width), int(height))
            name_mp4 = file[:-4] + "_" + str(seq_count) + ".mp4"
            out = cv2.VideoWriter(name_mp4, fourcc, fps, dim)
            frame_no = 0
            while(frame is not None):
                frame_no += 1
                
                out.write(frame)
                
                if frame_no >= l_seq:
                    out.release()
                    seq_count += 1
                    frame_no = 0
                    name_mp4 = file[:-4] + "_" + str(seq_count) + ".mp4"
                    out = cv2.VideoWriter(name_mp4, fourcc, fps, dim)
                
                ret, frame = cap.read()
            cap.release()
            out.release()
            
            os.remove(name_mp4)
            
        os.remove(file)
    
    os.chdir(cwd)
    
    
if __name__ == '__main__':
    split_sequences(20)