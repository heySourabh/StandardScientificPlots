# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 12:22:53 2021

@author: Dr. Sourabh Bhat ( https://spbhat.in )
"""

'''
Reads file in following format and plots it with appropriate legends etc.:
Title of the plot
t,   value1, value2, value3, ...
0.1, 234.9,  9824 ,   345.6, ...
-0.4, 34.0,  554.9,   58.7 , ...
...
'''

import numpy as np
import matplotlib.pyplot as plt

def linePlot(filename, useTex=True, fontFamily="serif", serifFont="Palatino", 
             sansSerifFont="DejaVu Sans", monospaceFont="Courier New",
             linewidth=3, xlabel=None, ylabel=None, showGrid = True,
             fontSize=14, figSizeInches=(10, 8), delimiter=",",
             markers = [None, 'o', 's', 'v', '^', 'x'], linestyles = ['-'],
             colors = ["black"],
             x_lim = None, y_lim = None,
             fig_dpi=300):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams['text.usetex'] = useTex
    plt.rcParams['font.family'] = fontFamily
    plt.rcParams['font.serif'] = serifFont
    plt.rcParams['font.sans-serif'] = sansSerifFont
    plt.rcParams['font.monospace'] = monospaceFont
    plt.rcParams['font.size'] = fontSize
    plt.rcParams['figure.figsize'] = figSizeInches
    
    # Read the file, ignore lines starting with '#' character
    fObj = open(filename, "r")
    title = ""
    for line in fObj:
        line = line.strip()
        if line.startswith("#"): continue
        title = line
        break
    
    headers = fObj.readline().split(delimiter)
    # strip spaces from headers
    for i in range(len(headers)):
        headers[i] = headers[i].strip()
        if headers[i] == "":
            raise Exception("Empty header text at index %d" % i)
    
    print("Title: %s" % title)
    print("Headers: %s" % str(headers))
    data = []
    for _ in headers:
        data += [[]]
    # read data
    for row in fObj:
        rowData = row.split(delimiter)
        for i in range(len(headers)):
            data[i].append(float(rowData[i]))
    fObj.close()
    
    data = np.array(data)
    min_x = np.min(data[0])
    max_x = np.max(data[0])
    min_y = np.min(data[1:])
    max_y = np.max(data[1:])
    
    range_y = np.max([max_y - min_y, 1e-12])
    number_of_markers = 20
    
    for p in range(1, len(headers)):
        plt.plot(data[0], data[p], lw=linewidth, label=headers[p], 
                 marker=markers[(p-1) % len(markers)], 
                 color=colors[(p-1) % len(colors)], 
                 linestyle=linestyles[(p-1) % len(linestyles)],
                 markevery=len(data[0]) // number_of_markers, markersize=10)
    
    if len(headers) > 2:
        plt.legend(loc="best", fontsize=fontSize * 1.2)
    if xlabel == None:
        xlabel = headers[0]
    if ylabel == None and len(headers) == 2:
        ylabel = headers[1]
    if ylabel == None:
        ylabel = ""
    plt.xlabel(xlabel, fontsize=fontSize * 1.2)
    plt.ylabel(ylabel, fontsize=fontSize * 1.2)
    
    if x_lim == None:
        plt.xlim(min_x, max_x)
    else:
        plt.xlim(x_lim[0], x_lim[1])
    
    if y_lim == None:
        plt.ylim(min_y - 0.1 * range_y, max_y + 0.1 * range_y)
    else:
        plt.ylim(y_lim[0], y_lim[1])
    
    plt.title(title)
    if showGrid: plt.grid(linestyle="dashed")
    
    plt.show()
    
    savefigName = filename  #[:filename.rindex(".")]
    plt.savefig(savefigName + ".png", dpi=fig_dpi, bbox_inches=0)
    plt.savefig(savefigName + ".svg", dpi=fig_dpi, bbox_inches=0)

def test():
    # test data
    title = r"$\displaystyle\int $Test Title$\ dx$"
    headers = [r"$x$", r"$\sqrt{x}$", r"$\cos (x)$"]
    x = np.linspace(0, 10, 500)
    x_root = np.sqrt(x)
    cos_x = np.cos(x)
    filename = "test_data.dat"
    fObj = open(filename, "w")
    fObj.write(title + "\n")
    for i in range(len(headers)):
        h = headers[i]
        fObj.write(h)
        if i != len(headers) - 1: 
            fObj.write(", ")
        else:
            fObj.write("\n")
    
    for (xd, x_rootd, cos_xd) in zip(x, x_root, cos_x):
        fObj.write("%f, %f, %f\n" % (xd, x_rootd, cos_xd))
        
    fObj.close()
    
    linePlot(filename)


if __name__ == "__main__":
    test()
    


    