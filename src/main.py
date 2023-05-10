import random
import tkinter as tk
from tkinter import ttk
import os
from src.custom_text import CustomText
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
FONT = "Arial"
WHITESPACE_CHAR = u"\u00B7"
INPUT_PATH = os.path.join("..", "input")


class Game:
    root: tk.Tk
    sentence_label: tk.Text
    input_field: CustomText
    package_dropdown: ttk.OptionMenu
    sentences: list[str]
    current_sentence: str

    def __init__(self):
        self.setup_window()

        self.sentence_label = tk.Text(self.root, state="disabled", font=FONT, padx=10, pady=10, height=10, wrap=tk.WORD)
        self.input_field = CustomText(self.root, padx=10, pady=10, font=FONT, wrap=tk.WORD)
        self.setup_dropdown()
        self.pack_components()

        self.root.bind("<Return>", self.next_round)
        self.sentence_label.tag_config("red", background="salmon1")
        self.sentence_label.tag_config("green", background="OliveDrab1")
        self.input_field.bind("<<TextModified>>", self.onModified)

    def setup_window(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.title("TypeLearner")

    def setup_dropdown(self):
        options = [filename.strip(".txt").replace("_", " ") for filename in os.listdir(INPUT_PATH)]
        options.append("All")
        self.load_sentences("All")
        self.package_dropdown = ttk.OptionMenu(self.root, tk.StringVar(), "All", command=self.load_sentences, *options)

    def pack_components(self):
        self.package_dropdown.pack()
        self.sentence_label.pack(pady=10)
        self.input_field.pack(pady=10)

    def next_round(self, event):
        self.input_field.delete(1.0, tk.END)
        self.next_sentence()

        self.sentence_label.config(state="normal")
        self.sentence_label.delete(1.0, tk.END)
        self.sentence_label.insert(1.0, self.current_sentence)
        self.sentence_label.config(state="disabled")

    def next_sentence(self):
        if len(self.sentences) == 0:
            self.current_sentence = ""
            return
        self.current_sentence = self.sentences[random.randint(0, len(self.sentences) - 1)].strip("\n")

    def load_all(self):
        sentences = []
        for filename in os.listdir(INPUT_PATH):
            with open(os.path.join(INPUT_PATH, filename), "r", encoding="utf-8") as file:
                sentences.extend(file.readlines())
        self.sentences = sentences

    def load_sentences(self, selected_package: tk.StringVar):
        if (selected_package == "All"):
            self.load_all()
        else:
            filename = os.path.join(INPUT_PATH, f"{selected_package.replace(' ', '_')}.txt")
            with open(filename, "r", encoding="utf-8") as file:
                self.sentences = file.readlines()
        self.next_round(None)

    def onModified(self, event):
        input_text = self.input_field.get(index1=1.0, index2=tk.END)
        i = len(input_text) - 2
        try:
            if (self.current_sentence[i] != input_text[i]):
                self.sentence_label.tag_add("red", f"1.{i}")
            else:
                self.sentence_label.tag_add("green", f"1.{i}")

            self.sentence_label.tag_remove("red", f"1.{i+1}")
            self.sentence_label.tag_remove("green", f"1.{i+1}")

        except IndexError:
            print("IndexError input_field onModified")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Game().run()
    
