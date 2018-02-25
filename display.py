from tkinter import *
from tkinter import ttk
import threading

class Display(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def close(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.title("FM Helper")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Item :").grid(column=1, row=1, sticky=E)
        self.item = ttk.Label(self.mainframe, text="no item")
        self.item.grid(column=2, row=1, sticky=W)

        ttk.Label(self.mainframe, text="Rune :").grid(column=1, row=2, sticky=E)
        self.rune = ttk.Label(self.mainframe, text="no rune")
        self.rune.grid(column=2, row=2, sticky=W)

        self.lines = ttk.Frame(self.mainframe, padding="3 3 12 12")
        self.lines.grid(column=1, columnspan=2, row=3, sticky=E+W)

        ttk.Label(self.lines, text="Min").grid(column=1, row=1, sticky=W)
        ttk.Label(self.lines, text="Max").grid(column=2, row=1, sticky=W)
        ttk.Label(self.lines, text="Effet").grid(column=3, row=1, sticky=W)
        ttk.Label(self.lines, text="Poids").grid(column=4, row=1, sticky=W)
        for child in self.lines.winfo_children(): child.grid_configure(padx=5, pady=2)

        ttk.Label(self.mainframe, text="last ID :").grid(column=1, row=4, sticky=E)
        self.lastID = ttk.Label(self.mainframe, text="aucun")
        self.lastID.grid(column=2, row=4, sticky=W)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=2)

        self.root.mainloop()

    def test(self, lastID):
        self.lastID["text"] = str(lastID)

    def updateRune(self, rune):
        self.rune["text"] = rune.getName() + ' | ' + rune.getDescription() + ' (poids : ' + str(rune.getWeight()) + ')'

    def updateItem(self, item):
        self.item["text"] = item.getName() + ' (niveau : '+ str(item.getLevel()) +')'
        for widget in self.lines.winfo_children():
            if widget.grid_info()["row"] != 1:
                widget.destroy()
        row = 2
        for line in item.getLines():
            ttk.Label(self.lines, text=str(line.getMin())).grid(column=1, row=row, sticky=W)
            ttk.Label(self.lines, text=str(line.getMax())).grid(column=2, row=row, sticky=W)
            ttk.Label(self.lines, text=line.getDescription()).grid(column=3, row=row, sticky=W)
            ttk.Label(self.lines, text=str(line.getWeight()) + "/" + str(line.getMaxWeight())).grid(column=4, row=row, sticky=W)
            row+=1
        for child in self.lines.winfo_children(): child.grid_configure(padx=5, pady=2)
