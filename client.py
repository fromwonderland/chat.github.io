import socket
import threading
import tkinter as tk
import json
import os
from tkinter import messagebox, font, colorchooser, Menu, messagebox
from datetime import datetime
from tkinter import ttk

SERVER_HOST = '172.17.41.174'
SERVER_PORT = 12345

username = "Utilisateur"

def send_message(event=None):
    message = message_entry.get("1.0", tk.END)
    if message:
        timestamp = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
        message_with_timestamp = f"{username}: {message}"
        try:
            client_socket.send(message_with_timestamp.encode('utf-8'))
        except Exception as e:
            print(f"Erreur survenue lors de l'envoi du message : {e}")
        message_entry.delete("1.0", tk.END)  # Efface le contenu de l'entrée de message après l'envoi

def change_username():
    global username
    old_username = username
    new_username = username_entry.get()
    if new_username:
        username = new_username

def show_emoji_window():
    emoji_window = tk.Toplevel(root)
    emoji_window.title("Bibliothèque d'émojis")
    emoji_window.geometry("610x380")

    # Désactiver le redimensionnement de la fenêtre
    emoji_window.resizable(width=False, height=False)  

    # Obtenir les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculer les coordonnées pour centrer la fenêtre d'emojis en bas de l'écran
    emoji_window_width = 610
    emoji_window_height = 380
    x = (screen_width - emoji_window_width) // 2  # Centrer horizontalement
    y = screen_height - emoji_window_height      # Placer en bas de l'écran
    
    # Définir la géométrie de la fenêtre d'emojis
    emoji_window.geometry(f"{emoji_window_width}x{emoji_window_height}+{x}+{y}")
    
    # Créer un widget Notebook pour les onglets
    notebook = ttk.Notebook(emoji_window)
    notebook.pack(fill="both", expand=True)

    emoji_categories = {
        "😀": ["😀","😃","😄","😁","😆","🥹","😅","😂","🤣","🥲","😊","😇",
                    "🙂","🙃","😉","😌"]
    }
    
    # Pour chaque catégorie, créer un cadre pour les emojis et les ajouter à un onglet
    for category, emojis in emoji_categories.items():
        frame = tk.Frame(notebook)
        notebook.add(frame, text=category.capitalize())

        row, col = 0, 0
        for emoji in emojis:
            emoji_button = tk.Label(frame, text=emoji, font=("Helvetica", 24), relief="flat", bd=0)
            emoji_button.grid(row=row, column=col, padx=5, pady=5)
            emoji_button.bind("<Button-1>", lambda event, emoji=emoji: insert_emoji(emoji))

            col += 1
            if col > 14:
                col = 0
                row += 1
        
def insert_emoji(emoji):
    global message_entry
    message_entry.insert(tk.END, emoji)

