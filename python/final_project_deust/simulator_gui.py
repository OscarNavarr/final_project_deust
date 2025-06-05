# for execution, run the command: python3 simulator_gui.py

import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:8000"

class RobotSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controleur du Robot")

        # UUID input
        tk.Label(root, text="UUID du robot:").pack()
        self.uuid_entry = tk.Entry(root, width=40)
        self.uuid_entry.pack()

        # Status display
        self.status_text = tk.Text(root, height=10, width=60)
        self.status_text.pack()

        # Button to load status
        tk.Button(root, text="Afficher état", command=self.get_status).pack(pady=5)

        # Input for position and status
        tk.Label(root, text="Position:").pack()
        self.position_entry = tk.Entry(root, width=40)
        self.position_entry.pack()

        tk.Label(root, text="État:").pack()
        self.status_entry = tk.Entry(root, width=40)
        self.status_entry.pack()

        # Send status button
        tk.Button(root, text="Envoyer mise à jour", command=self.send_status).pack(pady=10)

    def get_status(self):
        uuid = self.uuid_entry.get()
        if not uuid:
            messagebox.showwarning("UUID manquant", "Entrez un UUID valide.")
            return

        try:
            response = requests.get(f"{BASE_URL}/robot/{uuid}/status")
            if response.status_code == 200:
                data = response.json()
                self.status_text.delete("1.0", tk.END)
                self.status_text.insert(tk.END, f"Position: {data['position']}\n")
                self.status_text.insert(tk.END, f"État: {data['status']}\n")
                self.status_text.insert(tk.END, f"Horodatage: {data['timestamp']}")
            else:
                self.status_text.delete("1.0", tk.END)
                self.status_text.insert(tk.END, "Aucun état trouvé ou erreur de requête.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la requête: {e}")

    def send_status(self):
        uuid = self.uuid_entry.get()
        position = self.position_entry.get()
        status = self.status_entry.get()

        if not uuid or not position or not status:
            messagebox.showwarning("Champs manquants", "Remplissez tous les champs.")
            return

        try:
            response = requests.post(
                f"{BASE_URL}/status/",
                params={"robot_id": uuid, "position": position, "status": status}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Mise à jour envoyée.")
                self.get_status()
            else:
                messagebox.showerror("Erreur", f"Erreur: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la requête: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotSimulatorApp(root)
    root.mainloop()
