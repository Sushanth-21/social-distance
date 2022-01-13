
from detection import social_distancing_config as config
from detection.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
import utils
import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import sys

fig = plt.figure()
axis=fig.add_subplot(111, projection='3d')
#axis = plt.axes(xlim =(-50, 50),ylim =(-50, 50))
axis.set_xlim(-2000,2000)

axis.set_ylim(-2000,2000)

axis.set_zlim(-2000,2000)
line = axis.scatter([], [],[])

def init():
    line._offsets3d=([], [],[])
    return line,


xdata, ydata, zdata = [], [], []

def animate(i):
	global xdata
	global ydata
	global zdata
	if i>=len(xdata):
		sys.exit()
	print(i)
	line._offsets3d=(xdata[i], ydata[i],zdata[i])
	return line,


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
args = vars(ap.parse_args())


labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")


weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])


net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


if config.USE_GPU:
	
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


ln = net.getLayerNames()
ln = [ln[i- 1] for i in net.getUnconnectedOutLayers()]

vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None
flag=True



while True:
	
	(grabbed, frame) = vs.read()

	
	if not grabbed:
		break

	
	frame = imutils.resize(frame, width=460,height=460)
	results = detect_people(frame, net, ln,
		personIdx=LABELS.index("person"))

	
	violate = set()

	
	if len(results) >= 2:
		
		
		obj_coord=[]
		plane_eq=[]
		n=0
		c=[]
		centroids=[]
		x,y,z=[],[],[]
		for r in results:

			# print(r)
			#print(r[1])
			x3=((r[1][0]-229)/utils.scale)
			y3=(((r[1][1]-229)/utils.scale))*-1
			x4=((r[1][2]-229)/utils.scale)
			y4=(((r[1][1]-229)/utils.scale))*-1
			x1=((r[1][0]-229)/utils.scale)
			y1=(((r[1][3]-229)/utils.scale))*-1
			x2=((r[1][2]-229)/utils.scale)
			y2=(((r[1][3]-229)/utils.scale))*-1

			

			# x1,x3=x3,x1
			# y1,y3=y3,y1

			# x2,x4=x4,x2
			# y2,y4=y4,y2


			m=(r[1][3]-r[1][1])/utils.m
			#m=145
			#print(m)
			l=utils.l

			# print((x2-x1)*(y4-y2),(x4-x2)*(y2-y1),(x4-x2)*(y3-y2),(x3-x2)*(y4-y2))
			# x1 = -1.74
			# y1 = -0.46875
			# x2 = -0.83
			# y2 = -0.46875
			# x3 = -1.74
			# y3 = 1.72
			# x4 = -0.83 
			# y4 = -1.72
			a=(((x2-x1)*(y4-y2)-((x4-x2)*(y2-y1))))/(((x4-x2)*(y3-y2)-((x3-x2)*(y4-y2))))
			b=(((x2-x1)*(y3-y2)-((x3-x2)*(y2-y1))))/(((x4-x2)*(y3-y2)-((x3-x2)*(y4-y2))))
			
			t0=m/math.sqrt((((a*x3)-x1)**2)+(((a*y3)-y1)**2)+(l**2)*(((a-1))**2))

			t2=a*t0
			t3=b*t0
			t1=t0+t3-t2

			#print("t0 -> ",t0,'t1 -> ',t1,'t2 -> ',t2,'t3 -> ',t3)

			#print(a,b)
			#print(t0,t1,t2,t3)
			tmp=[(t0*x1*-1,t0*y1*-1,t0*l),(t1*x2*-1,t1*y2*-1,t1*l),(t2*x3*-1,t2*y3*-1,t2*l),(t3*x4*-1,t3*y4*-1,t3*l)]
			#tmp=[(t0*x1*-1,t0*l,t0*y1*-1),(t1*x2*-1,t1*l,t1*y2*-1),(t2*x3*-1,t2*l,t2*y3*-1),(t3*x4*-1,t3*l,t3*y4*-1)]
			obj_coord.append(tmp)
			plane_eq.append(utils.equation_plane(tmp[0][0],tmp[0][1],tmp[0][2],tmp[1][0],tmp[1][1],tmp[1][2],tmp[2][0],tmp[2][1],tmp[2][2]))
			n+=1
			c=((tmp[0][0]+tmp[1][0])/2,(tmp[0][1]+tmp[2][1])/2,(t0*l+t1*l+t2*l+t3*l)/2)
			#print(tmp)
			x.append(c[0])
			y.append(c[1])
			z.append(c[2])


		# for i in range(n):
		# 	for j in range(i+1,n):
		# 		#print(utils.get_distance(obj_coord[i],obj_coord[j]))
		# 		# if utils.get_distance(c[i],c[j])<180:
		# 		# 	violate.add(i)
		# 		# 	violate.add(j)
		# 		#print(utils.get_distance(obj_coord[i],obj_coord[j]))
		# 		if utils.get_distance(obj_coord[i],obj_coord[j])<180:
		# 			violate.add(i)
		# 			violate.add(j)

			

			centroids.append(c)

		for i in range(len(centroids)):
			for j in range(i+1,len(centroids)):
			#print(utils.euclidean(c,centroids[i]))
				if utils.euclidean(centroids[i],centroids[j])<180:
					violate.add(i)
					violate.add(j)
						

		# for i in range(n):
		# 	for j in range(i+1,n):
		# 		if utils.shortest_distance(obj_coord[i][0][0],obj_coord[i][0][1],obj_coord[i][0][2],plane_eq[j][0],plane_eq[j][1],plane_eq[j][2],plane_eq[j][3]) < 10:
		# 			violate.add(i)
		# 			violate.add(j)
				
			



	
	for (i, (prob, bbox, centroid)) in enumerate(results):
		
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

	
		if i in violate:
			color = (0, 0, 255)

		
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		cv2.circle(frame, (cX, cY), 5, color, 1)

	
	text = "Social Distancing Violations: {}".format(len(violate))
	cv2.putText(frame, text, (10, frame.shape[0] - 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

	
	if args["display"] > 0:
		
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		
		if key == ord("q"):
			break

	
	if args["output"] != "" and writer is None:
		
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 25,
			(frame.shape[1], frame.shape[0]), True)

	
	if writer is not None:
		writer.write(frame)

	flag=False

	xdata.append(x)
	ydata.append(y)
	zdata.append(z)

anim = animation.FuncAnimation(fig, animate,
                            init_func = init,
							interval=2000,
                            blit = False, cache_frame_data=False)

anim.save('animation1.gif', writer='PillowWriter', fps=30)


