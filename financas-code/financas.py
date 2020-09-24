import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
import datetime
import re

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.voltar = tk.Button(self)
        self.voltar['text'] = 'Voltar'
        self.voltar['command'] = self.back_to_main_page
        self.voltar.config(height=1, width=14)

        self.fontRoboto = tkFont.Font(family='Roboto', size=16)
        
        self.create_window()
        self.create_widgets()

    def create_window(self):
        self.master.geometry('400x300+800+150')
        self.master.resizable(False, False)
        self.master.title('Finanças')
    
    def create_widgets(self):
        self.grid()

        self.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=50)
        self.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=35)

        self.capital = tk.Button(self)
        self.capital['text'] = 'Capital Atual'
        self.capital['command'] = self.capital_window
        self.capital.config(height=2, width=14)
        self.capital.grid(row=2, column=3, sticky='EW')

        self.registros = tk.Button(self)
        self.registros['text'] = 'Registros'
        self.registros['command'] = self.registers_window
        self.registros.config(height=2, width=14)
        self.registros.grid(row=3, column=3, pady=[10, 0], sticky='EW')

        self.sair = tk.Button(self)
        self.sair['text'] = 'Sair'
        self.sair['fg'] = 'red'
        self.sair['command'] = self.master.destroy
        self.sair.config(height=1, width=14)
        self.sair.grid(row=4, column=3, pady=[10, 0], sticky='EW')

    def capital_window(self):
        #Apagar a main page
        self.capital.grid_forget()
        self.registros.grid_forget()
        self.sair.grid_forget()

        #Capital page
        self.voltar.grid(row=0, column=0, padx=[10, 0], pady=[10, 0])

        self.capital_value = self.get_capital()
        self.capital_text = tk.Label(self, text=f'Capital atual: R${self.capital_value:.2f}', font=self.fontRoboto)
        self.capital_text['fg'] = 'green'
        self.capital_text.grid(row=3, column=1)

        self.change_capital = tk.Button(self)
        self.change_capital['text'] = 'Alterar'
        self.change_capital['command'] = self.new_register
        self.change_capital.config(height=2, width=14)
        self.change_capital.grid(row=7, column=0, padx=[10, 0])

    def registers_window(self):
        self.capital.grid_forget()
        self.registros.grid_forget()
        self.sair.grid_forget()

        #Register page
        self.voltar.grid(row=0, column=0, padx=[10, 0], pady=[10, 0])
        self.voltar['command'] = self.back_to_main_page_from_register

        self.tree = ttk.Treeview(self)
        self.tree.heading('#0', text='Registros')
        self.tree.column('#0', minwidth=0, width=350, stretch=tk.NO)
        self.get_registers()
        self.tree.grid(row=1, column=0, columnspan=6, padx=[10, 0], pady=[10, 0])

        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=1, column=6, sticky=tk.N+tk.S+tk.W)   

    def get_registers(self):
        registros_archive = open('src/registros.txt', 'r')
        registros_lines = registros_archive.readlines()
        registros_archive.close()

        registros_lines_formated = []
        for c in registros_lines:
            registros_lines_formated.append(c[:-1]) #Retira o '\n'

        iter_registros = len(registros_lines_formated)
        registros_lines_formated_reverse = [None]*iter_registros
        for c in registros_lines_formated:
            iter_registros -= 1
            registros_lines_formated_reverse[iter_registros] = c

        for c in registros_lines_formated_reverse:
            comma1_index = c.index(',')
            value = c[1:comma1_index]

            comma2_index = c[comma1_index+1:].index(',')
            comment = c[comma1_index+3:comma2_index + comma1_index]

            date = c[(comma2_index + comma1_index + 1)+3:-2]
            date = date[-2:] + '-' + date[-5:-3] + '-' + date[:4]

            self.tree.insert('', 'end', f'R${value} ({date}) - {comment}', text=f'R${value} ({date}) - {comment}')

    def back_to_main_page(self):
        self.capital_text.grid_forget()
        self.change_capital.grid_forget()
        self.voltar.grid_forget()
        
        self.create_widgets()

    def back_to_main_page_from_register(self):
        self.voltar['command'] = self.back_to_main_page
        self.voltar.grid_forget()
        self.tree.grid_forget()
        self.vsb.grid_forget()
        
        self.create_widgets()
    
    def back_to_capital_page(self):
        self.voltar['command'] = self.back_to_main_page
        
        self.register_value_label.grid_forget()
        self.register_value_entry.grid_forget()
        self.register_comment_label.grid_forget()
        self.register_comment_entry.grid_forget()
        self.submit_register.grid_forget()

        self.capital_window()

    #Encontrar o valor do capital atual
    def get_capital(self):
        self.capital_archive = open('src/capital.txt', 'r')

        self.capital_value = list(self.capital_archive)[0]

        self.capital_archive.close()

        return float(self.capital_value)

    def new_register(self):
        self.capital_text.grid_forget()
        self.change_capital.grid_forget()

        self.voltar['command'] = self.back_to_capital_page

        self.register_value_label = tk.Label(self, text='Valor (R$ +/-):')
        self.register_value_label.grid(row=2, column=0)

        self.register_value_entry = tk.Entry(self, width=40)
        self.register_value_entry.grid(row=3, column=0, columnspan=3, padx=[10, 0])

        self.register_comment_label = tk.Label(self, text='Comentário:')
        self.register_comment_label.grid(row=4, column=0)

        self.register_comment_entry = tk.Entry(self, width=40)
        self.register_comment_entry.grid(row=5, column=0, columnspan=3, padx=[10, 0])

        self.submit_register = tk.Button(self, text='Adicionar registro', command=self.add_register)
        self.submit_register.config(height=2, width=14)
        self.submit_register.grid(row=7, column = 0)

    def add_register(self):
        try:
            self.register_value = float(self.register_value_entry.get())
            self.register_comment = self.register_comment_entry.get()

            self.registros_archive = open('src/registros.txt', 'r')
            self.registros_list = []
            self.registros_list = list(self.registros_archive)
            self.registros_archive.close()
            
            self.registros_list.append(f'({self.register_value:.2f}, "{self.register_comment}", "{datetime.date.today()}")\n')

            self.registros_archive = open('src/registros.txt', 'w')
            self.registros_archive.writelines(self.registros_list)
            self.registros_archive.close()

            self.capital_value = self.get_capital()
            self.capital_value += self.register_value
            self.capital_archive = open('src/capital.txt', 'w')
            self.capital_archive.writelines(f'{self.capital_value}')

            self.back_to_capital_page()

        except ValueError: #CORRIGIR
            messagebox.showerror('Erro', 'Por favor, verifique os valores digitados.')
            print(list(ValueError)[0])

root = tk.Tk()
app = App(master=root)
app.mainloop()