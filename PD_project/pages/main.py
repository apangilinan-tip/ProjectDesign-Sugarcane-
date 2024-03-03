from tkinter import *
from dashboard import DashboardPage
from reports import ReportsPage
from help import HelpPage

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("CANE CHECK")
        self.attributes('-fullscreen', True)
        
        self.side_nav = Frame(self, bg="gray", width=200)
        self.side_nav.pack(side=LEFT, fill=Y)

        pages = ["DASHBOARD", "REPORTS", "HELP"]
        for page_name in pages:
            button = Button(self.side_nav, text=page_name, width=15, command=lambda page_name=page_name: self.show_page(page_name))
            button.pack(pady=10)

        exit_frame = Frame(self.side_nav, bg="gray")
        exit_frame.pack(side=BOTTOM, pady=20)

        exit_button = Button(exit_frame, text="Exit", width=15, command=self.destroy)
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
