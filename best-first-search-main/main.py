import os
import sys
import matplotlib.pyplot as plt
from graph import Graph
from algorithms import BestFirstSearch
from visualization import GraphVisualizer
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class BestFirstSearchApp:
    """
    Application principale pour exécuter et visualiser l'algorithme Best-First Search.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Visualiseur Best-First Search")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ffffff")  # Fond blanc partout
        
        # Variables
        self.graph = None
        self.visualizer = None
        self.results = None
        
        # Création du répertoire pour les exemples s'il n'existe pas
        os.makedirs("example_graphs", exist_ok=True)
        
        # Créer l'interface utilisateur
        self._create_widgets()
        
    def _create_widgets(self):
        """Crée les widgets de l'interface utilisateur."""
        # Frame principale
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        button_style = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "#ffffff",          # Fond blanc pour les boutons
            "fg": "#232946",          # Texte foncé
            "activebackground": "#e6e6e6",
            "activeforeground": "#232946",
            "bd": 1,
            "relief": tk.GROOVE,
            "padx": 16,
            "pady": 8,
            "cursor": "hand2"
        }
        
        # Boutons principaux
        tk.Button(button_frame, text="Charger un graphe", command=self.load_graph, **button_style).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Sauvegarder le graphe", command=self.save_graph, **button_style).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Exécuter Best-First Search", command=self.run_bfs, **button_style).pack(side=tk.LEFT, padx=10)
        
        # Frame pour le graphe
        self.graph_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Zone de texte pour les informations
        self.info_text = tk.Text(
            main_frame,
            height=8,
            font=("Consolas", 12),
            bg="#ffffff",        # Fond blanc pour la console utilisateur
            fg="#232946",        # Texte foncé pour le contraste
            bd=0,
            relief=tk.FLAT
        )
        self.info_text.pack(fill=tk.X, pady=5)
        
        # Message initial
        self.update_info("Bienvenue dans le visualiseur de Best-First Search !\n"
                        "Chargez un graphe pour commencer.")
        
    def update_info(self, message):
        """Met à jour la zone d'information avec un message."""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        self.info_text.config(state=tk.DISABLED)
    
    def load_graph(self):
        """Charge un graphe depuis un fichier JSON."""
        try:
            filename = filedialog.askopenfilename(
                title="Sélectionner un fichier de graphe",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
            )
            
            if not filename:  # L'utilisateur a annulé
                return
            
            self.graph = Graph.load_from_file(filename)
            self.visualizer = GraphVisualizer(self.graph)
            
            self.display_graph()
            self.update_info(f"Graphe chargé depuis {filename}\n"
                           f"Nœud de départ: {self.graph.start_node}\n"
                           f"Nœud d'arrivée: {self.graph.goal_node}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le graphe: {str(e)}")
    
    def save_graph(self):
        """Sauvegarde le graphe courant dans un fichier JSON."""
        if not self.graph:
            messagebox.showerror("Erreur", "Aucun graphe à sauvegarder.")
            return
        try:
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder le graphe",
                defaultextension=".json",
                filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
            )
            if not filename:
                return
            self.graph.save_to_file(filename)
            self.update_info(f"Graphe sauvegardé dans {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde du graphe: {str(e)}")
    
    def display_graph(self):
        """Affiche le graphe dans l'interface."""
        # Effacer les widgets existants dans le frame du graphe
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if self.graph and self.visualizer:
            fig, ax = self.visualizer.draw_graph("Graphe initial")
            
            # Intégrer la figure matplotlib dans tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Ajouter une barre d'outils pour naviguer dans le graphique
            toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def run_bfs(self):
        """Exécute l'algorithme Best-First Search et affiche les résultats."""
        if not self.graph:
            messagebox.showerror("Erreur", "Veuillez d'abord charger un graphe.")
            return
        
        try:
            # Exécuter l'algorithme
            bfs = BestFirstSearch(self.graph)
            path, expanded_nodes, steps = bfs.search()
            self.results = (path, expanded_nodes, steps)
            
            # Afficher le chemin trouvé
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if path:
                fig, ax = self.visualizer.visualize_path(path, "Chemin trouvé par Best-First Search")
                
                # Intégrer la figure matplotlib dans tkinter
                canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Ajouter une barre d'outils pour naviguer dans le graphique
                toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
                toolbar.update()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Mise à jour des informations
                path_str = " → ".join(path)
                expanded_str = " → ".join(expanded_nodes)
                
                self.update_info(f"Chemin trouvé : {path_str}\n"
                              f"Nœuds explorés : {expanded_str}\n"
                              f"Longueur du chemin : {len(path)-1} arêtes")
            else:
                self.update_info("Aucun chemin trouvé de {} à {}".format(
                    self.graph.start_node, self.graph.goal_node))
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution de Best-First Search: {str(e)}")

def main():
    root = tk.Tk()
    app = BestFirstSearchApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()