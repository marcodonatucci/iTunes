import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestdTot = 0
        self._bestComp = []
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, durata):
        self.graph.clear()
        lista_album = DAO.getAlbum(durata)
        self.graph.add_nodes_from(lista_album)
        for node in self.graph.nodes:
            self.idMap[node.AlbumId] = node
        archi = DAO.getConnessioni(durata, self.idMap)
        for arco in archi:
            self.graph.add_edge(arco.album1, arco.album2)
        return f"Grafo creato con {len(self.graph.nodes)} nodi e {len(self.graph.edges)} archi"

    def get_nodes(self):
        return self.graph.nodes

    def analyze(self, album):
        comp = nx.node_connected_component(self.graph, album)
        durata = 0
        for a in comp:
            durata += a.durata_totale
        return len(comp), durata

    def getPath(self, a0, dTot):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = [a0]
        comp = nx.node_connected_component(self.graph, a0)
        for a in comp:
            if a not in parziale and (self._getScore(parziale) + a.durata_totale) < dTot:
                parziale.append(a)
                self._ricorsionev2(parziale, dTot)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp

    def _ricorsionev2(self, parziale, dTot):
        # verifico se soluzione è migliore di quella salvata in cache
        if len(parziale) > len(self._bestComp) and self._getScore(parziale) < dTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = self._getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        comp = nx.node_connected_component(self.graph, parziale[0])
        for a in comp:
            if a not in parziale and (self._getScore(parziale) + a.durata_totale) < dTot:
                parziale.append(a)
                self._ricorsionev2(parziale, dTot)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    def _getScore(self, listOfNodes):
        durata = 0
        for a in listOfNodes:
            durata += a.durata_totale
        return durata


