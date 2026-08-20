class AI:
    def __init__(self ,master, start = None , stream = None , end = None  , send_ans = None):
        self.start = start
        self.stream = stream
        self.end = end
        self.ai = Client()
        self.master = master
        self.send = send_ans
    def get_ai_reply(self , message):
        answer = self.ai.chat(
            model='Qwen2.5',
            messages=[{'role' : 'user' , 'content' : message}],
            stream=True
        )
        ans = ''
        for chunk in answer:
            ans += chunk['message']['content']
            self.master.after(0 , lambda content = chunk['message']['content'] : self.stream(content))
        self.master.after(0, self.end)
        self.master.after(0, lambda: self.send(ans))
    def aireply(self , message):
        self.start()
        ans = Thread(target=lambda : self.get_ai_reply(message))
        ans.start()
