from pathlib import Path
import tkinter as tk
from tkinter import ttk

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
            tk.PhotoImage(name='logo', file=PATH / 'sugarcane.png'),
            tk.PhotoImage(name='dashboard', file=PATH / 'dashboard_icon.png'),
            tk.PhotoImage(name='reports', file=PATH / 'reports_icon.png'),
            tk.PhotoImage(name='help', file=PATH / 'help_icon.png')
        ]

        # Header
        hdr_frame = tk.Frame(self, bg='lightgray')
        hdr_frame.pack(fill=tk.X)

        hdr_label = tk.Label(
            master=hdr_frame,
            image=self.images[0],  # Assuming the logo is the header background
            bg='lightgray',
            borderwidth=0
        )
        hdr_label.pack(side=tk.LEFT, padx=20, pady=20)

        logo_text = tk.Label(
            master=hdr_frame,
            text='CANECHECK',
            font=('Arial', 64, 'bold'),
            bg='lightgray',
            fg='white'  # Adjust text color
        )
        logo_text.pack(side=tk.LEFT, padx=10, pady=20)

        # Sidebar
        sidebar_frame = tk.Frame(self, bg='#9E8DB9', width=200)
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
            button.pack(fill=tk.X, padx=10, pady=10)

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


if __name__ == '__main__':
    app = tk.Tk()
    app.title("CaneCheck: Sugarcane Variety Detection")
    app.geometry("1000x600")  # Set initial window size
    CaneCheckMain(app)
    app.mainloop()