def open_color_settings():
    color_window = tk.Toplevel(root)
    color_window.title("Paramètres de couleur, police et taille de la fenêtre")
    color_window.geometry("550x350")

    # Labels et champs d'entrée pour les paramètres de couleur
    background_label = tk.Label(color_window, text="Couleur de la fenêtre d'affichage:")
    background_label.grid(row=0, column=0, padx=10, pady=10)

    background_color_button = tk.Button(color_window, text="Choisir", command=set_background_color)
    background_color_button.grid(row=0, column=1, padx=10, pady=10)

    message_label = tk.Label(color_window, text="Couleur des messages:")
    message_label.grid(row=1, column=0, padx=10, pady=10)

    message_color_button = tk.Button(color_window, text="Choisir", command=set_message_color)
    message_color_button.grid(row=1, column=1, padx=10, pady=10)

    #Couleur du background des fenêtres
    chat_bg_label = tk.Label(color_window, text="Couleur du chat:")
    chat_bg_label.grid(row=2, column=0, padx=10, pady=10)

    chat_bg_color_button = tk.Button(color_window, text="Choisir", command=set_chat_background_color)
    chat_bg_color_button.grid(row=2, column=1, padx=10, pady=10)

    # Label et roulette pour la taille de la police
    font_size_label = tk.Label(color_window, text="Taille de la police:")
    font_size_label.grid(row=3, column=0, padx=10, pady=10)

    font_size_var = tk.IntVar(color_window)
    font_size_var.set(30)  # Taille de police par défaut
    font_size_scale = tk.Scale(color_window, from_=10, to=80, orient=tk.HORIZONTAL, variable=font_size_var, length=200)
    font_size_scale.grid(row=3, column=1, padx=10, pady=10)

    # Labels et champs d'entrée pour le style de police
    font_family_label = tk.Label(color_window, text="Police d'écriture:")
    font_family_label.grid(row=4, column=0, padx=10, pady=10)

    font_family_variable = tk.StringVar(color_window)
    font_family_variable.set("Arial")  # Police par défaut
    font_family_option = tk.OptionMenu(color_window, font_family_variable, *font.families())
    font_family_option.grid(row=4, column=1, padx=10, pady=10)

    # Label et menu déroulant pour la taille de la fenêtre
    window_size_label = tk.Label(color_window, text="Taille de la fenêtre (prédéfinie):")
    window_size_label.grid(row=5, column=0, padx=10, pady=10)

    window_size_var = tk.StringVar(color_window)
    window_size_var.set("500x400")  # Taille de fenêtre prédéfinie
    window_size_options = ["600x400","700x500","800x600","900x700","1000x800"]  # Valeurs suggérées
    window_size_option_menu = tk.OptionMenu(color_window, window_size_var, *window_size_options)
    window_size_option_menu.grid(row=5, column=1, padx=10, pady=10)

    # Bouton pour appliquer les modifications
    apply_button = tk.Button(color_window, text="Appliquer les modifications", command=lambda: apply_settings(font_size_var.get(), font_family_variable.get(), window_size_var.get()))
    apply_button.grid(row=6, columnspan=2, padx=10, pady=10)

def set_background_color():
    color = colorchooser.askcolor()[1]
    if color:
        chat_text.config(bg=color)

def set_message_color():
    color = colorchooser.askcolor()[1]
    if color:
        chat_text.tag_configure("message", foreground=color)

def set_chat_background_color():
    color = colorchooser.askcolor()[1]
    if color:
        root.config(bg=color)
        username_frame.config(bg=color)
        chat_frame.config(bg=color)
        bottom_frame.config(bg=color)

def apply_settings(font_size, font_family, window_size):
    try:
        font_size = int(font_size)
        if font_size <= 0:
            raise ValueError("La taille de la police doit être un nombre entier positif.")

        # Mettre à jour la taille de la fenêtre principale
        width, height = map(int, window_size.split('x'))
        root.geometry(f"{width}x{height}")

        # Créer une police spéciale pour le nom d'utilisateur qui est toujours en gras et en noir
        username_font = font.Font(family=font_family, size=font_size, weight="bold")
        chat_text.tag_configure("username", font=username_font, foreground="black")

        # Configurer la police des messages
        message_font = font.Font(family=font_family, size=font_size)
        chat_text.tag_configure("message", font=message_font)

        # Configurer la police des métadonnées de manière proportionnelle à la police des messages
        metadata_font_size = int(font_size / 2)
        metadata_font = font.Font(family=font_family, size=metadata_font_size)
        chat_text.tag_configure("metadata", font=metadata_font, foreground="grey")
    except Exception as e:
        messagebox.showwarning("Erreur", f"Une erreur est survenue lors de la modification de la police ou de la taille de la fenêtre : {e}")

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_text.config(state=tk.NORMAL)
                username_length = len(username) + 1
                chat_text.insert(tk.END, message[:username_length], "username")
                chat_text.insert(tk.END, message[username_length:], "message")
                chat_text.insert(tk.END, f"\nEnvoyé le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n",'metadata')
                chat_text.see(tk.END)
                chat_text.config(state=tk.DISABLED)
                print(message)
        except ConnectionResetError:
            print("Le serveur a fermé la connexion.")
            return
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            client_socket.close()
            return

def on_resize(event):
    # Récupérer la nouvelle largeur et hauteur à partir des coordonnées du curseur
    new_width = event.x - chat_frame.winfo_x()
    new_height = event.y - chat_frame.winfo_y()

    # Mettre à jour la géométrie du widget Text
    chat_text.config(width=int(new_width / chat_text.cget("font").measure("0")), height=int(new_height / chat_text.cget("font").measure("0")))

    canvas = tk.Canvas(root, width=500, height=300)
    canvas.pack()
    # Mettre à jour la taille du Canvas
    canvas.config(width=new_width, height=new_height)

