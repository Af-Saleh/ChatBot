class messagebox:
    def __init__(self , master , send_command=None):
        self.master = master
        self.running = True
        self.frame , self.textbox , self.scrlbar , self.canvas , self.oval , self.placeholder= [None]*6
        self.text = ''
        self.send_command = send_command
    def initialize_shapes(self):
        self.frame = CTkFrame(self.master , corner_radius=25 , border_color='black' , border_width=2 , fg_color='white')
        self.textbox = Text(self.frame, height =1, border=0, font=('Noto Sans' , 17) , wrap='word',width = 60)
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
    def hover(self , e=None):
        if e.type == '7' :
            self.canvas.itemconfigure(self.oval, fill = "#6AC5EE")
        else :
            self.canvas.itemconfigure(self.oval, fill = 'blue')
    def click(self):
        if self.running:
            self.canvas.itemconfigure(self.oval, fill = 'blue')
            self.master.after(50 , self.click)
        text = self.textbox.get('1.0' , 'end-1c').strip()
        if text != '': 
            self.text = text
            self.send_command(self.text)
            self.textbox.delete('1.0' , 'end')
            self.update_messagebox()
    def start(self , e=None):
        self.running = True
        self.click()
    def stop(self , e=None):
        self.running = False
        self.canvas.itemconfigure(self.oval, fill="#6AC5EE")
    def update_height(self):
        lines = self.textbox.count('1.0' , 'end-1c' , 'displaylines' , return_ints=True)
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
            self.start()
            self.stop()
            self.canvas.itemconfigure(self.oval, fill = 'blue')
            return 'break'
    def binds(self):
        self.update_placeholder()
        self.textbox.bind('<KeyPress>' , self.update_messagebox , add='+')
        self.placeholder.bind('<Button-1>' , self.update_placeholder)
        self.canvas.bind('<Enter>' , self.hover)
        self.canvas.bind('<Leave>' , self.hover)
        self.canvas.bind('<Button-1>' , self.start)
        self.canvas.bind('<ButtonRelease-1>' , self.stop)
        self.textbox.bind('<Return>' , self.enter , add='+')
    def main(self):
        self.initialize_shapes()
        self.place_components()
        self.binds()
