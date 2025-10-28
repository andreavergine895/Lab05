import flet as ft
from alert import AlertManager  # Importa la classe che gestisce le finestre di avviso
from autonoleggio import Autonoleggio

# Nome del file CSV da cui vengono lette le automobili
FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    """
    Funzione principale dell'applicazione Flet.
    'page' rappresenta la finestra principale in cui vengono aggiunti tutti i controlli grafici.
    """

    # Impostazioni di base della pagina
    page.title = "Lab05"  # Titolo della finestra
    page.horizontal_alignment = "center"  # Centra gli elementi orizzontalmente
    page.theme_mode = ft.ThemeMode.DARK  # Tema iniziale: scuro

    # --- ALERT ---
    # Crea un gestore di avvisi (finestre di errore o notifiche)
    alert = AlertManager(page)

    # --- LOGICA ---
    # Crea un oggetto Autonoleggio (preso dal Lab03)
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")

    # Tenta di caricare i dati delle automobili dal file CSV
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO)
    except Exception as e:
        # Se c'è un errore (es. file mancante), mostra un alert
        alert.show_alert(f"❌ {e}")

    # --- UI ELEMENTI BASE ---
    # Titolo grande con il nome dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)

    # Sottotitolo con il nome del responsabile
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # Campo di testo per modificare il nome del responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # Lista che mostrerà tutte le automobili (usa un ListView per scorrimento verticale)
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # --- SEZIONE 3: NUOVA AUTO ---
    # Titolo della sezione
    txt_aggiungi_auto = ft.Text("Aggiungi Nuova Automobile", size=20)

    # Campi di testo per inserire i dati della nuova automobile
    input_marca = ft.TextField(label="Marca")
    input_modello = ft.TextField(label="Modello")
    input_anno = ft.TextField(label="Anno", width=150)

    # Campo di testo disabilitato per mostrare il numero di posti (modificabile solo con i pulsanti + e -)
    txt_posti = ft.TextField(
        width=80,
        disabled=True,  # Non modificabile direttamente
        value="0",
        border_color="green",
        text_align=ft.TextAlign.CENTER
    )

    # --- EVENT HANDLER: contatore dei posti ---
    # Aumenta il numero di posti quando si preme il pulsante "+"
    def aumenta_posti(e):
        val = int(txt_posti.value)
        txt_posti.value = str(val + 1)
        txt_posti.update()  # Aggiorna il valore mostrato sullo schermo

    # Diminuisce il numero di posti quando si preme il pulsante "-"
    def diminuisci_posti(e):
        val = int(txt_posti.value)
        if val > 1:  # Evita che scenda sotto 1
            txt_posti.value = str(val - 1)
            txt_posti.update()

    # Pulsanti per modificare il contatore dei posti
    btn_minus = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", on_click=diminuisci_posti)
    btn_plus = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", on_click=aumenta_posti)

    # Contenitore orizzontale con i due pulsanti e il campo del numero di posti
    row_posti = ft.Row(
        controls=[btn_minus, txt_posti, btn_plus],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # --- EVENT HANDLER: aggiunta di una nuova automobile ---
    def aggiungi_auto(e):
        """
        Controlla i dati inseriti e, se validi,
        aggiunge una nuova automobile all'autonoleggio.
        """
        # Legge i valori dai campi di testo
        marca = input_marca.value.strip()
        modello = input_modello.value.strip()
        anno_str = input_anno.value.strip()
        posti_str = txt_posti.value.strip()

        # Controlla che nessun campo sia vuoto
        if not marca or not modello or not anno_str or not posti_str:
            alert.show_alert("⚠️ Compila tutti i campi prima di aggiungere un'auto.")
            return

        # Verifica che i campi numerici siano validi
        try:
            anno = int(anno_str)
            posti = int(posti_str)
            if anno < 1900 or anno > 2025:
                raise ValueError
        except ValueError:
            alert.show_alert("❌ Anno o numero di posti non validi!")
            return

        # Se i dati sono validi, aggiunge l’auto alla lista dell’autonoleggio
        autonoleggio.aggiungi_automobile(marca, modello, anno, posti)

        # Pulisce i campi dopo l'inserimento
        input_marca.value = ""
        input_modello.value = ""
        input_anno.value = ""
        txt_posti.value = "4"

        # Aggiorna la lista di automobili mostrata a schermo
        aggiorna_lista_auto()
        page.update()

    # Pulsante che attiva la funzione di aggiunta auto
    btn_aggiungi_auto = ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_auto)

    # --- FUNZIONI DI SUPPORTO ---
    def aggiorna_lista_auto():
        """Aggiorna la lista delle automobili mostrate nella ListView."""
        lista_auto.controls.clear()  # Svuota la lista
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"  # Mostra se disponibile o no
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    def cambia_tema(e):
        """Cambia il tema da scuro a chiaro e viceversa."""
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        """Aggiorna il nome del responsabile con il valore inserito nel campo di testo."""
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # --- EVENTI E LAYOUT ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # --- LAYOUT PAGINA ---
    # Aggiunge tutti i componenti grafici alla pagina principale, nell’ordine desiderato
    page.add(
        toggle_cambia_tema,

        # Sezione 1: intestazione
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2: modifica responsabile
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        ft.Divider(),

        # Sezione 3: aggiunta nuova auto
        txt_aggiungi_auto,
        ft.Row([input_marca, input_modello, input_anno, row_posti],
               alignment=ft.MainAxisAlignment.CENTER),
        btn_aggiungi_auto,

        ft.Divider(),

        # Sezione 4: lista auto
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    # Carica subito la lista delle automobili all'avvio dell'app
    aggiorna_lista_auto()

# Avvia l'applicazione Flet e mostra l'interfaccia
ft.app(target=main)
