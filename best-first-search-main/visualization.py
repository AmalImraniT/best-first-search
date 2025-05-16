import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import numpy as np

class GraphVisualizer:
    """
    Classe pour visualiser le graphe et les résultats de l'algorithme BFS.
    """
    def __init__(self, graph):
        """
        Initialise le visualiseur avec un graphe.
        
        Args:
            graph: Instance de la classe Graph à visualiser
        """
        self.graph = graph
        self.fig = None
        self.ax = None
        self.pos = None
        
    def draw_graph(self, title="Graphe"):
        """
        Dessine le graphe avec les nœuds et les arêtes.
        
        Args:
            title: Titre du graphique
        """
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        graph_nx = self.graph.graph
        
        # Utiliser spring_layout pour positionner les nœuds automatiquement
        self.pos = nx.spring_layout(graph_nx, seed=42)
        
        # Couleurs et styles personnalisés
        node_colors = []
        node_border_colors = []
        for node in graph_nx.nodes():
            if node == self.graph.start_node:
                node_colors.append("#274690")  # Bleu foncé
                node_border_colors.append("#142850")
            elif node == self.graph.goal_node:
                node_colors.append("#f9a826")  # Orange
                node_border_colors.append("#c97d10")
            else:
                node_colors.append("#21e6c1")  # Turquoise
                node_border_colors.append("#146356")
        
        # Dessiner les arêtes avec style
        nx.draw_networkx_edges(
            graph_nx, self.pos, arrows=True, arrowsize=25, width=2.5, edge_color="#393e46", style="dashed", ax=self.ax
        )
        # Labels des arêtes
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
        nx.draw_networkx_edge_labels(
            graph_nx, self.pos, edge_labels=edge_labels, font_color="#f9a826", font_size=12, ax=self.ax
        )
        # Labels des nœuds
        node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" for node in graph_nx.nodes()}
        # Nœuds avec bordures
        nx.draw_networkx_nodes(
            graph_nx, self.pos, node_color=node_colors, node_size=900, edgecolors=node_border_colors, linewidths=3, ax=self.ax
        )
        nx.draw_networkx_labels(
            graph_nx, self.pos, labels=node_labels, font_size=13, font_color="#232946", font_weight="bold", ax=self.ax
        )
        plt.title(title, fontsize=18, color="#f9a826", fontweight="bold")
        plt.axis('off')
        self.fig.patch.set_facecolor("#ffffff")  # Fond blanc figure
        self.ax.set_facecolor("#ffffff")         # Fond blanc axes
        return self.fig, self.ax
    
    def visualize_path(self, path, title="Chemin trouvé par Best-First Search"):
        """
        Visualise le chemin trouvé par l'algorithme.
        
        Args:
            path: Liste des nœuds formant le chemin solution
            title: Titre du graphique
        """
        if path is None:
            print("Aucun chemin trouvé.")
            return
        
        fig, ax = self.draw_graph(title)
        
        # Créer une liste des arêtes du chemin pour les mettre en évidence
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        
        # Mettre en évidence les arêtes du chemin
        nx.draw_networkx_edges(
            self.graph.graph, self.pos, edgelist=path_edges, edge_color="#a259f7", width=5, style="solid", ax=ax
        )
        
        # Mettre en évidence les nœuds du chemin (hors départ/arrivée)
        path_nodes = path[1:-1]
        if path_nodes:
            nx.draw_networkx_nodes(
                self.graph.graph, self.pos, nodelist=path_nodes, node_color="#a259f7", node_size=1100, edgecolors="#232946", linewidths=4, ax=ax
            )
        
        fig.patch.set_facecolor("#ffffff")  # Fond blanc figure
        ax.set_facecolor("#ffffff")         # Fond blanc axes
        return fig, ax
    
    def animate_search(self, steps, path, interval=1000, save_animation=False, filename='search_animation.mp4'):
        """
        Crée une animation de l'algorithme de recherche.
        
        Args:
            steps: Liste des états à chaque étape de l'algorithme
            path: Chemin final trouvé
            interval: Intervalle entre les images en millisecondes
            save_animation: Si True, sauvegarde l'animation dans un fichier
            filename: Nom du fichier pour sauvegarder l'animation
            
        Returns:
            Animation
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def init():
            ax.clear()
            graph_nx = self.graph.graph
            
            # Dessiner les arêtes
            nx.draw_networkx_edges(graph_nx, self.pos, arrows=True, arrowsize=25, width=2.5, edge_color="#393e46", style="dashed", ax=ax)
            
            # Dessiner les nœuds avec leur label et valeur heuristique
            node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" for node in graph_nx.nodes()}
            
            # Couleurs spéciales pour les nœuds
            node_colors = []
            node_border_colors = []
            for node in graph_nx.nodes():
                if node == self.graph.start_node:
                    node_colors.append("#274690")
                    node_border_colors.append("#142850")
                elif node == self.graph.goal_node:
                    node_colors.append("#f9a826")
                    node_border_colors.append("#c97d10")
                else:
                    node_colors.append("#21e6c1")
                    node_border_colors.append("#146356")
            
            nx.draw_networkx_nodes(graph_nx, self.pos, node_color=node_colors, node_size=900, edgecolors=node_border_colors, linewidths=3, ax=ax)
            nx.draw_networkx_labels(graph_nx, self.pos, labels=node_labels, font_size=13, font_color="#232946", font_weight="bold", ax=ax)
            
            # Dessiner les poids des arêtes
            edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
            nx.draw_networkx_edge_labels(graph_nx, self.pos, edge_labels=edge_labels, font_color="#f9a826", font_size=12, ax=ax)
            
            ax.set_title("Exécution de Best-First Search", fontsize=18, color="#f9a826", fontweight="bold")
            ax.axis('off')
            fig.patch.set_facecolor("#ffffff")  # Fond blanc figure
            ax.set_facecolor("#ffffff")         # Fond blanc axes
            return []
        
        def update(frame_num):
            ax.clear()
            step = steps[frame_num] if frame_num < len(steps) else steps[-1]
            
            graph_nx = self.graph.graph
            
            # Dessiner toutes les arêtes normales
            nx.draw_networkx_edges(graph_nx, self.pos, arrows=True, arrowsize=25, width=2.5, edge_color="#393e46", style="dashed", ax=ax)
            
            # Dessiner les poids des arêtes
            edge_labels = {(u, v): f"{d['weight']}" for u, v, d in graph_nx.edges(data=True)}
            nx.draw_networkx_edge_labels(graph_nx, self.pos, edge_labels=edge_labels, font_color="#f9a826", font_size=12, ax=ax)
            
            # Préparer les couleurs des nœuds selon leur état
            node_colors = []
            node_border_colors = []
            for node in graph_nx.nodes():
                if node == self.graph.start_node:
                    node_colors.append("#274690")
                    node_border_colors.append("#142850")
                elif node == self.graph.goal_node:
                    node_colors.append("#f9a826")
                    node_border_colors.append("#c97d10")
                elif node == step['current']:
                    node_colors.append("#ff5e5b")  # Nœud actuel : rouge vif
                    node_border_colors.append("#c81d25")
                elif node in step['visited']:
                    node_colors.append("#b2bec3")  # Gris clair pour exploré
                    node_border_colors.append("#636e72")
                else:
                    node_colors.append("#21e6c1")
                    node_border_colors.append("#146356")
            
            # Dessiner tous les nœuds
            nx.draw_networkx_nodes(graph_nx, self.pos, node_color=node_colors, node_size=900, edgecolors=node_border_colors, linewidths=3, ax=ax)
            
            # Dessiner les labels des nœuds
            node_labels = {node: f"{node}\nh={graph_nx.nodes[node]['heuristic']}" for node in graph_nx.nodes()}
            nx.draw_networkx_labels(graph_nx, self.pos, labels=node_labels, font_size=13, font_color="#232946", font_weight="bold", ax=ax)
            
            # Dessiner le chemin trouvé jusqu'à présent
            path_so_far = step['path_so_far']
            if len(path_so_far) > 1:
                path_edges = [(path_so_far[i], path_so_far[i+1]) for i in range(len(path_so_far)-1)]
                nx.draw_networkx_edges(graph_nx, self.pos, edgelist=path_edges, edge_color="#a259f7", width=5, style="solid", ax=ax)
                nx.draw_networkx_nodes(graph_nx, self.pos, nodelist=path_so_far[1:-1], node_color="#a259f7", node_size=1100, edgecolors="#232946", linewidths=4, ax=ax)
            
            # Ajouter des informations sur l'état actuel
            info_text = f"Étape {frame_num+1}/{len(steps)}\n"
            info_text += f"Nœud actuel: {step['current']}\n"
            info_text += f"Nœuds visités: {', '.join(step['visited'])}\n"
            
            # Ajouter un titre
            if step['current'] == self.graph.goal_node:
                ax.set_title("Objectif atteint!", fontsize=18, color="#f9a826", fontweight="bold")
            else:
                ax.set_title(f"Exploration du nœud {step['current']}", fontsize=18, color="#f9a826", fontweight="bold")
            
            ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=12, color="#eebbc3",
                   bbox=dict(facecolor='#232946', edgecolor='#f9a826', boxstyle='round,pad=0.5', alpha=0.8))
            
            ax.axis('off')
            fig.patch.set_facecolor("#ffffff")  # Fond blanc figure
            ax.set_facecolor("#ffffff")         # Fond blanc axes
            return []
        
        # Créer l'animation
        ani = animation.FuncAnimation(fig, update, frames=len(steps), init_func=init, blit=True, interval=interval)
        
        # Sauvegarder l'animation si demandé
        if save_animation:
            # S'assurer que ffmpeg est installé pour MP4
            writer = animation.FFMpegWriter(fps=1)
            ani.save(filename, writer=writer)
        
        plt.close()  # Fermer la figure mais pas l'animation
        return ani
    
    def show(self):
        """Affiche la visualisation."""
        plt.tight_layout()
        plt.show()
    
    def save_figure(self, filename):
        """
        Sauvegarde la figure actuelle dans un fichier.
        
        Args:
            filename: Nom du fichier pour sauvegarder la figure
        """
        plt.savefig(filename, bbox_inches='tight')