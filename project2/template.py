import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog

#=====================Global Variable===============

#=====================option func===================
def camera_toggle():
    print("Camera toggled")
    
#--------------Save&Export----------------
def save_export():
    global cv_canvas

    win = tk.Toplevel()
    win.title("Save / Export")
    win.geometry("600x400")
    win.resizable(False, False)


    #=================================Click Save Button func
    def click_save():
        
        filepath = filedialog.asksaveasfilename(title="Save As", defaultextension="",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("PDF File", "*.pdf"),
                ("All Files", "*.*")])
        if not filepath:
            return 
        
        cv_canvas = drawing_canvas.cv_canvas  

        ext = filepath.split(".")[-1].lower()

        if ext not in ["png", "jpg", "jpeg", "pdf"]:
            filepath += ".png"
            ext = "png"

        if ext in ["png", "jpg", "jpeg"]:
            cv2.imwrite(filepath, cv_canvas)

        elif ext == "pdf":
            pil_img = Image.fromarray(cv2.cvtColor(cv_canvas, cv2.COLOR_BGR2RGB)).convert("RGB")
            pil_img.save(filepath, "PDF", resolution=100.0)
        print("Save:", filepath)

    #-----Bottom Buttons--------
    btn_frame = tk.Frame(win)
    btn_frame.pack(side="bottom",pady=20)

    save_btn = tk.Button(btn_frame, text="Save", width=10,command=click_save)
    save_btn.grid(row=0, column=0, padx=10)

    cancel_btn = tk.Button(btn_frame, text="Cancel", width=10, command=win.destroy)
    cancel_btn.grid(row=0, column=1, padx=10)

    #--------Preview Frame------
    preview_frame = tk.Frame(win, bg="#ddd", width=400, height=400)
    preview_frame.pack(padx=10, pady=10)
    preview_frame.pack_propagate(False)

    preview_label = tk.Label(preview_frame, bg="#ddd")
    preview_label.pack(expand=True)

    # canvas -> screenshot -> show preview_thumbnail
    win.update()
    canvas_x = drawing_canvas.winfo_rootx()
    canvas_y = drawing_canvas.winfo_rooty()
    canvas_w = drawing_canvas.winfo_width()
    canvas_h = drawing_canvas.winfo_height()

    img = ImageGrab.grab(bbox=(canvas_x,canvas_y,canvas_x + canvas_w,canvas_y + canvas_h))
    img.thumbnail((400, 400))
    preview_img = ImageTk.PhotoImage(img)

    preview_label.config(image=preview_img)
    preview_label.image = preview_img
    print("Save selected")

#======================draw func===================
def pen_mode():
    print("Pen mode selected")

def erase_mode():
    print("Erase mode selected")
def clear_canvas():
    print("clear_canvas selected")

#======================Info func===================
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
    window.update() 

    #-------------Generate empty Canvas-----------
    canvas_w = drawing_canvas.winfo_width()
    canvas_h = drawing_canvas.winfo_height()

    cv_canvas = np.ones((canvas_h, canvas_w,3), dtype=np.uint8) 
    cv_canvas = cv_canvas * 255
    
    #===============================================================
    cv2.rectangle(cv_canvas, (50, 50), (200, 200), (0, 0, 255), -1) # test for create red rectangle
    #===============================================================

    pil_canvas = Image.fromarray(cv2.cvtColor(cv_canvas, cv2.COLOR_BGR2RGB))
    tk_canvas_image = ImageTk.PhotoImage(pil_canvas)
    drawing_canvas.create_image(0, 0, anchor="nw", image=tk_canvas_image)

    # store the OpenCV image for save/draw
    drawing_canvas.cv_canvas = cv_canvas
    # prevent image from disappearing
    drawing_canvas.tk_canvas_image = tk_canvas_image

    window.mainloop()

main()