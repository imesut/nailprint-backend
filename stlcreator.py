import numpy as np
import pyvista as pv
import time

# Constants
WIDTH = 16 #mm
LENGTH = 20
HEIGHT = 4

BASEPART = pv.read("nail_polisher.stl")

def generateMeshForNailShape(a, b, c):
    vertices = np.array([[0, yValForPntX(0, a, b, c), +1*HEIGHT],
                         [0, yValForPntX(0, a, b, c), -1*HEIGHT]])
    
    # iterate for 4 right, and 4 left nodes, each standing for 0.2 mm
    for x in range(1,5):
        x = x*2
        y = yValForPntX(x, a, b, c)
        vertices = np.append(vertices, [[+x, y, +1*HEIGHT],
                                        [-x, y, +1*HEIGHT],
                                        [+x, y, -1*HEIGHT],
                                        [-x, y, -1*HEIGHT]], axis=0)
        
    #Adding height vertices.
    vertices = np.append(vertices, [
        [-8, LENGTH, +1*HEIGHT], # Top-Left      n:18
        [+8, LENGTH, +1*HEIGHT], # Top-Right     n:19
        [+8, LENGTH, -1*HEIGHT], # Bottom-Right  n:20
        [-8, LENGTH, -1*HEIGHT]  # Bottom-Left   n:21
        ], axis=0)
    
    #PYVISTA METHOD
    faces = np.hstack(
        [
        [3, 0,1,2],
        [3, 0,1,3],
        [3, 1,2,4],
        [3, 2,4,6], # missed surface
        [3, 1,3,5],
        [3, 3,5,7], # missed surface
        [3, 4,6,8],
        [3, 5,7,9],
        [3, 8,6,10],
        [3, 7,9,11],
        [3, 8,10,12],
        [3, 9,11,13],
        [3, 10,12,14],
        [3, 11,13,15],
        [3, 12,14,16],
        [3, 13,15,17],
        [3, 19,14,16], # Right side
        [3, 19,20,16], # Right side
        [3, 18,21,17], # Left side
        [3, 18,15,17], # Left side
        [3, 18,21,20], # Back side
        [3, 18,19,20] # Back side
        ]
    )
    
     # Creating faces for bottom and top geometry
    topNodes = [15,11,7,3,0,2,6,10,14,19]
    bottomNodes = [17,13,9,5,1,4,8,12,16,20]
    # Knit faces
    for i in range(len(topNodes)-1): #topNodes = bottomNodes
        faces = np.append(faces, [[3, 18, topNodes[i], topNodes[i+1]],
                                  [3, 21, bottomNodes[i], bottomNodes[i+1]]])
    
    surface = pv.PolyData(vertices, faces)
    surface.save("diff.stl")
    return surface

# Y values for the point x based on the polynomic curve
def yValForPntX(x,a,b,c):
    return a*x**2 + b*x + c

def combineMeshes(a, b, c):
    partToDiff = generateMeshForNailShape(a, b, c)
    partToDiff = partToDiff.translate((11,0,0), inplace=True)
    partToDiff = partToDiff.rotate_x(-90, point=(11, (20-1.5), 0), inplace=True)
    part = (BASEPART + partToDiff)
    return part

def generateCustomizedSTLforFinger(fileName, a, b, c):
    data = combineMeshes(a, b, c)
    data.save(fileName)
