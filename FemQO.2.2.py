# -*- coding: utf-8 -*-
"""
FemQO: Flashcards per l'estudi i memorització de Química Orgànica
Adaptat a poder estudiar QOI, QOII o QOIII.
Aquesta versió et permet utilitzar tant el ratolí com el teclat per moure't entre les diferents zones
Inclou també una pantalla en què es pot decidir quines targetes estudiar: QOI, QOII o QOIII, o una combinació

"""

#necessary imports on python to make the executable
    #have python and pip installed
    #pip install pygame
    #pip install pillow
    #pip install fitz
    #pip install PyMuPDF
    
#To create an executable on Windows, insert the following command on the command prompt:
    #pip install pyinstaller
    #pyinstaller flashcards_study_executable.py --onefile --noconsole

##Texts specific to FemQO, to change to use for other purposes
#FlaschardsGameLoop
pygame_title = "FemQO"
pygame_icon_png = "benzene_icon.png"    #icon of pygame. Must be 32x32 pixels
                                        #must be in the folder "flashcards_docs"
#cover_screen
Title ="FemQO"
Subtitle = "Flashcards per l'estudi i memorització de Química Orgànica"
#welcome_screen
review_cards_in_order_msg = "Repassar en l'ordre del llibre ''Organic Chemistry'' de Paula Yurkanis."
change_front_back_card_msg = "(o clicar sobre la targeta) canvia entre reactius i producte."

#show_flashcard_in_screen
front_card_question = "Quins reactius es necessiten?"
rear_card_question = "Quin producte es forma?"
#initialpage_1st_decision
study_only_front = "Estudiar el producte que es forma"
study_only_rear = "Estudiar els reactius que es necessiten"


import pygame
import random
import os
import tempfile
import json
from PIL import Image
import fitz


#try to open the "pygame_icon_png" file by getcwd(). If it doesn't work, try "__file__"
try:
    filepath = os.getcwd()
    benzene_icon = open(os.path.join(filepath,"flashcards_docs",pygame_icon_png))
    benzene_icon.close()
except:
    filepath = os.path.dirname(__file__)
    benzene_icon = open(os.path.join(filepath,"flashcards_docs",pygame_icon_png))
    benzene_icon.close()


flashcards_docs = os.path.join(filepath,"flashcards_docs")
flashcard_dict_path = os.path.join(filepath,"flashcards_docs", "flashcard_dictionary.json")
QO_type_dict_path = os.path.join(filepath,"flashcards_docs", "QO_type_dictionary.json")


#parameters to initialize pygame
pygame.init() 
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

font_title = pygame.font.SysFont("Segoe UI", 40, bold = True)

font_18 = pygame.font.SysFont("calibri", 18)
font_16 = pygame.font.SysFont("calibri", 16)
font_14 = pygame.font.SysFont("calibri", 14) 
font_12 = pygame.font.SysFont("calibri", 12)

font_18_bold = pygame.font.SysFont("Segoe UI", 18, bold = True)
font_16_bold = pygame.font.SysFont("Segoe UI", 16, bold = True)
font_14_bold = pygame.font.SysFont("Segoe UI", 14, bold = True) 
font_12_bold = pygame.font.SysFont("Segoe UI", 12, bold = True) 


