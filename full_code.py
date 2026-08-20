from customtkinter import *
from tkinter import *
from ollama import Client
from pathlib import Path
from threading import Thread
import json

PARENT = Path(__file__).parent.resolve()
SAVEFILE = PARENT / 'Messages.json'
if not SAVEFILE.exists():
    with open(SAVEFILE , 'w') as f:
        json.dump({},f)

class messagebox:
    def __init__(self , master , send_command=None):
        self.master = master
        self.send_bool = True
        self.frame , self.textbox , self.scrlbar , self.canvas , self.oval , self.placeholder= [None]*6
        self.text = ''
        self.send_command = send_command
    def initialize_shapes(self):
        self.frame = CTkFrame(self.master , corner_radius=25 , border_color='black' , border_width=2 , fg_color='white')
        self.textbox = Text(self.frame, height =1, border=0, font=('Noto Sans' , 17) , wrap='word',width = 40)
        self.scrlbar = CTkScrollbar(self.frame,command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=self.scrlbar.set)
        self.canvas = Canvas(self.frame , width=39 , height=39 , bg='white' ,  borderwidth = 0 , highlightthickness=0)
        self.oval = self.canvas.create_oval(2,2,38,38 , fill='blue',outline="")
        self.placeholder = Label(self.frame , border=0 , text='Type a message...' , fg='grey' , font=('Noto Sans' ,16) , bg='white')
        self.canvas.create_text(21,21 , text='➤' , font=('Noto Sans' , 17) , fill='white')
    def place_components(self):
        self.frame.pack(pady = 15 , side = 'bottom' , padx = 10 )
        self.textbox.pack(pady =(9,8) , padx=(13,5), side='left')
        self.canvas.pack(pady = (4,5), padx=(0,11), side='bottom',anchor='e')
        self.frame.update()
        self.frame.pack_forget()
        self.frame.place(x=(self.master.winfo_width()-self.frame.winfo_width()-40)/2 , y=self.master.winfo_screenheight()-135)
    def hover(self , e=None):
        if e.type == '7' :
            self.canvas.itemconfigure(self.oval, fill = "#6AC5EE")
        else :
            self.canvas.itemconfigure(self.oval, fill = 'blue')
    def click(self , e=None):
        if self.send_bool:
            self.canvas.itemconfigure(self.oval, fill = 'blue')
            self.master.after(100 , lambda : self.canvas.itemconfigure(self.oval, fill = "#6AC5EE"))
            text = self.textbox.get('1.0' , 'end-1c').strip()
            if text != '' :
                self.send_command(text)
                self.textbox.delete('1.0' , 'end')
                self.update_messagebox()
                self.send_bool = False
    def update_height(self):
        lines = self.textbox.count('1.0' , 'end-1c' , 'displaylines' , return_ints=True)
        self.frame.place_configure(x=(self.master.winfo_width()-self.frame.winfo_width()-40)/2 , y=self.master.winfo_screenheight()-135-(min(lines , 8)*26))
        self.textbox['height'] = min(lines+1 , 9)
        if lines+1 > 9 :
            self.scrlbar.pack(side = 'top' , anchor = 'e' , padx = (0,17) , pady = (2,5))
        else:
            self.scrlbar.pack_forget()
    def update_placeholder(self , e=None):
        text = self.textbox.get('1.0' , 'end-1c')
        if text == '':
            self.textbox.focus_set()
            self.placeholder.place(x=16,y=11)
            self.textbox.mark_set('insert' , '1.0')
        else:
            self.placeholder.place_forget() 
    def update_messagebox(self , e=None):
        self.master.after_idle(self.update_height)
        self.master.after_idle(self.update_placeholder)
    def m(self , e=None):
        self.textbox.delete('1.0' , 'end')
        self.update_messagebox()
    def cmd(self):
        self.master.after(500 , self.m)
    def enter(self , e=None):
        if e and e.state & 0x0001:
            self.update_messagebox()
        else :
            self.click()
            self.master.after(200 , lambda: self.canvas.itemconfigure(self.oval, fill = 'blue'))
            return 'break'
    def binds(self):
        self.update_placeholder()
        self.textbox.bind('<KeyPress>' , self.update_messagebox , add='+')
        self.placeholder.bind('<Button-1>' , self.update_placeholder)
        self.canvas.bind('<Enter>' , self.hover)
        self.canvas.bind('<Leave>' , self.hover)
        self.canvas.bind('<Button-1>' , self.click)
        self.textbox.bind('<Return>' , self.enter , add='+')
    def send(self):
        self.send_bool = True
    def main(self):
        self.initialize_shapes()
        self.place_components()
        self.binds()
