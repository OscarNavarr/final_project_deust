import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


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
        tk.Button(root, text="Afficher le dernier statut", command=self.get_status).pack(pady=5)

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
        uuid = self.uuid_entry.get()    # 12312fz-12dd-1dad-11da5
        position = self.position_entry.get()
        status = self.status_entry.get()

        if not uuid or not position or not status:
            messagebox.showwarning("Champs manquants", "Remplissez tous les champs.")
            return

        try:
            # get the last instruction ID
            instructionID_reponse = requests.get(f"{BASE_URL}/robot/{uuid}/status")
            data = instructionID_reponse.json()

            if instructionID_reponse.status_code != 200 or "instructionId" not in data:
                messagebox.showerror("Erreur", "Impossible de récupérer l'ID de la dernière instruction.")
                return
            inst_id = data["instructionId"]
            robot_id = data["robot_id"]

            # send the status update
            response = requests.post(
                f"{BASE_URL}/update_status/",
                #params={"robot_id": uuid, "instructionID": inst_id,"position": position, "status": status}
                json={"robot_id": robot_id, "instructionID": inst_id, "position": position, "status": status}
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

            # get the robot ID by UUID
            robot_data_response = requests.post(
                f"{BASE_URL}/robot_data_by_uuid",
                json={"uuid": uuid}
            )
            robot_data = robot_data_response.json()
            if robot_data_response.status_code != 200 or "id" not in robot_data:
                messagebox.showerror("Erreur", "Impossible de récupérer l'ID du robot.")
                return
            robot_id = robot_data["id"]
            response = requests.post(
                f"{BASE_URL}/create_instruction",
                json={"robot_id": robot_id, "instruction": instruction}
            )
            if response.status_code == 200:
                messagebox.showinfo("Succès", "Instruction envoyée avec succès.")
            else:
                messagebox.showerror("Erreur", f"Erreur: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la requête: {e}")

    def show_stats(self):
        try:
            status_data = requests.post(
                f"{BASE_URL}/all_status_by_uuid/",
                json={"uuid": self.uuid_entry.get()}
            )
            if status_data.status_code != 200:
                messagebox.showerror("Erreur", "Impossible de récupérer les statistiques.")
                return
            stats = status_data.json()

            if not stats or "message" in stats:
                messagebox.showinfo("Statistiques", "Aucune statistique disponible pour ce robot.")
                return

            cubes = defaultdict(lambda: {"pickup": 0, "drop": 0, "last": None})
            total_actions = 0

            for entry in stats:
                status = entry["status"]
                timestamp = entry["timestamp"]

                if "pickup_c" in status or "drop_c" in status:
                    cube_id = status.split("_c")[-1]
                    action = "pickup" if "pickup" in status else "drop"
                    cubes[cube_id][action] += 1
                    cubes[cube_id]["last"] = timestamp
                    total_actions += 1

            # Mostrar ventana de estadísticas en texto
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Statistiques du Robot")
            stats_text = tk.Text(stats_window, height=20, width=80)
            stats_text.pack()

            stats_text.insert(tk.END, "📊 Statistiques globales du robot\n\n")
            stats_text.insert(tk.END, f"Total de cubes manipulés : {len(cubes)}\n")
            stats_text.insert(tk.END, f"Nombre total d'actions (pickup/drop) : {total_actions}\n")
            stats_text.insert(tk.END, "-" * 50 + "\n")

            for cube_id, data in sorted(cubes.items()):
                stats_text.insert(tk.END, f"🧊 Cube c{cube_id} :\n")
                stats_text.insert(tk.END, f"  - Pickups : {data['pickup']}\n")
                stats_text.insert(tk.END, f"  - Drops   : {data['drop']}\n")
                stats_text.insert(tk.END, f"  - Dernière action : {data['last']}\n")
                stats_text.insert(tk.END, "-" * 50 + "\n")

            stats_text.config(state=tk.DISABLED)

            # 🔥 Mostrar gráfico con matplotlib
            absolute_times = []
            cube_ids = []
            actions = []

            for entry in reversed(stats):  # orden cronológico
                status = entry["status"]
                timestamp = entry["timestamp"]
                if "pickup_c" in status or "drop_c" in status:
                    cube_id = int(status.split("_c")[-1])
                    action = "pickup" if "pickup" in status else "drop"
                    ts = datetime.fromisoformat(timestamp)
                    absolute_times.append(ts)
                    cube_ids.append(cube_id)
                    actions.append(action)

            if not absolute_times:
                messagebox.showinfo("Statistiques", "Aucune donnée temporelle à afficher.")
                return

            # Convertimos a minutos desde el primer evento
            start_time = absolute_times[0]
            relative_minutes = [(ts - start_time).total_seconds() / 60.0 for ts in absolute_times]

            # Dibujar gráfico
            plt.figure(figsize=(10, 5))
            colors = ["blue" if a == "pickup" else "orange" for a in actions]

            plt.scatter(relative_minutes, cube_ids, c=colors, s=100, label="pickup/drop")
            for i, action in enumerate(actions):
                plt.text(relative_minutes[i], cube_ids[i] + 0.2, action, ha='center', fontsize=8)

            plt.xticks(rotation=45)
            plt.xlabel("Temps écoulé (minutes)")
            plt.ylabel("Cube")
            plt.title("Timeline des cubes manipulés (temps relatif)")
            plt.yticks(range(0, max(cube_ids)+1), [f"c{i}" for i in range(max(cube_ids)+1)])
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des stats: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotSimulatorApp(root)
    root.mainloop()
