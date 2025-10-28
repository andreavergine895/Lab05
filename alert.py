import flet as ft  # Importa la libreria Flet per i controlli grafici

class AlertManager:
    """
    Classe che gestisce la visualizzazione di finestre di avviso (AlertDialog) all’interno dell’app Flet.
    È usata per mostrare messaggi di errore o notifiche all’utente.
    """

    def __init__(self, page: ft.Page):
        # Memorizza la pagina (necessaria per aggiungere l’alert)
        self._page = page

        # Crea un componente di tipo AlertDialog (una finestra popup)
        self._alert_dialog = ft.AlertDialog(
            title=ft.Text(""),  # Il testo del messaggio verrà impostato dinamicamente
            actions=[  # Pulsanti presenti nella finestra
                ft.TextButton("OK", on_click=self.close)  # Chiude la finestra quando si preme OK
            ]
        )

    def show_alert(self, message: str):
        """
        Mostra un messaggio di avviso a schermo.
        Se l’alert non è ancora presente nella pagina, lo aggiunge all’overlay.
        """
        self._alert_dialog.title.value = message  # Imposta il messaggio del titolo
        if self._alert_dialog not in self._page.overlay:
            # Se l’alert non è ancora stato aggiunto alla pagina, lo inserisce nell’overlay
            self._page.overlay.append(self._alert_dialog)

        # Mostra effettivamente l’alert
        self._alert_dialog.open = True
        self._page.update()  # Aggiorna la pagina per rendere visibile la finestra

    def close(self, e):
        """Chiude la finestra di avviso."""
        self._alert_dialog.open = False  # Nasconde la finestra
        self._page.update()  # Aggiorna la pagina per riflettere la modifica
