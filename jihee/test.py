import calendar
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App")
        
        self.calendar = calendar.monthcalendar(datetime.today().year, datetime.today().month)
        self.selected_date = None
        self.image_path = None
        self.image_labels = {}
        
        self.create_calendar()
    
    def create_calendar(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.calendar_label = tk.Label(self.frame, text="Calendar")
        self.calendar_label.pack()
        
        self.calendar_widget = tk.Frame(self.frame)
        self.calendar_widget.pack()
        
        self.update_calendar()
        
    def update_calendar(self):
        for widget in self.calendar_widget.winfo_children():
            widget.destroy()
        
        for week in self.calendar:
            week_frame = tk.Frame(self.calendar_widget)
            week_frame.pack()
            for day in week:
                if day == 0:
                    day_label = tk.Label(week_frame, text="   ")
                else:
                    day_label = tk.Label(week_frame, text=str(day))
                    day_label.bind("<Button-1>", lambda event, d=day: self.on_date_click(d))
                day_label.pack(side=tk.LEFT)
                
                if day in self.image_labels:
                    self.image_labels[day].destroy()
                    del self.image_labels[day]
    
    def on_date_click(self, day):
        self.selected_date = day
        self.select_image()
        
    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if self.image_path:
            self.display_image()
            
    def display_image(self):
        if self.image_path and self.selected_date:
            img = Image.open(self.image_path)
            img = img.resize((100, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            
            if self.selected_date in self.image_labels:
                self.image_labels[self.selected_date].destroy()
                del self.image_labels[self.selected_date]
            
            image_label = tk.Label(self.calendar_widget, image=img)
            image_label.image = img
            image_label.pack(side=tk.TOP)
            
            self.image_labels[self.selected_date] = image_label
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
    
