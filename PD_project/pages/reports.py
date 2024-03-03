from tkinter import *

class ReportsPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        search_frame = Frame(self)
        search_frame.pack(pady=50) 

        self.search_entry = Entry(search_frame, width=50, font=("Arial", 20))  
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        search_button = Button(search_frame, text="Search", command=self.perform_search)
        search_button.grid(row=0, column=1, padx=10, pady=10)

    def perform_search(self):
        search_query = self.search_entry.get()

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)
    root.mainloop()
