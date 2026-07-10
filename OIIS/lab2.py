import cv2 
import numpy as np

img1 = cv2.imread('img.png')
img2 = cv2.imread('img2.jpg')

height, width = img1.shape[:2]
img2_resized = cv2.resize(img2, (width, height), interpolation=cv2.INTER_AREA)

cv2.imshow('Image 1', img1)
cv2.imshow('Image 2 Resized', img2_resized)

hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
hsv2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2HSV)

value1 = np.mean(hsv1[:,:,2])
value2 = np.mean(hsv2[:,:,2])

print(f"Яркость img1: {value1}")
print(f"Яркость img2: {value2}")

ratio = value2 / value1
hsv1[:,:,2] = np.clip(hsv1[:,:,2] * ratio, 0, 255).astype(np.uint8)
corrected_img1 = cv2.cvtColor(hsv1, cv2.COLOR_HSV2BGR)
corrected_img2 = img2_resized

cv2.imshow('Corrected Image 1', corrected_img1)
cv2.imshow('Corrected Image 2', corrected_img2)

cv2.waitKey(0)
cv2.destroyAllWindows()