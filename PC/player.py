#!/usr/bin/env python2
# This Python file uses the following encoding: utf-8

import serial
import sys
import time
import operator


# TODO :
# - utiliser des rationnels

""" 
Définition : 
- rgb255 : rgb ou r, g, b sont dans [|0, 255|]
- rgb127 : idem, dans [|0, 127|]
- tsv : teinte val. sat. avec t \in [0, 360[, v, s \in [0, 1]

Déroulement général :
On convertit les données lues dans le fichier (rgb255) en tsv
Ensuite, on calcule les couleurs de l'animation (fondus, etc) en tsv
Puis,  pour les envoyer, on reconvertit en rgb127
"""

# Paramètres
red_coeff = 1.0
green_coeff = 1.0
blue_coeff = 1.0


first_led_index = 0

serial_port = '/dev/ttyACM0'
#serial_port = '/dev/ttyUSB0'
#serial_port = '/dev/ttyS0'


# TODO : il faudrait éviter les vars globales
ser = None

# Adapte les couleurs théoriques via des coefficients de correction,
# pour s'adapter au rendu des couleurs par les leds
# Les couleurs sont en rgb127
def get_corrected_color(r, g, b):
  # TODO : coeffs
  return [int(r * red_coeff), 
          int(g * green_coeff), 
          int(b * blue_coeff)]


# Envoie la couleur <(r, g, b)> (de type rgb127), en la corrigeant, à la led <id>
def send_color(id, (r, g, b)):
    data = [0x80 + id] # Header
    data.extend(get_corrected_color(r, g, b))
    print data
    for i in data:
        ser.flushInput()
        ser.write(chr(i))
        time.sleep(0.01)
        None
    # TODO : time.sleep(0.01) ?

    

# Envoie une frame (= liste de rgb127), en corrigeant les couleurs au passage
def send_frame(frame):
    for (col, i) in zip(frame, range(first_led_index, 
                                     len(frame) + first_led_index)):
        send_color(i, tsv_to_rgb127(*col))


def rgb255_to_tsv(r, g, b):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    ma = max(r, g, b)
    mi = min(r, g, b)
    
    if ma == mi:
        t = 0.0
    elif ma == r:
        t = (60 * (g - b) / ma - mi + 360) % 360 
    elif ma == g:
        t = (60 * (b - r) / ma - mi + 120)
    elif ma == b:
        t = (60 * (r - g) / ma - mi + 240)

    if ma == 0.0:
        s = 0.0
    else:
        s = 1 - mi / ma

    v = ma

    return (t, s, v)

def tsv_to_rgb127(t, s, v):
    qd = int(t / 60) % 6
    f = t / 60 - qd
    l = v * (1 - s)
    m = v * (1 - f * s)
    n = v * (1 - (1 - f) * s)

    # Pas de switch/case en python : utilisons donc un dictionnaire
    answer = {
        0 : (v, n, l),
        1 : (m, v, l),
        2 : (l, v, n),
        3 : (l, m, v),
        4 : (n, l, v),
        5 : (v, l, m),
        }
    
    # TODO : on pourrait adapter pour mettre le max en paramètre, si besoin
    return tuple(map(lambda x : int(x * 127), answer[qd]))


# Convertit une frame complète, pas juste une couleur
def frame_rgb255_to_tsv(frame):
    return map(lambda x : rgb255_to_tsv(*x), frame)