class button():
    def __init__(self, color, x,y,width,height, text='', font=font_12_bold):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self,screen):
        #Call this method to draw the button on the screen            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0,3)
        
        if self.text != '':
            text = self.font.render(self.text, 1, (255,255,255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def draw_triangle(self,screen, direction=None):
        if direction == "downwards":
            pygame.draw.polygon(screen, self.color,[(self.x, self.y), (self.x+self.width, self.y), (self.x+self.width/2, self.y+self.height)] )
        elif direction == "upwards":
            pygame.draw.polygon(screen, self.color,[(self.x, self.y+self.height), (self.x+self.width, self.y+self.height), (self.x+self.width/2, self.y)] )
        
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
def create_flashcard_dictionary():
    '''create flashcard dictionary and save it to a json file'''
    
    flashcard_dict = {}
    
    #creates the dictionary
    flashcard_pdfs = [("QOI","QOI_flashcards.pdf"),("QOII","QOII_flashcards.pdf"),("QOIII","QOIII_flashcards.pdf")]
    for name, pdf in flashcard_pdfs:
        doc = fitz.open(os.path.join(flashcards_docs, pdf))
        for number in range(doc.pageCount//2):
            flashcard = {
                "QO": name,
                "index": number,
                "flashcard_front": "fc_"+name+"_"+str(number)+"_front",
                "flashcard_rear": "fc_"+name+"_"+str(number)+"_rear",
                "score_front": 0,
                "score_rear": 0,
                }
            flashcard_dict["fc_"+name+"_"+str(number)] = flashcard
    
    #saves the dictionary into json format
    json_file = open(os.path.join(filepath,"flashcards_docs", "flashcard_dictionary.json"), "w")
    json.dump(flashcard_dict, json_file)
    json_file.close()
    
    return(flashcard_dict) 

#writes a message in the position defined by rectangle
def write_message(message, color = (0,0,0), rectangle=[0,0], font=font_16, update = True, centered = False):
    mesg = font.render(message, True, color)
    if centered:
        w,h = rectangle
        rectangle = [w-mesg.get_width()/2,h]
    screen.blit(mesg, rectangle)
    if update:
        pygame.display.update()  

#writes a button and the attached message in the position defined by rectangle        
def draw_button_and_message(key, message, rectangle=[0,0], text_color = (255,255,255), button_color = (0,0,0), text_font=font_14, button_font=font_12_bold, small=False, update=True):
    a, b = rectangle
    if small:
        width, height = 16, 16
        write_message(message, color = (0,0,0), rectangle=[a+25,b+1], update=update, font=text_font)
    else:
        width, height = 20, 20
        write_message(message, color = (0,0,0), rectangle=[a+25,b+4], update=update, font=text_font)

    button_key = button(button_color,a,b,width, height, key, font=button_font)
    button_key.draw(screen)
    return(button_key)
     
def change_button_color(button_key, pos, default_color=(0,0,0), isOver_color=(0,0,255)):
    if button_key.isOver(pos):
        button_key.color = isOver_color
    else:
        button_key.color = default_color
    button_key.draw(screen)
    pygame.display.update()

#returns boolean depending on whether the button/key has been pressed    
def press_button_and_key(event, key, button_key, pos, flashcard=False):
    Pressed = False
    if event.type == pygame.KEYDOWN:
        if event.key == key:
            Pressed = True
    elif event.type == pygame.MOUSEBUTTONUP:
        
        if button_key.isOver(pos):
            Pressed = True
    return(Pressed)

#creates a temp file with the flashcard obtained from the PDF and displays it on screen
def show_flashcard_in_screen(photo_name, front_rear, anki_back_card=False, arrows=(0, 0)):
    '''
    Loads the photo and shows it in the screen 
    '''
    "photo_name = fc_QOI_2_front"
    photo_name = photo_name.strip("fc_")
    photo_name = photo_name.strip("_front")
    photo_name = photo_name.strip("_rear")
    
    if "QOI_" in photo_name:
        doc = fitz.open(os.path.join(flashcards_docs, "QOI_flashcards.pdf"))
        photo_index = int(photo_name.strip("QOI_"))
    elif "QOII_" in photo_name:
        doc = fitz.open(os.path.join(flashcards_docs, "QOII_flashcards.pdf"))
        photo_index = int(photo_name.strip("QOII_"))
    elif "QOIII_" in photo_name:
        doc = fitz.open(os.path.join(flashcards_docs, "QOIII_flashcards.pdf"))
        photo_index = int(photo_name.strip("QOIII_"))

    if front_rear == "_front":
        photo_num = photo_index*2
    else:
        photo_num = photo_index*2+1
    
    zoom = 2
    mat = fitz.Matrix(zoom, zoom)
    page = doc.loadPage(photo_num)
    pix = page.getPixmap(matrix = mat)

    temp_photo_file = tempfile.NamedTemporaryFile()
    pix.writeImage(temp_photo_file.name)
    load_photo = pygame.image.load(temp_photo_file.name)
    
    flashcard_width, flashcard_height = Image.open(temp_photo_file.name).size
    
    screen.fill((255,255,255), rect=[0,0,screen_width, screen_height-65])
    
    if anki_back_card:
        pass
    else:
        if front_rear == "_front":
            write_message(front_card_question, rectangle = [screen_width/2,screen_height - flashcard_height-110], font=font_18, update=False, centered=True)
        else:
            write_message(rear_card_question, rectangle = [screen_width/2,screen_height - flashcard_height-110], font=font_18, update=False, centered=True)
    
    button_up, button_down = arrows
    if arrows != (0, 0):
        if button_up is None:
            button_down = button((200,200,200),screen_width/2-40, screen_height-65, 80,10)
            button_up = button((200,200,200),screen_width/2-40, (screen_height - flashcard_height-85), 80,10)
        else:
            button_down = button(button_down.color,screen_width/2-40, screen_height-65, 80,10)
            button_up = button(button_up.color,screen_width/2-40, (screen_height - flashcard_height-85), 80,10)
        button_down.draw_triangle(screen, direction="downwards")
        button_up.draw_triangle(screen, direction="upwards")
        
    screen.blit(load_photo,((screen_width - flashcard_width)/2 ,(screen_height - flashcard_height-70)))
    pygame.draw.line(screen, (0,0,0), ((screen_width - flashcard_width)/2, screen_height-70), ((screen_width + flashcard_width)/2 - 1, screen_height-70))
    pygame.draw.line(screen, (0,0,0), ((screen_width + flashcard_width)/2 - 1, screen_height-flashcard_height-70), ((screen_width + flashcard_width)/2 - 1, screen_height-70))
    pygame.display.update()
    
    return(button_up, button_down, temp_photo_file) #temp_photo_file is returned to be used in the IsOverFlashcard function
 
#returns True if the mouse is over the Flashcard   
def IsOverFlashcard(pos, temp_photo_file):
    #dada
    flashcard_0 = Image.open(temp_photo_file.name)
    flashcard_width, flashcard_height = flashcard_0.size
    x=(screen_width - flashcard_width)/2
    y=screen_height - flashcard_height-70
    
    if pos[0] > x and pos[0] < x + flashcard_width:
        if pos[1] > y and pos[1] < y + flashcard_height:
            return True
        
    return False

#defines all buttons in Ankistyle revision    
def anki_buttons():
    screen.fill((255,255,255))
    button_help = draw_button_and_message("H", "Help", rectangle = [screen_width - 70, screen_height-45], small=True, update=False)
    button_Q = draw_button_and_message("Q", "Quit", rectangle = [screen_width - 70, screen_height-25], small=True, update=False)
    button_B = draw_button_and_message("B", "Borrar", rectangle = [screen_width - 70, screen_height-65], small=True, update=False)
    
    
    button_1 = button((255,0,0),screen_width/2-195, screen_height-50, 90, 30, "Fallat (1)", font=font_16_bold)
    button_1.draw(screen)
    
    button_2 = button((255,130,0),screen_width/2- 95, screen_height-50, 90, 30, "Difícil (2)", font=font_16_bold)
    button_2.draw(screen)
    
    button_3 = button((210,190,0),screen_width/2+ 5, screen_height-50, 90, 30, "Mitjà (3)", font=font_16_bold)
    button_3.draw(screen)
    
    button_4 = button((10,200,0),screen_width/2+ 105, screen_height-50, 90, 30, "Fàcil (4)", font=font_16_bold)
    button_4.draw(screen)
    
    return(button_1, button_2, button_3, button_4, button_B, button_help, button_Q)

#first screen displayed when the program is run
def cover_screen(GameLoop):
    screen.fill((255,255,255))
    write_message(Title, font=font_title, rectangle = [screen_width/2, 100], centered=True)
    write_message(Subtitle, font=font_18, rectangle = [screen_width/2,180], centered=True)
    write_message("(clica o prem qualsevol tecla per continuar)", font=font_12, rectangle = [screen_width/2,250], centered=True)
    
    write_message("Núria Fàbrega Ribas", font=font_12, color=(120,120,120), rectangle = [screen_width - 120,screen_height - 50] )
    write_message("nuriafarimd@gmail.com", font=font_12, color=(120,120,120), rectangle = [screen_width - 140,screen_height - 30] )
    
    pygame.display.update()
    
    Cover_screen = True
    while Cover_screen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                Cover_screen = False
            elif event.type == pygame.QUIT:
                Cover_screen = False
                GameLoop = False
    return(GameLoop)


def choose_QO_type(GameLoop):
    '''Asks the user which types of QO does he want to study and saves them in a json dictionary'''
    
    screen.fill((255,255,255))
    write_message("De quina de les 3 QO vols estudiar les reaccions?", font=font_16_bold, rectangle = [20,20])
    write_message("Pots escollir més d'una opció. Prem Enter quan hagis escollit", font=font_16, rectangle = [20,50])
    
    button_1 = draw_button_and_message("1", "QO I", rectangle=[50, 76], text_font=font_16)
    button_2 = draw_button_and_message("2", "QO II", rectangle=[50, 100], text_font=font_16)
    button_3 = draw_button_and_message("3", "QO III", rectangle=[50, 125], text_font=font_16)
    button_RETURN = button((0,0,0),40,155, 40, 20, "Enter", font=font_16)
    button_RETURN.draw(screen)
    
    pygame.display.update()
 
    fixed_button_color = (50,50,255)
    
    TypeQO = None
    while TypeQO is None:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                if button_1.color != fixed_button_color:
                    change_button_color(button_1, pos)
                if button_2.color != fixed_button_color:
                    change_button_color(button_2, pos)
                if button_3.color != fixed_button_color:
                    change_button_color(button_3, pos) 
                change_button_color(button_RETURN, pos)
            if event.type == pygame.QUIT:
                GameLoop = False
                return(GameLoop)        
            elif press_button_and_key(event, pygame.K_RETURN, button_RETURN, pos):
                TypeQO = True
                break
            elif press_button_and_key(event, pygame.K_1, button_1, pos):
                if button_1.color == fixed_button_color:
                    change_button_color(button_1, pos)
                else:
                    button_1.color = fixed_button_color
                    button_1.draw(screen)
                    pygame.display.update()
            elif press_button_and_key(event, pygame.K_2, button_2, pos):
                if button_2.color == fixed_button_color:
                    change_button_color(button_2, pos)
                else:
                    button_2.color = fixed_button_color
                    button_2.draw(screen)
                    pygame.display.update()
            elif press_button_and_key(event, pygame.K_3, button_3, pos):
                if button_3.color == fixed_button_color:
                    change_button_color(button_3, pos)
                else:
                    button_3.color = fixed_button_color
                    button_3.draw(screen)
                    pygame.display.update()
        
        
    #Create a dictionary with the answers
    QO_type_dict = {
        "QOI": False,
        "QOII": False,
        "QOIII": False}
  
    if button_1.color == fixed_button_color:
        QO_type_dict["QOI"] = True    
    if button_2.color == fixed_button_color:
        QO_type_dict["QOII"] = True
    if button_3.color == fixed_button_color:
        QO_type_dict["QOIII"] = True
    
    #saves the dictionary into json format
    json_file = open(os.path.join(filepath,"flashcards_docs", "QO_type_dictionary.json"), "w")
    json.dump(QO_type_dict, json_file)
    json_file.close()
    
    return(GameLoop)

def Welcome_screen(GameLoop):
    screen.fill((255,255,255))
    write_message("Com vols repassar?", rectangle = [20,20], font=font_16_bold)
    button_Y = draw_button_and_message("Y", review_cards_in_order_msg, rectangle = [40,50] )
    button_R = draw_button_and_message("R", "Repassar les targetes en ordre aleatori (random).", rectangle = [40,75] )
    button_A = draw_button_and_message("A", "Auto-avaluació (les targetes que menys et saps surten més sovint).", rectangle = [40,100] )
    
    write_message("Utilitza les fletxes o el ratolí per moure't entre les targetes", rectangle=[20,130], font=font_14_bold)
    draw_button_and_message("→", "", rectangle = [30, 155], button_font=font_12, small=True)  
    draw_button_and_message("←", change_front_back_card_msg, rectangle = [53, 155], button_font=font_12, small=True)
    draw_button_and_message("↑", "", rectangle = [30, 180], button_font=font_12, small=True)  
    draw_button_and_message("↓", "canvien de targeta (només aplicable als modes Y i R).", rectangle = [53, 180], button_font=font_12, small=True)

    button_D = draw_button_and_message("D", "Decidir de quina assignatura estudiar les reaccions. El progrés quedarà guardat.", rectangle = [20,screen_height-30], text_font=font_14)
    
    pygame.display.update()
    Pantalla_inici = True
    StudyType = None
    while Pantalla_inici:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                change_button_color(button_Y, pos)
                change_button_color(button_R, pos)
                change_button_color(button_A, pos)  
                change_button_color(button_D, pos)  
                
            if event.type == pygame.QUIT:
                GameLoop = False
                return(StudyType, GameLoop)          
            if press_button_and_key(event, pygame.K_y, button_Y, pos):
                StudyType = "ordre_cronologic"
                Pantalla_inici = False
            elif press_button_and_key(event, pygame.K_r, button_R, pos):
                StudyType = "ordre_random"
                Pantalla_inici = False
            elif press_button_and_key(event, pygame.K_a, button_A, pos):
                StudyType = "Anki"
                Pantalla_inici = False
            elif press_button_and_key(event, pygame.K_d, button_D, pos):
                GameLoop = choose_QO_type(GameLoop)
                StudyType = None
                Pantalla_inici = False
                        
    return(StudyType, GameLoop)

def Ankistyle_review(GameLoop):
    with open(flashcard_dict_path) as json_file:
        flashcard_dict = json.load(json_file)
    
    with open(QO_type_dict_path) as json_file:
        QO_type_dict = json.load(json_file)
    
    
    #creates a list with the names of all flashcards that must be studied
    flashcard_dict_tostudy = []      
    for flashcard in flashcard_dict:
        if QO_type_dict["QOI"] is True and flashcard_dict[flashcard]["QO"]=="QOI": 
            flashcard_dict_tostudy.append(flashcard) 
        if QO_type_dict["QOII"] is True and flashcard_dict[flashcard]["QO"]=="QOII":
            flashcard_dict_tostudy.append(flashcard)
        if QO_type_dict["QOIII"] is True and flashcard_dict[flashcard]["QO"]=="QOIII":
            flashcard_dict_tostudy.append(flashcard)   


    Repas = True

    def Anki_help(decision, Repas, GameLoop):
        '''Gives help when you don't remember what number meant at the middle of the program'''
        screen.fill((255,255,255))
        
        row=20
        
        draw_button_and_message("→", "", rectangle = [20,row], button_font=font_12, small=True)  
        draw_button_and_message("←", "(o clicar sobre la targeta) canvien entre la part del davant i darrere de la targeta.", rectangle = [43, row], button_font=font_12, text_font=font_14, small=True)

        write_message("Prem la tecla o clica en el botó corresponent depenent de la dificultat de la targeta:", rectangle=[20,row+25])
        row = 50
        draw_button_and_message("1", "Fallat", rectangle=[30,row+20], small=True)
        write_message("Quan has girat la targeta, no era el que esperaves.", rectangle=[105, row+21], font=font_14)
        draw_button_and_message("2", "Difícil", rectangle=[30,row+40], small=True)
        write_message("Quan has girat la targeta, ha sortit el que t'esperaves, però no n'estaves segur/a.", rectangle=[105, row+41], font=font_14)
        draw_button_and_message("3", "Mitjà", rectangle=[30,row+60], small=True)
        write_message("Quan has girat la targeta, ha sortit el que esperaves, però no t'ha vingut de forma fluïda.", rectangle=[105, row+61], font=font_14)
        draw_button_and_message("4", "Fàcil", rectangle=[30,row+80], small=True)
        write_message("Quan has girat la targeta, era el que esperaves, i ho has recordat instantàniament.", rectangle=[105, row+81], font=font_14)
        draw_button_and_message("B", "Borrar", rectangle=[30,row+100], small=True)
        write_message("Prem si no vols tornar a veure la targeta. Només ho podràs desfer fent un reset del progrés.", rectangle=[105, row+101], font=font_14)
        
        button_H = draw_button_and_message("H", "Retornar a l'estudi de les targetes", rectangle = [20,screen_height-55], text_font = font_14)
        button_Q = draw_button_and_message("Q", "Retornar a la pantalla d'inici (quit)", rectangle = [20,screen_height-30], text_font = font_14)
        
        pygame.display.update()

        Help = True
        while Help:
            for event in pygame.event.get(): 
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    change_button_color(button_Q, pos)
                    change_button_color(button_H, pos)
                if event.type == pygame.QUIT:
                    decision = True
                    Repas = False
                    GameLoop = False
                    Help = False
                if press_button_and_key(event, pygame.K_h, button_H, pos):
                    Help = False
                    
                if press_button_and_key(event, pygame.K_q, button_Q, pos):
                    Repas = False
                    decision = True
                    Help = False   
        
        return(decision, Repas, GameLoop) 

        
    def initialpage_general_screen():
        '''Shows the general screen of Ankistyle review'''
        #create the mean score for the flashcards
        screen.fill((255,255,255))
        
        def create_score_list_and_punctuation(flashcard_dict): 
            score_list = []
            for item in flashcard_dict:
                if item in flashcard_dict_tostudy:
                    if float(flashcard_dict[item]["score_rear"]) <= 10:
                        score_list.append(float(flashcard_dict[item]["score_rear"]))
                    if float(flashcard_dict[item]["score_front"]) <= 10:
                        score_list.append(float(flashcard_dict[item]["score_front"]))    
                
            #Changes the colour depending on the score value
            write_message("Puntuació actual:", rectangle=[20,20], font=font_16_bold)
            
            #Counts the number of flashcards of each type
            write_message("Noves", rectangle=[300,20], font=font_14, color = (0,0,50), centered=True)
            write_message("Fallades", rectangle=[360,20], font=font_14, color = (255,0,0), centered=True)
            write_message("Difícils", rectangle=[420,20], font=font_14, color = (255,150,0), centered=True)
            write_message("Mitjanes", rectangle=[480,20], font=font_14, color = (180,160,0), centered=True)
            write_message("Fàcils", rectangle=[540,20], font=font_14, color = (0,200,0), centered=True)
            
            nova = sum(i == 0 for i in score_list)
            fallada = sum(0 < i < 1.1 for i in score_list)
            dificil = sum(1.1 < i < 4.1 for i in score_list)
            mitjana = sum(4.1 < i < 7.9 for i in score_list)
            facil = sum(7.9 < i < 10 for i in score_list)
            
            write_message("{}".format(nova), rectangle=[300,40], font=font_14, color = (0,0,50), centered=True)
            write_message("{}".format(fallada), rectangle=[360,40], font=font_14, color = (255,0,0), centered=True)
            write_message("{}".format(dificil), rectangle=[420,40], font=font_14, color = (255,150,0), centered=True)
            write_message("{}".format(mitjana), rectangle=[480,40], font=font_14, color = (180,160,0), centered=True)
            write_message("{}".format(facil), rectangle=[540,40], font=font_14, color = (0,200,0), centered=True)

    
            if len(score_list)-nova == 0:
                mean_score = 0
            else:
                mean_score = sum(score_list)/(len(score_list)-nova)
            
            return(mean_score)
        
        mean_score = create_score_list_and_punctuation(flashcard_dict)
        
        if mean_score == 0:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold)
        elif mean_score < 3:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (255,0,0))        
        elif mean_score < 5:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (255,150,0))
        elif mean_score < 6:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (255,230,0))
        elif mean_score < 7:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (180,160,0))        
        elif mean_score < 8:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (150,200,0))            
        elif mean_score < 9:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (0,200,0))        
        elif mean_score < 10:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (0,200,200))
        else:
            write_message("{:.2f}".format(mean_score), rectangle=[170,20], font=font_16_bold, color = (0,150,255))
        
        #Instructions
        row=230
        write_message("Instruccions a l'hora d'estudiar les targetes:", rectangle=[20,row-55], font=font_14_bold)
       
        draw_button_and_message("→", "", rectangle = [20,row-30], button_font=font_12, small=True)  
        draw_button_and_message("←", "(o clicar sobre la targeta) canvia entre la part del davant i darrere de la targeta.", rectangle = [43, row-30], button_font=font_12, text_font=font_14, small=True)

        write_message("Prem la tecla o clica en el botó corresponent depenent de la dificultat de la targeta:", rectangle=[20,row-5])

        draw_button_and_message("1", "Fallat", rectangle=[30,row+20], small=True)
        write_message("Quan has girat la targeta, no era el que esperaves.", rectangle=[105, row+21], font=font_14)
        draw_button_and_message("2", "Difícil", rectangle=[30,row+40], small=True)
        write_message("Quan has girat la targeta, ha sortit el que t'esperaves, però no n'estaves segur/a.", rectangle=[105, row+41], font=font_14)
        draw_button_and_message("3", "Mitjà", rectangle=[30,row+60], small=True)
        write_message("Quan has girat la targeta, ha sortit el que esperaves, però no t'ha vingut de forma fluïda.", rectangle=[105, row+61], font=font_14)
        draw_button_and_message("4", "Fàcil", rectangle=[30,row+80], small=True)
        write_message("Quan has girat la targeta, era el que esperaves, i ho has recordat instantàniament.", rectangle=[105, row+81], font=font_14)
        draw_button_and_message("B", "Borrar", rectangle=[30,row+100], small=True)
        write_message("Prem si no vols tornar a veure la targeta. Només ho podràs desfer fent un reset del progrés.", rectangle=[105, row+101], font=font_14)

        
        
        
        button_R = draw_button_and_message("R", "Fer un reset del progrés. Retorna la puntuació a 0", rectangle=[20, screen_height-55], text_font=font_14)
        button_Q = draw_button_and_message("Q", "Retornar a la pantalla d'inici (quit)", rectangle = [20,screen_height-30], text_font=font_14)
        
        return(button_R, button_Q)

    def initialpage_1st_decision(Repas, GameLoop):
        def initialpage_1st_decision_screen():
            button_R, button_Q = initialpage_general_screen()
            write_message("Com vols estudiar?", rectangle=[20,60], font=font_14_bold)
            button_1 = draw_button_and_message("1", study_only_front, rectangle = [40,85] )
            button_2 = draw_button_and_message("2", study_only_rear, rectangle = [40,110] )
            button_3 = draw_button_and_message("3", "Estudiar una barreja", rectangle = [40,135] )
            pygame.display.update()
            return(button_1, button_2, button_3, button_R, button_Q)
        
        button_1, button_2, button_3, button_R, button_Q = initialpage_1st_decision_screen()
        
        TypeOfAnkiStudy = None
        while TypeOfAnkiStudy is None:
            for event in pygame.event.get(): 
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    change_button_color(button_1, pos)
                    change_button_color(button_2, pos)
                    change_button_color(button_3, pos)
                    change_button_color(button_R, pos)
                    change_button_color(button_Q, pos)          
                elif event.type == pygame.QUIT:
                    Repas = False
                    GameLoop = False
                    return(TypeOfAnkiStudy, Repas, GameLoop, button_R, button_Q)
                elif press_button_and_key(event, pygame.K_1, button_1, pos) or press_button_and_key(event, pygame.K_KP1, button_1, pos):
                    TypeOfAnkiStudy = "Rear_front"
                elif press_button_and_key(event, pygame.K_2, button_2, pos) or press_button_and_key(event, pygame.K_KP2, button_2, pos):
                    TypeOfAnkiStudy = "Front_rear"
                elif press_button_and_key(event, pygame.K_3, button_3, pos) or press_button_and_key(event, pygame.K_KP3, button_3, pos):
                    TypeOfAnkiStudy = "Mixed"
                elif press_button_and_key(event, pygame.K_r, button_R, pos):
                    Repas, TypeOfAnkiStudy, GameLoop = reset_cards(Repas, TypeOfAnkiStudy, GameLoop)
                    if Repas:
                        initialpage_1st_decision_screen()
                elif press_button_and_key(event, pygame.K_q, button_Q, pos):
                    Repas = False
                    TypeOfAnkiStudy = False
      
        return(TypeOfAnkiStudy, Repas, GameLoop, button_R, button_Q)
    
    def initialpage_2nd_decision(Repas, GameLoop, button_R, button_Q):
        def initialpage_2nd_decision_screen():
            initialpage_general_screen()
            write_message("Quantes targetes vols repassar?", rectangle=[20,60], font=font_14_bold)
            last_message = font_14_bold.render("Quantes targetes vols repassar?", True, (0,0,0))
            write_message("Escriu el nombre i prem Enter.", rectangle=[last_message.get_width()+40,65], font=font_14)
            
            write_message("per estudiar el valor per defecte: 50 targetes", rectangle=[70,85], font=font_12)
            button_RETURN = button((0,0,0),25,83, 35, 15, "Enter", font=font_12)
            button_RETURN.draw(screen)
            pygame.display.update()
            
            return(button_RETURN)
        
        button_RETURN = initialpage_2nd_decision_screen()
        
        num_cards = ""
        WriteNumberCards = True
        number_pressed = None
        while WriteNumberCards:  
            for event in pygame.event.get(): 
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    if number_pressed is None:
                        change_button_color(button_RETURN, pos)
                    change_button_color(button_Q, pos)
                    change_button_color(button_R, pos)
                    
                if event.type == pygame.QUIT:
                    Repas = False
                    GameLoop = False
                    return(0, Repas, GameLoop)
                elif press_button_and_key(event, pygame.K_q, button_Q, pos):
                    Repas = False
                    WriteNumberCards = False
                    
                elif press_button_and_key(event, pygame.K_RETURN, button_RETURN, pos):
                    WriteNumberCards = False
                    screen.fill((0,0,0))
                elif press_button_and_key(event, pygame.K_r, button_R, pos):
                    Repas, WriteNumberCards, GameLoop = reset_cards(Repas, WriteNumberCards, GameLoop)
                    if Repas:
                        initialpage_2nd_decision_screen()
                elif event.type == pygame.KEYDOWN:    
                    if (event.key == pygame.K_1 or event.key == pygame.K_KP1 or
                          event.key == pygame.K_2 or event.key == pygame.K_KP2 or
                          event.key == pygame.K_3 or event.key == pygame.K_KP3 or
                          event.key == pygame.K_4 or event.key == pygame.K_KP4 or
                          event.key == pygame.K_5 or event.key == pygame.K_KP5 or
                          event.key == pygame.K_6 or event.key == pygame.K_KP6 or
                          event.key == pygame.K_7 or event.key == pygame.K_KP7 or
                          event.key == pygame.K_8 or event.key == pygame.K_KP8 or
                          event.key == pygame.K_9 or event.key == pygame.K_KP9 or
                          event.key == pygame.K_0 or event.key == pygame.K_KP0):
                        number_pressed = True
                        num_cards += pygame.key.name(event.key).strip("[]")
                        screen.fill((255,255,255), rect=(0,81,screen_width,60))
                        write_message(num_cards, rectangle=[60,90], font=font_18)
                        pygame.display.update()
        if num_cards == "":
            num_cards = 50
        return(int(num_cards), Repas, GameLoop)
        
    def reset_cards(Repas, Loop, GameLoop):
        reset = True
        screen.fill((255,255,255))
        write_message("Segur que vols fer un reset del progrés? La teva puntuació tornarà a 0.", rectangle=[20,20], font=font_14_bold)
        button_R = draw_button_and_message("R","Prem per confirmar", rectangle=[25,50], small=True)
        write_message("Clica o prem qualsevol altra tecla per cancel·lar.", rectangle=[50,70], font=font_14)
          
        while reset:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    change_button_color(button_R, pos)
                if event.type == pygame.QUIT:
                    Loop = False
                    Repas = False
                    GameLoop = False
                    return(Repas, Loop, GameLoop)
                elif press_button_and_key(event, pygame.K_r, button_R, pos):
                    create_flashcard_dictionary()
                    Repas = False
                    Loop = False
                    reset = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    reset = False
        return(Repas, Loop, GameLoop)  

    def review_flashcards_Ankistyle(Repas, GameLoop):
        
        #creates a list of names and scores to use to randomly choose the cards
        flashcard_weights_front = []
        flashcard_weights_rear = []
        flashcard_names = []
        flashcard_front_names = []
        flashcard_rear_names = []
        
        #appends the names of the selected flashcards and its weights into a list
        for flashcard in flashcard_dict: 
            if flashcard in flashcard_dict_tostudy:
                flashcard_names.append(flashcard)
                flashcard_front_names.append(flashcard_dict[flashcard]["flashcard_front"])
                flashcard_rear_names.append(flashcard_dict[flashcard]["flashcard_rear"])
                if flashcard_dict[flashcard]["score_rear"] == 0:
                    flashcard_weights_rear.append(10)
                else:
                    flashcard_weights_rear.append(1/(flashcard_dict[flashcard]["score_rear"])**2)
                    
                if flashcard_dict[flashcard]["score_front"] == 0:
                    flashcard_weights_front.append(10)            
                else:
                    flashcard_weights_front.append(1/(flashcard_dict[flashcard]["score_front"])**2)
        
        
        #1st decision: front, rear or mixed.
        TypeOfAnkiStudy, Repas, GameLoop, button_R, button_Q = initialpage_1st_decision(Repas, GameLoop)
        #2nd decision: number of cards per set
        if Repas:
            cards_per_set, Repas, GameLoop = initialpage_2nd_decision(Repas, GameLoop, button_R, button_Q)
            
            if TypeOfAnkiStudy == "Front_rear":
                score = "score_front"
                set_cards = random.choices(flashcard_names, weights=flashcard_weights_front, k=cards_per_set)
            elif TypeOfAnkiStudy == "Rear_front":
                score = "score_rear"
                set_cards = random.choices(flashcard_names, weights=flashcard_weights_rear, k=cards_per_set)
            elif TypeOfAnkiStudy == "Mixed":
                set_cards = random.choices(flashcard_front_names+flashcard_rear_names, weights=flashcard_weights_front+flashcard_weights_rear, k=cards_per_set)
            
       
        button_1, button_2, button_3, button_4, button_B, button_help, button_Q = anki_buttons()
        
       
        #2. Change the score of the dict depending on the key pressed
        while Repas:
            for card in set_cards:
                if not Repas:
                    break
                decision = False
                if TypeOfAnkiStudy == "Front_rear":
                    front_rear = "_front"
                    
                elif TypeOfAnkiStudy == "Rear_front":
                    front_rear = "_rear"
                elif TypeOfAnkiStudy == "Mixed":
                    if "front" in card:
                        front_rear = "_front"
                        score = "score_front"
                        card = card.replace("_front", "")
                    if "rear" in card:
                        front_rear = "_rear"
                        score = "score_rear"
                        card = card.replace("_rear", "")
                
                if front_rear == "_front":
                    InitialPosition = "_front"
                else:
                    InitialPosition = "_rear"
                
                while decision is False:
                    photo = card+front_rear
                    
                    if InitialPosition == front_rear:             
                        _,_,temp_photo_file = show_flashcard_in_screen(photo, front_rear)
                    else:
                        _,_,temp_photo_file = show_flashcard_in_screen(photo, front_rear, anki_back_card=True)
                    

                    #rewrites the score depending on the user's answer
                    for event in pygame.event.get():
                        pos = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEMOTION:
                            change_button_color(button_1, pos, (255,0,0), (200,0,0))
                            change_button_color(button_2, pos, (255,130,0),(200,80,0))
                            change_button_color(button_3, pos, (210,190,0), (180,150,0))
                            change_button_color(button_4, pos, (10,200,0), (0,150,0))
                            change_button_color(button_help, pos)
                            change_button_color(button_Q, pos)
                            change_button_color(button_B, pos)
                            

                        if event.type == pygame.QUIT:
                            Repas = False
                            GameLoop = False
                            return(Repas, GameLoop)  
                        
                        elif press_button_and_key(event, pygame.K_1, button_1, pos) or press_button_and_key(event, pygame.K_KP1, button_1, pos):
                            flashcard_dict[card][score] = 1
                            decision = True
                        elif press_button_and_key(event, pygame.K_2, button_2, pos) or press_button_and_key(event, pygame.K_KP2, button_2, pos):
                            flashcard_dict[card][score] = 4
                            decision = True 
                        elif press_button_and_key(event, pygame.K_3, button_3, pos) or press_button_and_key(event, pygame.K_KP3, button_3, pos):
                            if flashcard_dict[card][score] <= 6:
                                flashcard_dict[card][score] = 6
                            else:
                                flashcard_dict[card][score] -= 1
                            decision = True
                        elif press_button_and_key(event, pygame.K_4, button_4, pos) or press_button_and_key(event, pygame.K_KP4, button_3, pos):
                            if flashcard_dict[card][score] < 7.9:
                                flashcard_dict[card][score] = 8
                            elif flashcard_dict[card][score] < 9.7:
                                flashcard_dict[card][score] += 0.3
                            else:
                                flashcard_dict[card][score] = 10
                            decision = True                           
                        elif press_button_and_key(event, pygame.K_h, button_help, pos):
                            decision, Repas, GameLoop = Anki_help(decision, Repas, GameLoop)
                            anki_buttons()
                        elif press_button_and_key(event, pygame.K_q, button_Q, pos):
                            Repas = False 
                            decision = True
                        elif press_button_and_key(event, pygame.K_b, button_B, pos):
                            flashcard_dict[card][score] = 10000
                            decision = True
                        elif event.type == pygame.MOUSEBUTTONUP and IsOverFlashcard(pos, temp_photo_file):
                            if front_rear == "_front":
                               front_rear = "_rear"
                            else:
                                front_rear = "_front"
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                if InitialPosition == "_front":
                                   front_rear = "_front"
                                else:
                                    front_rear = "_rear"
                            elif event.key == pygame.K_RIGHT:
                                if InitialPosition == "_front":
                                   front_rear = "_rear"
                                else:
                                    front_rear = "_front"                                


            json_file = open(flashcard_dict_path, "w")
            json.dump(flashcard_dict, json_file)
            json_file.close()
            Repas = False
        
        return(Repas, GameLoop)
   
    Repas, GameLoop = review_flashcards_Ankistyle(Repas, GameLoop)
    return(GameLoop)
    
