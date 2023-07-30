import cv2
import imageio

frames = []

for i in range(16):
    img = cv2.imread("frames/test" + str(i) +".png")
    frames.append(img)
    
    
imageio.mimsave("test_gif.gif", frames)