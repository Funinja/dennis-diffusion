from numpy import load
from PIL import Image

data = load('1x16x32x32x3.npz')
lst = data.files
info = data[lst[0]]
print(info.shape)

first_clip = info[0]

for i, frame in enumerate(first_clip):
    
    img = Image.fromarray(frame)
    img.save("frames/test" + str(i) + ".png")
