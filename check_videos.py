import os
cwd = os.getcwd()
videos = os.path.join(cwd, "videos")

os.chdir(videos)

vids = os.listdir(videos)

for v in vids:

    os.system("ffmpeg -v error -i " + v + " -f null - 2>error.log")
    

print("finished checking for errors")

log_file = open("error.log","r")
print (log_file.read())
    
os.chdir(cwd)