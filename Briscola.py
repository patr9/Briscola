import glob
import os
import random
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from tkinterdnd2 import DND_FILES, TkinterDnD

#Replaces the filepath name to get only the card name
def getCards(cards):
    char_to_replace = {"/Users/p/Documents/Briscola/assets/cards/": '', ".png": ''}
    for i in range(0, len(cards)):
        for key, value in char_to_replace.items():
            cards[i] = cards[i].replace(key, value)
    return cards

def createDeck():
    #Goes as [card suits, card number, card value, card image location], e.g. [['cups', 'ace', 11, 'path/to/img']])
    deck = [['' for x in range(4)] for y in range(len(cards))]
    for i in range(len(cards)):
        deck[i][0] = cards[i].split('_')[0]
        card = cards[i].split('_')[-1]
        deck[i][1] = card
        if values2.__contains__(card):
            deck[i][2] = str(values2[card])
        else:
            deck[i][2] = '0'
        deck[i][3] = cards_images_locations[i]
    random.shuffle(deck)
    return deck

#Gets the image and resizes it to match the rest of the cards
def getImage(cardtoget):
    img = Image.open(cardtoget)
    img = img.resize((screen_width//12,screen_height//6), Image.BICUBIC)
    image = ImageTk.PhotoImage(img)
    return image

def resize_image(event, card, imgpath):
    #Gets window size if event if None, otherwise gets size from event
    if event is None:
        new_width = card.winfo_width()
        new_height = card.winfo_height()
    else:
        new_width = event.width
        new_height = event.height

    #Resize image if new dimensions are great than 0
    if new_width > 0 and new_height > 0:
        image = Image.open(imgpath)

        #Checks if the card is the trump card and rotates it
        if card._name == '!label8':
            image = image.rotate(90, expand=True)
        image = image.resize((new_width, new_height), Image.BICUBIC)
        photo = ImageTk.PhotoImage(image)
        card.config(image = photo)
        card.image = photo

def perform_resize():
    # Get the new card dimensions using the window dimensions
    card_width = root.winfo_width() // 12
    card_height = root.winfo_height() // 5.3

    # Update card sizes and resize images
    for card, imgpath in [
        (p1handslot1, player1_hand[0][3]),
        (p1handslot2, player1_hand[1][3]),
        (p1handslot3, player1_hand[2][3]),
        (p2handslot1, backofcard),
        (p2handslot2, backofcard),
        (p2handslot3, backofcard),
        (deckImg, backofcard),
        (trump, trumpdetails[3]),
        (p1pick, pilecard1img),
        (p2pick, pilecard1img),
    ]:

        #Checks if the card is placed/seen on screen
        if card.winfo_viewable() == 1:
            #Checks if the card is the trump card to swap width and height and match the default card size
            if card._name == '!label8':
                card.place_configure(width=card_height, height=card_width)
            else:
                card.place_configure(width=card_width, height=card_height)
            resize_image(None, card, imgpath)

#Removes the button/card when clicked
def on_click(card):
    global pilecard1img, pile1, pile2
    card.place_forget()
    #Updates the played card image in the middle. Currently only updates player 1's card, will need updating
    if card._name == '!label':
        p1img1 = getImage(player1_hand[0][3])
        p1pick.config(image=p1img1)
        pilecard1img = p1img1
        pile1 = player1_hand[0]
    elif card._name == '!label2':
        p1img2 = getImage(player1_hand[1][3])
        p1pick.config(image=p1img2)
        pilecard1img = p1img2
        pile1 = player1_hand[1]
    elif card._name == '!label3':
        p1img3 = getImage(player1_hand[2][3])
        p1pick.config(image=p1img3)
        pilecard1img = p1img3
        pile1 = player1_hand[2]

def deckClick():
    global deck, player1_hand, p1handslot1, p1handslot2, p1handslot3
    #Checks if the deck is empty
    if not deck:
        return("Deck is empty")
    
    #Checks which hand slot was used and updates that card slot with a new card
    if not p1handslot1.winfo_ismapped():
        player1_hand[0] = deck.pop()
        new_card = getImage(player1_hand[0][3])
        p1handslot1.config(image=new_card)
        p1handslot1.image = new_card
        p1handslot1.place(relx=0.42, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
    elif not p1handslot2.winfo_ismapped():
        player1_hand[1] = deck.pop()
        new_card = getImage(player1_hand[1][3])
        p1handslot2.config(image=new_card)
        p1handslot2.image = new_card
        p1handslot2.place(relx=0.5, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
    elif not p1handslot3.winfo_ismapped():
        player1_hand[2] = deck.pop()
        new_card = getImage(player1_hand[2][3])
        p1handslot3.config(image=new_card)
        p1handslot3.image = new_card
        p1handslot3.place(relx=0.58, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
        player1_hand.append(deck.pop())

#Waits for user to stop resizing the window before resizing all cards/images
def on_window_resize(event):
    global resize_timer
    if resize_timer:
        root.after_cancel(resize_timer)
    resize_timer = root.after(0, lambda: perform_resize())
    '''
    new_width = root.winfo_width()//12
    new_height = root.winfo_height()//5.3
    #Update label size in proportion to window size
    p1pick.place_configure(width=new_width, height=new_height)
    p2pick.place_configure(width=new_width, height=new_height)
    p1handslot1.place_configure(width=new_width, height=new_height)
    p2handslot1.place_configure(width=new_width, height=new_height)
    p1handslot2.place_configure(width=new_width, height=new_height)
    p2handslot2.place_configure(width=new_width, height=new_height)
    p1handslot3.place_configure(width=new_width, height=new_height)
    p2handslot3.place_configure(width=new_width, height=new_height)
    #Resize images to fit the new label size
    resize_image(None, p1pick, pilecard1img)
    resize_image(None, p2pick, pilecard1img)
    resize_image(None, p1handslot1, backofcard)
    resize_image(None, p2handslot1, backofcard)
    resize_image(None, p1handslot2, backofcard)
    resize_image(None, p2handslot2, backofcard)
    resize_image(None, p1handslot3, backofcard)
    resize_image(None, p2handslot3, backofcard)
'''
#Rotates the trump card
def rotateImg(card, imgpath, angle):
    img = Image.open(imgpath)
    rotated_img = img.rotate(angle, expand=True)
    rotated_img = rotated_img.resize((screen_height//6, screen_width//12), Image.BICUBIC)
    photo=ImageTk.PhotoImage(rotated_img)
    card.config(image=photo)
    card.image = photo

#Game variables (cards and suits and player decks/totals)
suits = ['Coins', 'Cups', 'Clubs', 'Swords']
values2 = {
    'ace': 11,
    '3': 10,
    'king': 4,
    'knight': 3,
    'jack': 2,
}

#The 2 piles will be updated everytime a card is played and will hold 1 card value at a time
pile1 = []
pile2 = []
#The 2 hands will hold 3 cards at a time, until the deck is empty and they start emptying their hand
player1_hand = []
player2_hand = []
player1_total = 0
player2_total = 0

#Timer variable for resizing the window
resize_timer = None

#Creates the deck of cards and organises them by suit and value, card value and image location
cards_location = os.path.dirname(os.path.realpath(__file__))+'/assets/cards/'
cards_images_locations = glob.glob(os.path.join(cards_location, '*.png'))
cards = glob.glob(os.path.join(cards_location, '*.png'))
backofcard = os.path.dirname(os.path.realpath(__file__))+'/assets/backofcard.png'
pilecard1img = os.path.dirname(os.path.realpath(__file__))+'/assets/clubs_2.png'
getCards(cards)
deck = createDeck()
trumpdetails = deck.pop()

#Starts both players with 3 cards each)
for i in range(3):
    player1_hand.append(deck.pop())
    player2_hand.append(deck.pop())

#Base GUI Variables
root = TkinterDnD.Tk()
root.title("Briscola")
root.config(bg='green')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}')

#Get images of all cards to be shown such as back and front of cards, trump card etc.
backofcardimg = getImage(backofcard)
trumpimg = getImage(trumpdetails[3])

#Currently a temp variable for front of card
pile = getImage(pilecard1img)
p1img1=getImage(player1_hand[0][3])
p1img2=getImage(player1_hand[1][3])
p1img3=getImage(player1_hand[2][3])

#Buttons to place and display the cards
p1handslot1 = Label(image=p1img1, borderwidth=0)
p1handslot2 = Label(image=p1img2, borderwidth=0)
p1handslot3 = Label(image=p1img3, borderwidth=0)
p2handslot1 = Label(image=backofcardimg, borderwidth=0)
p2handslot2 = Label(image=backofcardimg, borderwidth=0)
p2handslot3 = Label(image=backofcardimg, borderwidth=0)
deckImg = Label(image=backofcardimg, borderwidth=0)
trump = Label(image=trumpimg, borderwidth=0)
rotateImg(trump, trumpdetails[3], 90)
p1pick = Label(image=pile, borderwidth=0)
p2pick = Label(image=pile, borderwidth=0)

#Bind the cards to a function when pressed
p1handslot1.bind("<ButtonRelease-1>", lambda event: on_click(p1handslot1))
p1handslot2.bind("<ButtonRelease-1>", lambda event: on_click(p1handslot2))
p1handslot3.bind("<ButtonRelease-1>", lambda event: on_click(p1handslot3))
#Need to add functionality for deck card
deckImg.bind("<ButtonRelease-1>", lambda event: deckClick())

#Place the buttons in position
p1handslot1.place(relx=0.42, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
p2handslot1.place(relx=0.42, rely=0.2, anchor="center", width=screen_width // 12, height=screen_height // 6)
p1handslot2.place(relx=0.5, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
p2handslot2.place(relx=0.5, rely=0.2, anchor="center", width=screen_width // 12, height=screen_height // 6)
p1handslot3.place(relx=0.58, rely=0.8, anchor="center", width=screen_width // 12, height=screen_height // 6)
p2handslot3.place(relx=0.58, rely=0.2, anchor="center", width=screen_width // 12, height=screen_height // 6)
deckImg.place(relx=0.1, rely=0.5, anchor="center", width=screen_width // 12, height=screen_height // 6)
trump.place(relx=0.193, rely=0.5, anchor="center", width=screen_height // 6, height=screen_width // 12)
p1pick.place(relx=0.45, rely=0.5, anchor="center", width=screen_width // 12, height=screen_height // 6)
p2pick.place(relx=0.55, rely=0.5, anchor="center", width=screen_width // 12, height=screen_height // 6)

#Calls a function to resize all labels/images when the window is resized
root.update()
root.bind('<Configure>', on_window_resize)
root.mainloop()