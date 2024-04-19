from tkinter import *
from tkinter import ttk

class ReportsPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Search Frame
        search_frame = Frame(self, bg="lightgrey")
        search_frame.pack(pady=20)

        # Search Entry
        self.search_entry = Entry(search_frame, width=50, font=("Arial", 16))
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Search Button
        search_button = Button(search_frame, text="Search", command=self.perform_search, bg="#9E8DB9", fg="white", font=("Arial", 14), relief=RAISED)
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Creating the table
        self.table = ttk.Treeview(self, columns=("Name", "Date", "Actions"), show="headings", height=3)
        self.table.heading("Name", text="Name")
        self.table.heading("Date", text="Date")
        self.table.heading("Actions", text="Actions")

        # Style for the table
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="lightgrey")
        style.map("Treeview", background=[("selected", "lightblue")])

        self.table.pack(pady=20)

        # Inserting sample data
        self.insert_sample_data()

    def perform_search(self):
        search_query = self.search_entry.get()

    def exit_app(self):
        self.master.destroy()

    def view_details(self, item_id):
        # This function will be called when a "View" button is clicked
        print("View details for item:", item_id)

    def insert_sample_data(self):
        # Sample data
        sample_data = [
            ("John", "2024-03-04"),
            ("Alice", "2024-03-05"),
            ("Bob", "2024-03-06")
        ]

        # Inserting sample data into the table
        for i, data in enumerate(sample_data):
            # Insert data
            self.table.insert("", "end", values=data)
            
            # Add View button for each row
            view_button = Button(self.table, text="View", command=lambda item_id=i: self.view_details(item_id))
            self.table.column("#3", width=100, anchor="center")
            #self.table.window_create("", window=view_button, anchor="center")

if __name__ == "__main__":
    root = Tk()
    root.title("Reports Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()