def on_right_click(event):
    menu.post(event.x_root, event.y_root)

    index = chat_text.index(tk.CURRENT)
    message_tag = chat_text.tag_names(index)[0]

    if message_tag == 'user_message':
        menu.tk_popup(event.x_root, event.y_root)

def edit_message():
    index = chat_text.index(tk.CURRENT)
    message_tag = chat_text.tag_names(index)[0]

    if message_tag == 'user_message':
        message = chat_text.get(index + " linestart", index + " lineend")
        message_entry.delete(0, tk.END)
        message_entry.insert(tk.END, message)

def delete_message():
    index = chat_text.index(tk.CURRENT)
    message_tag = chat_text.tag_names(index)[0]

    if message_tag == 'user_message':
        confirmation = messagebox.askyesno("Confirmation de la suppression du message", "Confirmer la suppression du message ?")
        if confirmation:
            chat_text.delete(index + " linestart", index + " lineend")

def configure_message_frame(event):
    # Configure la taille de la colonne 0 et de la ligne 0 du message_frame pour qu'ils s'étendent lors de la redimension de la fenêtre
    message_frame.grid_rowconfigure(0, weight=1)
    message_frame.grid_columnconfigure(0, weight=1)

    # Ajuster la visibilité de la barre de défilement verticale
    chat_text.yview_moveto(1.0)

root = tk.Tk()
root.title("Chat Client")
# Zone de saisie et de modification du nom d'utilisateur
username_frame = tk.Frame(root)
username_frame.pack(fill=tk.X)

username_label = tk.Label(username_frame, text="Nom d'utilisateur:")
username_label.pack(side=tk.LEFT, padx=5, pady=5)

username_entry = tk.Entry(username_frame, width=30)
username_entry.pack(side=tk.LEFT, padx=5, pady=5)
username_entry.focus()

username_button = tk.Button(username_frame, text="Changer", command=change_username)
username_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton Aide
def open_help_window():
    help_text = """    Bienvenue dans notre app de chat cryptée!
    Voici à quoi renvoient les fonctionnalités de l'app:
    
    - "@IA": à utiliser dans vos messages pour faire instantanément appel à l'IA de l'app de chat. Elle peut vous renseigner
    sur la plateforme, n'hésitez pas à lui poser vos questions.

    - "Connexion": Première connexion? Entrez le mot "COMPTE" dans la case "Nom d'utilisateur" et rien dans la case Mot de passe,
    puis cliquez sur "Valider la création de mon compte chat" pour créer vos identifiants. Connexion à votre compte? Entrez vos
    identifiants et cliquez sur "Me connecter".

    - "Entrez votre nom d'utilisateur" et 'Changer': pour modifier votre nom dans les futurs messages.
    
    - 'Utilisateurs': permet de suivre les connexions à l'app et les changements de noms d'utilisateurs.

    -'Personnaliser": grâce à cette fonctionnalité, vous pouvez personnaliser la couleur et la police de vos messages ainsi que
    la couleur de la fenêtre de chat et du background de chat afin de créer le l'environnement de chat qui vous convient.

    - '😊' : permet d'accéder à la bibliothèque d'émojis pour personnaliser et animer vos messages. Vous pouvez accéder à tous
    les emojis grâce aux barres de défilement.

    - 'Conversations' : vous permet de naviguer d'une conversation à une autre ainsi que d'en créer de nouvelles, en incluant
    un ou plusieurs autres utilisateurs.

    -Modifier/Supprimer les messages : pour modifier un de vos messages, faites un simple *clic droit* sur le message puis
    cliquez sur 'Modifier le message' ou 'Supprimer le message'.

    Sauvegarde des modifications effectuées sur l'app : vos identifiants sont automatiquement enregistrés sur notre server
    lors de la création de votre compte, de même que la dernière personnalisation de vôtre fenêtre de chat et vos
    conversations, au moment de votre déconnexion. Veillez ainsi à cliquer sur le bouton "Déconnexion" pour vous connecter et
    valider les sauvegardes ✅.

    Amusez-vous bien! 🙂
    -Sarah, Lara, Camilia
    """
    help_window = tk.Toplevel(root)
    help_window.title("Aide: naviguer à travers le chat")
    help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT)
    help_label.pack(padx=10, pady=10)

