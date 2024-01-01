import tkinter as tk


root = tk.Tk()

w = tk.Text(root, width=40, height=1)
w.insert(tk.END, "tmp/Seq_5_T2_FL2D_TRA_STERN_png")
w.pack()

w = tk.Scale(root, from_=0, to=200, orient=tk.HORIZONTAL)
w.pack()
w = tk.Scale(root, from_=0, to=200, orient=tk.VERTICAL)
w.pack()

tk.mainloop()
