import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

#--------------------------Global Variable---------------------

#--------------------------menu func-----------------------
def camera_toggle():
    print("Camera toggled")

def pen_mode():
    print("Pen mode selected")

def erase_mode():
    print("Erase mode selected")
def clear_canvas():
    print("clear_canvas selected")
 #--------------Camera----------------

#--------------export IMG----------------
def save_export():
    print("Save selected")

 #--------------team info window------------
def open_team_info(root):
    win = tk.Toplevel(root)
    win.title("Team Info")
    win.geometry("350x220")

    tk.Label(win, text="Team Members", font=("Arial", 14, "bold")).pack(pady=10)
    members = [
        "KeonLee - Hand/Finger Detection",
        "Nathan - Camera Input / Image Processing",
        "Nghia Dao - Drawing / Interaction Logic",
        "SungJoonAn - GUI"
    ]

    for m in members:
        tk.Label(win, text=m, font=("Arial", 11)).pack( padx=20)

    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)
 #--------------project info window------------
def open_project_info(root):
    win = tk.Toplevel(root)
    win.title("About Project")
    win.geometry("350x220")
    
    tk.Label(win, text="Image Processing", font=("Arial",14,"bold")).pack(pady=10)
    text = (
        "Project: Virtual Drawing\n"
        "Dev: 2025-11\n"
        
        "\nThis project allows users to draw using\n"
        "hand gestures captured through the camera"
    )
    tk.Label(win, text=text,font=("Arial", 10)).pack(fill="both", padx=20)
    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)
    

#---------------------------main UI----------------------
def main():
    global drawing_canvas
    
    window = tk.Tk()
    window.title("Virtual drawing App")
    window.geometry("600x800")
    window.resizable(False, False)
    
    
    
    #--------------Top menu bar------------
    top_menu = tk.Frame(window, height=50, bg="#e6e6e6")
    top_menu.pack(fill="x")
    
    #--------------option menu-------------
    option_btn = tk.Button(top_menu, text="Option", width=10)
    option_btn.pack(side="left",padx= 10, pady=10)
    
    def open_option_menu(event):
        x = option_btn.winfo_rootx()
        y= option_btn.winfo_rooty() + option_btn.winfo_height()
        option_menu.post(x, y)
        
    option_btn.bind("<ButtonRelease-1>",open_option_menu)
    
    
    
    #--------------option popup menu-----------
    option_menu = tk.Menu(window)
    option_menu.add_command(label="Camera On/Off", command=camera_toggle)
    option_menu.add_command(label="Save/Export", command=save_export)
    
    #--------------draw menu-------------------
    draw_btn = tk.Button(top_menu, text="Draw", width=10)
    draw_btn.pack(side="left",padx = 10, pady=5)
    
    def open_draw_menu(event):
        x = draw_btn.winfo_rootx()
        y= draw_btn.winfo_rooty() + draw_btn.winfo_height()
        draw_menu.post(x, y)
        
    draw_btn.bind("<ButtonRelease-1>",open_draw_menu)
    
    #--------------draw popup menu-------------
    draw_menu = tk.Menu(window)
    draw_menu.add_command(label="Pen Mode", command=pen_mode)
    draw_menu.add_command(label="Erase Mode", command= erase_mode)
    draw_menu.add_command(label="Clear", command= clear_canvas)
    
    #--------------info menu--------------
    info_btn = tk.Button(top_menu, text="Info", width=10)
    info_btn.pack(side="left", padx= 10, pady= 10)
    
    def open_info_menu(event):
        x = info_btn.winfo_rootx()
        y = info_btn.winfo_rooty() + info_btn.winfo_height()
        info_menu.post(x,y)
    
    info_btn.bind("<ButtonRelease-1>", open_info_menu)
    #--------------info  popup menu--------------
    info_menu = tk.Menu(window)
    info_menu.add_command(label="Team Info", command=lambda: open_team_info(window))
    info_menu.add_command(label="Project Info", command=lambda: open_project_info(window))

    #--------------Camera area-----------------
    camera_frame = tk.Frame(window, bg="white", height= 300)
    camera_frame.pack(fill="x")

    camera_view = tk.Label(camera_frame, bg="black", width=80, height=20)
    camera_view.pack(fill="both", expand=True, padx=10, pady=10)
    
    #--------------Canvas area-------------
    canvas_frame = tk.Frame(window, bg="white")
    canvas_frame.pack(fill="both", expand=True)

    drawing_canvas = tk.Canvas(canvas_frame, bg="lightgray")
    drawing_canvas.pack(fill="both", expand=True, padx=10, pady=10)



    window.mainloop()

main()