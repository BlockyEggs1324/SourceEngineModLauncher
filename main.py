import base64
import os
import tkinter as tk
from tkinter import messagebox

default_gamepath = r"C:/Program Files (x86)/Steam/steamapps/common/Half-Life 2/hl2.exe"

default_modpath = r"C:/Program Files (x86)/Steam/steamapps/sourcemods/"


class Mod():

  def __init__(self,modname, modpath=default_modpath,gamepath=default_gamepath):
    self.modpath = modpath
    self.gamepath = gamepath
    self.name = modname   

mods = []

class App(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Source Engine Mod Launcher and Manager")
    self.geometry("680x400")
    self.resizable(False, False)
    self.configure(bg="#F0F0F0")
    self.create_widgets()

  def create_widgets(self):
    self.launchbutton = tk.Button(self,text="Launch Mod",font=("Arial", 16),bg="#F0F0F0",fg="black",command=lambda: self.launch_mod(),borderwidth="0",highlightbackground="#F0F0F0")
    self.launchbutton.place(relx=1, rely=1, anchor="se", bordermode="outside")
    self.addbutton = tk.Button(self,text="Add Mod",font=("Arial", 16),bg="#F0F0F0",fg="black",command=lambda: self.add_mod(),borderwidth="0",highlightbackground="#F0F0F0")
    
    self.addbutton.place(x="1", y="3", anchor="nw", bordermode="outside")

    self.mod_listbox_name = tk.Listbox(self,
    font=("Arial", 7),
    bg="#FFFFFF",
    fg="#333333",
    selectbackground="#F0F0F0",
    selectforeground="black")

    self.mod_listbox_name.place(x="1", y="45", width="225", height="310")

    self.mod_listbox_modpath = tk.Listbox(self,
      font=("Arial", 7),
      bg="#FFFFFF",
      fg="#333333",
      selectbackground="#F0F0F0",
      selectforeground="black")
    
    self.mod_listbox_modpath.place(x="225", y="45", width="225", height="310")

    self.mod_listbox_gamepath = tk.Listbox(self,
      font=("Arial", 7),
      bg="#FFFFFF",
      fg="#333333",
      selectbackground="#F0F0F0",
      selectforeground="black")

    self.mod_listbox_gamepath.place(x="450", y="45", width="225", height="310")
    
    self.save_button = tk.Button(self,
    text="Save Mods",
    font=("Arial", 16),
    bg="#F0F0F0",
    fg="black",
    command=lambda: self.save_mods(),
    borderwidth="0",
    highlightbackground="#F0F0F0")
    
    self.save_button.place(x="300", y="3", bordermode="outside")
    for mod in self.load_mods():
      mods.append(mod)
    for mod in mods:
      self.mod_listbox_name.insert(tk.END, mod.name)
      self.mod_listbox_gamepath.insert(tk.END, mod.gamepath)
      self.mod_listbox_modpath.insert(tk.END, mod.modpath)
      
    
    

    self.save_button = tk.Button(self,text="Save Mods",font=("Arial", 16),bg="#F0F0F0",fg="black",command=lambda: self.save_mods())
      

  def add_mod(self):
    global modwindow
    modwindow = tk.Toplevel(self)
    modwindow.geometry("400x230")
    modwindow.title("Create a mod to launch")
    modwindow.resizable(False, False)

    # Default Paths
    self.default_gamepathvar = tk.StringVar()
    self.default_gamepathvar.set(
        r"C:/Program Files (x86)/Steam/steamapps/common/Half-Life 2/hl2.exe")

    self.default_modpathvar = tk.StringVar()
    self.default_modpathvar.set(
        r"C:/Program Files (x86)/Steam/steamapps/sourcemods/")

    self.namevar = tk.StringVar()

    self.namevar.set("Mod name")
    # Mod path
    modpathlabel = tk.Label(modwindow, text="Path to mod folder:")
    modpathlabel.pack()

    modpathbox = tk.Entry(modwindow,
                          font=("Arial", 8),
                          bg="#FFFFFF",
                          fg="#333333",
                          width="50",
                          text=self.default_modpathvar)
    modpathbox.pack(pady=10)

    # Game path
    gamepathlabel = tk.Label(modwindow, text="Path to game exe:")
    gamepathlabel.pack()

    gamepathbox = tk.Entry(modwindow,
      font=("Arial", 8),
      bg="#FFFFFF",
      fg="#333333",
      width="50",
      text=self.default_gamepathvar)
    gamepathbox.pack(pady=10)
    # Name
    namelabel = tk.Label(modwindow, text="Mod Name:")
    namelabel.pack()

    namebox = tk.Entry(modwindow,
      font=("Arial", 10),
      bg="#FFFFFF",
      fg="#333333",
      width=35,
      text=self.namevar)
    namebox.pack(pady=10)

    createbutton = tk.Button(
      modwindow,
      text="Create",
      font=("Arial", 16),
      bg="#F0F0F0",
      command=lambda:self.create_mod(namebox.get(), modpathbox.get(),gamepathbox.get()))
    createbutton.place(relx=1, rely=1, anchor="se", bordermode="outside")

  def create_mod(self, modname, modpath, gamepath):
    global mods
    if gamepath == "":
      messagebox.showerror("Error", "No gamepath set")
    if modpath == "":
      messagebox.showerror("Error", "No modpath set")
    if modname == "":
      messagebox.showerror("Error", "No name set")

    if gamepath and modname and modpath != "":
      if self.checkformod(modname):
        self.close_mod_window = True  # Set flag to close window
        modwindow.destroy()
        local_mods = mods
        mods = []
        for mod in local_mods:
          mods.append(mod)
        mods.append(Mod(modname, modpath, gamepath))
        self.mod_listbox_name.insert(tk.END, modname)
        self.mod_listbox_gamepath.insert(tk.END, gamepath)
        self.mod_listbox_modpath.insert(tk.END, modpath)
      else:
        if messagebox.askyesno("Name is already in mods", "The name you entered is already in the list of mods. Do you want to add anyway?"):
          self.close_mod_window = True  # Set flag to close window
          mods.append(Mod(modname, modpath, gamepath))
          self.mod_listbox_name.insert(tk.END, modname)
          self.mod_listbox_gamepath.insert(tk.END, gamepath)
          self.mod_listbox_modpath.insert(tk.END, modpath)
        else:
          self.close_mod_window = False  # Don't close the window

      if self.close_mod_window:
        modwindow.destroy()  # Close the window after message box interaction
          

  def launch_mod(self):
    print(mods)
    mod = self.mod_listbox_name.curselection()
    mod = mod[0]
    mod = mods[mod]
    os.startfile(mod.gamepath, "open", f'-game "{mod.modpath}"')

  def save_mods(self):
    if mods != []:
        encoded_mods = [
            base64.b64encode(
                str([
                    mod.name.encode(),
                    mod.modpath.encode(),
                    mod.gamepath.encode()
                ]).encode()).decode() for mod in mods
        ]
        with open("mods.dat", "w") as f:
            f.write(str(encoded_mods))
    else:
        messagebox.showerror("Error", "No mods to save.")

  def load_mods(self):
      mods = []  # Assign the loaded mods to the mods variable
      if os.path.exists("mods.dat"):
        with open("mods.dat", "r") as f:
          file = f.read()
          if file:
            if str(file) != "" or "[]":
              encoded_mods_str = file.strip('[]')
              encoded_mods = encoded_mods_str.split(', ')
              for encoded_mod in encoded_mods:
                decoded_mod = base64.b64decode(encoded_mod.encode()).decode()
                print(decoded_mod)
                mod_data = eval(decoded_mod)
                name, modpath, gamepath = mod_data
                mods.append(Mod(name, modpath, gamepath))
            else:
              messagebox.showwarning("Mods file empty", "The 'mods.dat' file exists but has no data.")
      
        return mods

      else:
        return []

  def checkformod(self, modname):
    global mods
    modcheck = bool(False)
    for mod in mods:
      if mod.name == modname:
        modcheck = True
      else:
        if not modcheck:
          modcheck = False

    if not mods:
      modcheck = True
  
    return modcheck

  def list_mods(self):
    for mod in mods:
      print(mod)

    len(mods)
    print(not mods)
    
# Launch the app

if __name__ == "__main__":
  app = App()
  app.mainloop()
