class historymanager:
    def __init__(self ,send_the_message = None):
        self.send = send_the_message
        self.data = None
        self.quest , self.ans = ['']*2
    def upload_data(self):
        with open(SAVEFILE) as f:
            self.data = json.load(f)
    def get_user_message(self , message):
        self.quest = message
    def get_ai_responce(self , airesp):
        self.ans = airesp
    def add(self):
        conv = {'user': self.quest , 'you' : self.ans}
        if len(list(self.data)) == 0 :
            self.data['0'] =  conv
        else:
            last = int(list(self.data)[-1])
            self.data[str(last+1)] = conv
        with open(SAVEFILE , 'w') as f:
            json.dump(self.data , f)
    def restart(self):
        self.add()
        self.quest , self.ans = ['']*2
    def remake(self):
        history = ''
        for conv in self.data.keys():
            history+= f'conversation {int(conv)+1} : \n'
            for person,res in self.data[conv].items():
                history += f'{person}: {res} '
            history += '\n'

        prompt = f"""
        You are a helpful AI assistant.
        Current user message: {self.quest}
        Conversation history: 
        {history}
        Use the conversation history only when it is relevant or necessary to answer the current user message.
        If the history is not relevant, ignore it.
        Maintain context when the user refers to something discussed earlier.
        Answer the current message directly and naturally.
        """
        self.send(prompt)
