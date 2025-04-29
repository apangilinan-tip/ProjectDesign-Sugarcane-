from pathlib import Path
import tkinter as tk
import sqlite3

try:
    from main import DashboardPage
    from reports import ReportsPage
    from frontEnd import UiPage
except ImportError as e:
    print(f"Error importing page modules: {e}")
    print("Please ensure main.py, reports.py, and frontEnd.py are in the same directory as App.py or adjust the import paths.")
    exit()


DB_FILE = Path(__file__).parent.parent / 'canecheck.db'


class CaneCheckMain(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        assets_path = Path(__file__).parent / 'assets'

        self.images = []
        try:
            self.images = [
                tk.PhotoImage(name='logo', file=assets_path / 'sugarcane.png'),
                tk.PhotoImage(name='dashboard', file=assets_path / 'dashboard_icon.png'),
                tk.PhotoImage(name='reports', file=assets_path / 'reports_icon.png'),
                tk.PhotoImage(name='help', file=assets_path / 'help_icon.png')
                ]
        except tk.TclError as e:
            print(f"Error loading images: {e}")
            print(f"Attempted to load images from: {assets_path.resolve()}")
            if "no such file or directory" in str(e):
                print("-> Check if the image files (sugarcane.png, dashboard_icon.png, etc.) exist in that directory.")
                print("-> If they are in a subfolder (e.g., 'images' or 'assets'), update the 'assets_path' variable accordingly.")
            raise RuntimeError(f"Failed to load required images from {assets_path}") from e
        except Exception as e:
            print(f"An unexpected error occurred during image loading: {e}")
            raise


        if not self.images:
             print("Image list is empty. Cannot continue.")
             master.destroy()
             return

        self.images[0]= self.images[0].subsample(2)

        sidebar_frame = tk.Frame(self, bg='#9E8DB9', width=50)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        logo_text = tk.Label(
            master=sidebar_frame,
            text='CANECHECK',
            font=('Lexend', 14, 'bold'),
            bg='#9E8DB9',
            fg='white' )


        logo = tk.Label(
            master=sidebar_frame,
            image=self.images[0],
            bg='#9E8DB9',
            borderwidth=0 )

        logo.grid(row = 0, column = 0, pady = 15)

        pages = ["Dashboard","Reports"]
        self.pages = {}

        rownum = 1
        for page_name in pages:
            image_index = pages.index(page_name) + 1
            if image_index < len(self.images):
                 self.images[image_index] = self.images[image_index].subsample(4)

                 logo_button = tk.Button(
                     master=sidebar_frame,
                     image=self.images[image_index],
                     compound=tk.TOP,
                     borderwidth=0,
                     bg='#9E8DB9',
                     highlightthickness = 0, bd = 0,
                     command=lambda p=page_name: self.show_page(p)
                 )
                 logo_button.grid(row=rownum, column = 0, pady = 2)

                 text_button = tk.Button(
                    master=sidebar_frame,
                    text=page_name,
                    font=('Arial', 14),
                    bg='#9E8DB9',
                    fg='white',
                    highlightthickness = 0, bd = 0,
                    command=lambda p=page_name: self.show_page(p)
                 )

            else:
                print(f"Warning: Missing image for page '{page_name}' at expected index {image_index}.")
                text_button = tk.Button(
                    master=sidebar_frame,
                    text=page_name,
                    font=('Arial', 14),
                    bg='#9E8DB9',
                    fg='white',
                    highlightthickness=0, bd=0,
                    command=lambda p=page_name: self.show_page(p)
                )
                text_button.grid(row=rownum, column=0, pady=2)

            rownum +=1

        try:
            self.pages["Dashboard"] = UiPage(self)
            self.pages["Reports"] = ReportsPage(self)
        except NameError as e:
            print(f"Error creating page instances: {e}")
            print("Make sure the imported page classes (UiPage, ReportsPage) are defined correctly.")
            master.destroy()
            return
        except Exception as e:
            print(f"An unexpected error occurred creating page instances: {e}")
            master.destroy()
            return


        if "Dashboard" in self.pages:
            self.show_page("Dashboard")
        else:
            print("Error: Dashboard page not found after initialization.")


    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()

        if page_name in self.pages:
            self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        else:
            print(f"Error: Attempted to show non-existent page '{page_name}'")


if __name__ == '__main__':
    app = tk.Tk()
    app.title("CaneCheck: Sugarcane Variety Detection")
    app.geometry("800x480")

    try:
        main_app = CaneCheckMain(app)
        app.mainloop()
    except Exception as e:
        print("\n--- An unhandled error occurred ---")
        import traceback
        traceback.print_exc()
        print("------------------------------------")
        try:
            from tkinter import messagebox
            messagebox.showerror("Application Error", f"A critical error occurred:\n\n{e}\n\nSee console for details.")
        except:
            pass
        finally:
             if 'app' in locals() and app.winfo_exists():
                 app.destroy()