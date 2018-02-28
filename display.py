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
        ttk.Label(self.lines, text="Modif").grid(column=4, row=1, sticky=W)
        ttk.Label(self.lines, text="Poids").grid(column=5, row=1, sticky=W)
        for child in self.lines.winfo_children(): child.grid_configure(padx=5, pady=2)

        ttk.Label(self.mainframe, text="Reliquat :").grid(column=1, row=4, sticky=E)
        self.reliquat = ttk.Label(self.mainframe, text="aucun")
        self.reliquat.grid(column=2, row=4, sticky=W)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=2)

        self.root.mainloop()

    def updateRune(self, rune):
        self.rune["text"] = rune.getName() + ' | ' + rune.getDescription() + ' (poids : ' + str(rune.getWeight()) + ')'

    def updateItem(self, item):
        self.item["text"] = item.getName() + ' (niveau : '+ str(item.getLevel()) +')'
        self.reliquat["text"] = self.myStr(item.getReliquat())
        if item.getLastReliquatModification() != 0:
            self.reliquat["text"] += ' (' + self.myStrWithSign(item.getLastReliquatModification()) + ')'
        for widget in self.lines.winfo_children():
            if widget.grid_info()["row"] != 1:
                widget.destroy()
        row = 2
        for line in item.getLines():
            ttk.Label(self.lines, text=str(line.getMin())).grid(column=1, row=row, sticky=W)
            ttk.Label(self.lines, text=str(line.getMax())).grid(column=2, row=row, sticky=W)
            ttk.Label(self.lines, text=line.getDescription()).grid(column=3, row=row, sticky=W)
            ttk.Label(self.lines, text=self.myStrWithSign(line.getLastModification())).grid(column=4, row=row, sticky=W)
            ttk.Label(self.lines, text=self.myStr(line.getWeight()) + "/" + self.myStr(line.getMaxWeight())).grid(column=5, row=row, sticky=W)
            if line.getLastModification() > 0:
                for widget in self.lines.winfo_children():
                    if widget.grid_info()["row"] == row:
                        widget['foreground'] = 'green'
            elif line.getLastModification() < 0:
                for widget in self.lines.winfo_children():
                    if widget.grid_info()["row"] == row:
                        widget['foreground'] = 'red'
            else:
                for widget in self.lines.winfo_children():
                    if widget.grid_info()["row"] == row:
                        widget['foreground'] = ''
            row+=1
        for child in self.lines.winfo_children(): child.grid_configure(padx=5, pady=2)

    def myStr(self, number):
        if number == int(number):
            return str(int(number))
        else:
            return "%.1f" % number

    def myStrWithSign(self, number):
        if number > 0:
            return ('+' + str(number))
        else:
            return str(number)
