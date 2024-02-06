import pandas as pd
import os

class ProcessadorArquivo:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df = None
        self.target = None
        self.targets = None
    def ler_arquivo(self):
        try:
            tipo = self.caminho_arquivo.split('.')[1]
            if tipo in ['xls', 'xlsx']:
                self.df = pd.read_excel(self.caminho_arquivo)
            elif tipo == 'csv':
                with open(self.caminho_arquivo, 'r') as file:
                    first_line = file.readline().strip()
                    delimiter = ',' if ',' in first_line else ';'
                self.df = pd.read_csv(self.caminho_arquivo, sep=delimiter)
            else:
                raise ValueError("Tipo de arquivo não suportado. Por favor, forneça 'xls', 'xlsx' ou 'csv'.")
            
            self.targets = [coluna for coluna in self.df.columns]

        except FileNotFoundError:
            return(f"Arquivo não encontrado: {self.caminho_arquivo}")
        except Exception as e:
            return(f"Erro ao ler o arquivo: {e}")

    def processar_dataframe(self, scale):
        if self.df is None:
            return("O DataFrame não foi carregado.")
        colunas_drop = []
        textura_componentes = {'textura_c1': [], 'textura_c2': [], 'textura_c3': [], 'textura_c4': [],'textura_c5': [],}
        solos_componentes = {'solos_c1': [], 'solos_c2': [], "solos_c3":[],"solos_c4":[],"solos_c5":[]}

        for coluna in self.df.columns:
            lowerString = coluna.lower()
            if "pedre" in lowerString:
                self.df.rename(columns={coluna:f"pedrego_c{coluna[0]}"}, inplace=True)
            elif "nivel" in lowerString:
                self.df[coluna] = self.df[coluna].astype(str)
                if(int(coluna[0]) and int(coluna[-1])):
                    self.df.rename(columns={coluna: f'{coluna[0]} Nivel{coluna[-1]}'}, inplace=True)
                    solos_componentes[f'solos_c{coluna[0]}'].append(f'{coluna[0]} Nivel{coluna[-1]}')
            elif "rocho" in lowerString:
                self.df.rename(columns={coluna:f"rocho_c{coluna[0]}"}, inplace=True)
            elif "relevo" in lowerString:
                self.df.rename(columns={coluna:f"relevo_c{coluna[0]}"}, inplace=True)
            elif "adum" in lowerString:
                self.df.rename(columns={coluna:f"ad_um"}, inplace=True)
            elif "solo_" in lowerString:
                continue
            elif "ad_" in lowerString:
                continue
            elif self.target.lower() == lowerString:
                self.df.rename(columns={coluna:'ind_csv'}, inplace=True)
                
            elif "ad solo" in lowerString or "adsolo" in lowerString:
                self.df.rename(columns={coluna:f"ad_c{coluna[0]}"}, inplace=True)
                continue
            elif "textu" in lowerString:
                self.df[coluna] = self.df[coluna].astype(str)
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


        for key, value in solos_componentes.items():
            self.df[key] = self.df[value].apply(lambda row: ' '.join(filter(lambda x: x if x !="nan" else None, row)), axis=1)
            self.df.drop(columns=value, inplace=True)

        for key, value in textura_componentes.items():
            self.df[key] = self.df[value].apply(lambda row: ', '.join(filter(lambda x: x if x !="nan" else None, row)), axis=1)
            self.df.drop(columns=value, inplace=True)

        self.df['c1_class'] = self.df['solos_c1']+' - ' + self.df['ind_csv']
        if(scale == ""):
            self.df['escala'] = f"Escala: 1:250.000"
        else:
            self.df['escala'] = f"Escala: 1:{scale}"

        self.df.drop(columns=colunas_drop, inplace=True)

    def exportar_dataframe(self, nome_arquivo_saida):
        if self.df is None:
            return("O DataFrame não foi carregado.")
            
        try:
            path_saida = os.path.join(os.path.dirname(self.caminho_arquivo), nome_arquivo_saida)
            self.df.to_csv(path_saida, index=False, encoding='utf-8-sig', sep=',')
            return(f"DataFrame exportado com sucesso para: {path_saida}")
        except Exception as e:
            return(f"Erro ao exportar o DataFrame: {e}")


# # Exemplo de uso da classe
# nome_do_arquivo = 'tabela_ad_df.csv'
# caminho_do_arquivo = ""
# indice_join = "Legenda 1"
# folder = 'DF'
# if os.path.isdir('CE'):
#     caminho_do_arquivo = os.path.join(os.path.abspath(folder), nome_do_arquivo)
# else:
#     raise Exception("Não Existe o caminho do arquivo")

# processador = ProcessadorArquivo(caminho_do_arquivo, indice_join)
# processador.ler_arquivo()
# processador.processar_dataframe()
# processador.exportar_dataframe('tabela_ad_df_novo.csv')
