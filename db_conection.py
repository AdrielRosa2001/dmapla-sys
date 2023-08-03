import pyodbc

class ServerDB():

    cursor = None
    sessao = False

    def __init__(self):
        driver = "{SQL Server}"
        server = "DESKTOP-BOE9DIN\SQLEXPRESS"
        port = "35980"
        database = "SICNET_139726"
        user = "ADMIN"
        password = "Ab04042112#"
        #conn = pyodbc.connect(f"DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={user};PWD={port};PORT={port}")
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BOE9DIN\SQLEXPRESS,35980;DATABASE=SICNET_139726;UID=ADMIN;PWD=Ab04042112#;PORT=35980')
        print("Server DB connected")
        self.sessao = True
        self.cursor = conn.cursor()
    
    def consulta(self, codigo):
        if self.sessao == True:
            self.cursor.execute(f"SELECT [produto], [precovenda] FROM [SICNET_139726].[dbo].[TABEST1] WHERE [codigo] = '{codigo}'")
            row = self.cursor.fetchone()
            if row:
                return dict({"PRODUTO": row[0], "VALOR": str(round(row[1], 2)).replace(".", ",") })
            else:
                return dict({"PRODUTO": "Produto não localizado!", "VALOR": "0,00" })

    def consulta_dict(self, codigo):
        if self.sessao == True:
            self.cursor.execute(f"SELECT [produto], [precovenda] FROM [SICNET_139726].[dbo].[TABEST1] WHERE [codigo] = '{codigo}'")
            row = self.cursor.fetchone()
            if row:
                codigo_item = codigo
                titulo = row[0]
                valor = str(round(row[1], 2)).replace(".", ",")
                dicionario = {
                    "titulo": titulo,
                    "preço": f"R$ {valor}",
                    "codigo": codigo_item
                }
                #return dict({"PRODUTO": row[0], "VALOR": str(round(row[1], 2)).replace(".", ",") })
                return dicionario
            else:
                return None
    
    def consulta_tuple_quant(self, codigo):
        if self.sessao == True:
            self.cursor.execute(f"SELECT [produto], [precovenda] FROM [SICNET_139726].[dbo].[TABEST1] WHERE [codigo] = '{codigo}'")
            row = self.cursor.fetchone()
            if row:
                codigo_item = codigo
                titulo = row[0]
                valor = str(round(row[1], 2)).replace(".", ",")
                dicionario = {
                    "titulo": titulo,
                    "codigo": codigo_item,
                    "preco": f"R$ {valor}"
                }
                #return dict({"PRODUTO": row[0], "VALOR": str(round(row[1], 2)).replace(".", ",") })
                return dicionario
            else:
                return None
            