def study_flashcards(StudyType, GameLoop):
    
    screen.fill((255,255,255))
    button_Q = draw_button_and_message("Q", "Retornar a la pantalla d'inici (quit)", rectangle = [20,screen_height-30], text_font=font_14)
    
    with open(flashcard_dict_path) as json_file:
        flashcard_dict = json.load(json_file)
    
    with open(QO_type_dict_path) as json_file:
        QO_type_dict = json.load(json_file)
       
    #creates a list with the names of all flashcards that must be studied
    flashcard_dict_tostudy = []      
    for flashcard in flashcard_dict:
        if QO_type_dict["QOI"] is True and flashcard_dict[flashcard]["QO"]=="QOI": 
            flashcard_dict_tostudy.append(flashcard) 
        if QO_type_dict["QOII"] is True and flashcard_dict[flashcard]["QO"]=="QOII":
            flashcard_dict_tostudy.append(flashcard)
        if QO_type_dict["QOIII"] is True and flashcard_dict[flashcard]["QO"]=="QOIII":
            flashcard_dict_tostudy.append(flashcard)   

    
    flashcard_names = []
    for flashcard in flashcard_dict: 
        if flashcard in flashcard_dict_tostudy:
            flashcard_names.append(flashcard)

    
    fc_cron_i = 0 #flashcard cronological index
    next_flashcard = flashcard_names[fc_cron_i]
    
    random_flashcards_list = []
    if StudyType == "ordre_random":
        next_flashcard = random.choice(flashcard_names)
        #He de canviar això a que sigui "random.choices()" o algo semblant, que no depengui del número
        random_flashcards_list.append(next_flashcard)
    front_rear = "_rear"
    
    Repas = True
    
    button_up, button_down = None, None
    
    while Repas:
        photo = next_flashcard+front_rear
        
        button_up, button_down, temp_photo_file = show_flashcard_in_screen(photo, front_rear, arrows=(button_up, button_down))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                change_button_color(button_Q, pos)
                if button_up.isOver(pos):
                    button_up.color = (200,220,250)
                    button_up.draw_triangle(screen, direction="upwards")
                elif button_down.isOver(pos):
                    button_down.color = (200,220,250)
                    button_down.draw_triangle(screen, direction="downwards")
                else: 
                    button_up.color = (200,200,200)
                    button_down.color = (200,200,200)
            elif event.type == pygame.QUIT:
                GameLoop = False
                return(GameLoop)
            elif press_button_and_key(event, pygame.K_q, button_Q, pos):
                Repas = False

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) or (event.type == pygame.MOUSEBUTTONUP and button_down.color == (200,220,250)):
                if StudyType == "ordre_cronologic":
                    if fc_cron_i == len(flashcard_names)-1:
                        fc_cron_i = 0
                    else:
                        fc_cron_i +=1
                    
                    next_flashcard = flashcard_names[fc_cron_i]
                else:
                    next_flashcard = random.choice(flashcard_names)
                    random_flashcards_list.append(next_flashcard)
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (event.type == pygame.MOUSEBUTTONUP and button_up.color == (200,220,250)):
                if StudyType == "ordre_cronologic":
                    if fc_cron_i == 0:    
                        fc_cron_i = len(flashcard_names)-1
                    else:
                        fc_cron_i -=1
                    next_flashcard = flashcard_names[fc_cron_i]
                else:   
                    if len(random_flashcards_list) <= 1:
                        pass
                    else:    
                        next_flashcard = random_flashcards_list[-2]
                        random_flashcards_list.pop()   
                    
            elif event.type == pygame.MOUSEBUTTONUP and IsOverFlashcard(pos, temp_photo_file):
                if front_rear == "_front":
                   front_rear = "_rear"
                else:
                    front_rear = "_front"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    front_rear = "_rear"
                elif event.key == pygame.K_RIGHT:
                    front_rear = "_front"

    return(GameLoop)

