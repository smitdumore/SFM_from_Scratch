Reference :

1. https://github.com/sakshikakde/SFM/blob/master/Code/PnPRansac.py
2. https://github.com/naitri/SFM/tree/main/Code


TODO : 
1. DisambiguateCameraPose.py
2. SVD understanding 
3. Add images

# Why are there 2 versions on PnP ?


Yes, at its core, Perspective-n-Point (PnP) is also a linear technique. The classic PnP problem involves solving a set of linear equations to estimate the camera pose (rotation and translation) from a set of 3D points in world coordinates and their corresponding 2D points in image coordinates.

Here's how the linear aspect works:

Linear Equations: Given the intrinsic camera matrix (calibration matrix), 3D world points, and their corresponding 2D image points, the PnP problem can be formulated as a set of linear equations that describe the relationship between the 3D points and their 2D projections onto the image plane.
Direct Solution: These linear equations can be solved directly using techniques such as Linear Least Squares to estimate the camera pose (rotation and translation). Ax = b


Yes, at its core, Perspective-n-Point (PnP) is also a linear technique. The classic PnP problem involves solving a set of linear equations to estimate the camera pose (rotation and translation) from a set of 3D points in world coordinates and their corresponding 2D points in image coordinates.

Here's how the linear aspect works:

Linear Equations: Given the intrinsic camera matrix (calibration matrix), 3D world points, and their corresponding 2D image points, the PnP problem can be formulated as a set of linear equations that describe the relationship between the 3D points and their 2D projections onto the image plane.
Direct Solution: These linear equations can be solved directly using techniques such as Linear Least Squares to estimate the camera pose (rotation and translation).
However, similar to triangulation, the term "non-linear PnP" refers to more sophisticated methods that go beyond the linear approach:

Non-linear Cost Function: Non-linear PnP constructs a non-linear cost function, often based on minimizing the reprojection error between the observed 2D image points and the projected 3D points.

The code you provided appears to be using two different types of PnP algorithms to estimate the camera pose (rotation and translation) and refine it further:

PnP RANSAC:
The first part of the code uses a method called PnP RANSAC, which combines the Perspective-n-Point (PnP) algorithm with the RANSAC (Random Sample Consensus) algorithm.
This approach is robust against outliers in the input data (3D and 2D point correspondences).
It estimates an initial camera pose (R_new_lt and T_new_lt) and also returns the inlier and outlier point correspondences (pnp_2d and pnp_3d), which can be useful for further optimization.
Non-linear PnP:
The second part of the code uses a non-linear optimization method (nonlinear_pnp) to refine the initial camera pose estimated by PnP RANSAC.
Non-linear PnP algorithms aim to find the optimal pose by minimizing the reprojection error between the observed 2D points (pnp_2d) and the projected 3D points (pnp_3d).
These algorithms use optimization techniques (e.g., Levenberg-Marquardt) to adjust the initial pose (R_new_lt and T_new_lt) to achieve the best fit.
Why Use Both Methods?
Using both PnP RANSAC and non-linear PnP provides a balance between robustness and accuracy:

PnP RANSAC:
This method provides a robust initial estimate of the camera pose, which can handle noisy data and outliers.
It returns a set of inlier points that are consistent with the estimated pose.
Non-linear PnP:
After obtaining an initial estimate and a set of inlier points from PnP RANSAC, non-linear PnP is used to refine the pose by minimizing the reprojection error.
This optimization process can improve the accuracy of the pose estimate.
By combining both methods, the code leverages the robustness of PnP RANSAC to deal with noisy data and outliers, and then uses non-linear PnP to optimize the pose and achieve a more accurate estimate. This approach is common in computer vision applications that involve camera pose estimation.

# Why are there 2 versions of Triangulation ?

Yes, you are correct in stating that the core process of triangulation is fundamentally a linear problem. Triangulation involves solving a set of linear equations to estimate the 3D position of points from multiple 2D views. However, when it comes to the optimization process, it becomes known as non-linear triangulation due to the use of a non linear least sqaure error cost function.

Yes, similar to PnP, triangulation can also be approached using both linear and non-linear methods, each offering distinct advantages.

Linear Triangulation:
Fast and Simple: Linear triangulation uses a direct method to estimate the 3D positions of points based on camera poses and 2D points.
Suitable for Initial Estimates: Linear triangulation can provide a good initial estimate of 3D point positions quickly and easily.
Less Accurate: Since it does not account for noise and errors in a more sophisticated manner, linear triangulation might be less accurate compared to non-linear methods.
Non-linear Triangulation:
Refinement: Non-linear triangulation aims to refine the initial estimates from linear triangulation to achieve better accuracy.
Minimizes Reprojection Error: By minimizing the reprojection error, non-linear triangulation optimizes the 3D points’ positions relative to camera poses and 2D points.
Iterative: It may involve iterative optimization and, therefore, could be slower and computationally more intensive.
Combining Linear and Non-linear Triangulation:
Initial Estimates: Linear triangulation provides a fast and efficient way to compute initial estimates of the 3D point positions, which can then be refined using non-linear triangulation.
Accuracy: Non-linear triangulation refines the initial estimates from linear triangulation, improving the accuracy of the 3D point positions.
In the code provided, the approach mirrors that of PnP where linear triangulation is used initially to estimate 3D points quickly, followed by non-linear triangulation to refine these points for greater accuracy. This approach balances speed and efficiency with precision, depending on the quality of the data and the specific requirements of your application.

# 3. Is Bundle Adjustment also a linear problem ? 

No its not
