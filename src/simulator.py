'''Simulation loop'''
import numpy as np
import matplotlib.pyplot as plt

from .trajectory_planner import *
from .mpc import *
from .util import *

def update_state(state):
    return state

def check_goal(goal):
    return False

def simulate(rx, ry, rphi, rv, speed, dl):
    '''
    inputs:
    rx: reference x
    ry: reference y
    rphi: reference phi
    rv: reference v
    speed: speed profile
    dl: tick [m]

    returns:
    t: time (list for plotting)
    x: x position
    y: y position
    phi: heading
    v: velocity
    a: acceleration
    delta: steering angle
    '''

    # initialize stuff
    DT = 0.1 # 100 ms time loop
    MAX_TIME = 500.0 # max simulation time

    calc_nearest_index()
    # smooth_yaw -> Don't do for now

    # Initialize the state
    state = vehicle_state(rx[0], ry[0], rv[0], rphi[0])
    goal = [rx[-1], ry[-1]]

    # time loop
    time = 0.0
    
    while (time <= MAX_TIME):
        # calc_ref_trajectory every time loop
        calc_ref_trajectory()
        # iterative linear mpc every time loop
        linear_mpc()
        # update state every time loop
        state = update_state(state)
        # update the lists for book-keeping

        # terminate if goal is reached (checkgoal())
        if check_goal(goal):
            break

        # increment time
        print(time)
        time += DT
    
    t, x, y, phi, v, a, delta = [], [], [], [], [], [], []
    return t, x, y, phi, v, a, delta