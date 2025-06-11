import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://0.0.0.0:8000"

class RobotSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Console de Contrôle du Robot")

        # UUID
        tk.Label(root, text="UUID du robot:").pack()
        self.uuid_entry = tk.Entry(root, width=40)
        self.uuid_entry.pack()

        # STATUS
        self.status_text = tk.Text(root, height=10, width=60)
        self.status_text.pack()
        tk.Button(root, text="Afficher état", command=self.get_status).pack(pady=5)

        # ENVIAR STATUS
        tk.Label(root, text="Position:").pack()
        self.position_entry = tk.Entry(root, width=40)
        self.position_entry.pack()
        tk.Label(root, text="État (ex: obstacle):").pack()
        self.status_entry = tk.Entry(root, width=40)
        self.status_entry.pack()
        tk.Button(root, text="Envoyer mise à jour", command=self.send_status).pack(pady=10)

        # ENVIAR INSTRUCTION
        tk.Label(root, text="Nouvelle instruction:").pack()
        self.instruction_entry = tk.Entry(root, width=40)
        self.instruction_entry.pack()
        tk.Button(root, text="Envoyer instruction", command=self.send_instruction).pack(pady=5)

        # AFFICHER STATISTIQUES
        tk.Button(root, text="Afficher statistiques", command=self.show_stats).pack(pady=10)

    def get_status(self):
        uuid = self.uuid_entry.get()
        if not uuid:
            messagebox.showwarning("UUID manquant", "Entrez un UUID valide.")
            return

        try:
            response = requests.get(f"{BASE_URL}/robot/{uuid}/status")
            data = response.json()

            self.status_text.delete("1.0", tk.END)

            if response.status_code == 200 and "ligne" in data:
                self.status_text.insert(tk.END, f"Position: {data['ligne']}\n")
                self.status_text.insert(tk.END, f"État: {data['status']}\n")
                self.status_text.insert(tk.END, f"Horodatage: {data['timestamp']}")
            else:
                self.status_text.insert(tk.END, data.get("message", "Aucun état trouvé ou erreur."))
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
                f"{BASE_URL}/update_status/",
                params={"robot_id": uuid, "position": position, "status": status}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Mise à jour envoyée.")
                self.get_status()
            else:
                messagebox.showerror("Erreur", f"Erreur: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la requête: {e}")

    def send_instruction(self):
        uuid = self.uuid_entry.get()
        instruction = self.instruction_entry.get()
        if not uuid or not instruction:
            messagebox.showwarning("Champs manquants", "UUID ou instruction manquants.")
            return

        try:
            response = requests.post(
                f"{BASE_URL}/create_instruction",
                json={"robot_id": uuid, "instruction": instruction}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Instruction envoyée avec succès.")
            else:
                messagebox.showerror("Erreur", f"Erreur: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la requête: {e}")

    def show_stats(self):
        try:
            status_data = requests.get(f"{BASE_URL}/all_status/").json()
            robots = {}
            for r in status_data:
                rid = r[0]
                robots[rid] = robots.get(rid, 0) + 1

            stats = "Statistiques d'utilisation des REF :\n"
            for robot_id, count in robots.items():
                stats += f"- Robot {robot_id[:8]}... : {count} états\n"

            self.status_text.delete("1.0", tk.END)
            self.status_text.insert(tk.END, stats)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des stats: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotSimulatorApp(root)
    root.mainloop()
