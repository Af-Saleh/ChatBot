class header:
    def __init__(self,master , color):
        self.master = master
        self.frame , self.avatar , self.textframe = [None]*3
        self.photo = PhotoImage(file=PARENT / 'bot.png')
        self.color = color
    def font(self , size):
        return 'Cascadia Code' , size , 'bold'
    def initialize(self):
        self.frame = CTkFrame(self.master , fg_color=self.color , corner_radius=10)
        self.avatar = CTkCanvas(self.frame , width=70 , height=70 , bg=self.color , borderwidth = 0 , highlightthickness=0)
        self.textframe = CTkFrame(self.frame , fg_color=self.color)
        shrink = 9
        self.photo = self.photo.subsample(shrink,shrink)
        self.avatar.create_image(35, 35,image=self.photo)
    def placeall(self):
        self.frame.pack(side = 'top' , fill = 'x' , padx = 5 , pady = 5)
        self.avatar.pack(side='left' , padx=10 , pady=10)
        self.textframe.pack(side='left' , padx=5)
        CTkLabel(self.textframe , text='Local AI' , font=self.font(17) , fg_color=self.color , text_color='white').pack(padx = 1 , pady=5)
        CTkLabel(self.textframe , text='● Online' , font=self.font(15) , fg_color=self.color , text_color="#29B805").pack(padx = 1)
    def main(self):
        self.initialize()
        self.placeall()
