from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
import sqlite3
from io import BytesIO  # To handle image data
from datetime import datetime

class ReportsPage(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Connect to SQLite database
        self.conn = sqlite3.connect('sessiondb.db')
        self.cursor = self.conn.cursor()

        # Search Frame
        search_frame = Frame(self, bg="lightgrey")
        search_frame.pack(pady=5)

        # Session Name Label
        session_name_label = Label(search_frame, text="Session Name:", font=("Arial", 12))
        session_name_label.grid(row=0, column=0, padx=(5, 5), pady=5)

        # Session Name Entry
        self.session_name_entry = Entry(search_frame, width=20, font=("Arial", 10))
        self.session_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Edit Button
        edit_button = Button(search_frame, text="Edit", command=self.edit_session_name, bg="#9E8DB9", fg="white", font=("Arial", 12), relief=RAISED)
        edit_button.grid(row=0, column=2, padx=(0, 5), pady=5)

        # Search Entry
        self.search_entry = Entry(search_frame, width=30, font=("Arial", 12))
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=(5, 0), pady=5)

        # Search Button
        search_button = Button(search_frame, text="Search", command=self.perform_search, bg="#9E8DB9", fg="white", font=("Arial", 12), relief=RAISED)
        search_button.grid(row=1, column=2, padx=(0, 5), pady=5)

        # Refresh Button
        refresh_button = Button(self, text="Refresh", command=self.refresh_all, bg="#9E8DB9", fg="white", font=("Arial", 12), relief=RAISED)
        refresh_button.pack(padx=1, pady=5, anchor="n")

        # Create a scrollbar
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Creating the table
        self.table = ttk.Treeview(self, columns=("SessionName", "ElapsedTime"), show="headings", height=15)
        self.table.heading("SessionName", text="Session Name")
        self.table.heading("ElapsedTime", text="Elapsed Time")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="lightgrey")
        style.map("Treeview", background=[("selected", "lightblue")])
        self.table.pack(pady=20)

        scrollbar.config(command=self.table.yview)

        # Fetch data from the SQLite database and populate the table
        self.fetch_data_from_sqlite()

        # Bind double click event
        self.table.bind("<Double-1>", self.open_session)

    def fetch_data_from_sqlite(self):
        """Fetches data from the SQLite database and populates the table."""
        self.table.delete(*self.table.get_children())
        self.cursor.execute("SELECT SessionName,StartTime, EndTime FROM SessionDB")
        sessions = self.cursor.fetchall()
        
        for session in sessions:
            session_name = session[0]
            start_time = self.parse_datetime(session[1])
            end_time = self.parse_datetime(session[2])
            elapsed_time = end_time - start_time
            self.table.insert("", "end", values=(session_name, str(elapsed_time)))

    def parse_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    def open_session(self, event):
        """Handles opening a session and displaying its image."""
        selected_row = self.table.selection()
        if selected_row:
            session_name = self.table.item(selected_row, "values")[0]
            self.show_session_image(session_name)

    def show_session_image(self, session_name):
        """Fetches and displays the image associated with the selected session."""
        
        # First, retrieve the Session_ID from the Session table using the session name
        self.cursor.execute("SELECT Session_ID FROM Session WHERE SessionName=?", (session_name,))
        session_id_result = self.cursor.fetchone()

        if session_id_result:
            session_id = session_id_result[0]

            # Now, fetch the ImageData from SessionDetail table using Session_ID
            self.cursor.execute("SELECT ImageData FROM SessionDetail WHERE Session_ID=?", (session_id,))
            image_data = self.cursor.fetchone()

            if image_data and image_data[0]:
                try:
                    # Assuming image data is stored as binary (BLOB)
                    image = Image.open(BytesIO(image_data[0]))  # Read binary data as image
                    image = image.resize((400, 300), Image.ANTIALIAS)  # Resize image
                    photo = ImageTk.PhotoImage(image)

                    # Create a new window to show the image
                    image_window = Toplevel(self)
                    image_window.title("Session Image")
                    image_window.geometry("450x350")

                    image_label = Label(image_window, image=photo)
                    image_label.image = photo  # Keep a reference to avoid garbage collection
                    image_label.pack(pady=20)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image: {e}")
            else:
                messagebox.showerror("Error", "No image available for this session.")
        else:
            messagebox.showerror("Error", "No session ID found for this session name.")



    def edit_session_name(self):
        """Edits the session name."""
        session_name = self.session_name_entry.get()
        if session_name:
            new_session_name = simpledialog.askstring("Edit Session Name", f"Enter new name for session '{session_name}':")
            if new_session_name:
                self.cursor.execute("UPDATE Session SET SessionName=? WHERE SessionName=?", (new_session_name, session_name))
                self.conn.commit()
                self.fetch_data_from_sqlite()

    def perform_search(self):
        """Searches for a session by name."""
        search_query = self.search_entry.get()
        self.table.delete(*self.table.get_children())
        self.cursor.execute("SELECT SessionName, StartTime, EndTime FROM Session WHERE SessionName LIKE ?", (f"%{search_query}%",))
        sessions = self.cursor.fetchall()

        for session in sessions:
            session_name = session[0]
            start_time = self.parse_datetime(session[1])
            end_time = self.parse_datetime(session[2])
            elapsed_time = end_time - start_time
            self.table.insert("", "end", values=(session_name, str(elapsed_time)))

    def refresh_all(self):
        """Refreshes the table with all sessions."""
        self.fetch_data_from_sqlite()

if __name__ == "__main__":
    root = Tk()
    root.title("Reports Page")
    root.geometry("700x500")
    root.configure(bg="white")

    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)

    root.mainloop()