help_button = tk.Button(username_frame, text="Aide", command=open_help_window)
help_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton Connexion
connected = False  # Ajoutez cette ligne en dehors des fonctions

#Bouton Déconnexion
# Charger la liste des utilisateurs connectés à partir du fichier JSON
with open("utilisateurs_connectes.json", "r") as f:
    connected_users = json.load(f)

def confirm_disconnect():
    confirmation = messagebox.askyesno("Déconnexion", "Êtes-vous sûr de vouloir vous déconnecter?")
    if confirmation:
        # Supprimer le nom d'utilisateur actuel de la liste
        connected_users.remove(username_entry.get())

        # Enregistrer la liste mise à jour dans le fichier JSON
        with open("utilisateurs_connectes.json", "w") as f:
            json.dump(connected_users, f)

        # Fermer la fenêtre principale
        root.destroy()

# Fonction pour ouvrir la fenêtre de connexion
def open_login_window(root):
    global disconnect_button
    login_window = tk.Toplevel(root)
    login_window.title("Connexion")
    login_window.geometry("420x255")

    # Phrase d'introduction
    intro_label = tk.Label(login_window, text="Entrez vos identifiants pour vous connecter:")
    intro_label.pack(pady=(30, 10))  # Ajoute un espace de 30 pixels en haut

    # Label et entrée pour le nom d'utilisateur
    username_label = tk.Label(login_window, text="Nom d'utilisateur:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    # Label et entrée pour le mot de passe
    password_label = tk.Label(login_window, text="Mot de passe:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")  # Le mot de passe est masqué pendant la connexion
    password_entry.pack(pady=5)

    # Étiquette pour afficher les erreurs
    error_label = tk.Label(login_window, text="", fg="red")
    error_label.pack(pady=5)

    # Bouton Valider
    validate_button = tk.Button(login_window, text="Valider", command=lambda: check_credentials(username_entry.get(), password_entry.get(), login_window, error_label))
    validate_button.pack(pady=10)  # Ajoute un espace après l'entrée du mot de passe

    # Bouton Déconnexion
    disconnect_button = tk.Button(username_frame, text="Déconnexion", command=lambda: confirm_disconnect())
    disconnect_button.pack(side=tk.LEFT, padx=5, pady=5)
    disconnect_button.pack_forget()

# Fonction pour ouvrir la fenêtre de création de compte
def open_create_account_window():
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Création du compte")
    create_account_window.geometry("420x240")

    intro_label = tk.Label(create_account_window, text="Créer de nouveaux identifiants:\nEntrez un Nom d'utilisateur et un Mot de passe et cliquez sur valider")
    intro_label.pack(pady=(30, 10))

    username_label = tk.Label(create_account_window, text="Nom d'utilisateur:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(create_account_window, width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(create_account_window, text="Mot de passe:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(create_account_window, width=30)#Le mot de passe est visible pendant sa création
    password_entry.pack(pady=5)

    validate_button = tk.Button(create_account_window, text="Valider", command=lambda: add_account(username_entry.get(), password_entry.get(), create_account_window))
    validate_button.pack(pady=10)

# Chemin relatif vers le fichier identifiants.json
identifiants_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive", "Bureau", "INFORMATIQUE", "PROJET INFO", "identifiants.json")

# Fonction pour ajouter un compte dans le fichier identifiants.json
def add_account(username, password, window):
    # Ouvrir le fichier JSON
    with open(identifiants_path, "r") as file:
        identifiants = json.load(file)

    # Ajouter le nouveau compte
    identifiants["utilisateurs"].append({"nom_utilisateur": username, "mot_de_passe": password})

    # Enregistrer les modifications dans le fichier JSON
    with open(identifiants_path, "w") as file:
        json.dump(identifiants, file)

    # Afficher une notification pour informer l'utilisateur
    messagebox.showinfo("Création de compte réussie", "Le compte a été créé avec succès!")

    # Fermer la fenêtre de création de compte
    window.destroy()

# Appeler la fonction pour ouvrir la fenêtre de connexion au démarrage de l'application
open_login_window(root)
# Fonction pour vérifier les identifiants de l'utilisateur
def check_credentials(username, password, login_window, error_label):
    try:
        with open("identifiants.json", "r") as file:
            identifiants = json.load(file)

        for user in identifiants["utilisateurs"]:
            if user["nom_utilisateur"] == username and user["mot_de_passe"] == password:
                messagebox.showinfo("Connexion réussie", "Connexion réussie! Amusez vous bien!!")
                login_window.destroy()  # Ferme la fenêtre de connexion

                # Ajouter le nom d'utilisateur à la liste des utilisateurs connectés
                with open("utilisateurs_connectes.json", "r") as f:
                    utilisateurs_connectes = json.load(f)
                utilisateurs_connectes.append(username)
                with open("utilisateurs_connectes.json", "w") as f:
                    json.dump(utilisateurs_connectes, f)

                # Afficher le bouton "Déconnexion" et masquer le bouton "Connexion"
                disconnect_button.pack(side=tk.LEFT, padx=5, pady=5)
                connect_button.pack_forget()
                return

        # Si les identifiants ne correspondent à aucun utilisateur
        error_label.config(text="Identifiants incorrects, réessayez", fg="red")
        error_label.pack(pady=5)

        # Vérifier si l'utilisateur est "COMPTE" et le mot de passe est vide
        if username == "COMPTE" and password == "":
            # Fermer la fenêtre de connexion
            login_window.destroy()
            # Ouvrir la fenêtre de création de compte
            open_create_account_window()

    except FileNotFoundError:
        error_label.config(text="Fichier identifiants.json introuvable", fg="red")
        error_label.pack(pady=5)

connect_button = tk.Button(username_frame, text="Connexion", command=lambda: open_login_window(root))
connect_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton Utilisateurs
# Chemin d'accès au fichier utilisateurs_connectes.json
users_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive", "Bureau", "INFORMATIQUE", "PROJET INFO", "utilisateurs_connectes.json")

def show_users():
    # Ouvrir le fichier JSON contenant la liste des utilisateurs connectés
    with open('utilisateurs_connectes.json', 'r') as f:
        connected_users = json.load(f)

    # Créer une fenêtre pour afficher la liste des utilisateurs connectés
    users_window = tk.Toplevel(root, width=400, height=400)
    users_window.geometry("400x400")
    users_window.title("Utilisateurs connectés")

    # Créer un LabelFrame pour contenir la liste des utilisateurs
    users_frame = tk.LabelFrame(users_window, text="Utilisateurs connectés")
    users_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Créer une Listbox pour afficher la liste des utilisateurs
    users_listbox = tk.Listbox(users_frame, height=12)
    users_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # Ajouter chaque utilisateur connecté à la Listbox
    for user in connected_users:
        users_listbox.insert(tk.END, user)

    # Ajouter un bouton pour fermer la fenêtre
    close_button = tk.Button(users_window, text="Fermer", command=users_window.destroy)
    close_button.pack(pady=10)

button = tk.Button(username_frame, text="Utilisateurs", command=show_users)
button.pack(side="left", padx=10, pady=10)

# Bouton Recherche de messages
# Déclaration de la variable search_entry en dehors de la fonction search_window()
search_entry = None
def search_window():
    global search_entry
    search_win = tk.Toplevel(root)
    search_win.title("Recherche")
    search_win.geometry("300x100")  # Définit la taille de la fenêtre
    search_label = tk.Label(search_win, text="Entrez le/les mots à rechercher dans le chat :")
    search_label.pack()
    search_entry = tk.Entry(search_win)
    search_entry.pack()
    search_entry.bind("<KeyRelease>", lambda event: search_messages(search_entry.get()))

    # Fonction pour fermer la fenêtre de recherche et supprimer les surlignages
    def close_search_window():
        search_win.destroy()
        chat_text.tag_delete("highlight")
    search_win.protocol("WM_DELETE_WINDOW", close_search_window)

def search_messages(search_text):
    # Supprimer tous les tags de surlignage précédents
    chat_text.tag_delete("highlight")

    # Vérifier si l'entrée est vide
    if not search_text:
        return

    # Rechercher le texte dans le chat
    start_index = "1.0"
    while True:
        # Trouver la prochaine occurrence du texte
        end_index = chat_text.search(search_text, start_index, stopindex="end", nocase=True)
        if not end_index:
            break

        # Ajouter un tag de surlignage à l'occurrence trouvée
        chat_text.tag_add("highlight", end_index, f"{end_index}+{len(search_text)}c")

        # Définir l'index de début pour la prochaine recherche
        start_index = f"{end_index}+{len(search_text)}c"

    # Configurer le tag de surlignage pour qu'il soit jaune
    chat_text.tag_config("highlight", background="grey")

search_button = tk.Button(username_frame, text="Recherche", command=search_window)
search_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton Conversations
conversations_button = tk.Button(username_frame, text="Conversations")
conversations_button.pack(side=tk.LEFT, padx=5, pady=5)

# Bouton Personnaliser
color_button = tk.Button(username_frame, text="Personnaliser", command=open_color_settings)
color_button.pack(side=tk.LEFT, padx=5, pady=5)

# Fenêtre de chat
chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_text = tk.Text(chat_frame, height=20, width=50, bd=2, relief="solid")
chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Limiter la taille minimale de la fenêtre
root.update()
root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())
root.minsize(width=960, height=400)

# Désactiver l'entrée de texte dans le widget Text
chat_text.config(state="disabled")

# Associer la fonction on_resize au widget chat_frame
chat_frame.bind("<B1-Motion>", on_resize)

# Configurer le tag "username" avec une police en gras et en noir
chat_text.tag_configure("username", font=("Arial", 12, "bold"), foreground="black")

# Configurer le tag "message" avec une police normale
chat_text.tag_configure("message", font=("Arial", 12, "normal"))

# Configurer le tag "metadata" avec une police plus petite et une couleur plus claire
chat_text.tag_configure("metadata", font=("Arial", 6), foreground="grey")

# Barre de défilement verticale
vscrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=chat_text.yview)
vscrollbar.pack(side="right", fill="y")
chat_text.config(yscrollcommand=vscrollbar.set)

