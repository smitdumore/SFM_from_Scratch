import numpy as np
import cv2

# Input params
# k           : intrinsic camera parameter matrix
# pt1 and pt2 : are the pixel coordinates of the same real-world 
#               point as seen in two different images.
# R1 and R2   : Relative rotation of cameras when images were captured
# t1 and t2   : Relative translation of cameras when images were captured

def point_triangulation(k,pt1,pt2,R1,t1,R2,t2):
    points_3d = []

    I = np.identity(3)
    t1 = t1.reshape(3,1)
    t2 = t2.reshape(3,1)

    # Calculating projection matrix P = K[R|t]
    # A projection matrix maps the 3D world points to 2D pixel coordinates
    P1 = np.dot(k,np.dot(R1,np.hstack((I,-t1))))
    P2 = np.dot(k,np.dot(R2,np.hstack((I,-t2))))
  
    # Homogeneous coordinates for images
    # The operation of adding a 1 at the end of the 2D coordinates 
    # (making it [x, y, 1] instead of just [x, y]) is what makes it homogeneous.

    # use of homogeneous coordinates greatly simplifies the mathematics, 
    # especially when dealing with transformations and projections.
    xy = np.hstack((pt1,np.ones((len(pt1),1))))      # pt1
    xy_cap = np.hstack((pt2,np.ones((len(pt1),1))))  # pt2

    # So we have a 3D world point 'X'
    # Using the prjection matrix we can say that 
    # pt1 = P1.X and pt2 = P2.X
    # problem is to find 'X' , given pt1, pt2, P1 and P2

    # Due to noise and inaccuracies we cant solve this analytically
    # So the system is solved for 'X' in a least sqaures sense, which 
    # minimizes the sum of the sqaures of the differences between the 
    # left and right side of equations.

    # Now,
    # FACT : The cross-product of a vector with itself is zero. 
    # So, pt1 x pt1 = 0 and pt2 x pt2 = 0 
    # thus pt1 = P1.X can be written as pt1 x (P1 * X) = 0
    # and  pt2 = P2.X can be written as pt2 x (P2 * X) = 0
    # So, this is a constraint equation, it says 
    # "the result should be this if the projection is perfect". 
    # But in real cases due to noise and other factors, it won't be exactly zero. 
    # So, we try to minimize it which leads to the least squares solution.

    # we can then take the two equations and make triangualtion into
    # an AX = 0 problem. 

    
    p1,p2,p3 = P1
    p1_cap, p2_cap,p3_cap = P2

    #constructing contraints matrix
    for i in range(len(xy)):
        A = []
        x = xy[i][0]
        y = xy[i][1]
        x_cap = xy_cap[i][0]
        y_cap = xy_cap[i][1] 
        
        A.append((y*p3) - p2)
        A.append((x*p3) - p1)
        
        A.append((y_cap*p3_cap)- p2_cap)
        A.append((x_cap*p3_cap) - p1_cap)

        # The Singular Value Decomposition (SVD) approach is a 
        # kind of analytical method to solve the least squares problem.
        # Levenberg Marquat, Gradient Descent, Guass-Newton

        # TODO : understand SVD thoroughly

        A = np.array(A).reshape(4,4)

        _, _, v = np.linalg.svd(A)
        x_ = v[-1,:]
        x_ = x_/x_[-1]
        # x_ =x_[:3]
        points_3d.append(x_)


    return np.array(points_3d)
