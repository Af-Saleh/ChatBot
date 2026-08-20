class chat_display:
    def __init__(self , master , enable_chat=None , sendreq = None):
        self.AIreply , self.frame  , self.spaceframe = [None]*3
        self.master = master
        self.enable = enable_chat
        self.send = sendreq
    def initialize_and_place_frame(self):
        self.frame = CTkScrollableFrame(self.master , fg_color='white' , scrollbar_button_color='white' , scrollbar_button_hover_color="#BCBBBB")
        self.frame.pack(fill = 'both' , expand = True)
        self.spaceframe = CTkFrame(self.frame , height=75 , fg_color='white' , border_width=0 , border_color='black')
        self.spaceframe.pack(side='bottom' , fill = 'x')
    def add_user_message(self, user_text):
        maxwidth = 1
        for line in user_text.splitlines():
            maxwidth = max(len(line), maxwidth)
        userframe = CTkFrame(self.frame,fg_color='blue',border_color='black',border_width=0,corner_radius=25)
        user_message = Text(userframe,wrap='word',bg='blue',fg='white',border=0,height=1,width=min(maxwidth, 40),
                           font=('Cascadia Code', 14, 'bold'),
                           #Courier New
                           padx=0 , pady=0)
        user_message.pack(padx=10, pady=10)
        userframe.pack(anchor='e' , padx = 5 , pady = 5)
        user_message.insert('1.0', user_text)
        user_message.update_idletasks()
        height = user_message.count('1.0','end-1c','displaylines',return_ints=True)
        user_message.configure(height=height+1,state='disabled')
        self.send(user_text)
        self.frame._parent_canvas.yview_moveto(1.0)
    def create_place_ai_text(self):
        self.AIreply = Text(self.frame , wrap='word' , bg='white' , font=('Segoe UI' , 15 , 'bold') , fg='black' , width=82 , border=0 , height=1 , state='disabled')
        self.AIreply.pack(anchor='w')
    def add_ai_chunk(self , chunk):
        self.AIreply.configure(state='normal')
        self.AIreply.insert('end-1c' , chunk)
        self.AIreply.update_idletasks()
        height = self.AIreply.count('1.0' , 'end-1c' , 'displaylines' , return_ints=True)
        self.AIreply.configure(height=height+1 , state='disabled')
        self.frame._parent_canvas.yview_moveto(1.0)
    def stop(self):
        self.AIreply = None
        self.enable()
