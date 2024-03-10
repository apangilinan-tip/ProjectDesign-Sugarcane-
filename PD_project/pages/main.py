from tkinter import *
from dashboard import DashboardPage
from reports import ReportsPage
from help import HelpPage

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("CANE CHECK")
        self.attributes('-fullscreen', True)
        
        self.side_nav = Frame(self, bg="#9E8DB9", width=200)  # Change background color to light purple using hexadecimal code
        self.side_nav.pack(side=LEFT, fill=Y)

        title_label = Label(self.side_nav, text="CANE CHECK", font=("Arial", 16, "bold"), bg="#9E8DB9", fg="white")  # Adjust text and background color
        title_label.pack(side=TOP, pady=10, padx=10)

        hr_line = Frame(self.side_nav, height=2, bg="white")
        hr_line.pack(fill=X, pady=5, padx=10)

        pages = ["DASHBOARD", "REPORTS", "HELP"]
        for page_name in pages:
            button = Button(self.side_nav, text=page_name, width=15, command=lambda page_name=page_name: self.show_page(page_name))
            button.pack(pady=10)

        exit_frame = Frame(self.side_nav)  # Adjust background color
        exit_frame.pack(side=BOTTOM, pady=20)

        exit_button = Button(exit_frame, text="Exit", width=15, command=self.destroy, bg="white")  # Adjust button color
        exit_button.pack()

        self.pages = {
            "DASHBOARD": DashboardPage(self),
            "REPORTS": ReportsPage(self),
            "HELP": HelpPage(self)
        }

        self.current_page = None
        self.show_page("DASHBOARD")
        
    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[page_name]
        self.current_page.pack(side=LEFT, fill=BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()