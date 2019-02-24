import json
from tkinter import (BOTH, DISABLED, END, INSERT, LEFT, NORMAL, RIGHT, YES,
                     Button, Canvas, E, Entry, Frame, Label, Menu, N, S,
                     Scrollbar, Text, Tk, W, X, Y)
import tools


class App:
    def __init__(self, master: Tk):
        self._master = master
        self._master.title("Monoalphabetische Substitution")
        self._mapping = list()
        self._ent = list()
        self._chars = set()
        with open("labels.json") as char_label_file:
            self._char_labels = json.loads(char_label_file.read())
            print(self._char_labels["\n"])

        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        """creates the intial widgets"""

        self._txt_input = Text(self._master)
        self._txt_input.grid(row=0, column=0, sticky=E+N, padx=5)
        self._txt_input.bind("<KeyRelease>", self._update_mapping_gui)

        self._txt_output = Text(self._master, state=DISABLED)
        self._txt_output.grid(row=0, column=1, sticky=W+N, padx=5)

        self._mapping_frame = Frame(self._master)
        self._mapping_frame.grid(row=1, column=0)

    def _create_menu(self):
        self._menu = Menu(self._master)
        self._master.config(menu=self._menu)
        self._master.option_add('*tearOff', False)

        self._menu_file = Menu(self._menu)
        self._menu.add_cascade(label="File", menu=self._menu_file)

        self._menu_file.add_command(
            label="Beispieltext laden", command=self._load_example)

    def _load_example(self) -> None:
        with open("esel.txt", "r") as file:
            tools.write_to_text(self._txt_input, file.read())
            self._update_mapping_gui()

    def _update_mapping_gui(self, *args) -> None:
        """
        updates the mapping gui (labels and entries)
        fired when the input text changes

        updates output automatically
        """
        old_chars = self._chars.copy()
        # all characters in the input
        self._chars = {c for c in self._txt_input.get("1.0", "end-1c")}

        # destroy mappings that aren't needed anymore
        for lbl, ent in self._mapping[:]:
            if tools.from_label(self._char_labels, lbl["text"]) not in self._chars:
                lbl.destroy()
                ent.destroy()
                self._mapping.remove((lbl, ent))
            else:
                lbl.place_forget()
                ent.place_forget()

        # create new mapping if they don't already exist
        for c in self._chars:
            if c not in old_chars:
                lbl = Label(self._mapping_frame,
                            text=tools.to_label(self._char_labels, c))
                ent = Entry(self._mapping_frame)
                ent.bind("<KeyRelease>", self._update_output)
                self._mapping.append((lbl, ent))
        self._mapping.sort(key=lambda m: m[0]["text"])

        row = 0
        i = 0
        for lbl, ent in self._mapping:
            lbl.grid(row=row, column=i*2, pady=2)
            ent.grid(row=row, column=i*2+1, pady=2)
            i += 1
            if i == 3:
                row += 1
                i = 0
        self._update_output(*args)

    def _update_output(self, *args) -> None:
        text = self._txt_input.get(1.0, "end-1c")
        mapping_dict = tools.create_mapping_dict(
            self._char_labels, self._mapping)

        # make widget writeable
        self._txt_output.config(state=NORMAL)
        self._txt_output.delete(1.0, END)
        for c in text:
            modified, char = tools.replace_char(mapping_dict, c)
            self._txt_output.insert("end", char)
            pos = self._txt_output.index(INSERT)
            prev_pos = pos.split(".")[0] + "." + str(int(pos.split(".")[1])-1)
            if modified:
                self._txt_output.tag_add("modified", prev_pos, pos)
        self._txt_output.tag_config(
            "modified", background="gray85")
        self._txt_output.see("end")
        # make widget unwriteable again
        self._txt_output.config(state=DISABLED)


root = Tk()
app = App(root)
root.geometry("1200x800")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.config({"padx": 20, "pady": 20})
root.mainloop()
