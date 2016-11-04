#!/usr/bin/python3

import numpy as np

q = [0,
	 0.66,
	-0.44,
	 1.06,
	 1.33]

T_b_L1 = np.matrix([
	[ np.cos(q[1]), -np.sin(q[1]), 0, 0],
	[ np.sin(q[1]),  np.cos(q[1]), 0, 0],
	[            0,             0, 1, 0.16],
	[            0,             0, 0, 1]])

T_L1_L2 = np.matrix([
	[  np.cos(q[2]), 0, np.sin(q[2]), 0],
	[             0, 1,            0, 0],
	[ -np.sin(q[2]), 0, np.cos(q[2]), 0.15],
	[             0, 0,            0, 1]])

T_L2_L3 = np.matrix([
	[  np.cos(q[3]), 0, np.sin(q[3]), 0],
	[             0, 1,            0, 0],
	[ -np.sin(q[3]), 0, np.cos(q[3]), 0.2],
	[             0, 0,            0, 1]])

T_L3_L4 = np.matrix([
	[  np.cos(q[4]), 0, np.sin(q[4]), 0],
	[             0, 1,            0, 0],
	[ -np.sin(q[4]), 0, np.cos(q[4]), 0.15],
	[             0, 0,            0, 1]])

T_L4_g = np.matrix([
	[ 1, 0, 0, 0],
	[ 0, 1, 0, 0],
	[ 0, 0, 1, 0.35],
	[ 0, 0, 0, 1]])

T_b_L2 = np.dot(T_b_L1, T_L1_L2)
T_b_L3 = np.dot(T_b_L2, T_L2_L3)
T_b_L4 = np.dot(T_b_L3, T_L3_L4)
T_b_g  = np.dot(T_b_L4, T_L4_g)

print(T_b_g)

#
# Output:
#
# [[-0.29243998 -0.61311685  0.73387096  0.25840905]
#  [-0.22696411  0.78999223  0.56956086  0.20055253]
#  [-0.92895972  0.         -0.37018083  0.48346881]
#  [ 0.          0.          0.          1.        ]]
#
