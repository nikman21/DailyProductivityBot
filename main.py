import tkinter as tk
from tkinter import messagebox
from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()
# Load API key from .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise Exception('Please provide OPENAI_API_KEY in your .env file')

# Create OpenAI client with loaded API key
client = OpenAI(api_key=OPENAI_API_KEY)

class NavBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#282c34")

        # Create navigation buttons
        buttons = [
            ("Home", HomePage),
            ("Habit Tracker", HabitTracker),
            ("Chatbot", chatBot),
            ("Check-in", CheckInPage),
        ]

        for text, frame_class in buttons:
            button = tk.Button(
                self,
                text=text,
                command=lambda f=frame_class: controller.show_frame(f),
                font=("Arial", 12),
                fg="#61dafb",
                bg="#282c34",
            )
            button.pack(side="left", padx=10, pady=5)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.navbar = NavBar(self, controller)
        self.navbar.pack(side="top", fill="x")

        
        greeting_label = tk.Label(
            self,
            text="Welcome to Dailybot!",
            font=("Arial", 18, "bold"),
            fg="#61dafb",
            bg="#282c34",
        )
        greeting_label.pack(pady=20)
        
        

        
class HabitTracker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.navbar = NavBar(self, controller)
        self.navbar.pack(side="top", fill="x")

        greeting_label = tk.Label(
            self,
            text="Habit Tracker",
            font=("Arial", 18, "bold"),
            fg="#61dafb",
            bg="#282c34",
        )
        greeting_label.pack(pady=20)

        # Create input fields for each habit
        self.habit1_entry = self.create_habit_entry("Habit 1:")
        self.habit2_entry = self.create_habit_entry("Habit 2:")
        self.habit3_entry = self.create_habit_entry("Habit 3:")

        # Submit button
        submit_button = tk.Button(
            self,
            text="Submit",
            command=self.submit_habits,
            font=("Arial", 14),
            bg="#61dafb",
            fg="#282c34",
        )
        submit_button.pack(pady=20)

        self.result_label = tk.Label(
            self,
            text="",
            font=("Arial", 14),
            fg="#61dafb",
            bg="#282c34",
        )
        self.result_label.pack(pady=10)

    def create_habit_entry(self, habit_name):
        label = tk.Label(
            self,
            text=habit_name,
            font=("Arial", 12),
            fg="#61dafb",
            bg="#282c34",
        )
        label.pack(pady=5)

        entry = tk.Entry(self, width=40, font=("Arial", 12))
        entry.pack(pady=5)

        return entry

    def submit_habits(self):
        habit1 = self.habit1_entry.get()
        habit2 = self.habit2_entry.get()
        habit3 = self.habit3_entry.get()

        # You can add further logic or processing for the submitted habits

        self.result_label.config(text=f"Habit 1: {habit1}\nHabit 2: {habit2}\nHabit 3: {habit3}")

        
       
        

class chatBot(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.navbar = NavBar(self, controller)
        self.navbar.pack(side="top", fill="x")

        greeting_label = tk.Label(
            self,
            text="Chatbot",
            font=("Arial", 18, "bold"),
            fg="#61dafb",
            bg="#282c34",
        )
        greeting_label.pack(pady=20)

        # Text entry for user input
        self.user_input = tk.Entry(self, width=40, font=("Arial", 12))
        self.user_input.pack(pady=10)

        # Button to submit user input
        submit_button = tk.Button(
            self,
            text="Submit",
            command=self.submit_user_input,
            font=("Arial", 14),
            bg="#61dafb",
            fg="#282c34",
        )
        submit_button.pack(pady=20)

        # Label to display chat history
        self.chat_history = tk.Label(
            self,
            text="",
            font=("Arial", 12),
            fg="#61dafb",
            bg="#282c34",
        )
        self.chat_history.pack(pady=10)

    def submit_user_input(self):
        user_input = self.user_input.get()

        # Format the user input as a message for OpenAI
        user_message = {"role": "user", "content": user_input}

        # Create prompt with the user's input
        prompt = [
            {"role": "system", "content": "You are a helpful assistant."},
            user_message,
        ]

        # Make an API call to GPT-3
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
        )

        # Get the generated response from GPT-3
        gpt_response = response.choices[0].message.content

        # Display the user input and GPT-3 response
        chat_history_text = f"User: {user_input}\nAssistant: {gpt_response}"
        self.chat_history.config(text=chat_history_text)
        

        

# Define the CheckInPage class
class CheckInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.navbar = NavBar(self, controller)
        self.navbar.pack(side="top", fill="x")


        greeting_label = tk.Label(
            self,
            text="Dailybot Morning Check-in",
            font=("Arial", 18, "bold"),
            fg="#61dafb",
            bg="#282c34",
        )
        greeting_label.pack(pady=20)

        # Create input fields for each question
        self.task_entry = self.create_input_field("3 Tasks that need to be done today")
        self.dream_entry = self.create_input_field("Did you have a dream last night?")
        self.skill_entry = self.create_input_field("Is there any specific skill or knowledge you want to enhance today?")
        self.positive_entry = self.create_input_field("What's one positive thing you're looking forward to today?")

        # Submit button
        submit_button = tk.Button(
            self,
            text="Submit",
            command=self.submit_response,
            font=("Arial", 14),
            bg="#61dafb",
            fg="#282c34",
        )
        submit_button.pack(pady=20)

        self.result_label = tk.Label(
            self,
            text="",
            font=("Arial", 14),
            fg="#61dafb",
            bg="#282c34",
        )
        self.result_label.pack(pady=10)

    def create_input_field(self, question):
        label = tk.Label(
            self,
            text=question,
            font=("Arial", 12),
            fg="#61dafb",
            bg="#282c34",
        )
        label.pack(pady=5)

        entry = tk.Entry(self, width=40, font=("Arial", 12))
        entry.pack(pady=5)

        return entry

    def submit_response(self):
        task_response = self.task_entry.get()
        dream_response = self.dream_entry.get()
        skill_response = self.skill_entry.get()
        positive_response = self.positive_entry.get()

        prompt = [
            {"role": "system", "content": "Act as a productivity guru and life coach. Be motivating and give suggestions based on the user's response for tasks break down each task offer ways to complete and knowledge about the tasks list them out, dream you should offer insight based of their response, for what they want to learn you should offer resources, knowledge and a plan to learn with assignments, lastly their positive response you should give positive feedback and let them know why that is a good thing to be looking forward to:"},
            {"role": "user", "content": f"1. Tasks: {task_response}"},
            {"role": "user", "content": f"2. Dream: {dream_response}"},
            {"role": "user", "content": f"3. Skill: {skill_response}"},
            {"role": "user", "content": f"4. Positive: {positive_response}"},
        ]

        # Make an API call to GPT-3
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
        )

        # Get the generated suggestion from GPT-3
        gpt_suggestion = response.choices[0].message.content

        # Display the GPT-3 suggestion in a pop-up window
        messagebox.showinfo("GPT-3 Suggestion", gpt_suggestion)

        self.result_label.config(text=f"Task: {task_response}\nDream: {dream_response}\nSkill: {skill_response}\nPositive: {positive_response}")

# Define the SampleApp class
class App(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # Container to hold all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frames
        self.frames = {}

        # Create and add frames to the dictionary
        for F in (HomePage, HabitTracker, chatBot, CheckInPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial page
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



if __name__ == "__main__":
    app = App()
    app.geometry("600x600")
    app.title("Dailybot")
    app.mainloop()