menu = Menu(root, tearoff=0)
menu.add_command(label="Modifier", command=edit_message)
menu.add_command(label="Supprimer", command=delete_message)

message_frame = tk.Frame(root)
message_frame.pack(padx=10, pady=10)

chat_text.bind("<Button-3>", on_right_click)

# Créer un nouveau Frame pour contenir la zone de saisie, le bouton d'émoji et le bouton d'envoi
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Zone de saisie du message
message_entry = tk.Text(bottom_frame, height=5, width=50)
message_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# Barre de défilement verticale pour la zone de saisie
message_entry_scrollbar_message = tk.Scrollbar(bottom_frame, orient="vertical", command=message_entry.yview)
message_entry_scrollbar_message.pack(side="right", fill="y")
message_entry.config(yscrollcommand=message_entry_scrollbar_message.set)

# Bouton d'émoji
emoji_button = tk.Label(bottom_frame, text="😊", font=("Helvetica", 24), relief="flat", bd=0)
emoji_button.pack(side=tk.LEFT, padx=5, pady=5)
emoji_button.bind("<Button-1>", lambda event: show_emoji_window())

# Bouton d'envoi
send_button = tk.Button(bottom_frame, text="Envoyer", command=send_message, font=("Helvetica", 14, "bold"))
send_button.pack(side=tk.RIGHT, padx=10, pady=5)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Demander à l'utilisateur son nom
username = ""
username_entry.insert(0, "Entrez votre nom d'utilisateur")
username_label.config(text="")
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Configurer la fonction configure_message_frame pour être appelée lorsque la fenêtre est redimensionnée
root.bind("<Configure>", configure_message_frame)

#Fermeture du chat
def close_client():
    # Vérifier si l'utilisateur est connecté
    if username_entry.get() in connected_users:
        # Supprimer l'utilisateur de la liste des utilisateurs connectés
        connected_users.remove(username_entry.get())

        # Sauvegarder la liste mise à jour dans le fichier JSON
        with open('utilisateurs_connectes.json', 'w') as f:
            json.dump(connected_users, f)

    # Demander une confirmation avant de fermer le chat
    confirmation = messagebox.askyesno("Fermer le chat", "Êtes-vous sûr de vouloir fermer le chat ?")

    # Fermer la fenêtre du client
    if confirmation:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", close_client)
root.mainloop()