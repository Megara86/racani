import math
import sys

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

camera_position = np.array([0.0, 0.0, 10.0])  # Example camera position
target = np.array([0.0, 0.0, 0.0])  # Example point the camera is looking at
up_vector = np.array([0.0, 1.0, 0.0])  # Example up vector
X_rot = -30
Y_rot = 0
Z_rot = 0
sve_tangente = []
svi_kutevi_orijentacije = []
sve_osi_orijentacije = []
svi_periodicki_segmenti = []
vertices = []
faces = []
start_orientation = np.array([0.0, 0.0, 1.0])
norm_s = np.linalg.norm(start_orientation)
norm_e = 0  # You should define the value for norm_e

B = np.array([[-1, 3, -3, 1],
              [3, -6, 3, 0],
              [-3, 0, 3, 0],
              [1, 4, 1, 0]])

B_derv = np.array([[-1, 3, -3, 1],
                   [2, -4, 2, 0],
                   [-1, 0, 1, 0]])

spirala = [[0, 0, 0],
           [0, 10, 5],
           [10, 10, 10],
           [10, 0, 15],
           [0, 0, 20],
           [0, 10, 25],
           [10, 10, 30],
           [10, 0, 35],
           [0, 0, 40],
           [0, 10, 45],
           [10, 10, 50],
           [10, 0, 55]]


def load_object():
    with open("porsche.obj", "r") as obj_file:
        for line in obj_file:
            if line.startswith("v "):
                parts = line.split()
                vertex_indices = [float(part) for part in parts[1:4]]
                vertices.append(vertex_indices)
            elif line.startswith("f "):
                parts = line.split()
                vertex_indices = [int(part.split('/')[0]) for part in parts[1:4]]
                faces.append(vertex_indices)


def tangenta(t, R):
    T = [t ** 2, t, 1]
    p = (1 / 2.0) * np.matmul(np.matmul(T, B_derv), R)
    return p


def rotacija(e):
    os_rotacije = (np.cross(start_orientation, e))
    os_rotacije_norm = np.linalg.norm(os_rotacije)
    norm_e = np.linalg.norm(e)
    kut_rotacije = math.acos(os_rotacije_norm / (norm_s * norm_e)) * 180 / math.pi
    return os_rotacije, kut_rotacije

load_object()

for i in range(len(spirala) - 3):
    r1 = spirala[i]
    r2 = spirala[i + 1]
    r3 = spirala[i + 2]
    r4 = spirala[i + 3]
    R = [r1, r2, r3, r4]
    for t_not_nomr in range(0, 101, 1):
        t = t_not_nomr / 100.0
        tang = tangenta(t, R)
        sve_tangente.append(tang)
        os_orijentacije, kut_orijentacije = rotacija(tang)
        sve_osi_orijentacije.append(os_orijentacije)
        svi_kutevi_orijentacije.append(kut_orijentacije)

        periodicki_segment = (1 / 6) * np.dot(np.dot([t ** 3, t ** 2, t, 1], B), R)
        svi_periodicki_segmenti.append(periodicki_segment)

i = 0  # Initialize i to 0
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Set up the view using gluLookAt
    gluLookAt(
        camera_position[0], camera_position[1], camera_position[2],
        target[0], target[1], target[2],
        up_vector[0], up_vector[1], up_vector[2]
    )
    glScale(2,2,2)
    glBegin(GL_LINE_STRIP)
    for point in svi_periodicki_segmenti:
        glColor3f(1.0, 1.0, 1.0)  # Set the color for the B-spline curve
        glVertex3f(point[0] / 20, point[1] / 20, point[2] / 20)
    glEnd()

    glBegin(GL_LINES)
    start = svi_periodicki_segmenti[i]
    end = np.add(start, sve_tangente[i])
    glVertex3f(start[0] / 20, start[1] / 20, start[2] / 20)
    glVertex3f(end[0] / 20, end[1] / 20, end[2] / 20)
    glEnd()

    glTranslatef(svi_periodicki_segmenti[i][0]/20, svi_periodicki_segmenti[i][1]/20, svi_periodicki_segmenti[i][2]/20)
    glRotatef(svi_kutevi_orijentacije[i], sve_osi_orijentacije[i][0], sve_osi_orijentacije[i][1],
              sve_osi_orijentacije[i][2])
    glScale(0.5,0.5,0.5)

    # Render the tetrahedron
    glBegin(GL_TRIANGLES)
    for face in faces:
        glColor3f(0.0, 0.0, 1.0)  # Set the color for the tetrahedron
        for vertex_index in face:
            vertex = vertices[vertex_index - 1]
            glVertex3f(vertex[0], vertex[1], vertex[2])
    glEnd()
    glutSwapBuffers()

def reshape(width, height):
    glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, (width / height), 0.1, 100.0)
    glTranslatef(0, 1, -4)

    glRotatef(-30, 1, 0, 0)
    glRotatef(0, 0, 1, 0)
    glRotatef(0, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def idle():
    global i
    if i < len(sve_tangente) - 1:
        i += 1
    else:
        # Animation has reached the end, you can loop it if needed
        i = 0
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowPosition(100, 100)
glutInitWindowSize(500, 500)
glutCreateWindow("Prva vjezba")

glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutIdleFunc(idle)

# Add the reshape function

glutMainLoop()
