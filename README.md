# MicroEvoBrain:

## DESCRIPCION:

Este proyecto es un simulador evolutivo para competencia de algoritmos de
inteligencia artificial, el simulador fue hecho en Game Maker Studio, se
incluye el codigo fuente en la carpeta **"MicroEvo.gmx"**, todos estos archivos
van incluidos tambien en el ejecutable **"MicroEvoBrain.exe"**.

Consta de un mundo virtual 2D con alimento generado al azar, se pueden poner
muros para complejizar la navegacion, se pueden seleccionar de 1 a 5 especies
de agentes, diferenciados por color, es decir que cada uno puede tener su propio
algoritmo de inteligencia artificial.

Un agente requiere energia para funcionar y reproducirse, tiene un contador de
puntos que hacen las veces de fitness, tiene 23 entradas o sensores del medio y
6 salidas o acciones (caminar, rotar, disparar, donar energia, fecundar huevo,
gritar); las entradas son de tipo: olor, tacto, oido, vision, rayo de contacto,
energia de otros y propia, percepcion del tiempo y proximidad a huevo.

El software de simulacion puede funcionar por si solo, aunque limitadamente,
consta de un algoritmo experto basico, una red neuronal evolutiva MLP, un modo
manual para controlar al agente, y el modo UDP que es la estrella del asunto.

Resumiendo, el UDP conecta al software de Game Maker con el codigo Python que
administra los algoritmos de inteligencia artificial externos, este administrador
figura como **"MicroEvoAdmin.py"**, basicamente GMS envia las entradas del agente, los
algoritmos externos procesan y envian de vuelta a travez del administrador, las
salidas que llegan al respectivo agente.

## ARCHIVOS:

**"MicroEvo.gmx"**:

codigo fuente del simulador hecho en Game Maker Studio.

**"cerebroNeurotico.py"**:

libreria creada para proposito general, donde se requiera usar redes neuronales
MLP (multi layer perceptron) y DMNN (dendral morphologycal neural network), estas
son totalmente configurables, exportables y graficables en 2D, no tiene aun
algoritmos de gradiente descendente para su uso, en cambio usan mutacion y
recombinacion genetica, puediendo aumentar o disminuir el numero de unidades
logicas durante el entreno (neuronas/capas, dendritas); en parte esto es porque
se pretende comparar estas dos arquitecturas de redes neuronales en iguales
condiciones, y para problemas no supervizados (sin patrones ademas).

**"MicroEvoAdmin.py"**:

administrador de IAs para **"MicroEvoBrain.exe"** u otro software que cumpla con la
comunicacion UDP, estando dentro de la ejecucion de este archivo Python, lance
el comando "ayuda" para obtener todos los comandos, encontrara alli informacion
acerca del codigo, descripcion de comandos, controles del software simulador, etc.

**"brainDMNN1.py"**, **"brainDMNN2.py"**, **"brainMLP1.py"**, **"brainMLP2.py"**:

son ejemplos de algoritmo IA para ser manejados por el administrador, estos tienen
en comun que usan a la libreria **"cerebroNeurotico.py"** aqui contenida.

**"brainOmi1.py"**:

otro ejemplo de algoritmo IA para ser manejado por el administrador, es el mismo
algoritmo que internamente tiene el codigo hecho en Game Maker y el cual fue
mencionado como algoritmo experto basico.

**"templateAI.py"**:

este documento en blanco, es la base para crear su propia IA, siguiendo las reglas
ahi escritas, y el protocolo, esto garantizara que se pueda conectar adecuadamente
a simulador, el documento contiene toda la informacion concerniente a las entradas
y salidas del agente.

**"testRedes.py"**:

este codigo es una prueba en bruto de la libreria **"cerebroNeurotico.py"**, aqui se
pueden importar problemas de clasificacion en txt, para ser testeados, tambien
tiene unos ejemplos internos, como compuertas o puntos con ruido escogidos a dedo,
este software para clasificacion utiliza la mayoria de funciones evolutivas de
la libreria, demostrando los alcances de ambos tipos de redes y la viabilidad de
solucionar problemas estocasticamente.

**"mlp_ejemplote.png"**, **"dmnn_ejemplote.png"**:

dos imagenes resultado del codigo **"testRedes.py"**, donde se ve como es la
superficie de decicion de ambos tipos de redes, para un problema 2D pero con forma
geometrica exigente, este problema por defecto viene en el codigo mencionado, solo
ejecute el codigo y digite el comando **"demo"**.

**"ejemplito.txt"**, **"espiral2.txt"**, **"glass.txt"**, **"iris.txt"**:

datasets para usar con **"testRedes.py"**, iris y glass son clasicas y pertenecientes
a problemas reales, ejeplito y espiral2 son sinteticas y 2D, creadas para exigir
al maximo a las redes.

## PRUEBA:

Para el test de la libreria, ejecute **"testRedes.py"** y luego digite el comando
**"demo"**, devera verificar el funcionamiento, luego con el comando **"ayuda"** puede
asceder a todos los comandos.

Para el software de simulacion, que es la leche del asunto, ejecute
**"MicroEvoBrain.exe"** (o el editable desde GMS), vera como funciona por si solo,
luego ejecute **"MicroEvoAdmin.py"** (realmente el orden no importa), y digite
la orden **"demo"** tras lo cual devera verificar el funcionamiento en conjunto,
puede hacerlo digitando **"informacion"** y luego **"2"**; finalmente digite **"ayuda"** para
obtener todos los deliciosos comandos.

## FUNCIONAMIENTO:

La simulacion GMS hace ciclos donde sensa el medio con cada agente, ejecuta la IA
y obtiene las salidas, con las que se calcula todo, colisiones, disparos, muerte,
fitness (ver **"EvoPID.exe"** otra creacion del autor).

Cuando los personajes se reproducen asexualmente, se crea un huevo con la
informacion, que al momento de eclosionar, generara a el nuevo agente; si el huevo
es fecundado, la reproduccion podra ser sexual si el algoritmo asi lo soporta.

En el momento de resetear el mundo, se guardara a las mejores IAs, para que estas
desoben a una nueva generacion.

El administrador Python recibe diferentes ordenes, el protocolo UDP se puede leer
en el archivo **"help.rtf"** dentro de la carpeta de GMS, si no existe una clase de
IA asociada al ID del agente, una nueva es creada, si se envian datos de entrada
el administrador creara un hilo para ejecutar la IA y devolver la salida.

Los datos recibidos para ejecucion se van encolando y un hilo se encarga de
recorrer la cola, para obtener los ultimos, si no se han vencido; este hilo
tambien revisara si una IA lleva tiempo inactiva y no pertenece al grupio de las
mejores, entonces la eliminara para liberar memoria (seguramente su agente murio).

En caso de reproduccion, GMS enviara la orden, y el administrador se encargara
de buscar a las clases IA correspondientes para darles la orden de recombinacion
o mutacion; se manejan muchas sentencias try para evitar fallos provenientes de
los codigos de cada IA.

## TRABAJO FUTURO:

El softwar en GMS esta finalizado, quiza se le pueden agregar sonidos o unos
cuantos flags mas, por ejemplo para desactivar los disparos violentos, o agregar
fitness a estos.

Aun asi, tanto la simulacion GMS como el administrador Python son suficientes
por si solos, es decir, se puede crear una simulacion en Godot, que es software
libre y soporta 3D, para reemplazar a GMS, asi como por el contrario crear
un mejor administrador, con GUI por ejemplo.

Hacer en Godot un software extra, que permita a diversos jugadores humanos, ver
de manera limitada (como veria un agente), el entorno y poder actuar, para asi
comparar al cerebro humano con las redes neuronales, sin la todopoderosa habilidad
humana de ver la pantalla de simulacion al manejar manualmente; esto tambien
seria por UDP, un 3er software independiente, que incluso convierta el proyecto
en un entretenido juego (y obtener mejores patrones para entrenamiento
supervizado).

La libreria **"cerebroNeurotico.py"** (ok ni se si le puedo llamar asi), tiene dentro
una lista de trabajo futuro y mejoras.

Testear todo para buscar y corregir fallos.

## PRETENCION:

Y si retamos a nuestros colegas programadores a hacer la mejor IA? una que por
ejemplo cree un mapa interno del entorno (como en la robotica movil), se pueden
hacer competiciones, por grupos, universidades, etc, con premios jugoso incluidos.

## CREADOR:

Omwekiatl (Omar Jordan Jordan)

Colombia 2020

mail: [ojorcio@gmail.com]

devianart: [https://www.deviantart.com/omarsaurus]

dropbox: [https://www.dropbox.com/sh/plhbo1ornjah8jb/AAAOdaSe5JArLE1XRo--Eh_7a?dl=0]

Desarrollador de videojuegos indie en tiempo libre, asi como de software variado,
en el link veras mi arte, asi como otros links a mis proyectos (ver Dropbox)

Recomiendo para entender las DMNN, buscar **"SoftwareDMNN.exe"** que esta por ahi
en algun lado, fue mi trabajo de tesis, por lo que esta bien documentado (y con
tildes), y es codigo abierto.

## LICENCIA:

Software finalizado, libre y codigo abierto, puede usarse y modificarse, siempre y
cuando se conserve atribucion a su creador, *be free honey*.
