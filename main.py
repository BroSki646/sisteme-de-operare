import tkinter as tk
from timer import CountdownTimer


def main():
  root = tk.Tk()
  app = CountdownTimer(root)
  root.mainloop()


if __name__ == "__main__":
  main()