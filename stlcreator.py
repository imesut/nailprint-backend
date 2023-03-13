import numpy as np
from stl import mesh

width = 16 #mm

def calcBorderOfTemplate(a, b, c):
    vertices = np.array([[0, yVal(0, a, b, c), +1], [0, yVal(0, a, b, c), -1]])
    for x in range(1,5):
        x = x*2
        y = yVal(x, a, b, c)
        vertices = np.append(vertices, [[x, y, +1], [-x,y,+1], [x, y, -1], [-x,y,-1]], axis=0)
    
    faces = np.array([
        [0,1,2],
        [0,1,3],
        [1,2,4],
        [1,3,5],
        [4,6,8],
        [5,7,9],
        [8,6,10],
        [7,9,11],
        [8,10,12],
        [9,11,13],
        [10,12,14],
        [11,13,15],
        [12,14,16],
        [13,15,17]
        ])
                 
    # Create the mesh
    surface = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            surface.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    surface.save('surface.stl')

def yVal(x,a,b,c):
    return a*x**2 + b*x + c
    
calcBorderOfTemplate(2,-5,0)
