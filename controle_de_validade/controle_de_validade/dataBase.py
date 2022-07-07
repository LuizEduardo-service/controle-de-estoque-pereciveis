import os
import sqlite3 as sq


class DataBase:
    def __init__(self, tipo: int) -> None:
        self.dblocal =r'..\data\dataBaseLocal.db'
        self.banco_global ='\dataBaseGlobal.db'
        self.dbGlobal  = ''
        self.tipo = tipo
        self.connect_data_base(self.tipo)

    def conecta_banco_global(self):
        try:
            sql ="""SELECT dir_bd FROM tb_config WHERE id = 1"""
            self.connect_data_base(1)
            caminho_global = self.selectAll(sql)
            self.dbGlobal = caminho_global[0][0] + self.banco_global
            if self.teste_de_conexao(self.dbGlobal):
                return True
            else:
                return True
        except:
            print(f'Erro de Conexão...')
            return False

    def teste_de_conexao(self, dir):
        try:
            self.conn = sq.connect(dir)
            self.conn.close()
            return True
        except:
            return False

    def connect_data_base(self, tipo: int):
        try:

            if tipo == 1:
                self.conn = sq.connect(self.dblocal)
                self.cursor = self.conn.cursor()
            elif tipo == 2:
                if self.conecta_banco_global():
                    self.conn = sq.connect(self.dbGlobal)
                    self.cursor = self.conn.cursor()
            else:
                pass
        except:
            print('Erro ao conectar no banco de dados')

    def insert(self, stringSQL, data: list = []):
        self.cursor.executemany(stringSQL, data)
        self.conn.commit()
        self.conn.close()

    def update(self, stringSQL):
        self.cursor.execute(stringSQL)
        self.conn.commit()
        self.conn.close()

    def delete(self, stringSQL):
        self.cursor.execute(stringSQL)
        self.conn.commit()
        self.conn.close()

    def selectAll(self,stringSQL)-> list:
        self.cursor.execute(stringSQL)
        data = self.cursor.fetchall()
        self.conn.close()
        return data


    def cria_tabelas_global(self):


        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_periodo_rec(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             r_minimo INTEGER,
                             a_comercial INTEGER                               

                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_dataBase(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            matricula VARCHAR(10),
                            conferente VARCHAR(150),
                            produto VARCHAR(10),
                            descricao VARCHAR(200),
                            data_min_rec VARCHAR(10),
                            alerta_comercial VARCHAR(10),
                            descri_status VARCHAR(50),
                            data_fabricacao VARCHAR(10),
                            data_vencimento VARCHAR(10),
                            data_recebimento VARCHAR(10),
                            hora_recebimento VARCHAR(10),
                            status_de_recebimento VARCHAR(20)

                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_usuarios(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            matricula VARCHAR(10),
                            usuario VARCHAR(150),
                            cargo VARCHAR(50),
                            setor VARCHAR(50),
                            acesso INTEGER,
                            senha VARCHAR(50)
                              
                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_produtos(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                produto VARCHAR(10),
                                descricao VARCHAR(200),
                                categoria VARCHAR(20)

                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_cargo (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    cargo VARCHAR(50)
                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_setor(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    setor VARCHAR(50)
                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_categoria(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                categoria VARCHAR(20)

                            )""")


        self.conn.commit()
        self.conn.close()

    def cria_tabelas_local(self):
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_config(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             dir_bd VARCHAR(250),
                             nome_pdf VARCHAR(50),
                             nome_rel VARCHAR(50)                          

                            )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS tb_primeiro_acesso(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             valor INTEGER
                            )""")
        self.conn.commit()
        self.conn.close()
   

if __name__ == '__main__':
    lista =[
(None, 'GAMES/CAMERAS'),
(None, 'BEBES'),
(None, 'TELEFONIA CELULAR'),
(None, 'ACESSORIOS E COMPLEMENTOS'),
(None, 'ESPORTE'),
(None, 'FERRAMENTAS'),
(None, 'AUTOMOTIVOS'),
(None, 'CAMA/MESA/BANHO'),
(None, 'ELETRO-PORTATEIS'),
(None, 'BRINQUEDOS/PEDAL'),
(None, 'INOX/ALUMINIO/ETC'),
(None, 'INFORMATICA E EQUIP.ESCRITORIO'),
(None, 'SOM LEVE'),
(None, 'BELEZA & SAUDE'),
(None, 'MOVEIS PLANEJADOS'),
(None, 'DECORACOES'),
(None, 'PERFUMARIA'),
(None, 'QUEIMADORES'),
(None, 'RELOGIOS'),
(None, 'ESTOFADOS'),
(None, 'LAVADORAS'),
(None, 'MOVEIS DE SALA DE JANTAR'),
(None, 'TELEVISORES'),
(None, 'MALAS / MOCHILAS / ACESSORIOS'),
(None, 'SAZONAIS LINHA BRANCA'),
(None, 'MOVEIS DE COPA E COZINHA'),
(None, 'MOVEIS DE QUARTO'),
(None, 'SAZONAIS PORTATEIS'),
(None, 'LINHA INDUSTRIAL'),
(None, 'CALCADOS/ACESSORIOS FEMININO'),
(None, 'MOVEIS INFANTIS'),
(None, 'CONFECCAO MASCULINA'),
(None, 'COLCHOES'),
(None, 'CONFECCAO FEMININA'),
(None, 'PRODUTOS DE LIMPEZA'),
(None, 'MOVEIS SALA DE ESTAR'),
(None, 'CONFECCAO BEBE/INFANTIL'),
(None, 'REFRIGERACAO'),
(None, 'DISNEY SUPER LOJA'),
(None, 'PAPELARIA E MAT.ESCRITORIO'),
(None, 'CALCADOS/ACESSORIOS INFANTIL'),
(None, 'REVISTAS/LIVROS'),
(None, 'DVD FILMES E CDS MUSICAIS'),
(None, 'BICICLETAS'),
(None, 'TAPECARIA')

    ]
    bd = DataBase(1)
    bd.cria_tabelas_local()
    # sql = f'INSERT INTO tb_categoria VALUES (?,?)'

    # bd.insert(sql, lista)