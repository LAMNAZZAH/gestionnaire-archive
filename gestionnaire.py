from calendar import TextCalendar
from tkcalendar import *
from enum import Flag
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox, StringVar, simpledialog
import tkinter
from typing import Sized, TextIO
from datetime import date
import datetime
import time
import random
import sqlite3

# Create needed tables if they don't exist
def initDb (sqlConnection):
    cursor = sqlConnection.cursor()
    
    # Create dossier database if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS dossier (
        reference varchar(40) PRIMARY KEY,
        annee varchar(45) DEFAULT NULL,
        nature varchar(45) DEFAULT NULL,
        archive_le varchar(45) DEFAULT NULL,
        numero varchar(45) DEFAULT NULL,
        status varchar(45) DEFAULT NULL,
        local varchar(45) DEFAULT NULL,
        boitier varchar(45) DEFAULT NULL,
        travee varchar(45) DEFAULT NULL,
        tablette varchar(45) DEFAULT NULL,
        valable varchar(45) DEFAULT NULL,
        informations_additionnelles varchar(45) DEFAULT NULL
    );''')
    
    # Create movement database if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS mouvement (
        idmouvement int NOT NULL,
        parqui varchar(45) DEFAULT NULL,
        le varchar(45) DEFAULT NULL,
        action varchar(45) DEFAULT NULL,
        dossier_reference varchar(40) NOT NULL REFERENCES dossier (reference)
    );''')
    
    # Create dossier_reference index
    cursor.execute('CREATE INDEX IF NOT EXISTS fk_mouvement_dossier_idx ON mouvement (dossier_reference);')
    sqlConnection.commit()

class management_sys:
    def __init__(self, root):
        self.sqlCon = sqlite3.connect('gestionnaire.db')
        initDb(self.sqlCon) # Initialize database tables
        self.root = root
        self.root.title("gestionnaire de marchés")
        self.root.geometry('1000x650')
        #self.root.resizable(width=False, height=False)
        tabcontrol = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(tabcontrol)
        self.tab2 = ttk.Frame(tabcontrol)
        tabcontrol.add(self.tab1, text='Saisie')
        tabcontrol.add(self.tab2, text='Tableau')
        tabcontrol.pack(expand=1, fill=BOTH)