def make_GameLoop(GameLoop):
    #screen parameters:
    
    #Set the caption and icon of the program:
    pygame.display.set_caption(pygame_title)
    programIcon = pygame.image.load(os.path.join(filepath,"flashcards_docs",pygame_icon_png))
    pygame.display.set_icon(programIcon)
    
    GameLoop = True
    GameLoop = cover_screen(GameLoop)
    
    if GameLoop: 
        #chose_QO_type appears if all values of the dictionary are false (If no cards are chosen)
        with open(QO_type_dict_path) as json_file:
            QO_type_dict = json.load(json_file)
        if all(QO_type_dict[value] is False for value in QO_type_dict):
            GameLoop = choose_QO_type(GameLoop)
    while GameLoop:
        StudyType, GameLoop = Welcome_screen(GameLoop)
        with open(QO_type_dict_path) as json_file:
            QO_type_dict = json.load(json_file)
        if all(QO_type_dict[value] is False for value in QO_type_dict) and GameLoop:
            GameLoop = choose_QO_type(GameLoop)
        else:
            if StudyType == "ordre_cronologic" or StudyType == "ordre_random": 
                GameLoop = study_flashcards(StudyType, GameLoop)
            elif StudyType == "Anki":
                GameLoop = Ankistyle_review(GameLoop)

def main():   
    GameLoop = True
    make_GameLoop(GameLoop)
    pygame.quit() 
    

if __name__ == "__main__":
   main()

#PDF_to_JPG()