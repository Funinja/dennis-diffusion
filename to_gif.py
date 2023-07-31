import cv2

frames = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for i in range(16):
    img = cv2.imread("frames/test" + str(i) +".png")
    frames.append(img)
    
dim = frames[0].shape[0:2]
out = cv2.VideoWriter("test.mp4", fourcc, 24, dim)

for i in frames:
    out.write(i)
    
out.release()