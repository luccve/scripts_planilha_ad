from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from format_file import ProcessadorArquivo
import os

class InterfaceTkinter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Selecione o arquivo")

        messagebox.showinfo('Tutorial', 'Selecione o arquivo no padrao de cabeçalhos confira a planilha modelo.\n O valor de escala padrão é 250.000')
        # Centralizando a janela na tela
        self.root.eval('tk::PlaceWindow . center')

        # Dimensões da janela
        largura = 400
        altura = 300

        # Obtendo a largura e altura da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        # Calculando as coordenadas para centralizar a janela
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        # Definindo a geometria da janela
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')

        self.name_file_out = StringVar()
        self.target = StringVar()
        self.path_file = StringVar()
        self.escala = StringVar()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=30)

        style = ttk.Style()
        style.configure("Botao.TButton", foreground="green", background="white", font=("Arial", 12, "bold"))
        

        self.label = tk.Label(self.frame, textvariable=self.path_file, font=("Arial", 8))
        self.label.pack()


        self.botao_selecionar = tk.Button(self.frame, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        self.botao_selecionar.pack()

        self.label2 = tk.Label(self.root, text="Selecione o target:")
        self.label2.pack()

        self.target_combobox = ttk.Combobox(self.root, textvariable=self.target)
        self.target_combobox.pack()

        self.label3 = tk.Label(self.root, text="Valor da Escala:")
        self.label3.pack(anchor="center")

        self.target_combobox2 = ttk.Combobox(self.root, textvariable=self.escala)
        self.target_combobox2['values']=['5.000','10.000', '15.000','25.000', '30.000', '50.000', '75.000', '100.000', '150.000', '200.000', '250.000', '500.000', '1.000.000' ]
        self.target_combobox2.pack()


        self.botao_executar = ttk.Button(self.root, text="Executar", command=self.executar_processadomento, style="Botao.TButton")
        self.botao_executar.pack()

        self.texto = tk.Label(self.root, text="Estevão Lucas\nhurryblank@gmail.com\nversion 1.0.0")
        self.texto.pack()


        self.root.mainloop()

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(initialdir='./', filetypes=[("Arquivos XLSX", "*.xlsx"),("Arquivos XLS", "*.xls"), ("Arquivos CSV", "*.csv")])
        self.path_file.set(caminho_arquivo)
        if caminho_arquivo:
            messagebox.showinfo('Aviso', 'Selecione o valor de índice que irá ser usado para o join')
            name_file = os.path.basename(caminho_arquivo).split('.')
            print(name_file)
            if(len(name_file)==2):
                name_file = name_file[0].strip()
            else:
                name_file = (name_file[0]+'_'+name_file[1]).strip()
            self.name_file_out.set(name_file)

            def update_combobox(targets):
                self.target_combobox['values'] = targets
            # Instancia a classe ProcessadorArquivo com o callback
            processador = ProcessadorArquivo(caminho_arquivo, callback=update_combobox)
            processador.ler_arquivo()

        else:   
            messagebox.showerror('Error', 'Selecione um arquivo válido')

    def executar_processadomento(self):
        self.processar_arquivo(self.path_file.get())

    def processar_arquivo(self, caminho_arquivo):
        try:
            processador = ProcessadorArquivo(caminho_arquivo)
            processador.ler_arquivo()
            self.target_combobox['values'] = processador.targets
            processador.target = self.target.get()
            processador.processar_dataframe(self.escala.get())
            msg =processador.exportar_dataframe(f'{self.name_file_out.get()}_novo.csv')
            messagebox.showinfo('Concluído', msg)
        except Exception as e:
            self.generate_message('Error', e)

    def generate_message(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    InterfaceTkinter()