# ? new window ##########################?  ##########################?
        new_window = ''

        def openwidow():
            global new_window
            new_window = Toplevel(root)
            new_window.geometry("350x230")
            new_window.title("New Window")
            new_window.resizable(False, False)

            top_window_frame = Frame(
                new_window, height=20, width=250, bg='', relief=RIDGE)
            top_window_frame.pack(side=TOP)

            content_window_frame = Frame(
                new_window, height=170, width=250,  bg='', relief=RIDGE)
            content_window_frame.pack()

            bottom_window_frame = Frame(
                new_window, height=170, width=250,  bg='', relief=RIDGE)
            bottom_window_frame.pack(side=BOTTOM)

            lbl = Label(top_window_frame, text="Informations de Mouvement:", font=(
                "arial", 13, "bold"), fg="grey")
            lbl.grid(row=0, column=0, sticky=W)

            self.actionlbl = Label(content_window_frame, text="action", font=(
                "arial", 12, "italic"), fg="grey")
            self.actionlbl.grid(row=0, column=0, sticky=W)

            self.action = ttk.Combobox(
                content_window_frame, values=('', 'pris', 'déposé'))
            self.action.grid(row=0, column=1, sticky=EW)

            self.parquilbl = Label(content_window_frame, text="par qui", font=(
                "arial", 12, "italic"), fg="grey")
            self.parquilbl.grid(row=1, column=0, sticky=W)

            self.parquientry = Entry(content_window_frame, textvariable=self.parqui, font=(
                "arial", 12, "italic"), fg="black")
            self.parquientry.grid(row=1, column=1, sticky=W)

            self.lelbl = Label(content_window_frame, text="Le",
                               font=("arial", 12, "italic"), fg="grey")
            self.lelbl.grid(row=2, column=0, sticky=W)

            self.leentry = Entry(content_window_frame, textvariable=self.le, font=(
                "arial", 12, "italic"), fg="black")
            self.leentry.grid(row=2, column=1, sticky=W)

            new_window_cal = DateEntry(content_window_frame, width=2, date_pattern='dd/mm/y',
                                       locale='fr', background='darkblue', foreground='white')
            new_window_cal.grid(row=3, column=1, sticky=W)

            def gettakendate(event):
                takendate = new_window_cal.get_date()
                self.le.set(takendate)

            new_window_cal.bind("<<DateEntrySelected>>", gettakendate)

            '''''
            def addaline():
                
                    theline = 'par: ' + self.taken_by.get() + ' Le: ' + self.taken_le.get()
                    self.mouvementtxt.configure(state='normal')
                    self.mouvementtxt.insert(END, theline + '\n')
                    self.mouvementtxt.configure(state='disabled')
            '''''

            btn2 = Button(bottom_window_frame, text="fermer",
                          command=lambda: new_window.destroy())
            btn2.grid(row=0, column=0, padx=6, pady=4)

            btn3 = Button(bottom_window_frame, text="sauvgarder",
                          command=add_mouvement)
            btn3.grid(row=0, column=1, padx=6, pady=4)

        def add_mouvement():
            # self.valable.set("valable")
            # selectededit()
            # self.informations_additionnelles.set(self.note.get("1.0",END))

            if len(self.reference.get()) == 0:
                messagebox.showerror(
                    "", "veuillez entrer les informations requises!!")
            else:
                try:
                    rd = random.randint(0, 1000)
                    id = self.reference.get() + "-" + rd
                    cur = self.sqlCon.cursor()
                    cur.execute("INSERT INTO mouvement (idmouvement, parqui, le, action, dossier_reference) SELECT ?, reference FROM dossier WHERE reference=?", (
                        id.get(),
                        self.parqui.get(),
                        self.le.get(),
                        self.action.get(),
                        self.reference.get(),
                        self.reference.get(),
                        self.reference.get()
                    ))
                    self.sqlCon.commit()
                    messagebox.showinfo(
                        "", "un marché a été ajouté avec succès")
                    #sqlCon = pymysql.connect(host="localhost", user="root", password="1234", database="thenew")
                    #cur = sqlCon.cursor()
                    # cur.execute("UPDATE thenew.dossier SET valable=? WHERE reference=?", (
                    # self.valable.get(),
                    # self.reference.get()
                    # ))
                    Display()
                except:
                    messagebox.showerror(
                        "", "attention: le numéro de référence est dupliqué, essayez de le corriger")
                pass
# ? ##########################?  ##########################?


########################################### !  Variables  ##########################################################
        # ?data entry
        self.reference = tk.StringVar()
        self.annee = tk.StringVar()
        self.nature = tk.StringVar()
        self.archive_le = tk.StringVar()
        self.numero = tk.StringVar()
        self.status = tk.StringVar()
        self.local = tk.StringVar()
        self.boitier = tk.StringVar()
        self.travee = tk.StringVar()
        self.tablette = tk.StringVar()
        self.valable = tk.StringVar()
        #self.mouvement = tk.StringVar()
        self.informations_additionnelles = tk.StringVar()

        self.parqui = tk.StringVar()
        self.le = tk.StringVar()
        self.action = tk.StringVar()

        self.login = tk.StringVar()
        self.passw = tk.StringVar()
        self.byyear = tk.StringVar()


