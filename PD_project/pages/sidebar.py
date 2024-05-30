from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# Importing the DashboardPage, ReportsPage, and HelpPage classes
from dashboard import DashboardPage
from reports import ReportsPage
from helps import HelpPage

PATH = Path(__file__).parent / 'assets'


class CaneCheckMain(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        # Application images
        self.images = [
            tk.PhotoImage(name='logo', file=PATH / 'sugarcane.png').subsample(2),  
            tk.PhotoImage(name='dashboard', file=PATH / 'dashboard_icon.png').subsample(2),  
            tk.PhotoImage(name='reports', file=PATH / 'reports_icon.png').subsample(2),
            tk.PhotoImage(name='help', file=PATH / 'help_icon.png').subsample(2)  
        ]

        # Header
        hdr_frame = tk.Frame(self, bg='lightgray', height=70)  # Set a fixed height
        hdr_frame.pack(fill=tk.X)
        hdr_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its children

        hdr_label = tk.Label(
            master=hdr_frame,
            image=self.images[0],  # Assuming the logo is the header background
            bg='lightgray',
            borderwidth=0
        )
        hdr_label.pack(side=tk.LEFT, padx=5, pady=10)  # Reduced padding

        logo_text = tk.Label(
            master=hdr_frame,
            text='CANECHECK',
            font=('Arial', 20, 'bold'),  # Smaller font size
            bg='lightgray',
            fg='white',  # Adjust text color
            padx=10  # Reduced padding to the left
        )
        logo_text.pack(side=tk.LEFT, padx=5, pady=20)

        # Center header content
        hdr_label.pack_configure(anchor='center')
        logo_text.pack_configure(anchor='center')

        # Sidebar
        sidebar_frame = tk.Frame(self, bg='#9E8DB9', width=100, borderwidth=2, relief='solid')  # Added border
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Action buttons
        pages = ["Dashboard", "Reports", "Help"]  # Page names
        self.pages = {}  # Dictionary to hold page instances

        for page_name in pages:
            button = tk.Button(
                master=sidebar_frame,
                image=self.images[pages.index(page_name) + 1],  # Get the corresponding image
                text=page_name,
                compound=tk.TOP,
                borderwidth=0,
                bg='#9E8DB9',
                command=lambda page_name=page_name: self.show_page(page_name)
            )
            button.pack(fill=tk.X, padx=10, pady=5)  

        # Create and add pages to the dictionary
        self.pages["Dashboard"] = DashboardPage(self)
        self.pages["Reports"] = ReportsPage(self)
        self.pages["Help"] = HelpPage(self)

        # Show the initial page
        self.show_page("Dashboard")

    def show_page(self, page_name):
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()

        # Show the selected page
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)


class HelpPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)

        # Path to the logo image
        PATH = Path(__file__).parent / 'assets'
        logo_path = PATH / 'sugarcane.png'

        # Load sugarcane logo
        sugarcane_logo = Image.open(logo_path)
        sugarcane_logo = sugarcane_logo.resize((100, 100))  # Resize the image to a smaller size
        self.sugarcane_logo_img = ImageTk.PhotoImage(sugarcane_logo)

        # Create header
        header_frame = tk.Frame(self, bg='#9E8DB9')
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Need Help?",
            font=('Arial', 18, 'bold'),  # Smaller font size
            bg='#9E8DB9',
            fg='white'
        )
        header_label.pack(pady=10)  # Reduced padding

        # Sugarcane logo
        sugarcane_logo_label = tk.Label(
            header_frame,
            image=self.sugarcane_logo_img,
            bg='#9E8DB9'
        )
        sugarcane_logo_label.pack()

        # Contact information
        contact_frame = tk.Frame(self)
        contact_frame.pack(pady=10)  # Reduced padding

        contact_label = tk.Label(
            contact_frame,
            text="Contact Him:",
            font=('Arial', 14),  # Smaller font size
            fg='black'
        )
        contact_label.pack()

        contact_info = tk.Label(
            contact_frame,
            text="Phone: 09396018365\nEmail: mmhdbiston@tip.edu.ph",
            font=('Arial', 12),  # Smaller font size
            fg='black'
        )
        contact_info.pack()

        # Additional help or information
        additional_info = tk.Label(
            self,
            text="For additional help or information, please contact our support team.",
            font=('Arial', 12),  # Smaller font size
            fg='black'
        )
        additional_info.pack(pady=10)  # Reduced padding


if __name__ == '__main__':
    app = tk.Tk()
    app.title("CaneCheck: Sugarcane Variety Detection")
    app.geometry("600x400")  
    CaneCheckMain(app)
    app.mainloop()
