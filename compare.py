import cv2
import matplotlib.pyplot as plt


f_img = cv2.imread('img1.png')
s_img = cv2.imread('img2.png')
f_img = cv2.cvtColor(f_img, cv2.COLOR_BGR2RGB)
s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2RGB)
ans = cv2.cvtColor(cv2.subtract(f_img, s_img), cv2.COLOR_RGB2GRAY)

ret, thresh = cv2.threshold(ans, 0, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(contours)

for cnt in contours:
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(f_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.rectangle(s_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
plt.sca(axs[0])
plt.imshow(f_img)
plt.sca(axs[1])
plt.imshow(s_img)
plt.sca(axs[2])
plt.imshow(ans, cmap='gray')

plt.savefig("test.png")