########################################### !  Methodes ##########################################################
        # ?numero maker


        def selected(event):
            # .grid(row=3, column=0)
            label = Label(dataframe, text=clicked.get())
            self.nature.set(clicked.get())
            numero = self.reference.get() + '-' + self.annee.get() + '-' + self.nature.get()
            self.numero.set(numero)

        def selectededit():
            numero = self.reference.get() + '-' + self.annee.get() + '-' + self.nature.get()
            self.numero.set(numero)
            return True
        # ?

        def archive_le():
            today = datetime.datetime.now()
            self.archive_le.set('')
            self.archive_le.set(today.strftime("%d/%m/%Y"))

        def getSelectedDate(event):
            selectededit()
            theDate = cal.get_date()
            self.archive_le.set('')
            self.archive_le.set(theDate.strftime("%d/%m/%Y"))

        # ? taken or not btn color

        def tekenornotbtn(event):
            selectededit()
            if self.valable.get() == "valable":
                self.valablegreen.grid(row=4, column=1, sticky=W)
            else:
                self.valablegreen.grid_forget()
                self.valablered.grid(row=4, column=1, sticky=W)

        # ?
        self.text = tk.StringVar()

        def getNoteText():
            self.text = self.note.get("1.0", END)
            return self.text

        def add_data():
            self.valable.set("valable")
            selectededit()
            self.informations_additionnelles.set(self.note.get("1.0", END))

            if len(self.reference.get()) == 0:
                messagebox.showerror(
                    "", "veuillez entrer les informations requises!!")
            else:
                try:
                    cur = self.sqlCon.cursor()
                    cur.execute("INSERT INTO dossier VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (

                        self.reference.get(),
                        self.annee.get(),
                        self.nature.get(),
                        self.archive_le.get(),
                        self.numero.get(),
                        self.status.get(),
                        self.local.get(),
                        self.boitier.get(),
                        self.travee.get(),
                        self.tablette.get(),
                        self.valable.get(),
                        #self.mouvement = tk.StringVar()
                        self.informations_additionnelles.get()
                    ))

                    self.sqlCon.commit()
                    messagebox.showinfo(
                        "", "un marché a été ajouté avec succès")
                    Display()
                except:
                    messagebox.showerror(
                        "", "attention: le numéro de référence est dupliqué, essayez de le corriger")
                pass

        def Update():
            selectededit()
            self.informations_additionnelles.set(self.note.get("1.0", END))
            cur = self.sqlCon.cursor()
            cur.execute("UPDATE dossier SET annee=?, nature=?, archive_le=?, numero=?, status=?, local=?, boitier=?, travee=?, tablette=?, valable=?, informations_additionnelles=? WHERE  reference=?", (
                self.annee.get(),
                self.nature.get(),
                self.archive_le.get(),
                self.numero.get(),
                self.status.get(),
                self.local.get(),
                self.boitier.get(),
                self.travee.get(),
                self.tablette.get(),
                self.valable.get(),
                #self.mouvement = tk.StringVar()
                self.informations_additionnelles.get(),
                self.reference.get()
            ),)
            answer = messagebox.askyesno(
                "confirmer", "est-ce-que vous voulez vraiment mis a jour")
            if answer:
                self.sqlCon.commit()
                messagebox.showinfo(
                    "", "un marché a été mise à jour avec succèss")
                Display()

        def Display():
            cur = self.sqlCon.cursor()
            cur.execute("SELECT * FROM dossier")
            result = cur.fetchall()
            if len(result) != 0:
                self.info_de_marche.delete(*self.info_de_marche.get_children())
                for row in result:
                    self.info_de_marche.insert('', END, values=row)
            self.sqlCon.commit()

        def Exit():
            iExit = messagebox.askyesno("quitter", "voulez vous quitter?")
            if iExit > 0:
                root.destroy()
                return

        def Reset():
            self.reference.set('')
            self.annee.set('')
            self.nature.set('')
            self.archive_le.set('')
            self.numero.set('')
            self.status.set('')
            self.local.set('')
            self.boitier.set('')
            self.travee.set('')
            self.tablette.set('')
            self.valable.set('')
            self.numero.set('')
            self.informations_additionnelles.set('')
            self.note.delete('1.0', END)

        def Delete():
            cur = self.sqlCon.cursor()
            cur.execute(
                "DELETE FROM dossier WHERE reference=?", self.reference.get())

            if self.info_de_marche.focus() == "":
                messagebox.showinfo(
                    "", "Veuillez d'abord selectionner un marché")
            else:
                answer = messagebox.askyesno(
                    "confirmation", "est-ce-que vous voulez vraiment supprimer definitivement un marche")
                if answer:

                    self.sqlCon.commit()
                    messagebox.showinfo(
                        "", "un marché a été suprimer definitivement")
                    Display()

        def item_selected(event):
            for selected_item in self.info_de_marche.selection():
                item = self.info_de_marche.item(selected_item)
                record = item['values']
            self.reference.set(record[0])
            self.annee.set(record[1])
            self.nature.set(record[2])
            self.archive_le.set(record[3])
            self.numero.set(record[4])
            self.status.set(record[5])
            self.local.set(record[6])
            self.boitier.set(record[7])
            self.travee.set(record[8])
            self.tablette.set(record[9])
            self.valable.set(record[10])
            #self.mouvement = tk.StringVar()
            # self.informations_additionnelles.set(self.note.get("1.0",END))
            self.note.delete("1.0", END)
            self.note.insert(END, record[11])

        def Search():
            try:
                cur = self.sqlCon.cursor()
                cur.execute(
                    "SELECT* FROM dossier WHERE reference=?", self.reference.get())

                record = cur.fetchone()

                self.reference.set(record[0])
                self.annee.set(record[1])
                self.nature.set(record[2])
                self.archive_le.set(record[3])
                self.numero.set(record[4])
                self.status.set(record[5])
                self.local.set(record[6])
                self.boitier.set(record[7])
                self.travee.set(record[8])
                self.tablette.set(record[9])
                self.valable.set(record[10])
            #self.mouvement = tk.StringVar()
            # self.informations_additionnelles.set(self.note.get("1.0",END))
                self.note.delete("1.0", END)
                self.note.insert(END, record[11])

                self.sqlCon.commit()

            except:

                messagebox.showinfo(
                    "", "aucun résultat ne correspond à votre recherche")
                Reset()

        def byyear(event):
            cur = self.sqlCon.cursor()
            cur.execute(
                "SELECT * FROM dossier where annee=?", self.byyear.get())
            result = cur.fetchall()
            if len(result) != 0:
                self.info_de_marche.delete(*self.info_de_marche.get_children())
                for row in result:
                    self.info_de_marche.insert('', END, values=row)
            self.sqlCon.commit()


