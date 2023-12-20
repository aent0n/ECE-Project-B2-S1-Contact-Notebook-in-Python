import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import requests
from PIL import Image
from io import BytesIO
import csv
from tkinter import filedialog, messagebox



class CarnetAdressesGUI:

    url = "https://cdn.discordapp.com/attachments/788291502374780958/1186994876601090109/Group_119bgTK_2.png?ex=6595461f&is=6582d11f&hm=9403c5a147d94af7dd4364bfea3ada2898f3fdd90fbfd555fb320c7ef138cb3c&"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((650, 580))
    img.save("image.gif")

    def refresh_search(self):
        terme_recherche = self.entry_recherche.get()
        self.perform_actual_search(terme_recherche)

    def delete_contacts_table(self):
        self.cursor.execute('''
            DROP TABLE IF EXISTS contacts
        ''')
        self.conn.commit()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        credentials = {
            'user1': 'password1',
            'user2': 'password2',
        }

        if username in credentials and credentials[username] == password:
            self.login_page.destroy()
        else:
            tk.messagebox.showerror("Error", "Invalid credentials")

    def fermer_application(self):
        self.conn.close()
        self.master.destroy()

    def __init__(self, master, create_login_page=True):
        self.master = master
        self.master.title("Carnet d'Adresses")


        self.conn = sqlite3.connect('carnet_adresses.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT,
                email VARCHAR(50),
                telephone VARCHAR(10)
            )''')
        self.conn.commit()

        #self.supprimer_tous_les_contacts_START()

        self.nb = ttk.Notebook(master)
        self.page_ajout = ctk.CTkFrame(self.nb)
        self.page_recherche = ctk.CTkFrame(self.nb)

        self.nb.add(self.page_ajout, text='Ajouter Contact')
        self.nb.add(self.page_recherche, text='Rechercher Contact')

        self.nb.grid(row=0, column=0, padx=50, pady=50)

        if create_login_page:
            self.create_login_page()

        # Page Ajout
        ctk.CTkLabel(self.page_ajout, text="Nom : ", font=("Arial", 20)).grid(row=0, column=0, pady=5, sticky="w")
        self.entry_nom = ctk.CTkEntry(self.page_ajout)
        self.entry_nom.grid(row=0, column=1, pady=20, padx=10)

        ctk.CTkLabel(self.page_ajout, text="Prénom : ", font=("Arial", 20)).grid(row=0, column=2, pady=5, sticky="w")
        self.entry_prenom = ctk.CTkEntry(self.page_ajout)
        self.entry_prenom.grid(row=0, column=4, pady=20, padx=30)

        ctk.CTkLabel(self.page_ajout, text="E-mail : ", font=("Arial", 20)).grid(row=2, column=0, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.page_ajout)
        self.entry_email.grid(row=2, column=1, pady=20, padx=10)

        ctk.CTkLabel(self.page_ajout, text="Téléphone : ", font=("Arial", 20)).grid(row=2, column=2, pady=5, sticky="w")
        self.entry_telephone = ctk.CTkEntry(self.page_ajout)
        self.entry_telephone.grid(row=2, column=4, pady=20, padx=10)

        self.button_ajouter = ctk.CTkButton(self.page_ajout, text="Ajouter Contact", command=self.ajouter_contact)
        self.button_ajouter.grid(row=4, column=2, columnspan=2, pady=20)

        self.button_import = ctk.CTkButton(self.page_ajout, text="Importer CSV", command=self.importer_csv)
        self.button_import.grid(row=4, column=1, columnspan=1, pady=20)

        self.photo = tk.PhotoImage(file="image.gif")
        self.label = tk.Label(self.page_ajout, image=self.photo)
        self.label.grid(row=5, column=0, columnspan=5)

        # Page Recherche
        ctk.CTkLabel(self.page_recherche, text="Nom ou Email : ", font=("Arial", 20)).grid(row=0, column=0, pady=5, sticky="w")
        self.entry_recherche = ctk.CTkEntry(self.page_recherche)
        self.entry_recherche.grid(row=0, column=1, pady=5, padx=10)
        # Define the canvas and scrollbar
        self.canvas = tk.Canvas(self.page_recherche, width=600, height=400)
        self.scrollbar = tk.Scrollbar(self.page_recherche, orient="vertical", command=self.canvas.yview)
        # define the frame and add it to the canvas
        self.frame = tk.Frame(self.canvas)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        # Continue 
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.scrollbar.grid(row=3, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.button_rechercher = ctk.CTkButton(self.page_recherche, text="Rechercher Contact", command=self.rechercher_contact_with_progress, font=("Arial", 20))
        self.button_rechercher.grid(row=1, column=0, columnspan=2, pady=20)

        self.progressbar = ttk.Progressbar(self.page_recherche, orient="horizontal", length=200, mode="indeterminate")
        self.progressbar.grid(row=4, column=0, columnspan=2, pady=20)

        self.button_rechercher = ctk.CTkButton(self.page_recherche, text="Rechercher Contact", command=self.rechercher_contact_with_progress, font=("Arial", 20))
        self.button_rechercher.grid(row=1, column=0, columnspan=2, pady=20)

        self.button_afficher_all = ctk.CTkButton(self.page_recherche, text="Afficher tous les contacts", command=self.afficher_tous_les_contacts, font=("Arial", 20))
        self.button_afficher_all.grid(row=2, column=0, columnspan=1, pady=20)

        self.button_supprimer_tous_les_contacts = ctk.CTkButton(self.page_recherche, text="Supprimer tous les contacts", command=self.supprimer_tous_les_contacts, font=("Arial", 20))
        self.button_supprimer_tous_les_contacts.grid(row=2, column=1, columnspan=1, pady=20)

        self.progressbar = ttk.Progressbar(self.page_recherche, orient="horizontal", length=200, mode="indeterminate")
        self.progressbar.grid(row=4, column=0, columnspan=2, pady=20)

        self.master.protocol("WM_DELETE_WINDOW", self.fermer_application)

    def create_login_page(self):
        self.login_page = ctk.CTkFrame(self.master, bg_color='lightblue')
        self.login_page.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.login_page, text="Username:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = ctk.CTkEntry(self.login_page, font=("Arial", 14))
        self.entry_username.insert(0, "user1")
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.login_page, text="Password:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = ctk.CTkEntry(self.login_page, show="*", font=("Arial", 14))
        self.entry_password.insert(0, "password1")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(self.login_page, text="Login", command=self.login, bg_color='lightgreen').grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def ajouter_contact(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        email = self.entry_email.get()
        telephone = self.entry_telephone.get()

        if nom:
            self.cursor.execute('''
                INSERT INTO contacts (nom, prenom, email, telephone)
                VALUES (?, ?, ?, ?)
            ''', (nom, prenom, email, telephone))
            self.conn.commit()
            messagebox.showinfo("Succès", "Contact ajouté avec succès.")
        else:
            messagebox.showwarning("Erreur", "Veuillez saisir le nom du contact.")

    def supprimer_tous_les_contacts(self):
        self.cursor.execute("DELETE FROM contacts")
        self.conn.commit()
        self.afficher_tous_les_contacts()

    def supprimer_tous_les_contacts_START(self):
        self.cursor.execute("DELETE FROM contacts")
        self.conn.commit()

    def importer_csv(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        if filename:
            try:
                with open(filename, 'r') as txtfile:
                    for line in txtfile:
                        nom, prenom, email, telephone = line.strip().split(',')
                        self.cursor.execute('''
                            INSERT INTO contacts (nom, prenom, email, telephone)
                            VALUES (?, ?, ?, ?)
                        ''', (nom.strip(), prenom.strip(), email.strip(), telephone.strip()))
                    self.conn.commit()
                messagebox.showinfo("Succès", "Contacts importés avec succès.")
            except Exception as e:
                print(f"An error occurred while importing the text file: {str(e)}")
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'importation du fichier texte : {str(e)}")
        else:
            messagebox.showwarning("Attention", "Aucun fichier texte sélectionné.")


    def rechercher_contact_with_progress(self):
        terme_recherche = self.entry_recherche.get()
        if terme_recherche:
            self.progressbar.start()
            # Clear the frame's contents here
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.after(1000, lambda: self.perform_actual_search(terme_recherche))
        else:
            messagebox.showwarning("Erreur", "Veuillez saisir un nom ou un email pour la recherche.")

    def no_user_plus_prefill(self, terme_recherche):
        self.nb.select(self.page_ajout)
        self.entry_nom.delete(0, tk.END)
        self.entry_prenom.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telephone.delete(0, tk.END)
        self.entry_nom.insert(0, terme_recherche)

    def afficher_tous_les_contacts(self):
        self.cursor.execute('''
            SELECT * FROM contacts
        ''')
        contacts = self.cursor.fetchall()

        for widget in self.frame.winfo_children():
            widget.destroy()
        if not contacts:
            ctk.CTkLabel(self.frame, text="Aucun contact trouvé.").grid()
            return
        for i, contact in enumerate(contacts):
            tk.Label(self.frame, text=f"Nom: {contact[1]}", font=("Calibri", 20), anchor="w").grid(row=i*4, column=0, sticky="w")
            tk.Label(self.frame, text=f"Prénom: {contact[2]}",font=("Calibri", 20), anchor="w").grid(row=i*4+1, column=0, sticky="w")
            tk.Label(self.frame, text=f"Email: {contact[3]}", font=("Calibri", 20), anchor="w").grid(row=i*4+2, column=0, sticky="w")
            tk.Label(self.frame, text=f"Téléphone: {contact[4]}", font=("Calibri", 20), anchor="w").grid(row=i*4+3, column=0, sticky="w")
            ctk.CTkButton(self.frame, text="Supprimer Contact", bg_color="red", fg_color="red", command=lambda contact_id=contact[0]: self.delete_contact(contact_id)).grid(row=i*4, column=1)
            ctk.CTkButton(self.frame, text="Modifier Contact", bg_color="orange", fg_color="orange", command=lambda contact_id=contact[0]: self.edit_contact(contact_id)).grid(row=i*4+1, column=1)

    def perform_actual_search(self, terme_recherche):
        self.cursor.execute('''
            SELECT * FROM contacts
            WHERE nom LIKE ? OR email LIKE ?
        ''', ('%' + terme_recherche + '%', '%' + terme_recherche + '%'))
        resultats = self.cursor.fetchall()
        self.progressbar.stop()
        for widget in self.frame.winfo_children():
            widget.destroy()
        if not resultats:
            ctk.CTkLabel(self.frame, text="Aucun contact trouvé. Redirection vers la page d'ajout.").grid()
            self.frame.after(3000, self.no_user_plus_prefill, terme_recherche)
        else:
            for i, contact in enumerate(resultats):
                ctk.CTkLabel(self.frame, text=f"Nom: {contact[1]}", font=("Calibri", 20), anchor="w").grid(row=i*4, column=0, sticky="w")
                ctk.CTkLabel(self.frame, text=f"Prénom: {contact[2]}",font=("Calibri", 20), anchor="w").grid(row=i*4+1, column=0, sticky="w")
                ctk.CTkLabel(self.frame, text=f"Email: {contact[3]}", font=("Calibri", 20), anchor="w").grid(row=i*4+2, column=0, sticky="w")
                ctk.CTkLabel(self.frame, text=f"Téléphone: {contact[4]}", font=("Calibri", 20), anchor="w").grid(row=i*4+3, column=0, sticky="w")
                ctk.CTkButton(self.frame, text="Supprimer Contact", bg_color="red", fg_color="red", command=lambda contact_id=contact[0]: self.delete_contact(contact_id)).grid(row=i*4, padx=10, pady=10, column=2)
                ctk.CTkButton(self.frame, text="Modifier Contact", bg_color="orange", fg_color="orange", command=lambda contact_id=contact[0]: self.edit_contact(contact_id)).grid(row=i*4+1, padx=10, pady=5, column=2)

    def edit_contact(self, contact_id):
        self.cursor.execute(f'''
            SELECT * FROM contacts WHERE id = {contact_id}
        ''')
        contact = self.cursor.fetchone()
        edit_frame = tk.Frame(self.page_recherche)
        edit_frame.grid(row=3, column=4, ipadx=50, ipady=50, sticky='nsew')

        entry_nom = ctk.CTkEntry(edit_frame)
        entry_nom.insert(0, contact[1])
        entry_nom.grid(row=0, column=1)
        tk.Label(edit_frame, text="Nom:", font=("Calibri", 20)).grid(row=0, column=0)

        entry_prenom = ctk.CTkEntry(edit_frame)
        entry_prenom.insert(0, contact[2])
        entry_prenom.grid(row=1, column=1)
        tk.Label(edit_frame, text="Prénom:", font=("Calibri", 20)).grid(row=1, column=0)

        entry_email = ctk.CTkEntry(edit_frame)
        entry_email.insert(0, contact[3])
        entry_email.grid(row=2, column=1)
        tk.Label(edit_frame, text="Email:", font=("Calibri", 20)).grid(row=2, column=0)

        entry_telephone = ctk.CTkEntry(edit_frame)
        entry_telephone.insert(0, contact[4])
        entry_telephone.grid(row=3, column=1)
        tk.Label(edit_frame, text="Téléphone:", font=("Calibri", 20)).grid(row=3, column=0)

        def save_contact():
            self.cursor.execute('''
                UPDATE contacts
                SET nom = ?, prenom = ?, email = ?, telephone = ?
                WHERE id = ?
            ''', (entry_nom.get(), entry_prenom.get(), entry_email.get(), entry_telephone.get(), contact_id))
            self.conn.commit()
            edit_frame.destroy()
            self.refresh_search()

        self.button = ctk.CTkButton(edit_frame, text="Sauvegarder", font=("Calibri", 20), command=save_contact)
        self.button.grid(row=5, column=1, pady=20, sticky='nsew')
        

    def delete_contact(self, contact_id):
        self.cursor.execute(f'''
            DELETE FROM contacts
            WHERE id = ?
        ''', (contact_id,))
        self.conn.commit()
        self.refresh_search()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1920x1080")
    app = CarnetAdressesGUI(root)
    root.mainloop()