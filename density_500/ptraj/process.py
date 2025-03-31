#!/usr/bin/env python

import numpy as np
import string
import sys
import os

def getdipole(dpfile):
    arr = np.loadtxt(dpfile, usecols=(1,2,3,4,5,6))
    arr = np.split(arr, 2, 1)
    arr = np.swapaxes(arr, 0, 1)
    return arr

def gen_catarr():
    com = np.loadtxt('COM.dat', usecols=(1,2,3))

    frames = com.shape[0]
    molecules = max([int(s[6:].split('.')[0]) for s in os.listdir('dipoles')])+1

    data = np.zeros((molecules,frames,2,3))
    for molecule in range(molecules):
        data[molecule] = getdipole('dipoles/dipole{0}.dat'.format(str(molecule)))
    data = np.swapaxes(data, 0, 1) #shape: (frames,molecules,2,3)

    #subtract center of mass of the aerosol from each pos of water to get relative pos
    comsubarr = np.repeat(com,molecules,0)
    comsubarr = np.split(comsubarr, frames, 0)
    comsubarr = np.insert(comsubarr, [0, 0, 0], 0, 2)
    comsubarr = np.reshape(comsubarr, (frames, molecules, 2, 3))
    data = np.subtract(data, comsubarr)

    #normalizing constants for each molecule for each frame. shape: (frames, molecules)
    normc = np.prod(np.sqrt(np.sum(np.multiply(data,data),3)),2)
    #raw dot product for each molecule for each frame. shape: (frames, molecules)
    dotp = np.sum(np.prod(data,2),2)
    #cos(theta)
    cost = np.divide(dotp,normc)

    positions = np.delete(data,0,2) #shape: (frames, molecules, 1, 3)
    distances = np.sqrt(np.sum(np.multiply(positions,positions),3)) #shape: (frames, molecules)
    return np.concatenate((distances, np.resize(cost,(frames,molecules,1))),2)

def main():
    if (len(sys.argv)>1):
        print("Loading")
        catarr = np.load(sys.argv[1], allow_pickle=True)
    else:
        catarr = gen_catarr()
        catarr.dump('distcost.pkl')
    frames = catarr.shape[0]
    molecules = catarr.shape[1]

    bins = 30
    maxd = 24.0
    interval = maxd/bins

    data = np.zeros((frames,bins,2))
    for i, frame in enumerate(catarr):
        bin = np.minimum(bins-1,frame[:,0]//interval).astype(int)
        data[i,:,0] += np.arange(bins)*interval
        for e in range(frame.shape[0]):
            data[i,bin[e],1] += frame[e,1]

    hist = np.zeros((bins,2))
    hist[:,0] += data[0,:,0]
    for i, frame in enumerate(data):
        hist[:,1] += frame[:,1]/frames

    with open('output.csv', 'w') as outfile:
        for line in hist:
            outfile.write(str(line[0]) + ', ' + str(line[1]) +'\n')
    breakpoint()

def save_anim(data):
    import matplotlib.pyplot as plt
    fig = plt.figure(dpi=94, figsize=(10,10))
    ax = plt.subplot()
    print(np.amax(data[:,:,1]))
    plot = ax.plot(data[0,:,0], data[0,:,1], animated=True)[0]
    ax.set_ylim([-2,2])
    ax.set_xlim([0,20])
    fig.tight_layout()
    bg = fig.canvas.copy_from_bbox(fig.bbox)
    ax.draw_artist(plot)
    fig.canvas.blit(fig.bbox)

    for i, frame in enumerate(data):
        plot.set_data((frame[:,0],frame[:,1]))
        ax.draw_artist(plot)
        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()
        s = f"{round(i):03d}"
        fig.savefig('anim/'+s+'.png')
        print(i)

if __name__ == "__main__":
    main()
