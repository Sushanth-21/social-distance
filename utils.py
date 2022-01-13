import math

scale=38.4
# l=focal lenght
l=1
#scaling factor for object height m pixel = 1 cm
m=0.3


def euclidean(pt1,pt2):
    return math.sqrt(int(((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2)+((pt1[2]-pt2[2])**2)))



def get_distance(o1,o2):
    res=10**5
    violate=0
    crct=0
    for i in range(4):
        for j in range(4):
            x=euclidean(o1[i],o2[j])
            #print(x)
            if x<res:
                res=x
    return res
    # for i in range(4):
    #     for j in range(4):
    #         if euclidean(o1[i],o2[j])<180:
    #             violate+=1
    #         else:
    #             crct+=1
    
    # if violate>crct:
    #     return True
    # return False

def equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):
     
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    
    #print(z1,z2,z3)
    return (a,b,c,d)


def shortest_distance(x1, y1, z1, a, b, c, d):

    #print(type(a),type(b),type(c),type(d),type(x1),type(y1),type(z1))
    #print(x1,y1,z1,a,b,c,d)
    d = int(abs((a * x1 + b * y1 + c * z1 + d)))
    e = (math.sqrt(a * a + b * b + c * c))

    #print(d/e)
    return d/e