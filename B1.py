import cv2
import numpy as np

img = cv2.imread('sEuidy5yWe9A.png')
original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

b, g, r = cv2.split(img)
kernel = np.ones((5,5), np.uint8)

edges_channels = {}
for name, ch in [('b', b), ('g', g), ('r', r)]:
    ch_blur = cv2.GaussianBlur(ch, (9, 9), 1.5)
    ch_blur = cv2.medianBlur(ch_blur, 5)
    edges_ch = cv2.Canny(ch_blur, 50, 150)

    edges_ch = cv2.morphologyEx(edges_ch, cv2.MORPH_CLOSE, kernel, iterations=2)
    edges_channels[name] = edges_ch
edges = cv2.bitwise_or(edges_channels['r'], cv2.bitwise_or(edges_channels['g'], edges_channels['b']))

blur_for_circles = cv2.GaussianBlur(gray, (11, 11), 2)
blur_for_circles = cv2.medianBlur(blur_for_circles, 5)

circles = cv2.HoughCircles(
    blur_for_circles,
    cv2.HOUGH_GRADIENT,
    dp=1,                
    minDist=50,          
    param1=50,           
    param2=30,           
    minRadius=20,        
    maxRadius=400        
)

detected_circles = []
if circles is not None:
    circles = np.uint16(np.around(circles))

    for i, circle in enumerate(circles[0, :]):
        cx, cy, radius = circle
        
        cv2.circle(img, (cx, cy), radius, (255, 0, 255), 3)
        
        cv2.circle(img, (cx, cy), 2, (0, 0, 255), 3)

        x = cx - radius
        y = cy - radius
        cv2.rectangle(img, (x, y), (x + radius*2, y + radius*2), (255, 0, 255), 2)
        
        cv2.putText(img, f"Circle", (cx - radius, cy - radius - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        detected_circles.append({'center': (cx, cy), 'radius': radius})
        print(f"  Lingkaran {i+1}: Center=({cx},{cy}), Radius={radius}")

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = [c for c in contours if cv2.contourArea(c) > 500]


for cnt in contours:
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    shape = "Tidak diketahui"

    if len(approx) == 3:
        shape = "Segitiga"
    elif len(approx) == 4:
        ratio = w / float(h)
        shape = "Persegi" if 0.95 <= ratio <= 1.05 else "Persegi Panjang"
    elif len(approx) > 5:
        area = cv2.contourArea(cnt)
        circularity = 4 * np.pi * area / (peri * peri) if peri > 0 else 0
        
        if circularity > 0.8:
            shape = "Lingkaran (contour)"
        else:
            shape = "Polygon"

    cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    cv2.putText(img, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

cv2.imshow("Edges", edges)
cv2.imwrite("edges.png", edges)
cv2.imshow("Detected Shapes + Circles", img)
cv2.imwrite("detected.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
