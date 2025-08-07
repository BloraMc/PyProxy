import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

SERVER_HOST = 'exemple.lystech.org' # Remplacez par l'IP de votre serveur # Trad
SERVER_PORT = 12345 # Remplacez par le port de votre serveur # Trad

class PyProxyClientApp:
    def __init__(self, master):
        self.master = master
        master.title('PyProxy Messenger')  # No translation, it's a name lah
        master.geometry('540x600')
        master.configure(bg='#232946')
        self.my_id = None
        self.sock = None
        self.connected = False
        self.message_history = []
        self.create_widgets()
        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def create_widgets(self):
        bg_color = "#000000"
        fg_color = "#ffffff"
        accent_color = "#00ffd0"
        secondary_accent = "#ff00a6"
        chat_bg = "#000000"
        chat_fg = "#00ffd0"
        entry_bg = "#111111"
        entry_fg = "#00ffd0"
        button_bg = "#00ffd0"
        button_fg = "#000000"
        status_bg = "#000000"
        status_fg = "#ff00a6"
        id_fg = "#00ffd0"
        font_family = "Consolas"
        self.master.configure(bg=bg_color)
        self.title_label = tk.Label(self.master, text='PyProxy Messenger', font=(font_family, 20, 'bold'), fg=accent_color, bg=bg_color)  # No translation lah
        self.title_label.pack(pady=(18, 2))
        self.info_label = tk.Label(self.master, text='Connexion au serveur...', fg=status_fg, bg=status_bg, font=(font_family, 12))  # Trad
        self.info_label.pack(pady=(0, 2))
        self.id_label = tk.Label(self.master, text='Votre ID : ...', fg=id_fg, bg=bg_color, font=(font_family, 12))  # Trad
        self.id_label.pack(pady=(0, 8))
        self.chat_area = scrolledtext.ScrolledText(self.master, state='disabled', wrap=tk.WORD, height=20, font=(font_family, 12), bg=chat_bg, fg=chat_fg, insertbackground=accent_color, bd=0, padx=10, pady=10, highlightthickness=0)
        self.chat_area.pack(padx=18, pady=(0, 10), fill=tk.BOTH, expand=True)
        self.input_frame = tk.Frame(self.master, bg=bg_color)
        self.input_frame.pack(pady=(0, 12))
        self.target_id_entry = tk.Entry(self.input_frame, width=16, font=(font_family, 12), bg=entry_bg, fg=entry_fg, insertbackground=accent_color, bd=1, relief=tk.FLAT, highlightthickness=1, highlightbackground=accent_color, highlightcolor=accent_color)
        self.target_id_entry.grid(row=0, column=0, padx=(0, 8), pady=2)
        self.target_id_entry.insert(0, 'Entrez l’ID cible')  # Trad
        self.message_entry = tk.Entry(self.input_frame, width=28, font=(font_family, 12), bg=entry_bg, fg=entry_fg, insertbackground=accent_color, bd=1, relief=tk.FLAT, highlightthickness=1, highlightbackground=accent_color, highlightcolor=accent_color)
        self.message_entry.grid(row=0, column=1, padx=(0, 8), pady=2)
        self.message_entry.insert(0, 'Tapez votre message')  # Trad
        self.send_button = tk.Button(self.input_frame, text='Envoyer', font=(font_family, 12), bg=button_bg, fg=button_fg, activebackground=accent_color, activeforeground=bg_color, bd=0, padx=16, pady=4, command=self.send_message, cursor='hand2', highlightthickness=0)  # Trad
        self.send_button.grid(row=0, column=2, padx=(0, 0), pady=2)
        self.master.bind('<Return>', lambda event: self.send_message())

    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            self.info_label.config(text='Connecté au serveur !', fg='#a3f7bf')  # Trad
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.info_label.config(text=f'Connexion impossible : {e}', fg='#ffadad')  # Trad
            self.connected = False

    def receive_messages(self):
        while self.connected:
            try:
                data = self.sock.recv(1024)
                if not data:
                    self.append_chat('Déconnecté du serveur.', '#ffadad')  # Trad
                    break
                msg = data.decode().strip()
                if msg.startswith('YOUR_ID:'):
                    self.my_id = msg.split(':', 1)[1]
                    self.id_label.config(text=f'Votre ID : {self.my_id}')  # Trad
                elif msg.startswith('FROM:'):
                    _, sender_id, message = msg.split(':', 2)
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    entry = f'[{timestamp}] De {sender_id} : {message}'  # Trad
                    self.append_chat(entry, '#a3f7bf')
                elif msg.startswith('ERROR:'):
                    self.append_chat(f'Erreur serveur : {msg}', '#ffadad')  # Trad
                else:
                    self.append_chat(f'Serveur : {msg}', '#eebbc3')  # Trad
            except Exception as e:
                self.append_chat(f'Erreur : {e}', '#ffadad')  # Trad
                break

    def append_chat(self, message, color='#eebbc3'):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n', color)
        self.chat_area.tag_config(color, foreground=color)
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        if not self.connected or self.my_id is None:
            messagebox.showwarning('Non connecté', 'Vous n\'êtes pas connecté au serveur.')  # Trad
            return
        target_id = self.target_id_entry.get().strip()
        message = self.message_entry.get().strip()
        if not target_id or not message or target_id == 'Entrez l’ID cible' or message == 'Tapez votre message':
            messagebox.showwarning('Erreur de saisie', 'Veuillez entrer un ID cible et un message.')  # Trad
            return
        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = f'[{timestamp}] À {target_id} : {message}'  # Trad
        self.append_chat(entry, '#fffffe')
        send_str = f'SENDTO:{target_id}:{message}\n'
        try:
            self.sock.sendall(send_str.encode())
        except Exception as e:
            self.append_chat(f'Échec de l\'envoi du message : {e}', '#ffadad')  # Trad

if __name__ == '__main__':
    root = tk.Tk()
    app = PyProxyClientApp(root)
    root.mainloop()
