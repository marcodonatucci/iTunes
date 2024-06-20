import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._selected_album = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        d = self._view._txtInDurata.value
        if d is None or d == '':
            self._view.txt_result.controls.append(ft.Text("Inserisci una durata!", color='red'))
            self._view.update_page()
            return
        if not str(d).isdigit():
            self._view.txt_result.controls.append(ft.Text("Inserisci una durata in formato numerico!", color='red'))
            self._view.update_page()
            return
        flag = self._model.buildGraph(d)
        if flag:
            self._view.txt_result.controls.append(ft.Text(flag))
            self._view._ddAlbum.options.clear()
            nodi = self._model.get_nodes()
            for n in nodi:
                self._view._ddAlbum.options.append(ft.dropdown.Option(text=n.Title, data=n, on_click=self.readDDalbum))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore nella creazione del grafo!", color='red'))
            self._view.update_page()
            return

    def getSelectedAlbum(self, e):
        self._view._ddAlbum.options.clear()
        nodi = self._model.get_nodes()
        for n in nodi: 
            self._view._ddAlbum.options.append(ft.dropdown.Option(text=n.Title, data=n, on_click=self.readDDalbum))
        self._view.update_page()

    def handleAnalisiComp(self, e):
        self._view.txt_result.controls.clear()
        if self._model.graph is None:
            self._view.txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_album is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un album!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.analyze(self._selected_album)
        if componenti:
            self._view.txt_result.controls.append(ft.Text(f"Lunghezza componente connessa: {componenti[0]}, "
                                                          f"durata totale degli album della componente connessa: "
                                                          f"{componenti[1]}min."))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore durante l'analisi dei componenti!", color='red'))
            self._view.update_page()
            return

    def handleGetSetAlbum(self, e):
        self._view.txt_result.controls.clear()
        if self._model.graph is None:
            self._view.txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if self._selected_album is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un album!", color='red'))
            self._view.update_page()
            return
        if self._view._txtInSoglia.value is None or self._view._txtInSoglia.value == '':
            self._view.txt_result.controls.append(ft.Text("Selezionare una soglia!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(self._selected_album, float(self._view._txtInSoglia.value))
        if componenti:
            for c in componenti:
                self._view.txt_result.controls.append(ft.Text(f"{c.Title}"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(ft.Text("Errore durante l'analisi dei componenti!", color='red'))
            self._view.update_page()
            return
    
    def readDDalbum(self, e):
        if e.control.data is None:
            self._selected_album = None
        else:
            self._selected_album = e.control.data
            