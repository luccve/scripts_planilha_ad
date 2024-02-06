import pandas as pd

# Carregar o arquivo Excel
excel_file = 'CALCULO DE AD GERAL.xlsx'

# Ler o arquivo Excel
xls = pd.ExcelFile(excel_file)

# Iterar sobre as abas (planilhas) no arquivo Excel
for sheet_name in xls.sheet_names:
    # Ler a planilha atual
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Determinar o nome do arquivo CSV
    csv_file = f'{sheet_name}.csv'
    
    # Salvar a planilha como um arquivo CSV
    df.to_csv(csv_file, index=False)

    print(f'{sheet_name} salvo como {csv_file}')
