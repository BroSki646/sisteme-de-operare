import datetime
import tkinter as tk
from tkinter import messagebox

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer Numărătoare Inversă")
        self.root.geometry("380x280")
        self.root.resizable(False, False)

        self.running = False
        self.target_datetime = None

        # --- Etichete și câmpuri de introducere ---
        # Data (format YYYY-MM-DD)
        tk.Label(root, text="Data țintă (YYYY-MM-DD):", font=("Helvetica", 10)).pack(pady=(15, 2))
        self.entry_date = tk.Entry(root, font=("Helvetica", 11), justify="center")
        self.entry_date.pack()
        # Setăm automat data de azi ca exemplu
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        self.entry_date.insert(0, today_str)

        # Ora (format HH:MM:SS sau HH:MM)
        tk.Label(root, text="Ora țintă (HH:MM:SS):", font=("Helvetica", 10)).pack(pady=(10, 2))
        self.entry_time = tk.Entry(root, font=("Helvetica", 11), justify="center")
        self.entry_time.pack()
        self.entry_time.insert(0, "18:00:00")

        # Afișaj Timer
        self.label_timer = tk.Label(root, text="00:00:00", font=("Helvetica", 28, "bold"), fg="#1E88E5")
        self.label_timer.pack(pady=15)

        # Buton Start
        self.btn_start = tk.Button(
            root,
            text="START",
            font=("Helvetica", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=3,
            command=self.start_timer
        )
        self.btn_start.pack()

    def start_timer(self):
        if self.running:
            return

        date_str = self.entry_date.get().strip()
        time_str = self.entry_time.get().strip()

        # Validare și conversie dată/oră
        try:
            full_datetime_str = f"{date_str} {time_str}"
            try:
                self.target_datetime = datetime.datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.target_datetime = datetime.datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror(
                "Eroare de format",
                "Format incorect!\nFolosiți:\nData: YYYY-MM-DD\nOra: HH:MM:SS"
            )
            return

        now = datetime.datetime.now()
        if self.target_datetime <= now:
            messagebox.showwarning(
                "Atenție", "Data și ora specificate trebuie să fie în viitor!"
            )
            return

        self.running = True
        self.btn_start.config(state=tk.DISABLED)
        self.update_timer()

    def update_timer(self):
        if not self.running:
            return

        now = datetime.datetime.now()
        diff = self.target_datetime - now

        if diff.total_seconds() <= 0:
            self.label_timer.config(text="00:00:00", fg="#D32F2F")
            self.running = False
            self.btn_start.config(state=tk.NORMAL)
            messagebox.showinfo("Timpul a expirat!", "Numărătoarea inversă s-a încheiat!")
            return

        total_seconds = int(diff.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if days > 0:
            time_format = f"{days}z {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_format = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.label_timer.config(text=time_format)

        self.root.after(1000, self.update_timer)