########################################### !  Frames  ##########################################################
        mainframe2 = Frame(self.tab2, height=200, width=970,
                           bg='#F0F0F0', relief=RIDGE)
        mainframe2.pack(expand=1, fill=BOTH)

        titleframe = Frame(mainframe2, height=200, width=970,
                           bg='#F4F6F6', relief=RIDGE)
        titleframe.pack(side=TOP, fill=X, pady=5, padx=5)

        contentframe = Frame(mainframe2, height=200,
                             width=970, bg='#F4F6F6', relief=RIDGE)
        contentframe.pack(fill=BOTH, expand=1, padx=5, pady=5)

        self.thetitle = Label(titleframe, text="authentification",
                              bg='#F4F6F6', fg='#273746', font=('arial', 15, 'bold'))
        self.thetitle.grid(row=0, column=1, sticky='nwe', padx=10)

        # login
        self.lbl_login = Label(contentframe, text="Login", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_login.grid(row=0, column=0, padx=5, sticky=W)

        self.Entry_login = Entry(contentframe, textvariable=self.login, font=(
            'arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_login.grid(row=0, column=1, padx=10, )
        ##

        # pass
        self.lbl_pass = Label(contentframe, text="mot de passe", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_pass.grid(row=1, column=0, padx=5, sticky=W)

        self.Entry_pass = Entry(contentframe, textvariable=self.passw, font=(
            'arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_pass.grid(row=1, column=1, padx=10, )
        ##

        self.addbtn = Button(contentframe, font=('arial', 9, 'bold'), text='Entrer', bd=4, relief=FLAT, bg='#ECF0F1',
                             height=1, width=8, command="search").grid(row=2, column=1, sticky='w', padx=10, pady=6)

###########################################

        mainframe = Frame(self.tab1, height=200, width=970,
                          bg='#F0F0F0', relief=RIDGE)
        mainframe.pack(expand=1, fill=BOTH)

        topframe = Frame(mainframe, height=200, width=970,
                         bg='#E1E8F3', relief=RIDGE)
        topframe.pack(side=TOP, fill=X)

        contentframe = Frame(mainframe, height=200,
                             width=970, bg='#DDF0F0', relief=RIDGE)
        contentframe.pack(fill=BOTH, expand=1)

        treeframe = Frame(contentframe, height=200,
                          width=970, bg='#DD0000', relief=RIDGE)
        treeframe.pack(fill=BOTH, expand=1)

        btnframe = Frame(topframe, height=30, width=970,
                         bg='#F0F0F0', relief=RIDGE)
        btnframe.pack(side=BOTTOM, fill=X, pady=3, padx=3)

        topnote = Frame(topframe, height=200, width=200,
                        bg='#F4F6F6', relief=RIDGE)
        topnote.pack(side=LEFT, fill=X, padx=3)

        topentry = Frame(topframe, height=200, width=770,
                         bg='#E1E8F3', relief=RIDGE)
        topentry.pack(fill=BOTH, expand=1)

        ordersframe = Frame(topentry, height=30, width=770,
                            bg='#F4F6F6', relief=RIDGE)
        ordersframe.pack(side=BOTTOM, fill=X, padx=4, pady=3)

        # calendarframe = Frame(topentry, height=170, width=100, bg='#FCFCFC', relief=RIDGE)
        #calendarframe.pack(side=TOP,padx=4, pady=4)

        dataframe = Frame(topentry, height=170, width=300,
                          bg='#F4F6F6', relief=RIDGE)
        dataframe.pack(side=LEFT, fill=Y, padx=4, pady=4)

        storageframe = Frame(topentry, height=170,
                             width=300, bg='#F4F6F6', relief=RIDGE)
        storageframe.pack(side=LEFT, padx=4, pady=4, fill=Y)

        takenframe = Frame(topentry, height=170, width=170,
                           bg='#F4F6F6', relief=RIDGE)
        takenframe.pack(side=LEFT, padx=4, pady=4, fill=BOTH, expand=1)

        # ? taken frame lablels
        # ?nom d'utili
        self.lbl_utilisateur = Label(takenframe, text="utilisateur : ", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_utilisateur .grid(row=0, column=0, padx=2, pady=3, sticky=W)
        # ?nom d'utili
        self.lbl_user = Label(takenframe, text="Mr.tahiri", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'bold'), bd=5, relief=FLAT)
        self.lbl_user .grid(row=0, column=1, padx=2, pady=3, sticky=W)

        # ?type
        self.lbl_administrateur = Label(takenframe, text="ADMIN", bg='#F4F6F6', fg='#FF0000', font=(
            'arial', 9, 'bold'), bd=5, relief=FLAT)
        self.lbl_administrateur .grid(
            row=1, column=1, padx=2, pady=3, sticky=W)


########################################### !  data entry  ##########################################################

        # ?reference
        self.lbl_reference = Label(dataframe, text="Reference", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_reference .grid(row=0, column=0, padx=2, pady=3, sticky=W)

        self.Entry_reference = Entry(dataframe, validate=ALL, validatecommand=selectededit,
                                     textvariable=self.reference, font=('arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_reference .grid(
            row=0, column=1, padx=2, pady=3, sticky='we', ipady=2)

        # searching by ref button
        self.photo = tk.PhotoImage(file=r"./101791-200.png")
        self.search = Button(dataframe, text='', image=self.photo,
                             relief=FLAT, bg='#F4F6F6', command=Search).grid(row=0, column=2)
        ##

        # ?annee
        self.lbl_annee = Label(dataframe, text="annee", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_annee.grid(row=1, column=0, padx=5, pady=3, sticky=W)

        self.Entry_annee = Entry(dataframe, validate=ALL, validatecommand=selectededit,
                                 textvariable=self.annee, font=('arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_annee.grid(row=1, column=1, padx=2,
                              ipady=2,  pady=3, sticky='we')
        ##

        # ?nature
        natures = ['', 'M', 'BC', 'OP', 'EL', 'J', 'DE', 'DO', 'DC']
        clicked = tk.StringVar()
        clicked.set(natures[0])

        dropbox = OptionMenu(dataframe, clicked, *natures, command=selected)
        dropbox.grid(row=2, column=2, pady=3)
        # ?

        # ?autre_nature
        self.lbl_autre = Label(dataframe, text='Autre', bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_autre.grid(row=2, column=0, padx=5, pady=3, sticky=W)

        self.Entry_autre = Entry(dataframe, validate=ALL, validatecommand=selectededit,
                                 textvariable=self.nature, font=('arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_autre.grid(row=2, column=1, padx=2,
                              pady=3, ipady=2, sticky='w')

        # ?numero
        self.lbl_numero = Label(dataframe, text=self.numero, textvariable=self.numero, font=(
            'arial', 12, 'bold'), bd=3, relief=FLAT)
        self.lbl_numero.grid(row=5, column=1, pady=3, sticky='we')

        # ?archive_le
        self.lbl_archive_le = Label(dataframe, text='archivé Le', bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_archive_le.grid(row=4, column=0, padx=5, pady=3, sticky=W)

        self.Entry_archive_le = Entry(dataframe, textvariable=self.archive_le, font=(
            'arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_archive_le.grid(
            row=4, column=1, padx=2, pady=3, ipady=2, sticky='w')

        # ?statue
        self.lbl_reference = Label(dataframe, text="Reference", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_reference .grid(row=0, column=0, padx=2, pady=3, sticky=W)

        # ?aucour
        self.radiobtn1 = Radiobutton(dataframe, text='au cour', fg='green',
                                     bg='#F4F6F6', variable=self.status, command='', value='actif')
        self.radiobtn1.grid(row=6, column=1, pady=3, sticky=W)
        self.radiobtn2 = Radiobutton(dataframe, text='ferme', fg='red',
                                     variable=self.status, bg='#F4F6F6', command='',  value='ferme')
        self.radiobtn2.grid(row=6, column=1, pady=3, sticky=E)

########################################### !  calendar  ######################################

        cal = DateEntry(dataframe, width=2, date_pattern='dd/mm/y',
                        locale='fr', background='darkblue', foreground='white')
        cal.grid(row=4, column=2)
        cal.bind("<<DateEntrySelected>>", getSelectedDate)

########################################### !  storing data  ##########################################################

        # ?local
        self.lbl_local = Label(storageframe, text="Local", bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_local.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        self.Entry_local = Entry(storageframe, textvariable=self.local, font=(
            'arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.Entry_local.grid(row=0, column=1, padx=2,
                              pady=2, sticky='w', ipady=2)
        # ?

        # ?boitier
        self.lbl_boitier = Label(storageframe, text='Boitier', bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_boitier.grid(row=1, column=0, padx=2, pady=2, sticky=W)

        self.spin_boitier = Entry(storageframe, textvariable=self.boitier, font=(
            'arial', 9, 'bold'), bd=5, relief=GROOVE)
        self.spin_boitier.grid(row=1, column=1, padx=2,
                               pady=2, sticky='w', ipady=2)
        # ?

        # ?travee
        self.lbl_travee = Label(storageframe, text='travée', bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_travee.grid(row=2, column=0, padx=2, sticky=W)

        self.spin_travee = Spinbox(
            storageframe, from_=0, to=1000, textvariable=self.travee, font=('arial', 9, 'bold'))
        self.spin_travee.grid(row=2, column=1, padx=2,
                              pady=2, sticky='w', ipady=4)
        # ?

        # ?tablette
        self.lbl_tablette = Label(storageframe, text='tablette', bg='#F4F6F6', fg='#665782', font=(
            'arial', 9, 'italic'), bd=5, relief=FLAT)
        self.lbl_tablette.grid(row=3, column=0, padx=2, sticky=W)

        self.spin_tablette = Spinbox(
            storageframe, from_=0, to=1000, textvariable=self.tablette, font=('arial', 9, 'bold'))
        self.spin_tablette.grid(row=3, column=1, padx=2,
                                pady=2, sticky='w', ipady=4)
        # ?

        # ?valable
        self.valablegrey = Radiobutton(storageframe, fg='grey', bg="#F4F6F6")
        self.valablegrey.grid(row=4, column=1, sticky=W)
        self.valablered = Radiobutton(storageframe, fg='red', bg="#F4F6F6")
        self.valablegreen = Radiobutton(storageframe, fg='green', bg="#F4F6F6")

        self.valable = ttk.Combobox(storageframe, width=10, values=[
                                    "", "valable", "non valable"], textvariable=self.valable)
        self.valable.grid(row=4, column=1)
        self.valable.bind("<<ComboboxSelected>>", tekenornotbtn)

        self.byyear = ttk.Combobox(ordersframe, width=10, values=[
                                   "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"], textvariable=self.byyear)
        self.byyear.grid(row=0, column=0)
        self.byyear.bind("<<ComboboxSelected>>", byyear)

        self.openwindow = Button(
            storageframe, text="ajouter un mouvement", command=openwidow, relief=FLAT)
        self.openwindow.grid(row=5, column=1, sticky=EW, padx=5, pady=4)

########################################### !  informations additionnelles   ##########################################################

        # ?Text entry
        self.lbl_note = Label(topnote, text='informations additionnelles', bg='#F4F6F6',
                              fg='#665782', font=('arial', 10, 'bold'), bd=5, relief=FLAT)
        self.lbl_note.grid(row=0, column=0, padx=5, sticky=W)
        self.note = tk.Text(topnote, height=9, state='normal',
                            width=35, font=('arial', 9, 'bold'), wrap=tk.WORD)
        self.note.grid(row=1, column=0, pady=4, padx=4)

########################################### !  mouvement   ##########################################################
        '''''
        ##?Text entry
        self.lbl_mouvement = Label(takenframe, text='mouvement', bg='#F4F6F6', fg='#665782', font=('arial', 10, 'bold'), bd=5, relief=FLAT)
        self.lbl_mouvement.grid(row=0,column=0, padx=5, sticky=W)
        self.mouvementtxt = tk.Text(takenframe,height=9,state=DISABLED, width=35,font=('arial', 9, 'bold'), wrap=tk.WORD)
        self.mouvementtxt.grid(row=1, column=0, pady=4,padx=2)
        '''''

########################################### !  treebar   #########################################################
        scroll_x = Scrollbar(treeframe, orient=HORIZONTAL)
        scroll_y = Scrollbar(treeframe, orient=VERTICAL)

        columns = ('reference', 'annee', 'nature', 'archive le', 'numero', 'status', 'local',
                   'boitier', 'travee', 'tablette', 'valable', 'informations additionnelles')
        self.info_de_marche = ttk.Treeview(
            treeframe, height=450, columns=columns, xscrollcommand=scroll_x, yscrollcommand=scroll_y)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=LEFT, fill=Y)

        self.info_de_marche.heading("reference", text="Ref")
        self.info_de_marche.heading("annee", text="annee")
        self.info_de_marche.heading("nature", text="nature")
        self.info_de_marche.heading("archive le", text="archive le")
        self.info_de_marche.heading("numero", text="num")
        self.info_de_marche.heading("status", text="status")
        self.info_de_marche.heading("local", text="local")
        self.info_de_marche.heading("boitier", text="boitier")
        self.info_de_marche.heading("travee", text="travee")
        self.info_de_marche.heading("tablette", text="tablette")
        self.info_de_marche.heading("valable", text="valable")
        #self.info_de_marche.heading("mouvement", text="mouvement")
        self.info_de_marche.heading(
            "informations additionnelles", text="info. add.")

        self.info_de_marche['show'] = 'headings'

        self.info_de_marche.column("reference", width=20)
        self.info_de_marche.column("annee", width=10)
        self.info_de_marche.column("nature", width=10)
        self.info_de_marche.column("archive le", width=30)
        self.info_de_marche.column("numero", width=50)
        self.info_de_marche.column("status", width=10)
        self.info_de_marche.column("local", width=30)
        self.info_de_marche.column("boitier", width=20)
        self.info_de_marche.column("travee", width=8)
        self.info_de_marche.column("tablette", width=8)
        self.info_de_marche.column("valable", width=20)
        #self.info_de_marche.column("mouvement", width=50)
        self.info_de_marche.column("informations additionnelles", width=100)

        self.info_de_marche.pack(fill=BOTH, expand=1)
        #self.info_de_marche.bind("<ButtonRelease-1>", Fill_info )
        self.info_de_marche.bind('<<TreeviewSelect>>', item_selected)


########################################### !  buttons  ##########################################################

        self.btnaddnew = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7", width=5, text='ajouter', command=lambda: [
                                add_data(), getNoteText()], relief=FLAT).grid(row=0, column=0, padx=10, pady=5)

        self.btnupdate = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7",
                                width=5, text='editer', command=Update, relief=FLAT).grid(row=0, column=1, padx=10)

        self.btndelete = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7",
                                width=5, text='supprimer', command=Delete, relief=FLAT).grid(row=0, column=2, padx=10)

        self.btnreset = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7", width=5, text='vider',
                               command=Reset, relief=FLAT).grid(row=0, column=3, padx=10)

        self.btnresult = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7", width=5, text='resultat',
                                command=Display, relief=FLAT).grid(row=0, column=4, padx=10)

        self.btnexit = Button(btnframe, pady=1, padx=11,  bd=4, font=('arial', 8, 'bold'), bg="#CADDF7", width=5, text='sortir',
                              command=Exit, relief=FLAT).grid(row=0, column=5, padx=10)

        Display()


if __name__ == '__main__':
    root = Tk()
    application = management_sys(root)
    root.mainloop()
