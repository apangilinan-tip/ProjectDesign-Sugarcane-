
"""import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)"""

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
import os

from pages.main import DashboardPage


# solution for pathing error
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# constant
BG_COLOR = "#f0f2f5"
PRIMARY_COLOR = "#2d3436"
SECONDARY_COLOR = "#0984e3"
CARD_COLOR = "#ffffff"
FONTS = {
    'header': ("Lexend", 12, "bold"),
    'body': ("Lexend", 10),
    'large': ("Lexend", 24, "bold")}



class UiPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=BG_COLOR)
        self.imgname = "holder.jpg"
        
        self.counter_vars = [IntVar(value=0) for _ in range(7)]  # Index 0: total, 1-5: varieties
        self.status_vars = {
            'sensor': IntVar(value=0),
            'variety': IntVar(value=None),
            'conveyor': StringVar(value="Stopped"),
            'actuator': StringVar(value="Inactive"),
            'system': StringVar(value="Disabled"),
            'prompt': StringVar(value="")
        }
        self.setup_ui
        self.bind_events
    
    def setup_ui(self):
        """Initialize all UI components"""
        main_container = Frame(self, bg=BG_COLOR)
        main_container.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Camera Section
        self.camera_frame = Frame(main_container, bg=CARD_COLOR, bd=2, relief=RAISED)
        self.camera_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.init_camera_display()

        # Status Section
        status_frame = Frame(main_container, bg=BG_COLOR)
        status_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.create_status_card(status_frame)

        # Variety Counts
        counts_container = Frame(main_container, bg=BG_COLOR)
        counts_container.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)
        self.create_variety_counts(counts_container)

        # Configure grid weights
        main_container.grid_columnconfigure(0, weight=3)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_rowconfigure(0, weight=3)
        main_container.grid_rowconfigure(1, weight=1)

    def on_window_resize(self, event):
        if event.widget == self:
            self.after(100, self.update_camera_placeholder)

    def create_status_card(self, parent):
        """Create system status card"""
        card = Frame(parent, bg=CARD_COLOR, padx=15, pady=15)
        card.pack(fill=BOTH, expand=True)
        
        Label(card, text="SYSTEM STATUS", font=FONTS['header'], 
            bg=CARD_COLOR, fg=PRIMARY_COLOR).pack(anchor=NW)
        
        status_items = [
            ("Live Count", self.counter_vars[0], ['large']),
            ("Sensor Status", self.status_vars['sensor']),
            ("Detected Variety", self.status_vars['variety']),
            ("Conveyor", self.status_vars['conveyor']),
            ("Actuator", self.status_vars['actuator']),
            ("System", self.status_vars['system']),
            ("", self.status_vars['prompt'], FONTS['large'])
        ]
        
        for text, var, *font in status_items:
            self.create_status_row(card, text, var, font[0] if font else FONTS['body'])

    def init_camera_display(self):
        """Initialize camera display with dynamic sizing"""
        self.camera_image = None
        self.camera_label = Label(self.camera_frame, bg=CARD_COLOR)
        self.camera_label.pack(fill=BOTH, expand=True)
        self.update_camera_placeholder()

    def update_camera_placeholder(self):
        try:
            max_w = max(1, self.camera_frame.winfo_width() - 20)
            max_h = max(1, self.camera_frame.winfo_height() - 20)
            
            img = Image.open("images/"+self.imgname)
            
            # Maintain aspect ratio while fitting to available space
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            
            self.camera_image = ImageTk.PhotoImage(img)
            self.camera_label.configure(image=self.camera_image)

        except Exception as e:
            print(f"Error updating camera: {e}")

    def on_window_resize(self, event):
        """Handle window resize events with debounce"""
        if event.widget == self:
            self.after(100, self.update_camera_placeholder)

        def create_status_card(self, parent):
            """Create system status card"""
            card = Frame(parent, bg=CARD_COLOR, padx=15, pady=15)
            card.pack(fill=BOTH, expand=True)
            
            Label(card, text="SYSTEM STATUS", font=FONTS['header'], 
                bg=CARD_COLOR, fg=PRIMARY_COLOR).pack(anchor=NW)
            
            status_items = [
                ("Live Count", self.counter_vars[0], FONTS['large']),
                ("Sensor Status", self.status_vars['sensor']),
                ("Detected Variety", self.status_vars['variety']),
                ("Conveyor", self.status_vars['conveyor']),
                ("Actuator", self.status_vars['actuator']),
                ("System", self.status_vars['system']),
                
            ]
            
            for text, var, *font in status_items:
                self.create_status_row(card, text, var, font[0] if font else FONTS['body'])

    def create_variety_counts(self, parent):
        """Create variety count cards with responsive layout"""
        container = Frame(parent, bg=BG_COLOR)
        container.pack(fill=BOTH, expand=True)
        
        varieties = ["Variety 1", "Variety 2", "Variety 3", "Variety 4", "Variety 5"]
        for col, (variety, var) in enumerate(zip(varieties, self.counter_vars[1:6])):
            card = Frame(container, bg=CARD_COLOR, padx=10, pady=5)
            card.grid(row=0, column=col, padx=2, sticky="nsew")
            container.grid_columnconfigure(col, weight=1)
            
            Label(card, text=variety, font=FONTS['body'], 
                  bg=CARD_COLOR, fg=PRIMARY_COLOR, wraplength=80).pack()
            Label(card, textvariable=var, font=FONTS['large'],
                  bg=CARD_COLOR, fg=SECONDARY_COLOR).pack()

    def create_status_row(self, parent, label, var, font):
        """Create a status row with label and value"""
        row = Frame(parent, bg=CARD_COLOR)
        row.pack(fill=X, pady=2)
        
        Label(row, text=label+":", font=FONTS['body'], 
              bg=CARD_COLOR, fg=PRIMARY_COLOR, width=12, anchor=W).pack(side=LEFT)
        Label(row, textvariable=var, font=font, 
              bg=CARD_COLOR, fg=SECONDARY_COLOR).pack(side=LEFT)

    def bind_events(self):
        """Bind window resize events"""
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self:
            self.update_camera_placeholder()

    # Raspberry Pi integration methods
    def update_sensor_status(self, status):
        self.status_vars['sensor'].set(status)
    
    def update_variety(self, variety):
        self.status_vars['variety'].set(variety)
    
    def increment_counter(self, variety_index=0):
        """Increment counters (0 = total, 1-5 = specific varieties)"""
        if 0 <= variety_index <= 5:
            self.counter_vars[variety_index].set(self.counter_vars[variety_index].get() + 1)
        if variety_index != 0:
            self.counter_vars[0].set(self.counter_vars[0].get() + 1)

if __name__ == "__main__":
    root = Tk()
    root.title("CaneCheck")
    root.minsize(800, 600)  
    root.geometry("1024x768")
    root.configure(bg="white")
    
    reports_page = UiPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
