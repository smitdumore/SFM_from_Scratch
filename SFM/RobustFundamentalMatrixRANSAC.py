from EstimateFundamentalMatrix import *
import numpy as np
import cv2


# Params : 
# pt1 : all feature points in left image  (also present in left)
# pt2 : all feature points in right image (also present in right)
def ransac(pt1,pt2):

    n_rows = np.array(pt1).shape[0]
    thresh = 0.05
    
    ones = np.ones((pt1.shape[0], 1))
    pts_img1 = np.hstack((pt1, ones))
    pts_img2 = np.hstack((pt2, ones))

    max_inliers = 0

    for i in range(10000):
     
        # Select 8 random feature points
        random = np.random.choice(n_rows,size = 8)
        img1_8pt = pt1[random,:]
        img2_8pt = pt2[random,:]

        # img2_8pt is an array containing 8 randomly selected points from pt2.
        # img1_8pt is an array containing 8 randomly selected points from pt1.
       
        F = estimate_Fmatrix(img1_8pt,img2_8pt)

        ################################################################################
        # compute xl.F.xrT = 0                                                         #
        # Basically we are back substituting the estimated Fundamental matrix in the   #
        # epipolar contraint equation and seeing if it is euqal to zero                #
        ################################################################################

        vals = np.abs(np.diag(np.dot(np.dot(pts_img2, F), pts_img1.T)))

        # setting threshold
        # print(vals)
        inliers_index = np.where(vals<thresh)
        outliers_index = np.where(vals>=thresh)

        # checking for max_inliers and saving it's index
        if np.shape(inliers_index[0])[0] > max_inliers:
            max_inliers = np.shape(inliers_index[0])[0]
            max_inliers_index = inliers_index

    # using only inliers for final F matrix estimation
    img1_points = pt1[max_inliers_index ]
    img2_points = pt2[max_inliers_index ]
    F = estimate_Fmatrix(img1_points,img2_points)

    return img1_points,img2_points, F

 