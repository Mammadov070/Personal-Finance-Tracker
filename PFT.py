import random
import tkinter as tk
from PIL import Image, ImageTk


main_window = tk.Tk()

main_window.geometry("300x400")
main_window.title("Personal Finance Tracker")



greeting = tk.Label(main_window, text = "Welcome To Personal Finance Tracker", font = ("calibri", 14))
greeting.pack()

username = tk.Label(main_window, text="Username", font=("calibri", 14))
username.pack()

password = tk.Label(main_window, text="Password", font=("calibri", 14))
password.pack()

user_entry = tk.Entry(main_window, font=("calibri", 14))
user_entry.pack()

pass_entry = tk.Entry(main_window, show="*", font=("calibri", 14))
pass_entry.pack()

button = tk.Button(text="Enter", width=5, height=1, bg="white", fg="black")
button.pack()


main_window.mainloop()
