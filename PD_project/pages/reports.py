import tkinter as tk
from tkinter import ttk
import sqlite3
from pathlib import Path
import os 
from PIL import Image, ImageTk, UnidentifiedImageError

Image = None
ImageTk = None
UnidentifiedImageError = None

DB_FILE = Path(__file__).resolve().parent.parent / 'canecheck.db'
IMAGE_BASE_DIR = Path(__file__).resolve().parent.parent / 'images'

IMAGE_PREVIEW_MAX_WIDTH = 250
IMAGE_PREVIEW_MAX_HEIGHT = 200
PLACEHOLDER_TEXT = "Select to view image"

class ReportsPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.master = parent 
        self.conn = None
        self.cursor = None
        self.db_path = DB_FILE
        self.current_photo = None 

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3) 
        self.grid_rowconfigure(0, weight=1)

        list_frame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        detail_frame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        detail_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        detail_frame.grid_rowconfigure(1, weight=0)
        detail_frame.grid_rowconfigure(3, weight=1)
        detail_frame.grid_rowconfigure(5, weight=0)
        detail_frame.grid_rowconfigure(6, weight=1)
        detail_frame.grid_columnconfigure(0, weight=1)

        list_label = tk.Label(list_frame, text="Past Sessions", font=('Arial', 14, 'bold'))
        list_label.grid(row=0, column=0, pady=(5, 10), padx=5, sticky="ew")

        cols = ('Session ID', 'Name', 'Start Time', 'End Time')
        self.session_tree = ttk.Treeview(list_frame, columns=cols, show='headings', height=15)
        for col in cols:
            self.session_tree.heading(col, text=col)
            self.session_tree.column(col, width=100, anchor=tk.W, stretch=tk.YES)
        self.session_tree.column('Session ID', width=70, stretch=tk.NO)
        self.session_tree.column('Name', width=120)
        self.session_tree.column('Start Time', width=150)
        self.session_tree.column('End Time', width=150)
        self.session_tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        session_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.session_tree.yview)
        session_scrollbar.grid(row=1, column=1, sticky="ns")
        self.session_tree.configure(yscrollcommand=session_scrollbar.set)

        self.session_tree.bind('<<TreeviewSelect>>', self.on_session_select)

        refresh_button = tk.Button(list_frame, text="Refresh List", command=self.load_sessions, bg="#9E8DB9", fg="white")
        refresh_button.grid(row=2, column=0, columnspan=2, pady=5)

        detail_label = tk.Label(detail_frame, text="Session Details", font=('Arial', 14, 'bold'))
        detail_label.grid(row=0, column=0, columnspan=2, pady=(5,10), sticky="ew")

        summary_frame = tk.Frame(detail_frame)
        summary_frame.grid(row=1, column=0, columnspan=2, sticky="new", pady=5, padx=10)

        self.detail_labels = {}
        stat_labels = [
            "Session Name:", "Start Time:", "End Time:", "Total Detections:",
            "Variety 1:", "Variety 2:", "Variety 3:", "Variety 4:", "Variety 5:"
        ]
        num_labels = len(stat_labels)
        rows_per_col = (num_labels + 1) // 2
        for i, label_text in enumerate(stat_labels):
            row = i % rows_per_col
            col = (i // rows_per_col) * 2
            lbl_name = tk.Label(summary_frame, text=label_text, anchor=tk.W, font=('Arial', 10, 'bold'))
            lbl_name.grid(row=row, column=col, sticky=tk.W, padx=(5,2), pady=1)
            lbl_value = tk.Label(summary_frame, text="N/A", anchor=tk.W, width=25)
            lbl_value.grid(row=row, column=col+1, sticky=tk.W, padx=(0,15), pady=1)
            self.detail_labels[label_text.replace(":", "")] = lbl_value

        detections_label = tk.Label(detail_frame, text="Individual Detections", font=('Arial', 12, 'bold'))
        detections_label.grid(row=2, column=0, columnspan=2, pady=(15,5), sticky="ew", padx=10)

        det_cols = ('Seq', 'Time', 'Variety', 'Image File')
        self.detection_tree = ttk.Treeview(detail_frame, columns=det_cols, show='headings', height=10)
        for col in det_cols:
            self.detection_tree.heading(col, text=col)
            self.detection_tree.column(col, anchor=tk.W, stretch=tk.YES)
        self.detection_tree.column('Seq', width=50, stretch=tk.NO)
        self.detection_tree.column('Time', width=150)
        self.detection_tree.column('Variety', width=60, stretch=tk.NO)
        self.detection_tree.column('Image File', width=200)
        self.detection_tree.grid(row=3, column=0, sticky="nsew", padx=(10,0), pady=(0,10))

        det_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=self.detection_tree.yview)
        det_scrollbar.grid(row=3, column=1, sticky="ns", pady=(0,10), padx=(0,10))
        self.detection_tree.configure(yscrollcommand=det_scrollbar.set)

        self.detection_tree.bind('<<TreeviewSelect>>', self.on_detection_select)

        image_preview_label_text = tk.Label(detail_frame, text="Image Preview", font=('Arial', 12, 'bold'))
        image_preview_label_text.grid(row=4, column=0, columnspan=2, pady=(10,2), sticky="ew", padx=10)

        self.image_preview_frame = tk.Frame(detail_frame,
                                              width=IMAGE_PREVIEW_MAX_WIDTH + 10,
                                              height=IMAGE_PREVIEW_MAX_HEIGHT + 10,
                                              bd=1, relief=tk.SUNKEN)
        self.image_preview_frame.grid(row=5, column=0, columnspan=2, pady=(0,10), padx=10, sticky="n")
        self.image_preview_frame.grid_propagate(False)

        self.image_preview_label = tk.Label(self.image_preview_frame, text=PLACEHOLDER_TEXT,
                                             bg="lightgrey", anchor=tk.CENTER, justify=tk.CENTER, wraplength=IMAGE_PREVIEW_MAX_WIDTH-10)
        self.image_preview_label.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=25, font=('Arial', 9))
        style.configure("Treeview.Heading", font=('Arial', 10,'bold'))
        style.map("Treeview", background=[("selected", "#A9CCE3")])

        self.status_label = tk.Label(self, text="", fg="red", anchor='w')
        self.status_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))

        self.connect_db()
        if self.cursor:
            self.load_sessions()
            self.clear_details()
        else:
             self.status_label.config(text=f"Error: Database file not found or connection failed.\nExpected at: {self.db_path}")
             print(f"Error: Database file not found or connection failed. Expected at: {self.db_path}")

    def connect_db(self):
        if not self.db_path.exists():
            error_msg = f"Database file not found: {self.db_path}"
            print(error_msg)
            self.status_label.config(text=error_msg)
            self.conn = None
            self.cursor = None
            return
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Database connection successful to {self.db_path.name}")
            self.status_label.config(text="")
        except sqlite3.Error as e:
            error_msg = f"Database connection error: {e}"
            print(f"{error_msg} to {self.db_path}")
            self.status_label.config(text=error_msg)
            self.conn = None
            self.cursor = None

    def load_sessions(self):
        for item in self.session_tree.get_children(): self.session_tree.delete(item)
        for item in self.detection_tree.get_children(): self.detection_tree.delete(item)
        self.clear_details()

        if not self.cursor:
            self.connect_db()
            if not self.cursor:
                 print("Cannot load sessions, no database cursor.")
                 self.status_label.config(text="Error: Cannot load sessions, DB connection failed.")
                 self.session_tree.insert('', tk.END, values=("DB Connection Error", "", "", ""), tags=('error',))
                 self.session_tree.tag_configure('error', foreground='red')
                 return

        try:
            self.cursor.execute("SELECT session_id, session_name, start_time, end_time FROM Session ORDER BY start_time DESC")
            sessions = self.cursor.fetchall()
            if not sessions:
                self.session_tree.insert('', tk.END, values=("No sessions found.", "", "", ""))
            else:
                for session in sessions:
                    session_id, name, start, end = session
                    name = name if name else f"Session {session_id}"
                    start_str = start if start else "N/A"
                    end_str = end if end else "Ongoing or N/A"
                    self.session_tree.insert('', tk.END, iid=session_id, values=(session_id, name, start_str, end_str))
            self.status_label.config(text="")
        except sqlite3.Error as e:
            error_msg = f"Error fetching sessions: {e}"
            print(error_msg)
            self.status_label.config(text=error_msg)
            self.session_tree.insert('', tk.END, values=("Error loading sessions.", "", "", ""), tags=('error',))
            self.session_tree.tag_configure('error', foreground='red')

    def on_session_select(self, event=None):
        selected_items = self.session_tree.selection()
        if not selected_items:
            self.clear_details()
            return

        selected_iid = selected_items[0]
        try:
             session_id = int(selected_iid)
             self.load_session_details(session_id)
        except ValueError:
             print(f"Ignoring selection of non-numeric IID: {selected_iid}")
             self.clear_details()
        except sqlite3.Error as e:
             error_msg = f"Database error on selection: {e}"
             print(error_msg)
             self.status_label.config(text=error_msg)
             self.clear_details()

    def load_session_details(self, session_id):
        self.clear_details()

        if not self.cursor:
            print("Cannot load details, no database cursor.")
            self.status_label.config(text="Error: Cannot load details, DB connection failed.")
            return

        try:
            self.cursor.execute("SELECT session_name, start_time, end_time FROM Session WHERE session_id = ?", (session_id,))
            session_info = self.cursor.fetchone()
            if not session_info:
                print(f"Session {session_id} not found.")
                self.clear_details()
                return

            name, start, end = session_info
            self.detail_labels["Session Name"].config(text=name if name else f"Session {session_id}")
            self.detail_labels["Start Time"].config(text=start or "N/A")
            self.detail_labels["End Time"].config(text=end or "Ongoing or N/A")

            self.cursor.execute("SELECT variety_id, COUNT(*) FROM Detection WHERE session_id = ? GROUP BY variety_id", (session_id,))
            counts = self.cursor.fetchall()
            total_detections = 0
            variety_counts = {i: 0 for i in range(1, 6)}
            for var_id, count in counts:
                if var_id in variety_counts:
                    variety_counts[var_id] = count
                total_detections += count
            self.detail_labels["Total Detections"].config(text=str(total_detections))
            for i in range(1, 6):
                self.detail_labels[f"Variety {i}"].config(text=str(variety_counts[i]))

            for item in self.detection_tree.get_children(): self.detection_tree.delete(item)

            self.cursor.execute("SELECT sequence, detection_time, variety_id, image_file FROM Detection WHERE session_id = ? ORDER BY sequence ASC", (session_id,))
            detections = self.cursor.fetchall()
            if not detections:
                 self.detection_tree.insert('', tk.END, values=("No detections recorded", "", "", ""))
            else:
                for det in detections:
                    seq, time, var_id, img_file = det
                    image_file_val = img_file if img_file is not None else "N/A"
                    self.detection_tree.insert('', tk.END, values=(seq, time or "N/A", var_id, image_file_val))

            self.status_label.config(text="")

        except sqlite3.Error as e:
            error_msg = f"Error fetching details for session {session_id}: {e}"
            print(error_msg)
            self.status_label.config(text=error_msg)
            self.clear_details()

    def on_detection_select(self, event=None):
        selected_items = self.detection_tree.selection()
        if not selected_items:
            self.clear_image_preview()
            return

        selected_item = selected_items[0]
        item_data = self.detection_tree.item(selected_item, 'values')

        if not item_data or len(item_data) < 4 or item_data[0] == "No detections recorded":
             self.clear_image_preview()
             return

        image_filename = item_data[3]

        if not image_filename or image_filename == "N/A":
             self.display_image(None, message="No image path specified\nfor this detection.")
             return

        try:
            full_image_path = IMAGE_BASE_DIR / image_filename
            print(f"Attempting to load image: {full_image_path}")
            self.display_image(full_image_path)
        except TypeError as e:
             print(f"Error constructing image path (TypeError): {e}. Image filename was: '{image_filename}'")
             self.display_image(None, message=f"Error: Invalid image path data.\n({e})")
        except Exception as e:
             print(f"Error constructing or displaying image: {e}")
             self.display_image(None, message=f"Error displaying image:\n{e}")

    def display_image(self, image_path, message=None):
        if not ImageTk or not Image:
             self.image_preview_label.config(image='', text="Pillow library not installed\nor failed to import.\nCannot display images.", bg="lightgrey")
             self.current_photo = None
             return

        self.image_preview_label.config(image='', text="", bg="lightgrey")
        self.current_photo = None

        if message:
             self.image_preview_label.config(text=message)
             return

        if not image_path or not isinstance(image_path, Path) or not image_path.is_file():
             path_str = str(image_path) if image_path else "None"
             err_text = f"Image file not found at:\n{path_str}"
             self.image_preview_label.config(text=err_text)
             print(f"Image file not found at: {path_str}")
             return

        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            ratio = min(IMAGE_PREVIEW_MAX_WIDTH / img_width, IMAGE_PREVIEW_MAX_HEIGHT / img_height)
            if ratio < 1.0:
                 new_width = int(img_width * ratio)
                 new_height = int(img_height * ratio)
                 resampling_filter = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
                 resized_img = img.resize((new_width, new_height), resampling_filter)
            else:
                 resized_img = img

            photo = ImageTk.PhotoImage(resized_img)
            self.image_preview_label.config(image=photo, text="")
            self.image_preview_label.image = photo
            self.current_photo = photo

        except UnidentifiedImageError:
            error_msg = f"Cannot identify image file:\n{image_path.name}\n(Invalid format?)"
            print(f"Error loading image {image_path}: Cannot identify image file.")
            self.image_preview_label.config(image='', text=error_msg)
            self.current_photo = None
        except FileNotFoundError:
             error_msg = f"File not found error for:\n{image_path}"
             print(f"FileNotFoundError during image loading: {image_path}")
             self.image_preview_label.config(image='', text=error_msg)
             self.current_photo = None
        except Exception as e:
            error_msg = f"Error loading image:\n{image_path.name}\n{e}"
            print(f"Unexpected error loading image {image_path}: {e}")
            self.image_preview_label.config(image='', text=error_msg)
            self.current_photo = None

    def clear_image_preview(self):
         if hasattr(self, 'image_preview_label'):
             self.image_preview_label.config(image='', text=PLACEHOLDER_TEXT, bg="lightgrey")
             self.current_photo = None

    def clear_details(self):
        for label_key in self.detail_labels:
             if "Variety" in label_key or "Total Detections" in label_key:
                 self.detail_labels[label_key].config(text="0")
             else:
                 self.detail_labels[label_key].config(text="N/A")
        for item in self.detection_tree.get_children():
            self.detection_tree.delete(item)
        self.detection_tree.insert('', tk.END, values=("Select a session", "", "", ""))
        self.clear_image_preview()

    def destroy(self):
        print("Closing Reports database connection.")
        if self.conn:
            try:
                 self.conn.close()
            except sqlite3.Error as e:
                 print(f"Error closing DB connection on destroy: {e}")
        super().destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("CaneCheck Reports")
    root.geometry("1100x700")
    root.configure(bg="white")

    reports_page = ReportsPage(root)
    reports_page.pack(fill="both", expand=True)

    def on_closing():
        print("Application window closing.")
        reports_page.destroy()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
