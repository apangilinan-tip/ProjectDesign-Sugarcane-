from tkinter import *
from tkinter import ttk, simpledialog, messagebox 
from pymongo import MongoClient
from bson.son import SON
import threading
from datetime import datetime

class ReportsPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["CaneCheck"]
        self.collection = self.db["Session"]

        # Search Frame
        search_frame = Frame(self, bg="lightgrey")
        search_frame.pack(pady=10)
        
        # Session Name Label
        session_name_label = Label(search_frame, text="Session Name:", font=("Arial", 14))
        session_name_label.grid(row=0, column=0, padx=(5, 10), pady=5)
        
        # Session Name Entry
        self.session_name_entry = Entry(search_frame, width=30, font=("Arial", 12))
        self.session_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Edit Button
        edit_button = Button(search_frame, text="Edit", command=self.edit_session_name, bg="#9E8DB9", fg="white", font=("Arial", 14), relief=RAISED)
        edit_button.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        # Search Entry
        self.search_entry = Entry(search_frame, width=40, font=("Arial", 16))
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=(5, 0), pady=5)
        
        # Search Button
        search_button = Button(search_frame, text="Search", command=self.perform_search, bg="#9E8DB9", fg="white", font=("Arial", 14), relief=RAISED)
        search_button.grid(row=1, column=2, padx=(0, 10), pady=5)

        # Refresh Button
        refresh_button = Button(self, text="Refresh", command=self.refreshAll, bg="#9E8DB9", fg="white", font=("Arial", 10), relief=RAISED)
        refresh_button.pack(padx=1, pady=1, anchor="n")

        # Open Button
        open_button = Button(search_frame, text="Open",command=self.showSessionDetails, bg="#9E8DB9", fg="white", font=("Arial", 14), relief=RAISED)
        open_button.grid(row=0, column=3, padx=(0,10), pady=5)


        # Create a scrollbar
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        

        # Creating the table
        self.table = ttk.Treeview(self, columns=("SessionName", "ElapsedTime"), show="headings", height=20)
        self.table.heading("SessionName", text="Session Name")
        self.table.heading("ElapsedTime", text="Elapsed Time")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=35, fieldbackground="lightgrey")
        style.map("Treeview", background=[("selected", "lightblue")])
        self.table.pack(pady=40)

        scrollbar.config(command=self.table.yview)

        # Inserting data from MongoDB
        self.fetch_data_from_mongodb()

        # Refresh the self.table to reflect the changes
        self.table.update()

        # Bind double click event
        self.table.bind("<Double-1>", self.openSession)
        
    # For Double click
    def openSession(self, event):
        self.showSessionDetails()

    #For Refresh Button
    def refreshAll(self):
        self.fetch_data_from_mongodb()
        self.session_name_entry.delete(0,END)
        self.search_entry.delete(0,END)
    

    def perform_search(self):
        search_query = self.search_entry.get()
        for row in self.table.get_children():
            self.table.delete(row)
        try:
            search_query = int(search_query)
            data = self.collection.find({"SessionName": search_query})
        except ValueError:
            data = self.collection.find({"SessionName": {"$regex": search_query, "$options": "i"}})
        for row in data:
            session_name = row.get("SessionName", "")
            start_time = self.parse_datetime(row.get("StartTime", ""))
            end_time = self.parse_datetime(row.get("EndTime", ""))
            elapsed_time = end_time - start_time
            self.table.insert("", "end", values=(session_name, elapsed_time))
            self.table.tag_configure(session_name, foreground="blue", font=("Arial", 10, "underline"))

    def fetch_data_from_mongodb(self):

        self.table.delete(*self.table.get_children())

        data = self.collection.find()       
        for row in data:
            session_name = row.get("SessionName", "")
            start_time = self.parse_datetime(row.get("StartTime", ""))
            end_time = self.parse_datetime(row.get("EndTime", ""))
            elapsed_time = end_time - start_time
            self.table.insert("", "end", values=(session_name, elapsed_time))
            self.table.tag_configure(session_name, foreground="blue", font=("Arial", 10, "underline"))

    def parse_datetime(self, datetime_str):
        formats = ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S"]
        for fmt in formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                pass
        raise ValueError(f"Unable to parse datetime: {datetime_str}")

    def edit_session(self, session_name):
        print(f"Editing session with name: {session_name}")

    def edit_session_name(self):    
        new_session_name = self.session_name_entry.get()
        if new_session_name:
        # If a session name is entered, edit the input session
            self.edit_input_session_name(new_session_name)
        else:
        # If no session name is entered, edit the selected session
            self.edit_selected_session_name()

    def edit_input_session_name(self, new_session_name):
        # Entered session name
        current_session_name = self.session_name_entry.get()

        # Check if the current session name exists in MongoDB
        session_data = self.collection.find_one({"SessionName": current_session_name})
        if session_data:
            new_session_name = simpledialog.askstring("Edit Session Name", f"Enter new name for session '{current_session_name}':")
            if new_session_name:
        # Update the session name in MongoDB
                session_id = session_data.get("_id")
                self.collection.update_one({"_id": session_id}, {"$set": {"SessionName": new_session_name}})
                print(f"Updating session name from '{current_session_name}' to '{new_session_name}'")
                self.fetch_data_from_mongodb()
        # Update the session name in the table
                self.session_name_entry.delete(0, END)
                self.session_name_entry.insert(0, new_session_name)
        else:
            messagebox.showinfo("Session Not Found", "Session name does not exist.")


    def edit_selected_session_name(self):
        selected_items = self.table.selection()
        if selected_items:
            selected_item = selected_items[0]
            values = self.table.item(selected_item, "values")
            if values:
                selectedSessionName = values[0]
                new_session_name = simpledialog.askstring("Edit Session Name", f"Enter new name for session '{selectedSessionName}':")
                if new_session_name:
                # Perform database update with new session name
                    session_id = self.collection.find_one({"SessionName": selectedSessionName}).get("_id")
                    self.collection.update_one({"_id": session_id}, {"$set": {"SessionName": new_session_name}})
                    print(f"Updating session name from '{selectedSessionName}' to '{new_session_name}'")
                    self.fetch_data_from_mongodb()
                    if self.table.exists(selected_item):
                    # Update the session name in the Treeview
                        self.table.item(selected_item, values=(new_session_name,))

                

    def showSessionDetails(self):
        if self.session_name_entry.get():
        # If a session name is entered, open the session using the entered name
            self.open_session_by_name()
        else:
        # If no session name is entered, open the selected session from the table
            self.open_selected_session()

    def open_session_by_name(self):
    # Entry session name
        session_name = self.session_name_entry.get()

    # Retrieve session data from MongoDB based on session name
        session_data = self.collection.find_one({"SessionName": session_name})
        if session_data:
        # Process session data and display session details
            self.display_session_details(session_data)
        else:
            messagebox.showinfo("Session Not Found", "Session name not found.")

    def open_selected_session(self):
    # Get the selected row
        selected_row = self.table.selection()
        if selected_row:
        # Get the session name from the selected row
            session_name = self.table.item(selected_row, "values")[0]

        # Retrieve session data from MongoDB based on session name
            session_data = self.collection.find_one({"SessionName": session_name})
            if session_data:
            # Process session data and display session details
                self.display_session_details(session_data)

    def display_session_details(self, session_data):
    # Process session data and display session details
        start_time = self.parse_datetime(session_data.get("StartTime", ""))
        end_time = self.parse_datetime(session_data.get("EndTime", ""))
        elapsed_time = end_time - start_time
        elapsed_hours = int(elapsed_time.total_seconds() // 3600)
        elapsed_minutes = int((elapsed_time.total_seconds() % 3600) // 60)
        elapsed_seconds = int(elapsed_time.total_seconds() % 60)
        elapsed_time_str = f"{elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s"

    # Create a new window to display the session details
        detail_window = Toplevel(self)
        detail_window.title("Session Details")
        detail_window.geometry("800x600")

    # Create a frame to contain session info and variety details
        main_frame = Frame(detail_window)
        main_frame.pack(pady=10)

    # Create a frame to contain session info and variety details table
        info_frame = Frame(main_frame)
        info_frame.pack(side="left", fill="both", expand=True, padx=(20,10))

    # Create labels for session name and elapsed time
        session_name_label = Label(info_frame, text=f"Session Name: {session_data['SessionName']}", font=("Arial", 14))
        session_name_label.pack()

        elapsed_time_label = Label(info_frame, text=f"Elapsed Time: {elapsed_time_str}", font=("Arial", 14))
        elapsed_time_label.pack()

    # Create the variety details table
        detail_table = ttk.Treeview(info_frame, columns=("Sequence", "Variety_ID"), show="headings")
        detail_table.heading("Sequence", text="Sequence")
        detail_table.heading("Variety_ID", text="Variety ID")
        detail_table.pack(fill="both", expand=True)

    # Retrieve variety details for the session from MongoDB
        session_id = session_data.get("Session_ID")
        session_details = self.db["SessionDetail"].find({"Session_ID": session_id})

    # Insert variety details into the table
        for session_detail in session_details:
            sequence = session_detail.get("Sequence", "")
            variety_id = session_detail.get("Variety_ID", "")
            detail_table.insert("", "end", values=(sequence, variety_id))

            # Create a frame to hold the variety count table
        count_frame = Frame(main_frame)
        count_frame.pack(side="right", fill="both", expand=True, padx=(10,20), pady=(56,0))

    # Create the variety count table
        count_table = ttk.Treeview(count_frame, columns=("Variety", "Count"), show="headings", height=6)
        count_table.heading("Variety", text="Variety")
        count_table.heading("Count", text="Count")
        count_table.column("Count", width=100)

        # Retrieve variety counts for the session from MongoDB
        variety_counts = self.get_variety_counts(session_id)

        # Insert variety counts into the table
        for variety, count in variety_counts.items():
            count_table.insert("", "end", values=(variety, count))

        # Calculate the overall total count of varieties
        overall_total = sum(variety_counts.values())
        # Insert the overall total count as a new row
        count_table.insert("", "end", values=("Total Sugarcane Varieties", overall_total))
        count_table.pack(side="top", fill="both")


    def get_variety_counts(self, session_id):
        variety_counts = {}
        session_details = self.db["SessionDetail"].find({"Session_ID": session_id})
        for detail in session_details:
            variety_id = detail.get("Variety_ID", "")
            variety_counts[variety_id] = variety_counts.get(variety_id, 0) + 1
        return variety_counts

             


    def show_session_details_frame(self, session_details):
        # Destroy the current frame to clear the screen
        self.destroy()

        # Create a new frame to display the session details
        session_details_frame = Frame(self.parent, bg="white")
        session_details_frame.pack(fill="both", expand=True)

        # Print statement to verify frame creation
        print("Session details frame created.")

        # Create a new table to display the session details
        detail_table = ttk.Treeview(session_details_frame, columns=("Sequence", "Variety_ID"), show="headings")
        detail_table.heading("Sequence", text="Sequence")
        detail_table.heading("Variety_ID", text="Variety ID")

        # Print statement to verify table creation
        print(f"Number of session details: {len(session_details)}")

        # Insert session details into the table
        for session_detail in session_details:
            sequence = session_detail.get("Sequence", "")
            variety_id = session_detail.get("Variety_ID", "")
            detail_table.insert("", "end", values=(sequence, variety_id))
            # Print statement to verify insertion
            print(f"Inserted into detail table: {sequence}, {variety_id}")



    def exit_app(self):
        self.client.close()
        self.parent.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Reports Page")
    root.geometry("800x600")
    root.configure(bg="white")
    
    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)
    
    root.mainloop()
