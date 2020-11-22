import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from obj import *

def loadTexture(path):
    #Cargo la imagen a memoria. pygame se hace cargo de decodificarla correctamente
    surf = pygame.image.load(path)
    #Obtengo la matriz de colores de la imagen en forma de un array binario
    #Le indico el formato en que quiero almacenar los datos (RGBA) y que invierta la matriz, para poder usarla correctamente con OpenGL
    image = pygame.image.tostring(surf, 'RGBA', 1)
    #Obentego las dimensiones de la imagen
    ix, iy = surf.get_rect().size
    #Creo una textura vacia en memoria de video, y me quedo con el identificador (texid) para poder referenciarla
    texid = glGenTextures(1)
    #Activo esta nueva textura para poder cargarle informacion
    glBindTexture(GL_TEXTURE_2D, texid)
    #Seteo los tipos de filtro a usar para agrandar y achivar la textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #Cargo la matriz de colores dentro de la textura
    #Los parametros que le paso son:
    # - Tipo de textura, en este caso GL_TEXTURE_2D
    # - Nivel de mipmap, en este caso 0 porque no estoy usando mas niveles
    # - Formato en que quiero almacenar los datos en memoria de video, GL_RGB en este caso, porque no necesito canal Alfa
    # - Ancho de la textura
    # - Alto de la textura
    # - Grosor en pixels del borde, en este caso 0 porque no quiero agregar borde a al imagen
    # - Formato de los datos de la imagen, en este caso GL_RGBA que es como lo leimos con pygame.image
    # - Formato de los canales de color, GL_UNSIGNED_BYTE quiere decir que son 8bits para cada canal
    # - La imagen, en este caso la matriz de colores que creamos con pygame.image.tostring
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    #Una vez que tengo todo cargado, desactivo la textura para evitar que se dibuje por error mas adelante
    #Cada vez que quiera usarla, puedo hacer glBindTexture con el identificador (texid) que me guarde al crearla
    glBindTexture(GL_TEXTURE_2D, 0)
    #devuelvo el identificador de la textura para que pueda ser usada mas adelante
    return texid

def main():
    pygame.init()
    display = (1200,1200)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #Creo un programa de shading y guardo la referencia en la variable gouraud
#    gouraud = createShader("./shaders/gouraud_vs.hlsl", "./shaders/gouraud_fs.hlsl")
    
    modelAnimation = []

    rangeAn = 6

    for i in range(rangeAn):
        modelAn = Obj("model ani #" + str(i))
        path = "./knight_animado/knight_run_"+str(i)+".obj"
        print(path)
        modelAn.parse(path)
        modelAnimation.append(modelAn)

    smallIndex = 0
    index = 0

    #Activo el manejo de texturas
    glEnable(GL_TEXTURE_2D)
    #Activo la textura 0 (hay 8 disponibles)
    glActiveTexture(GL_TEXTURE0)
    #Llamo a la funcion que levanta la textura a memoria de video
    text = loadTexture("./knight_good.png")

    #Para el shader, me guardo una referencia a la variable que representa a la textura
#    unifTextura = glGetUniformLocation(gouraud, 'textura')

    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,display[0],display[1])
    glFrustum(-1,1,-1,1,1,1000)

    ang = 0.0
    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
#    light = False
    end = False

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode( GL_FRONT_AND_BACK, mode)
                if event.key == pygame.K_z:
                    zBuffer = not zBuffer
                    if(zBuffer):
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)
                if event.key == pygame.K_b:
                    bfc = not bfc
                    if(bfc):
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)
                if event.key == pygame.K_c:
                    bfcCW = not bfcCW
                    if(bfcCW):
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)
                elif event.key == pygame.K_ESCAPE:
                    end = True
                    
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0,0.0,-50)
        glRotatef(250, 0, 1, 0)
        glRotatef(0, 0, 0, 1)
        glRotatef(270, 1, 0, 0)
#        ang = 0.5
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        smallIndex += 1
        if(smallIndex == 5):
            index += 1
            smallIndex = 0
        
        if(index == rangeAn):
            index = 0

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        #Habilito el array de coordenadas de textura
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, modelAnimation[index].drawV)
        glNormalPointer(GL_FLOAT, 0, modelAnimation[index].drawN)
        glTexCoordPointer(2, GL_FLOAT, 0, modelAnimation[index].drawT)

        #Cargo la textura "text" en la posicion activa (que es la 0 en este ejemplo)
        glBindTexture(GL_TEXTURE_2D, text)

        glDrawArrays(GL_TRIANGLES, 0, len(modelAnimation[index].faces))

        #Luego de dibujar, desactivo la textura
        glBindTexture(GL_TEXTURE_2D, 0)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()
    
    #Cuando salgo del loop, antes de cerrar el programa libero todos los recursos creados
    glDeleteTextures([text])
    pygame.quit()
    quit()

main()