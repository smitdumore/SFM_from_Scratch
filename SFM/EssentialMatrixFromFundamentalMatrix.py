import numpy as np
import cv2

# The essential matrix requires calibrated cameras, meaning that the camera intrinsic parameters 
# (focal length, principal point, etc.) are known.
# The essential matrix encodes information about the relative motion (pose) between two cameras in a stereo vision system

###############
# E = K.F.K^T #
###############

def estimate_Essentialmatrix(k,F):
    E_est = np.dot(k.T,np.dot(F,k))

    # Enforce the Essential Matrix Constraints
    U, S, V = np.linalg.svd(E_est,full_matrices=True)
    S = np.diag(S)

    # The essential matrix should have two equal non-zero singular values and one singular value of zero.
    S[0,0],S[1,1],S[2,2] = 1,1,0
    E = np.dot(U,np.dot(S,V))

    return E