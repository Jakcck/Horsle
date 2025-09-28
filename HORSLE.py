import tkinter as tk
import time
import threading


answer = 'horse'


root = tk.Tk()

kb_Frame = tk.Frame(root)
kb_1 = tk.Frame(kb_Frame)
kb_2 = tk.Frame(kb_Frame)
kb_3 = tk.Frame(kb_Frame)

header = tk.Label(root, text = '')
text=''

header.pack(side = 'top')

# def label():
#     global text
#     print("thread started")
#     try:
#         while True:
#             if not text=='': 
#                 s_time = time.time()
#                 cur = text
#                 time.sleep(1)
#                 if cur==text: message('')
#     except:
#         quit()

def label():
    try:
        global header
        header['text'] = ''
    except:
        quit()



def message(input):
    global t
    global header
    header['text'] = input
    t = threading.Timer(3, label)
    t.start()




row1 = "qwertyuiop"
row2 = "asdfghjkl"
row3 = "zxcvbnm"
rows = [row1, row2, row3]




G_num = 1
L_cur = 1

ls = [[], [], [], [], [], []]
guess = ""

def check(g, a):
    r=[]
    gT = g
    ind = -1
    i = -1

    for i in range(0, len(a)):
        if gT[i]==a[i]:  
            r.append(3) #green
            a=(a[:i] + " " + a[i+1:])
            gT=(gT[:i] + " " + gT[i+1:])
        elif a.find(gT[i])==-1: 
            r.append(1) #gray
            gT=(gT[:i] + " " + gT[i+1:])
        else: r.append(0) #potential yellow
        gT=(gT[:i] + " " + gT[i+1:])

    while True:
        try: i = r.index(0) #index of character
        except: break #finish for loop
        ind = a.find(g[i])
        if ind != -1: r[i]=2 #yellow
        else: r[i]=1 #gray
        a=(a[:ind] + " " + a[ind+1:])
        g=(g[:i] + " " + g[i+1:])

    
    return r

def colour_fill(gN, gues, res):
    global bt
    colour_dict = {
        1: 'gray',
        2: 'yellow',
        3: 'green'
    }

    for l in ls[gN]:
        i = ls[gN].index(l)
        
        l['bg'] = colour_dict[res[i]]
        bt[gues[i]]['bg'] = colour_dict[res[i]]
        
    return   




def press(letter):
    global L_cur
    global G_num
    global guess
    global answer
    
    if letter == '\r':
        if L_cur == 6: 
            if guess.isalpha() and len(guess) == 5:
                g = guess.lower()
                G_num+=1
                L_cur = 1
                result = check(g, answer)
                colour_fill(G_num-2, guess, result)
                guess = ''
                if G_num == 7:
                    message(f'you lost, the word was {answer}')
                elif result == [3, 3, 3, 3, 3]:
                    G_num = 7
                    message('you win doofus')
                return
        guess = ""
        L_cur = 1
        for label in ls[G_num-1]:
            label['text'] = '    '
        return
    elif letter == '\x08':
        if L_cur == 1:
            return
        ls[G_num-1][L_cur-2]['text'] = '     '
        guess = guess[0:len(guess)-1]
        L_cur -= 1
        return
    
    if not letter.isalpha(): 
        message('enter a letter doofus')
        return
    
    elif L_cur == 6:
        return
    ls[G_num-1][L_cur-1]['text'] = f'  {letter}  '
    guess += letter
    L_cur += 1
    

    


bt = {}
for row in rows:
    for l in row: 
        if row==row1: fr=kb_1
        elif row==row2: fr=kb_2
        elif row==row3: fr=kb_3
        bt[l] = tk.Button(fr, text=l, command=lambda l=l: press(l), width=3 , height=3)
        bt[l].pack(side="left")
# r = [1,2,3,2,1]
# colour_map = {
#     1: 'gray',
#     2: 'yellow',
#     3: 'green'
# }
# for i in r:
#     bt[guess[i]]['bg'] = colour_map[i]
    

kb_1.pack()
kb_2.pack()
kb_3.pack()
kb_Frame.pack(side = "bottom")


g_Frame = tk.Frame(root)

for x in range(5):
    for y in range(6):
        ls[y].append(tk.Label(g_Frame, border=2, text=(f'     '), width=3, height=2, padx=10, pady=10, highlightthickness=2, highlightbackground = "gray", highlightcolor= "gray"))
        ls[y][-1].grid(column=x, row=y)  

g_Frame.pack(side="top", pady=40,padx=20)

def key_pressed(event):
    if (event.char) == '\x1b':
        root.destroy()
        try:
            t.cancel()
        except:
            print("f")
        quit()
    if not G_num == 7: press(event.char)
    time.sleep(0.1)
 

root.bind("<Key>",key_pressed)
          
root.mainloop()

