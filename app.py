from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk 
import pandas as pd
import os

class FileSelector(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.file_path = StringVar()
        self.save_path = StringVar()
        self.target = StringVar()
        self.targetList = []
        self.name_file = StringVar()
        self.button1 = Button(self, text="Selecionar Arquivo", command=self.get_file_path)
        self.button1.pack()

        self.label1 = Label(self, textvariable=self.file_path)
        self.label1.pack()

        self.button2 = Button(self, text="Salvar Arquivo", command=self.save_file_path)
        self.button2.pack()

        self.label2 = Label(self, textvariable=self.save_path)
        self.label2.pack()

        # Criando o widget Combobox (lista suspensa) chamado 'target'
        self.target_combobox = ttk.Combobox(self, textvariable=self.target)
        self.target_combobox['values'] = self.targetList  # Substitua com suas opções
        self.target_combobox.pack()

        self.button4 = Button(self, text="Ler", command=self.get_columns)
        self.button4.pack()
        
        self.button3 = Button(self, text="Executar", command=self.load)
        self.button3.pack()

    def get_columns(self):
        if(self.file_path.get() != ""):
            df = pd.read_excel(self.file_path.get())
     
            self.targetList =  [colunas for colunas in df.columns]
            self.target_combobox['values'] = self.targetList 
            self.name_file = os.path.basename(self.file_path.get())
        else:
            self.generate_error('selecione o arquivo')

    def get_file_path(self):
        self.file_path.set(filedialog.askopenfilename(title="Selecionar Arquivo"))
        

    def save_file_path(self):
        self.save_path.set(filedialog.askdirectory(initialdir=os.path.dirname(self.file_path.get()), title="Salvar Arquivo"))
    
    def generate_error(self, message):
        messagebox.showerror("Error", message)
    
    def load(self):
        if(self.save_path.get()!= ""):
            print(self.target.get())
            self.ler_arquivo_xlsx()
        else:
            self.generate_error('Pasta do arquivo não selecionada')

    def ler_arquivo_xlsx(self):
        try:

            path = self.file_path.get()
            data_frame = pd.read_excel(path)
            self.format_file(data_frame)
            
        except FileNotFoundError:
            self.generate_error(f"Arquivo não encontrado: {self.file_path.get()}")
        except Exception as e:
            self.generate_error(f"Erro ao ler o arquivo: {e}")
    
    def format_file(self, file):
            try:
                df = file
                target = self.target.get().lower()
               
                colunas_drop = []
                textura_componentes = {'textura_c1': [], 'textura_c2': [], 'textura_c3': [], 'textura_c4': [],'textura_c5': [],}
                solos_componentes = {'solos_c1': [], 'solos_c2': [], "solos_c3":[],"solos_c4":[],"solos_c5":[]}
                
                for coluna in df.columns:
                    lowerString = coluna.lower()
                    if "pedre" in lowerString:
                        df.rename(columns={coluna:f"pedrego_c{coluna[0]}"}, inplace=True)
                    elif "nivel" in lowerString:
                        df[coluna] = df[coluna].astype(str)
                        if(int(coluna[0]) and int(coluna[-1])):
                            df.rename(columns={coluna: f'{coluna[0]} Nivel{coluna[-1]}'}, inplace=True)
                            solos_componentes[f'solos_c{coluna[0]}'].append(f'{coluna[0]} Nivel{coluna[-1]}')
                    elif "rocho" in lowerString:
                        df.rename(columns={coluna:f"rocho_c{coluna[0]}"}, inplace=True)
                    elif "relevo" in lowerString:
                        df.rename(columns={coluna:f"relevo_c{coluna[0]}"}, inplace=True)
                    elif "adum" in lowerString:
                        df.rename(columns={coluna:f"ad_um"}, inplace=True)
                    elif "solo_" in lowerString:
                        continue
                    elif "ad_" in lowerString:
                        continue
                    elif target == lowerString:
                        print('Entrei', coluna)
                        df.rename(columns={coluna:'ind_csv'}, inplace=True)
                    elif "ad solo" in lowerString or "adsolo" in lowerString:
                        df.rename(columns={coluna:f"ad_c{coluna[0]}"}, inplace=True)
                    elif "textu" in lowerString:
                        df[coluna] = df[coluna].astype(str)
                        if(coluna.startswith("1") and not coluna in textura_componentes["textura_c1"]):
                            textura_componentes["textura_c1"].append(coluna)
                        if(coluna.startswith("2") and not coluna in textura_componentes["textura_c2"]):
                            textura_componentes["textura_c2"].append(coluna)
                        if(coluna.startswith("3")) and not coluna in textura_componentes["textura_c3"]:
                            textura_componentes["textura_c3"].append(coluna)
                        if(coluna.startswith("4")) and not coluna in textura_componentes["textura_c4"]:
                            textura_componentes["textura_c4"].append(coluna)
                        if(coluna.startswith("5")) and not coluna in textura_componentes["textura_c5"]:
                            textura_componentes["textura_c5"].append(coluna)
                    else:
                        colunas_drop.append(coluna)

        
                    #solos
                    for key, value in solos_componentes.items():
                        df[key] = df[value].apply(lambda row: ', '.join(filter(lambda x: x if x !="nan" else None, row)), axis=1)
                        df.drop(columns=value, inplace=True)
                    
              
                    #textura
                    for key, value in textura_componentes.items():
                        df[key] = df[value].apply(lambda row: ', '.join(filter(lambda x: x if x !="nan" else None, row)), axis=1)
                        df.drop(columns=value, inplace=True)
                  
                    #c1_class
                    df['c1_class'] = df['solos_c1']+' - ' + df['ind_csv']
                    print('teste4',self.target.get())
                    #limpando dataframe
                  
                    df.drop(columns=colunas_drop, inplace=True)
                    name = self.name_file.split('.')[0]
                    self.export_file(df,f'{name}_novo.csv')
                    return df
            except Exception as E:
                print(E)

          
    
    def export_file(self,file, nome_do_arquivo_out):
        path_saida = os.path.join(self.save_path.get(),nome_do_arquivo_out)
        file.to_csv(path_saida, index=False)
        return
        

app = FileSelector()
app.mainloop()