class header:
    def __init__(self,master , color):
        self.master = master
        self.frame , self.avatar , self.textframe = [None]*3
        self.photo = PhotoImage(file=PARENT / 'bot.png')
        self.color = color
    def font(self , size):
        return 'Cascadia Code' , size , 'bold'
    def initialize(self):
        self.frame = CTkFrame(self.master , fg_color=self.color , corner_radius=10 , width=1000 , height=90)
        self.avatar = CTkCanvas(self.frame , width=70 , height=70 , bg=self.color , borderwidth = 0 , highlightthickness=0)
        self.textframe = CTkFrame(self.frame , fg_color=self.color)
        shrink = 9
        self.photo = self.photo.subsample(shrink,shrink)
        self.avatar.create_image(35, 35,image=self.photo)
    def placeall(self):
        self.frame.pack( padx = 5 , pady = (3,5))
        self.frame.pack_propagate(False)
        self.avatar.pack(side='left' , padx=10 , pady=10)
        self.textframe.pack(side='left' , padx=5)
        CTkLabel(self.textframe , text='Local AI' , font=self.font(17) , fg_color=self.color , text_color='white').pack(padx = 1 , pady=5)
        CTkLabel(self.textframe , text='● Online' , font=self.font(15) , fg_color=self.color , text_color="#29B805").pack(padx = 1)
    def main(self):
        self.initialize()
        self.placeall()

class chat_display:
    def __init__(self , master):
        self.AIreply , self.frame  , self.spaceframe = [None]*3
        self.master = master
    def initialize_and_place_frame(self):
        self.frame = CTkScrollableFrame(self.master , fg_color='white')
        self.frame.pack(fill = 'both' , expand = True)
        self.spaceframe = CTkFrame(self.frame , height=75 , fg_color='white' , border_width=1 , border_color='black')
        self.spaceframe.pack(side='bottom' , fill = 'x')
        #self.AIreply = Text(self.frame , wrap='word' , bg='white' , font=('Segoe UI' , 15 , 'bold') , fg='black' , width=60 , border=0)
    def add_user_message(self, user_text):
        maxwidth = 1
        for line in user_text.splitlines():
            maxwidth = max(len(line), maxwidth)
        userframe = CTkFrame(self.frame,fg_color='white',border_color='black',border_width=2,corner_radius=25)
        user_message = Text(userframe,wrap='word',bg='white',fg='black',border=0,height=1,width=min(maxwidth, 40),
                           font=('Segoe UI', 14, 'bold'),
                           padx=0 , pady=0)
        user_message.pack(padx=10, pady=10)
        userframe.pack(anchor='e' , padx = 5 , pady = 5)
        user_message.insert('1.0', user_text)
        user_message.update_idletasks()
        height = user_message.count('1.0','end-1c','displaylines',return_ints=True)
        user_message.configure(height=height+1,state='disabled')
    
set_appearance_mode('light')
win = Tk()
win.configure(bg='white')
fframe = CTkFrame(win , fg_color='white')
fframe.pack(fill='y' , padx = 5 , expand = True)
win.state('zoomed')
win.update()
h = header(fframe , "#0B1F3A")
h.main()
main = chat_display(fframe)
main.initialize_and_place_frame()
messagebox(fframe , main.add_user_message).main()
win.mainloop()
