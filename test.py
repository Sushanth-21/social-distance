import matplotlib.pyplot as plt
import matplotlib.image as img
import cv2


def finding_bgr(image,winName):
    def bgr(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            #cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

            print(winName+'[' + str(x) + ',' + str(y) + ']', image[y,x])
            points.append((x, y))

    points =[]
    cv2.namedWindow(winName)
    cv2.setMouseCallback(winName,bgr)
    print(image.shape)

    cv2.imshow(winName , image)
    if cv2.waitKey(0) & 0xff == 's':
        cv2.destroyAllWindows()
    return points

img=cv2.imread("test_pic2.png")
new_img=cv2.resize(img,(460,460))
cv2.imshow("testing",new_img)
p=finding_bgr(new_img,"testing")
print(p)
cv2.waitKey(0)
cv2.destroyAllWindows()
