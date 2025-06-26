import tkinter as tk
from tkinter import scrolledtext
import datetime
import random
import re

class CodBot:
    def __init__(self, root):
        self.root = root
        self.root.title("shreyas's buddy")
        self.root.geometry("500x600")
        self.root.config(bg="#f3f4f6")
        self.root.resizable(False, False)

        self.colors = {
            'bg': "#f3f4f6", 'user_bg': "#aecda0", 'bot_bg': "#7d8aff",
            'user_fg': "black", 'bot_fg': "#000000"
        }

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled',
                                                      font=("Segoe UI", 11), bg="white", fg=self.colors['bot_fg'])
        self.chat_display.place(x=10, y=10, width=480, height=520)

        self.user_input = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.user_input, font=("Segoe UI", 12))
        self.entry.place(x=10, y=540, width=370, height=35)
        self.entry.bind('<KeyRelease>', self.toggle_send)
        self.entry.bind('<Return>', self.send_event)

        self.send_btn = tk.Button(root, text="Send", command=self.send,
                                  font=("Georgia", 11, "bold"), bg=self.colors['user_bg'],
                                  fg=self.colors['user_fg'], activebackground="#1d4ed8", state='disabled')
        self.send_btn.place(x=390, y=540, width=100, height=35)

        self.intents = {
            "greeting": ["hi", "hello", "hey", "good morning", "good evening"],
            "farewell": ["bye", "goodbye", "see you", "take care"],
            "name": ["what's your name", "who are you", "your name"],
            "help": ["help", "what can you do", "assist", "support", "features", "commands"],
            "time": ["tell me the time", "what's the time", "current time", "time"],
            "date": ["what's the date today", "today's date", "what day is it"],
            "thanks": ["thank you", "thanks", "thx", "appreciate it"],
            "weather": ["weather", "temperature", "is it hot", "is it cold"],
            "joke": ["tell me a joke", "joke", "make me laugh"],
            "creator": ["who made you", "your developer","who created you"],
            "location": ["where are you from", "your location"],
            "mood": ["how are you", "how do you feel", "what's up"],
            "hobby": ["what do you like", "your hobbies"],
            "age": ["how old are you", "your age"],
            "language": ["which language do you speak", "language"],
            "education": ["what do you know", "are you smart"],
            "motivation": ["motivate me", "inspire me", "i need motivation"]
        }

        self.responses = {
            "greeting": "Hey there! How can I assist you today?",
            "farewell": "Goodbye! Take care and stay awesome! ",
            "name": "I’m shreyas's buddy, your assistant.",
            "help": "Here’s what I can do:\n- Tell time & date\n- Crack jokes\n- Motivate you\n- Share info about me!",
            "time": lambda: f"It's currently {datetime.datetime.now().strftime('%H:%M:%S')}.",
            "date": lambda: f"Today's date is {datetime.datetime.now().strftime('%d-%m-%Y')}.",
            "thanks": "You're welcome! ",
            "weather": "I'm not connected to real-time weather, but I hope it's sunny where you are!",
            "joke": lambda: random.choice([
                "Why don’t scientists trust atoms? Because they make up everything!",
                "Why did the computer show up late? It had a hard drive!",
                "What did one wall say to the other? 'I'll meet you at the corner!'"
            ]),
            "creator": "I was created by Shreyas for CodSoft internship!",
            "location": "I live in your computer – floating in memory!",
            "mood": "I'm always happy to chat! ",
            "hobby": "I enjoy processing words and making people smile!",
            "age": "I'm just a few thousand lines of code. Still young!",
            "language": "I speak Python  and simple English.",
            "education": "I’m rule-based but coded with smart logic!",
            "motivation": lambda: random.choice([
                "Believe in yourself. You’re capable of amazing things! ",
                "Every expert was once a beginner. Keep learning!",
                "Push yourself because no one else will!"
            ])
        }

        self.display("CodBot", "Hi! I'm CodBot. Ask me anything!")

    def toggle_send(self, _=None):
        self.send_btn.config(state='normal' if self.user_input.get().strip() else 'disabled')

    def send_event(self, _):
        self.send()

    def detect_intents(self, text):
        text = text.lower()
        return [intent for intent, keys in self.intents.items()
                if any(re.search(rf'\b{re.escape(k)}\b', text) for k in keys)]

    def generate_reply(self, intents):
        if not intents:
            return "Sorry, I didn't understand that. Try asking something else."
        return " ".join(
            self.responses[i]() if callable(self.responses[i]) else self.responses[i] for i in intents
        )

    def display(self, sender, msg):
        self.chat_display.config(state='normal')
        tag = 'user' if sender == "You" else 'bot'
        self.chat_display.insert(tk.END, f"{sender}: {msg}\n", tag)
        self.chat_display.tag_config('user', foreground=self.colors['user_fg'], background=self.colors['user_bg'],
                                     font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config('bot', foreground=self.colors['bot_fg'], background=self.colors['bot_bg'],
                                     font=("Segoe UI", 11))
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send(self):
        text = self.user_input.get().strip()
        if not text:
            return
        self.display("You", text)
        self.user_input.set("")
        self.send_btn.config(state='disabled')
        self.root.after(300, lambda: self.display("CodBot", self.generate_reply(self.detect_intents(text))))

if __name__ == "__main__":
    root = tk.Tk()
    CodBot(root)
    root.mainloop()
