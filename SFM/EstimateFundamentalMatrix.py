# Fundamental matrix: denoted by F, is a 3×3 (rank 2) matrix that is used to 
# describe the geometric relationship between two views (or images) of the 
# same scene taken from different viewpoints

#  When you have two images of the same scene taken from different viewpoints 
# (as in stereo vision), every point in one image has a corresponding point 
# in the other image. These corresponding points are constrained by 
# epipolar geometry, and the fundamental matrix describes this constraint.


###########################################################
## https://www.youtube.com/watch?v=6kpBqfgSPRc&t=343s    ## 
## https://cmsc733.github.io/2022/proj/p3/#estfundmatrix ##
###########################################################

import numpy as np
import cv2
import glob

# Params : 
# img1_pts and img2_pts : Same features points in image 1 and image 2 (8 of those)

####################################
##  This is the 8-point algorithm ##
####################################
def estimate_Fmatrix(img1_pts,img2_pts):

    #normalize points
    # img1_pts,T1 = normalize_points(img1_pts)
    # img2_pts,T2 = normalize_points(img2_pts)
    
    # Extract coordinates from points in both images
    left_img_x_coords = img1_pts[:, 0]
    left_img_y_coords = img1_pts[:, 1]

    right_img_x_coords = img2_pts[:, 0]
    right_img_y_coords = img2_pts[:, 1]

    # Initialize the design matrix A
    num_points = len(left_img_x_coords)
    A = np.zeros((num_points, 9))

   
    # Populate the design matrix
    for i in range(num_points):
        x_left = left_img_x_coords[i]
        y_left = left_img_y_coords[i]
        x_right = right_img_x_coords[i]
        y_right = right_img_y_coords[i]
        
        A[i] = [
            x_right * x_left,
            x_right * y_left,
            x_right,
            y_right * x_left,
            y_right * y_left,
            y_right,
            x_left,
            y_left,
            1
        ]

    # Taking SVD of A for estimation of F
    U, S, V = np.linalg.svd(A,full_matrices=True)
    F_est = V[-1, :]
    F_est = F_est.reshape(3,3)

    # Enforcing rank 2 for F
    # Q. Why rank 2 ?
    # -> A fundamental matrix needs to have a rank of 2 to ensure that the epipolar constraint is 
    # satisfied and the geometric relationship between corresponding points in stereo vision is correctly represented.


    # Perform Singular Value Decomposition (SVD) on the fundamental matrix
    U, singular_values, V_T = np.linalg.svd(F_est, full_matrices=True)
    
    # Convert singular values array to diagonal matrix
    S = np.diag(singular_values)
    
    # Set the smallest singular value to zero to enforce rank-2
    S[2, 2] = 0
    
    # Reconstruct the fundamental matrix using modified singular values
    rank_2_fundamental_matrix = U @ S @ V_T

    return rank_2_fundamental_matrix