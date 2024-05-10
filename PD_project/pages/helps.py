import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path

class HelpPage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)

        # Path to the logo image
        PATH = Path(__file__).parent / 'assets'
        logo_path = PATH / 'sugarcane.png'

        # Load sugarcane logo
        sugarcane_logo = Image.open(logo_path)
        sugarcane_logo = sugarcane_logo.resize((200, 200))  # Resize the image if necessary
        self.sugarcane_logo_img = ImageTk.PhotoImage(sugarcane_logo)

        # Create header
        header_frame = tk.Frame(self, bg='#9E8DB9')
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Need Help?",
            font=('Arial', 24, 'bold'),
            bg='#9E8DB9',
            fg='white'
        )
        header_label.pack(pady=20)

        # Sugarcane logo
        sugarcane_logo_label = tk.Label(
            header_frame,
            image=self.sugarcane_logo_img,
            bg='#9E8DB9'
        )
        sugarcane_logo_label.pack()

        # Contact information
        contact_frame = tk.Frame(self)
        contact_frame.pack(pady=20)

        contact_label = tk.Label(
            contact_frame,
            text="Contact Him:",
            font=('Arial', 18),
            fg='black'
        )
        contact_label.pack()

        contact_info = tk.Label(
            contact_frame,
            text="Phone: 09396018365\nEmail: mmhdbiston@tip.edu.ph",
            font=('Arial', 14),
            fg='black'
        )
        contact_info.pack()

        # Additional help or information
        additional_info = tk.Label(
            self,
            text="For additional help or information, please contact our support team.",
            font=('Arial', 14),
            fg='black'
        )
        additional_info.pack(pady=20)


if __name__ == '__main__':
    app = tk.Tk()
    app.title("Help")
    app.geometry("800x600")  # Set window size
    HelpPage(app)
    app.mainloop()
