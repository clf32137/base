import numpy as np

def generate_edges(n):
    if n == 1:
        return {'vertices': np.array([[0], [1]]), 'edges':np.array([ [[0], [1]] ]) }
    else:
        previous = generate_edges(n-1)
        vertices = []
        edges = []
        for i in previous['vertices']:
            vertices.append(np.insert(i, n-1, 0))
            vertices.append(np.insert(i, n-1, 1))
            edges.append( np.array( [np.insert(i, n-1, 0),  np.insert(i, n-1, 1) ]  ) )
        for i in previous['edges']: #Loop through edges
            pt0 = np.insert(i[0], n-1 , 0)
            pt1 = np.insert(i[1], n-1 , 0)
            edges.append(np.array([ pt0, pt1 ]))
            pt0 = np.insert(i[0], n-1 , 1)
            pt1 = np.insert(i[1], n-1 , 1)
            edges.append(np.array([ pt0, pt1 ] ))
        return {'vertices' : vertices, 'edges' : edges}

def is_inside(r,pt):
    for i in np.dot(np.transpose(r),pt):
        if i < -1e-4 or 1.00001 < i:
            return False
    return True

def is_inside_teserract(r,pt):
    for i in np.dot(np.transpose(r),pt):
        if i[0] < -1e-4 or 1.00001 < i[0]:
            return False
    return True

def hash_edge(e):
    res = 0
    for i in range(len(e)):
        if np.abs(e[i]) > 0.5:
            res = res + 2**i
    return res

def rotation_matrix(theta,phi,alp,beta,gamma,delta):
    r1 = np.array(
    [
        [np.cos(theta), -np.sin(theta),0,0],
        [np.sin(theta), np.cos(theta),0,0],
        [0,0,1.0,0],
        [0,0,0,1.0]
    ])
    r2 = np.array(
    [
        [1.0,0,0,0],
        [0, np.cos(phi), -np.sin(phi),0],
        [0,np.sin(phi), np.cos(phi),0],
        [0,0,0,1.0]
    ])
    r3 = np.array(
    [
        [np.cos(alp), 0, -np.sin(alp), 0],
        [0, 1.0, 0, 0],
        [np.sin(alp), 0, np.cos(alp), 0],
        [0, 0, 0, 1.0]
    ])
    r4 = np.array(
    [
        [np.cos(beta), 0, 0, -np.sin(beta)],
        [0, 1.0, 0, 0],
        [0, 0, 1.0, 0],
        [np.sin(beta), 0, 0, np.cos(beta)]
    ])
    r5 = np.array(
    [
        [1.0,0,0,0],
        [0, np.cos(gamma), 0, -np.sin(gamma)],
        [0, 0, 1.0, 0],
        [0, np.sin(gamma), 0, np.cos(gamma)]
    ])
    r6 = np.array(
    [
        [1.0,0,0,0],
        [0, 1.0, 0, 0],
        [0, 0, np.cos(delta), -np.sin(delta)],
        [0, 0, np.sin(delta), np.cos(delta)]
    ])
    return np.array([r1,r2,r3,r4,r5,r6])

def rotation_matrix_ind(j):
    theta = j/100.0 * np.pi*2
    phi = j/100.0 * np.pi*2
    alp = j/100.0 * np.pi*2
    beta = (j/100.0) * np.pi*2
    gamma = (j/100.0) * np.pi*2
    delta = (j/100.0) * np.pi*2
    [r1,r2,r3,r4,r5,r6] = rotation_matrix(theta,phi,alp,beta,gamma,delta)
    return np.dot(r6,np.dot(r5,np.dot(r4,np.dot(r3,np.dot(r1,r2)))))


