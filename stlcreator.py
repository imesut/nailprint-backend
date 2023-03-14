import numpy as np
from stl import mesh
import pyvista as pv

# Constants
WIDTH = 16 #mm
LENGTH = 20

def generateMeshForNailShape(a, b, c):
    vertices = np.array([[0, yValForPntX(0, a, b, c), +1],
                         [0, yValForPntX(0, a, b, c), -1]])
    
    # iterate for 4 right, and 4 left nodes, each standing for 0.2 mm
    for x in range(1,5):
        x = x*2
        y = yValForPntX(x, a, b, c)
        vertices = np.append(vertices, [[+x, y, +1],
                                        [-x, y, +1],
                                        [+x, y, -1],
                                        [-x, y, -1]], axis=0)
        
    #Adding height vertices.
    vertices = np.append(vertices, [
        [-8, LENGTH, +1], # Top-Left      n:18
        [+8, LENGTH, +1], # Top-Right     n:19
        [+8, LENGTH, -1], # Bottom-Right  n:20
        [-8, LENGTH, -1]  # Bottom-Left   n:21
        ], axis=0)
        
    faces = np.array([
        [0,1,2],
        [0,1,3],
        [1,2,4],
        [2,4,6], # missed surface
        [1,3,5],
        [3,5,7], # missed surface
        [4,6,8],
        [5,7,9],
        [8,6,10],
        [7,9,11],
        [8,10,12],
        [9,11,13],
        [10,12,14],
        [11,13,15],
        [12,14,16],
        [13,15,17],
        [19,14,16], # Right side
        [19,20,16], # Right side
        [18,21,17], # Left side
        [18,15,17], # Left side
        [18,21,20], # Back side
        [18,19,20] # Back side
        ])
    
    # Creating faces for bottom and top geometry
    topNodes = [15,11,7,3,0,2,6,10,14,19]
    bottomNodes = [17,13,9,5,1,4,8,12,16,20]
    
    # Knit faces
    for i in range(len(topNodes)-1): #topNodes = bottomNodes
        faces = np.append(faces, [
            [18, topNodes[i], topNodes[i+1]],
            [21, bottomNodes[i], bottomNodes[i+1]]
            ], axis=0)
                 
    # Create the mesh
    surface = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            surface.vectors[i][j] = vertices[f[j],:]

    surface.save("diff.stl")

# Y values for the point x based on the polynomic curve
def yValForPntX(x,a,b,c):
    return a*x**2 + b*x + c

def combineMeshes(basefile, a, b, c):
    generateMeshForNailShape(a, b, c)
    baseFile = pv.read(basefile)
    partToDiff = pv.read("diff.stl")
    return baseFile.boolean_difference(partToDiff)

def generateCustomizedSTL(a, b, c):
    data = combineMeshes("nail_polisher.stl", a, b, c)
    data.save("data.stl")

# Run for the sample curve 
generateMeshForNailShape(0.25,-1,0)

generateCustomizedSTL(0.25, -1, 0)