# "Joue" une image et son fondu, l'image d'arrivée étant *exclue*
# Version quick and dirty : on calcule le fondu itérativement, juste avant
# de l'envoyer. Une version plus propre devrait précalculer tous les fondus
# au moment du chargement, pour stocker les animations "etendues"
# Les frames sont données au format courant (ie (couleurs, blend_time, blend_frames))
def play_blend((frame, blend_time, additional_frames), (next_frame, x, y)):
    total_frames = additional_frames + 1
    frame_time = float(blend_time) / total_frames


    # Liste des increments
    incr_list = [tuple((n - c)/float(total_frames) for n,c in zip(nex, cur)) 
                 for nex, cur in zip(next_frame, frame)]


    cur_frame = frame
    for i in range(0, total_frames): # Normalement, il y a bien <total_frames> élements dans le range
        begin_time = time.time() # On utilise pas clock() car on dépend du hardware

        send_frame(cur_frame)

        # Ajoute les valeurs d'incrément à la frame courante
        cur_frame = map(lambda (x,y) : map(operator.add, x, y), zip(cur_frame, incr_list))
        
        # TODO : sleep
        delta_t = time.time() - begin_time
        time.sleep(max(0, frame_time / 1000.0 - delta_t))

    return incr_list


# Charge une animation depuis un fichier .lna
# Retourne les valeurs (dictionnaire) ainsi que le numéro de la dernière frame
def load_animation_file(path):
    f = open(path, 'r')
    
    # Pour l'instant, on n'utilise pas la ligne de format
    f.readline()

    frame = 0

    values = {}
    
    for line in f:
        frame += 1
        # FIXME : attention, on fait un simple eval... Pas tres robuste...
        (colors, blendTime, blendFrames) = eval(line)
        # Conversion
        values[frame] = (frame_rgb255_to_tsv(colors), blendTime, blendFrames)
        

    f.close()

    return (values, frame)



# Charge un fichier de playlist
# Le format est simple : un nom de fichier .lna par ligne,
# les doublons étant acceptés
# Une ligne commençant par # (sans espace avant) est ignorée
def load_playlist_file(play_path):
    f = open(play_path, 'r')

    animations = {}
    anim_list = []
    
    for path in f:
        path = path.strip("\n")
        
        if path.startswith("#"):
            continue

        if not path in animations:
            animations[path] = load_animation_file(path)

        anim_list.append(path)
        print "Load: " + path


    return (animations, anim_list)


# Boucle à l'infini 
def main_loop((animations, anim_list)):
    anim_len = len(anim_list)

    cur = -1

    # Happy looping!
    while True:
        cur = (cur + 1) % anim_len
        nex = (cur + 1) % anim_len

        (cur_values, cur_max_frame) = animations[anim_list[cur]]
        (nex_anim_values, _) = animations[anim_list[nex]]

        print "Playing " + anim_list[cur]

        # La dernière image n'est pas là, car elle est traitée à part
        for i in range(1, cur_max_frame):
            play_blend(cur_values[i], cur_values[i+1])

            
        # Dernière frame (fondu sur l'anim suivante - du coup, mettre 0 images
        # de fondu sur la dernière frame pour ne pas avoir de fondu)
        play_blend(cur_values[cur_max_frame], nex_anim_values[1])




def main():
    global ser
    ser = serial.Serial(
      port = serial_port,
      baudrate = 115200,
    
    # parity = serial.PARITY_NONE,
    # stopbits = serial.STOPBITS_ONE,
    # bytesize = serial.EIGHTBITS,
    # timeout = 1
    
    )                           
    
  # ser.close()
  # ser.open()

  # if (not ser.isOpen()):
  #   print "NOT open"
  #   exit

    
  # for i in range(0, 127) :
  #   send_color(ser, i, i, i)
    # for j in [0x80, i, i, 0]:
    #   ser.write(chr(j))

  # print ser.readlines()

    if len(sys.argv) < 2:
        print "Error: playlist file name must be given as first argument"
        exit(1)
  
    anim_data = load_playlist_file(sys.argv[1])
    
    main_loop(anim_data)



    ser.close()


main()
# print rgb255_to_tsv(255, 255, 255)
# print rgb255_to_tsv(255, 0, 0)
# print rgb255_to_tsv(0, 255, 0)
# print rgb255_to_tsv(0, 127, 127)


# frame = frame_rgb255_to_tsv([(0, 0, 0), (10, 10, 10)])

# nex = frame_rgb255_to_tsv([(100, 100, 200), (50, 50, 50)])



# print play_blend((frame, 100, 99), (nex, 0, 0))
