import pyodbc

class ServerDB():

    cursor = None
    sessao = False

    def __init__(self):
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=server,port;DATABASE=database;UID=user;PWD=senha;PORT=port')
        print("Server DB connected")
        self.sessao = True
        self.cursor = conn.cursor()
    
    def consulta(self, codigo):
        if self.sessao == True:
            self.cursor.execute(f"SELECT [produto], [precovenda] FROM [database].[dbo].[TABEST1] WHERE [codigo] = '{codigo}'")
            row = self.cursor.fetchone()
            if row:
                return dict({"PRODUTO": row[0], "VALOR": str(round(row[1], 2)).replace(".", ",") })
            else:
                return dict({"PRODUTO": "Produto não localizado!", "VALOR": "0,00" })

server = ServerDB()






