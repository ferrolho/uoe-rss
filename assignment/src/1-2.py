#!/usr/bin/python3

from sympy import *
import math
import numpy as np

q_1 = Symbol('q_1')
q_2 = Symbol('q_2')
q_3 = Symbol('q_3')
q_4 = Symbol('q_4')

fvars = symbols('q_1, q_2, q_3, q_4')

q = [0.66,
	-0.44,
	 1.06,
	 1.33]

T_b_L1 = Matrix([
	[ cos(q_1), -sin(q_1), 0, 0],
	[ sin(q_1),  cos(q_1), 0, 0],
	[        0,         0, 1, 0.16],
	[        0,         0, 0, 1]])

T_L1_L2 = Matrix([
	[  cos(q_2), 0, sin(q_2), 0],
	[         0, 1,        0, 0],
	[ -sin(q_2), 0, cos(q_2), 0.15],
	[         0, 0,        0, 1]])

T_L2_L3 = Matrix([
	[  cos(q_3), 0, sin(q_3), 0],
	[         0, 1,        0, 0],
	[ -sin(q_3), 0, cos(q_3), 0.2],
	[         0, 0,        0, 1]])

T_L3_L4 = Matrix([
	[  cos(q_4), 0, sin(q_4), 0],
	[         0, 1,        0, 0],
	[ -sin(q_4), 0, cos(q_4), 0.15],
	[         0, 0,        0, 1]])

T_L4_g = Matrix([
	[ 1, 0, 0, 0],
	[ 0, 1, 0, 0],
	[ 0, 0, 1, 0.35],
	[ 0, 0, 0, 1]])

T_b_g = T_b_L1 * T_L1_L2 * T_L2_L3 * T_L3_L4 * T_L4_g

# - - - - - - - - - - - - - - - - -

dx_dq_1 = T_b_g[0].diff(q_1)
dx_dq_2 = T_b_g[0].diff(q_2)
dx_dq_3 = T_b_g[0].diff(q_3)
dx_dq_4 = T_b_g[0].diff(q_4)

dy_dq_1 = T_b_g[1].diff(q_1)
dy_dq_2 = T_b_g[1].diff(q_2)
dy_dq_3 = T_b_g[1].diff(q_3)
dy_dq_4 = T_b_g[1].diff(q_4)

dz_dq_1 = T_b_g[2].diff(q_1)
dz_dq_2 = T_b_g[2].diff(q_2)
dz_dq_3 = T_b_g[2].diff(q_3)
dz_dq_4 = T_b_g[2].diff(q_4)

jacobian = Matrix([
	[dx_dq_1, dx_dq_2, dx_dq_3, dx_dq_4],
	[dy_dq_1, dy_dq_2, dy_dq_3, dy_dq_4],
	[dz_dq_1, dz_dq_2, dz_dq_3, dz_dq_4]])

res = jacobian.evalf(subs = dict(zip(fvars, q)))

pprint(simplify(jacobian))

print('\n\n')

pprint(res)
