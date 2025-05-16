import heapq

class BestFirstSearch:
    """
    Implémentation de l'algorithme Best-First Search (recherche meilleur d'abord).
    Cet algorithme utilise une fonction heuristique pour guider la recherche vers le but.
    """

    
    
    def __init__(self, graph):
        """
        Initialise l'algorithme avec un graphe.
        
        Args:
            graph: Instance de la classe Graph contenant le graphe à explorer
        """
        self.graph = graph
        self.visited = set()
        self.path = {}  # Pour reconstruire le chemin
        self.expanded_nodes = []  # Liste des nœuds dans l'ordre où ils ont été explorés
        self.open_set = []  # File de priorité (heap) pour les nœuds à explorer
    
    def search(self):
        """
        Exécute l'algorithme Best-First Search sur le graphe.
        
        Returns:
            tuple: (chemin, nœuds_explorés, steps) où:
                - chemin est la liste des nœuds formant le chemin de la solution
                - nœuds_explorés est la liste des nœuds visités dans l'ordre
                - steps est une liste d'états pour visualiser l'exécution étape par étape
        """
        if not self.graph.start_node or not self.graph.goal_node:
            raise ValueError("Les nœuds de départ et d'arrivée doivent être définis")
        
        start = self.graph.start_node
        goal = self.graph.goal_node
        
        # Réinitialiser les structures de données
        self.visited = set()
        self.path = {}
        self.expanded_nodes = []
        self.open_set = []
        
        # Pour garder une trace de chaque étape pour la visualisation
        steps = []
        
        # Ajouter le nœud de départ à la file de priorité
        # Format (heuristic, node_id, parent)
        heapq.heappush(self.open_set, (self.graph.get_heuristic(start), start, None))
        
        while self.open_set:
            # Prendre le nœud avec la plus petite valeur heuristique
            _, current, parent = heapq.heappop(self.open_set)
            
            # Si le nœud a déjà été visité, passer au suivant
            if current in self.visited:
                continue
            
            # Marquer le nœud comme visité
            self.visited.add(current)
            self.expanded_nodes.append(current)
            
            # Enregistrer le parent pour reconstruire le chemin
            if parent:
                self.path[current] = parent
            
            # Enregistrer l'état actuel pour la visualisation
            steps.append({
                'current': current,
                'open_set': list(self.open_set),
                'visited': list(self.visited),
                'path_so_far': self._reconstruct_path(current)
            })
            
            # Si nous avons atteint l'objectif, terminer la recherche
            if current == goal:
                # Reconstruire et retourner le chemin trouvé
                path = self._reconstruct_path(current)
                return path, self.expanded_nodes, steps
            
            # Explorer les voisins non visités
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in self.visited:
                    # Ajouter le voisin à la file de priorité avec sa valeur heuristique
                    heapq.heappush(
                        self.open_set, 
                        (self.graph.get_heuristic(neighbor), neighbor, current)
                    )
        
        # Si aucun chemin n'est trouvé
        return None, self.expanded_nodes, steps
    
    def _reconstruct_path(self, node):
        """
        Reconstruit le chemin du nœud de départ jusqu'au nœud actuel.
        
        Args:
            node: Nœud actuel
            
        Returns:
            list: Liste des nœuds formant le chemin
        """
        path = [node]
        while node in self.path:
            node = self.path[node]
            path.append(node)
        
        # Inverser le chemin pour qu'il commence par le nœud de départ
        return path[::-1]