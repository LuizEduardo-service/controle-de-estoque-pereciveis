
import os
from sre_compile import isstring
import sys

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))


from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from datetime import date, datetime
# from controle_de_validade.layout_pdf import Relatorios
from controle_de_validade.layout_pdf import Relatorios
from controle_de_validade.dataBase import DataBase
import pandas as pd
import time




root = Tk()
FONT_INIT =('Poppins', 15)
FONT_INIT_TXT_AREA =('Poppins', 10)
BT_COLOR = '#676AA9'
BT_COLOR_PRESS = '#888AC1'

class validadorEntradas:
    def valida_matricula(self, text):
        if text == '': return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 10000000

class TelaPrincipal(validadorEntradas, Relatorios):

    def __init__(self) -> None:
        self.root = root
        self.imagens_layout()
        self.valida_entradas()
        self.lista_campos()
        self.info_usuario = {}
        self.usuario_logado = ''
        self.matricula_logado = ''
        self.acesso_logado = ''
        self.nome_saida_pdf =''
        self.nome_rel =''
        self.diretorio_bd = ''
        self.valor_rec_minimo = 0
        self.valor_ale_comercial = 0
        self.data_recebimento = datetime.now().date()
        self.start()
        self.root.mainloop()

    def start(self):
        self.tela()

    def lista_campos(self):
        self.lista_valida_comp_tela_inicial: list = []
        self.lista_valida_comp_config: list = []
        self.lista_valida_comp_produtos: list = []
        self.lista_valida_comp_usuario: list = []
        self.lista_valida_comp_historico: list = []

    def valida_entradas(self):
        self.campo_matricula = (self.root.register(self.valida_matricula),'%P')

    def valida_campos_vazios(self, lista_campos: list):

        campo_validado = False
        for campo in lista_campos:
            if(len(campo.get())==0):
                campo_validado = True
                break

        if campo_validado ==True:
            messagebox.showerror('Campos Vazios', 'Existem campos em branco\nVerifique os dados e tente novamente')
            return False

        return True

    def imagens_layout(self):
        self.parentDirectory = os.path.dirname(os.path.abspath(__file__))
        self.parentDirectory = os.path.dirname(os.path.abspath(self.parentDirectory))
        dir_image = os.path.join(self.parentDirectory, 'image\\')

        self.image_ajuda_alerta =  PhotoImage(file=dir_image + 'ajuda_alerta.png')                
        self.image_ajuda_rec =  PhotoImage(file=dir_image +'ajuda_rec.png')   
        self.image_ajuda_massivo =  PhotoImage(file=dir_image +'ajuda_massivo.png') 
        self.image_config = PhotoImage(file=dir_image + 'config.png')
        self.image_login = PhotoImage(file=dir_image + 'telaLogin.png')
        self.image_cad_login = PhotoImage(file=dir_image + 'cadastroLogin.png')
        self.imagem_historico = PhotoImage(file=dir_image + 'historico.png')
        self.imagem_produtos = PhotoImage(file=dir_image + 'produtos.png')
        self.imagem_usuarios = PhotoImage(file=dir_image + 'usuarios.png')
        self.imagem_v_senha = PhotoImage(file=dir_image + 'verSenha.png')
        self.imagem_acesso = PhotoImage(file=dir_image + 'p_acesso.png')
        self.imagem_tela = PhotoImage(file=dir_image + 'tela1.png')
        self.imagem_tela = PhotoImage(file=dir_image +'tela1.png')
        self.imagem_pesquisa = PhotoImage(file=dir_image +'pesquisar.png',width=64,height=30)
        self.imagem_excel = PhotoImage(file=dir_image + 'b_excel.png')
        self.imagem_ficha = PhotoImage(file=dir_image + 'g_ficha.png')
        self.imagem_calendario = PhotoImage(file=dir_image + 'calendario.png')

    def widget_de_ajuda(self, tipo: int):
  
        if tipo == 1:
            self.lb_image_ajuda = Label(self.root,image=self.image_ajuda_rec)
            self.lb_image_ajuda.place(x=1011, y=467, width=300, height=188)
        elif tipo == 2:
            self.lb_image_ajuda = Label(self.root,image=self.image_ajuda_alerta)
            self.lb_image_ajuda.place(x=1011, y=467, width=300, height=188)
        elif tipo == 3:
            self.lb_image_ajuda = Label(self.root,image=self.image_ajuda_massivo)
            self.lb_image_ajuda.place(x=277, y=391, width=300, height=188)

    def centralizacao_tela(self,largura, altura,root):
        param = []
        # dimens??o tela computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()
        # posi????o da janela
        posX = (largura_screen/2) - (largura/2)
        posY = (altura_screen/2) - (altura/2)
        # definir posi????o
        param.append(largura);param.append(altura);param.append(posX);param.append(posY)
        return param

    def convert_data_str(self, data):
        return format(data,'%d/%m/%Y')

    def limpa_campos(self, tipo: int):
        """limpa os campos da tela"""
        if tipo == 1:
            self.rec_minimo.set('')
            self.alerta_comercial.set('')
            self.dta_fab.delete(0, END)
            self.dta_venc.delete(0, END)
            self.numSku.set('')
            self.descri_produto.set('')
            self.categoria.set('')
            self.msg.set('')
            sleep(1)
            # self.bt_receber.configure(bg=None)
            # self.btReceber.set('Aguardando Analise...')
        elif tipo == 2:
            self.rec_minimo.set('')
            self.alerta_comercial.set('')
            self.dta_fab.delete(0, END)
            self.dta_venc.delete(0, END)
            self.btReceber.set('Aguardando Analise...')

    def destroi_widget(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def procura_produto(self, numProduto):
        try:
            bd = DataBase(2)
            sql=f"""SELECT * FROM tb_produtos WHERE produto = '{str(numProduto)}'"""
            lista_produtos = bd.selectAll(sql)

            if lista_produtos:
                self.descri_produto.set(lista_produtos[0][2])
                self.categoria.set(lista_produtos[0][3])
                self.txt_produto.configure(bg='#ffffff')
                self.msg.set('')
                self.limpa_campos(2)
                self.configura_btn_receber()
            else:
                self.msg.set('PRODUTO N??O LOCALIZADO')
                self.descri_produto.set('')
                self.categoria.set('')
                self.txt_produto.configure(bg='#FA8072')
                self.limpa_campos(2)
                self.numSku.set('')
                self.txt_produto.focus
        except:
            messagebox.showerror('Erro consulta', 'N??o foi possivel conectar ao banco de  dados, por favor verifique a conex??o.')
           
    def define_alerta_comercial(self, dta_venc, dta_fab, percent):
        """ define a data do alerta comercial"""
        data_final = dta_venc - ((dta_venc - dta_fab) * (percent/100))

        # return format(data_final,'%d/%m/%Y')
        return data_final

    def define_minimo_recebimento(self, dta_venc, dta_fab, percent):
        """Define a data minima para recebimento do produto"""
        data_final = dta_venc - ((dta_venc - dta_fab) * (percent/100))
        # return format(data_final,'%d/%m/%Y')
        return data_final

    def variaveis_tela_inicial(self):
        self.numSku_v = self.numSku.get()
        self.descri_produto_v = self.descri_produto.get()
        self.categoria_v = self.categoria.get()
        self.dta_fab_v = self.data_fab
        self.dta_venc_v = self.data_venc
        self.rec_minimo_v = self.r_minimo
        self.alerta_comercial_v = self.a_comercial
        self.dta_recebimento_v = self.data_recebimento
        self.hra_recebimento_v = time.strftime('%H:%M')
        self.usuario_v = self.formata_nome_usuario( self.info_usuario['usuario'])
        self.matricula_v = self.info_usuario['matricula']
        self.receber_v = self.btReceber.get()

    def relogio(self):
        hora = time.strftime('%H')
        min = time.strftime('%M')
        seg = time.strftime('%S')
        self.relogio_h.config(text=hora + ':' + min + ':' + seg)
        self.relogio_h.after(1000,self.relogio)

    def gerar_pdf(self):
            self.variaveis_tela_inicial()
            gerarPdf = Relatorios(
                                    numSku = self.numSku_v,
                                    descri_produto = self.descri_produto_v,
                                    categoria = self.categoria_v,
                                    dta_fab = self.dta_fab_v,
                                    dta_venc = self.dta_venc_v,
                                    rec_minimo = self.rec_minimo_v,
                                    alerta_comercial = self.alerta_comercial_v,
                                    dta_recebimento = self.dta_recebimento_v,
                                    usuario = self.usuario_v,
                                    matricula = self.matricula_v,
                                    nome_arquivo = self.nome_saida_pdf

            )
            gerarPdf.gerar_relatorio()

    def logoff(self):
        self.info_usuario = {}
        self.componentes_login_usuario()

    def executa_calculos(self):
        
            f_data_fab = datetime.strptime(str(self.dta_fab.get()),'%d/%m/%Y')
            f_data_fab = datetime.strftime(f_data_fab,'%Y-%m-%d')
            f_data_venc = datetime.strptime(str(self.dta_venc.get()),'%d/%m/%Y')
            f_data_venc = datetime.strftime(f_data_venc,'%Y-%m-%d')

            self.status_recebimento: str = ''
            self.data_fab = datetime.strptime(f_data_fab,'%Y-%m-%d').date()
            self.data_venc = datetime.strptime(f_data_venc,'%Y-%m-%d').date()
            self.r_minimo = self.define_minimo_recebimento(self.data_venc, self.data_fab, self.valor_rec_minimo)
            self.a_comercial = self.define_alerta_comercial(self.data_venc, self.data_fab, self.valor_ale_comercial)
            status_rec = self.btReceber.get()

        
            if self.data_fab >= self.data_venc:
                self.btReceber.set('DATA DE FABRICA????O MAIOR OU IGUAL AO VENCIMENTO')
                self.bt_receber.configure(bg='#FA8072')
                self.rec_minimo.set('')
                self.alerta_comercial.set('')
                

            elif  self.r_minimo >= datetime.now().date():
                
                self.btReceber.set('PRODUTO LIBERADO PARA RECEBIMENTO')
                self.bt_receber.configure(bg='#3CB371')
                self.rec_minimo.set(self.convert_data_str(self.r_minimo))
                self.alerta_comercial.set(self.convert_data_str(self.a_comercial))
                # self.limpa_campos()
                

            else:
                self.btReceber.set('PRODUTO N??O LIBERADO PARA RECEBIMENTO')
                self.bt_receber.configure(bg='#FA8072')
                self.rec_minimo.set(self.convert_data_str(self.r_minimo))
                self.alerta_comercial.set(self.convert_data_str(self.a_comercial))
                # self.rec_minimo.set('')
                # self.alerta_comercial.set('')
                

            status_rec_validado = self.btReceber.get()

            if status_rec == 'PRODUTO LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO LIBERADO PARA RECEBIMENTO':
                if self.valida_campos_vazios(self.lista_valida_comp_tela_inicial):
                    self.status_recebimento = 'RECEBIDO'
                    self.insere_registros_rec()
                    self.gerar_pdf()
                    self.select_dados_rec()
                    self.txt_produto.focus()
                    self.limpa_campos(1)
                    self.btReceber.set('RECEBIMENTO FINALIZADO')
                    self.configura_btn_receber()

            elif status_rec == 'PRODUTO N??O LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO N??O LIBERADO PARA RECEBIMENTO':
                opc = messagebox.askyesnocancel("Recebimento de Mercadoria", 
                                                'Mercadoria n??o esta nos parametros de recebimento.\nContinuar recebimento?')
                messagebox.showerror('er',f'{opc}')
                if opc:
                    if self.valida_campos_vazios(self.lista_valida_comp_tela_inicial):
                        # messagebox.showinfo('Recebimento','Produto recebido!')
                        self.status_recebimento = 'RECEBIDO'
                        self.insere_registros_rec()
                        self.gerar_pdf()
                        self.select_dados_rec()
                        self.txt_produto.focus()
                        self.limpa_campos(1)
                        self.btReceber.set('RECEBIMENTO FINALIZADO')
                        self.configura_btn_receber()

                elif opc is None:
                    pass
                    # self.txt_produto.focus()
                    # self.insere_registros_rec()
                    # self.select_dados_rec()
                    # self.txt_produto.focus_force()
                    # self.limpa_campos(1)
                    # self.status_recebimento = 'N??O RECEBIDO'
                    # self.configura_btn_receber()
                else:
                    self.status_recebimento = 'N??O RECEBIDO'
                    self.insere_registros_rec()
                    self.select_dados_rec()
                    self.txt_produto.focus_force()
                    self.limpa_campos(1)
                    self.configura_btn_receber()
            else:
                pass


    def define_diretorio(self, tipo: str) -> str:
            diretorio = askdirectory()
            if diretorio:
                if tipo == 'bd':
                    self.dir_bd.set(diretorio)
                elif tipo == 'pdf':
                    self.dir_pdf.set(diretorio)
                elif tipo == 'rel':
                    self.dir_relatorio.set(diretorio)

    def recebimento_fora_prazo(self):
        self.foraPrazo = Toplevel()
        self.foraPrazo.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))
        

    def configura_btn_receber(self):
        self.bt_receber.configure(bg='#676AA9', fg='#ffffff')

    def componentes_tela_inicial(self):
        self.destroi_widget()
        self.lista_campos()
        self.carrega_dados_config()

        self.componentes_menu_bar()
       
        lb_image = Label(self.root,image=self.imagem_tela)
        lb_image.place(x=0, y=0)

        # relogio
        self.relogio_h = Label(self.root, font=FONT_INIT,bg='#ffffff')
        self.relogio_h.place(x=1254, y=164, width=122, height=24)
        self.relogio()

       #label data
        self.dta_fab = Entry(self.root,
                            font=('Poppins',20), 
                            justify='center')

        self.dta_fab.bind('<1>', lambda e: self.calendario(self.dta_fab))

        self.dta_venc = Entry(self.root,
                            font=('Poppins',20), 
                            justify='center')

        self.dta_venc.bind('<1>', lambda e: self.calendario(self.dta_venc))

        self.dta_fab.place(x=60, y=263, width=307, height=43)
        self.dta_venc.place(x=399, y=263, width=307, height=43)
        self.lista_valida_comp_tela_inicial.append(self.dta_fab)
        self.lista_valida_comp_tela_inicial.append(self.dta_venc)
        self.dta_fab.delete(0, END)
        self.dta_venc.delete(0, END)

        #bot??es
        self.btReceber = StringVar()
        self.numSku = IntVar()

        self.bt_receber = Button(self.root,
                            text='Aguardando analise...',
                            textvariable=self.btReceber,
                            cursor='hand2',
                            bg='#676AA9',
                            fg='#ffffff',
                            font=('Poppins', 20),
                            command=lambda:self.executa_calculos())

        self.btReceber.set('Aguardando Analise...')

        self.bt_pesquisa_sku = Button(self.root,
                            # text='Pesquisar',
                            cursor='hand2',
                            # font=('Poppins', 10),
                            image=self.imagem_pesquisa,
                            bg='#ffffff',
                            compound=LEFT,
                            justify='left',
                            border=False,
                            command=lambda:self.procura_produto(self.numSku.get()))

        self.bt_receber.place(x=62, y=335,width=1328, height=50)
        self.bt_pesquisa_sku.place(x=281, y=83,width=60, height=40)

        #campo de texto
        self.txt_produto = Entry(self.root,
                                font=('Poppins', 20), 
                                textvariable=self.numSku)

        self.txt_produto.place(x=60, y=79,width=197,height=43)
        self.numSku.set('')
        self.lista_valida_comp_tela_inicial.append(self.txt_produto)

        #label
        self.dta_recebimento = StringVar()
        self.rec_minimo = StringVar()
        self.alerta_comercial = StringVar()
        self.descri_produto = StringVar()
        self.categoria = StringVar()
        self.l_usuario = StringVar()
        self.l_matricula = StringVar()
        self.msg = StringVar()

        self.l_usuario.set(self.formata_nome_usuario(self.info_usuario['usuario']))
        self.l_matricula.set(self.info_usuario['matricula'])


        self.lb_rec_minimo = Label(self.root,
                                  textvariable=self.rec_minimo,
                                  font=('Poppins', 20),
                                  justify='center')

        self.lb_alerta_comercial = Label(self.root,
                                        textvariable=self.alerta_comercial,
                                        font=('Poppins', 20),
                                        justify='center')

        self.lb_descri_produto = Label(self.root,
                                        textvariable=self.descri_produto,
                                        font=('Poppins', 15),
                                        justify='left')

        self.lb_categoria = Label(self.root,
                                    textvariable=self.categoria,
                                    font=('Poppins', 15),
                                    justify='center')

        self.lb_dta_recebimento =Label(self.root,
                                        text=self.convert_data_str(self.data_recebimento),
                                        font=('Poppins', 30),
                                        justify='center',
                                        bg='#ffffff')

        self.lb_usuario =Label(self.root,

                                font=('Poppins', 12),  
                                # justify='left',
                                compound=LEFT,
                                bg='#ffffff',
                                textvariable=self.l_usuario)

        self.lb_matricula =Label(self.root,
                                    text="Matricula: " + self.matricula_logado, 
                                    font=('Poppins', 15), 
                                    justify='center',
                                    bg='#ffffff',
                                    textvariable=self.l_matricula)

        self.lb_msg =Label(self.root,
                            textvariable=self.msg, 
                            font=('Poppins', 27),  
                            justify='center',
                            bg="#ffffff")



        self.lb_rec_minimo.place(x=740, y=263, width=307, height=43)
        self.lb_alerta_comercial.place(x=1081, y=263, width=307, height=43)
        self.lb_descri_produto.place(x=60, y=171, width=680, height=43)
        self.lb_categoria.place(x=770, y=171, width=288, height=43)
        self.lb_dta_recebimento.place(x=1167, y=122,width=211, height=39)
        self.lb_usuario.place(x=1212, y=77, width=164, height=26)
        # self.lb_matricula.place(x=1179, y=99, width=251, height=37)
        self.lb_msg.place(x=345, y=80, width=554, height=43)

        #tabela
        colunas = [
                    'id',
                    'usuario',
                    'produto',
                    'descricao',
                    'data_fabricacao',
                    'data_vencimento',
                    'data_min_rec',
                    'alerta_comercial',
                    'descri_status',
                    'status_de_recebimento'

        ]
        self.tr_scroll_inicial = Scrollbar(self.root)
        self.tr_vw = ttk.Treeview(self.root,columns=colunas, show='headings',yscrollcommand=self.tr_scroll_inicial.set)
        self.tr_scroll_inicial.config(command=self.tr_vw.yview)

        self.tr_vw.column('id', width=0)
        self.tr_vw.column('usuario', width=25)
        self.tr_vw.column('produto', width=25)
        self.tr_vw.column('descricao', width=225)
        self.tr_vw.column('data_fabricacao', width=25)
        self.tr_vw.column('data_vencimento', width=25)
        self.tr_vw.column('data_min_rec', width=25)
        self.tr_vw.column('alerta_comercial', width=25)
        self.tr_vw.column('descri_status', width=100)
        self.tr_vw.column('status_de_recebimento', width=25)


        self.tr_vw.heading('id',text= 'ID')
        self.tr_vw.heading('usuario',text= 'USUARIO')
        self.tr_vw.heading('produto',text= 'PRODUTO')
        self.tr_vw.heading('descricao',text= 'DESCRI????O')
        self.tr_vw.heading('data_fabricacao',text= 'FABRICA????O')
        self.tr_vw.heading('data_vencimento',text= 'VENCIMENTO')
        self.tr_vw.heading('data_min_rec',text= 'MIN_REC')
        self.tr_vw.heading('alerta_comercial',text= 'ALERTA_COMERCIAL')
        self.tr_vw.heading('descri_status',text= 'DESCRI_STATUS')
        self.tr_vw.heading('status_de_recebimento',text= 'STATUS')


        self.tr_vw.place(x=62, y=400, width=1299, height=323)
        self.tr_scroll_inicial.place(x=1361, y=400, width=25, height=323)

        self.select_dados_rec()
        self.style_treeview()

    def formata_nome_usuario(self, nome: str):

        if nome:
            separa_nome = nome.split(' ')
            primeiro_nome = separa_nome[0]
            ultimo_nome = separa_nome[-1]

            if primeiro_nome == ultimo_nome: return primeiro_nome

            nome_formatado = primeiro_nome + '.' + ultimo_nome

            return nome_formatado
        else:
            return 'DESCONHECIDO'

    def componentes_tela_config(self):
        self.destroi_widget()
        self.lista_campos()
        
        self.lb_img_config = Label(self.root,image=self.image_config)
        self.lb_img_config.place(x=0, y=0)
        self.componentes_menu_bar()

        # campos de entrada
        self.dir_bd = StringVar()
        # self.dir_pdf = StringVar()
        # self.dir_relatorio = StringVar()
        self.nome_pdf =StringVar()
        self.nome_relatorio = StringVar()



        self.txt_dir_bd = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.dir_bd,
                            )

        self.txt_nome_pdf = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.nome_pdf,
                            )

        self.txt_nome_relatorio = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.nome_relatorio,
                            )

        self.txt_dir_bd.place(x=70, y=186, width=826, height=30)
        self.txt_nome_pdf.place(x=70, y=265, width=826, height=30)
        self.txt_nome_relatorio.place(x=70, y=344, width=826, height=30)

        self.lista_valida_comp_config.append(self.txt_dir_bd)
        self.lista_valida_comp_config.append(self.txt_nome_pdf)
        self.lista_valida_comp_config.append(self.txt_nome_relatorio)



        #botoes de localiza pasta
        self.bd =StringVar()
        self.btn_dir_bd = Button(self.root,
                                text='...',
                                font=FONT_INIT,
                                justify='center',
                                command=lambda:self.define_diretorio('bd'),
                                )


        self.btn_dir_bd.place(x=915, y=186, width=55, height=30)


        #escala de valores
        self.scl_rec_minimo = IntVar()
        self.scl_alert_comercial = IntVar()

        self.sc_rec_minimo = Scale(self.root, 
                                    from_=5, to=100,
                                    variable=self.scl_rec_minimo, 
                                    orient='horizontal',
                                    resolution=5)

        self.sc_alert_comercial = Scale(self.root, 
                                        from_=5, to=100,
                                        variable=self.scl_alert_comercial, 
                                        orient='horizontal',
                                        resolution=5)
        
        self.ajd_rec_minimo = Label(self.root,
                                    text='?',
                                    font=('Poppins', 10))

        self.ajd_rec_minimo.bind('<Enter>',lambda e:self.widget_de_ajuda(1))
        self.ajd_rec_minimo.bind('<Leave>',lambda e:self.lb_image_ajuda.destroy())

        self.ajd_alert_comercial = Label(self.root,
                                        text='?',
                                        font=('Poppins', 10))

        self.ajd_alert_comercial.bind('<Enter>',lambda e:self.widget_de_ajuda(2))
        self.ajd_alert_comercial.bind('<Leave>',lambda e:self.lb_image_ajuda.destroy())

        self.sc_rec_minimo.place(x=70, y=532, width=826, height=30)
        self.sc_alert_comercial.place(x=70, y=618, width=826, height=30)

        self.ajd_rec_minimo.place(x=408, y=512, width=13, height=13)
        self.ajd_alert_comercial.place(x=360, y=598, width=13, height=13)

        self.salva_config = StringVar()
        self.cancelar_config = StringVar()

        self.btn_salva_config = Button(self.root,
                        text='SALVAR',
                        font=FONT_INIT,
                        justify='center',
                        command=lambda:self.atualiza_dados_config()
                        )

        self.btn_cancelar_config = Button(self.root,
                        text='CANCELAR',
                        font=FONT_INIT,
                        justify='center',
                        # textvariable=self.cancelar_config,
                        )
        

        self.btn_salva_config.place(x=1250, y=690, width=140, height=30)
        self.btn_cancelar_config.place(x=1073, y=690, width=140, height=30)

        self.carrega_dados_config()

        self.scl_alert_comercial.set(self.valor_ale_comercial)
        self.scl_rec_minimo.set(self.valor_rec_minimo)


        self.nome_relatorio.set(self.nome_rel)
        self.nome_pdf.set(self.nome_saida_pdf)
        self.dir_bd.set(self.diretorio_bd)

        if self.info_usuario['acesso'] == 'NIVEL 1':
            self.sc_alert_comercial.config(state='disabled')
            self.sc_rec_minimo.config(state='disabled')
            self.txt_dir_bd.config(state='disabled')
            self.btn_dir_bd.config(state='disabled')

    def componentes_menu_bar(self):

        self.menubar = Menu(self.root,tearoff=False)
        self.menu = Menu(self.menubar,tearoff=False)
        self.menuBd = Menu(self.menubar,tearoff=False)
        self.menuSair = Menu(self.menubar,tearoff=False)

        self.menubar.add_command(label='Inicio',command=self.componentes_tela_inicial)
        self.menubar.add_command(label='Configura????es',command=self.componentes_tela_config)
        self.menubar.add_command(label='Relat??rio',command=self.componentes_historico)

        self.menubar.add_cascade(label='Banco', menu=self.menuBd,)
        self.menuBd.add_command(label='Produtos', command=self.componentes_produtos)
        self.menuBd.add_command(label='Usuario', command=lambda:self.componentes_usuarios(nivelAcesso=self.info_usuario['acesso']))

        self.menubar.add_cascade(label='Sair', menu=self.menuSair,)
        self.menuSair.add_command(label='Logoff', command=self.logoff)
        self.menuSair.add_command(label='Fechar Aplica????o', command=lambda:self.root.destroy())

        self.root.config(menu=self.menubar)

    def componentes_login_usuario(self):
        self.destroi_widget()
        
        self.lb_img_login = Label(self.root,image=self.image_login)
        self.lb_img_login.place(x=0, y=0)
       
        self.lg_usuario = IntVar()
        self.lg_senha = StringVar()
        self.txt_usuario = Entry(self.root,
                                font=('Poppins', 25),
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                validate='key',
                                validatecommand=self.campo_matricula,
                                textvariable=self.lg_usuario)

        self.txt_senha = Entry(self.root,
                                font=('Poppins', 25),
                                show='???',
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                textvariable=self.lg_senha)

        self.txt_usuario.place(x=930, y=350, width=393, height=45)
        self.txt_senha.place(x=930, y=462, width=393, height=45)
        self.lg_usuario.set('')

        self.btn_entrar = Button(self.root,
                                 text='Entrar',
                                 bg=BT_COLOR,
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 activebackground=BT_COLOR,
                                 border=False,
                                 font=('Poppins', 25),
                                 command=lambda:self.logar_usuario(2))

        self.btn_entrar.place(x=978, y=586, width=243, height=51)

    def componentes_cadastro_usuario(self):
        self.destroi_widget()     
        
        self.lb_cad_login = Label(self.root,image=self.image_cad_login)
        self.lb_cad_login.place(x=0, y=0)
       
        self.lg_cad_usuario = IntVar()
        self.lg_cad_senha = StringVar()
        self.lg_rept_senha = StringVar()

        self.txt_cad_usuario = Entry(self.root,
                                font=('Poppins', 25),
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                validate='key',
                                validatecommand=self.campo_matricula,
                                textvariable=self.lg_cad_usuario)

        self.txt_cad_senha = Entry(self.root,
                                font=('Poppins', 25),
                                show='???',
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                textvariable=self.lg_cad_senha)

        self.txt_rept_senha = Entry(self.root,
                                font=('Poppins', 25),
                                show='???',
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                textvariable=self.lg_rept_senha)

        self.txt_cad_usuario.place(x=953, y=286, width=352, height=43)
        self.txt_cad_senha.place(x=953, y=392, width=352, height=43)
        self.txt_rept_senha.place(x=953, y=503, width=352, height=43)
        self.lg_cad_usuario.set('')

        self.btn_cad_entrar = Button(self.root,
                                 text='ALTERAR',
                                 bg=BT_COLOR,
                                 activebackground=BT_COLOR,
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 border=False,
                                 font=('Poppins', 25),
                                 command=lambda:self.logar_usuario(1))
        
        self.btn_cad_entrar.place(x=983, y=590, width=230, height=40)
        
    def componentes_historico(self):
        self.destroi_widget()
        self.lista_campos()
        data_rec = datetime.strftime(self.data_recebimento,'%d/%m/%Y')

        self.componentes_menu_bar()
        lb_image = Label(self.root,image=self.imagem_historico)
        lb_image.place(x=0, y=0)
       #label data

        self.relogio_h = Label(self.root, font=FONT_INIT)
        self.relogio_h.place(x=683, y=92, width=169, height=43)
        self.relogio()

        self.dta_inicio = Entry(self.root,
                            font=('Poppins',20), 
                            justify='center')

        self.dta_inicio.bind('<1>', lambda e: self.calendario(self.dta_inicio))
        self.dta_inicio.insert(0, data_rec)

        self.dta_fim = Entry(self.root,
                            font=('Poppins',20), 
                            justify='center')

        self.dta_fim.insert(0, data_rec)
        self.dta_fim.bind('<1>', lambda e: self.calendario(self.dta_fim))

        self.dta_inicio.place(x=180, y=92, width=157, height=43)
        self.dta_fim.place(x=462, y=92, width=157, height=43)

        self.lista_valida_comp_historico.append(self.dta_inicio)
        self.lista_valida_comp_historico.append(self.dta_fim)

        self.bt_pesquisa_data = Button(self.root,
                            text='PESQUISAR',
                            cursor='hand2',
                            font=('Poppins', 15),
                            bg='#676AA9',
                            fg='#ffffff',
                            compound=LEFT,
                            justify='left',
                            border=False,
                            command=lambda:self.popular_tabela_historico(
                                        self.dta_inicio.get(),
                                        self.dta_fim.get()
                                        ))

        self.bt_delete_registro = Button(self.root,
                            text='DELETAR',
                            cursor='hand2',
                            font=('Poppins', 15),
                            bg='#676AA9',
                            fg='#ffffff',
                            compound=LEFT,
                            justify='left',
                            border=False,
                            command=lambda:self.deletar_registro_historico())

        self.bt_gera_pdf = Button(self.root,
                            cursor='hand2',
                            bg='#ffffff',
                            border=False,
                            image=self.imagem_ficha,
                            command=lambda:self.selecao_de_item_historico())
        


        self.bt_gera_rel = Button(self.root,
                            cursor='hand2',
                            bg='#ffffff',
                            border=False,
                            image=self.imagem_excel,
                            command=lambda:self.gerar_relatorio_rec(
                                    self.dta_inicio.get(),
                                    self.dta_fim.get()
                                    ))

        self.bt_pesquisa_data.place(x=683, y=92, width=169, height=43)
        self.bt_gera_pdf.place(x=1260, y=92, width=51, height=51)
        self.bt_gera_rel.place(x=1339, y=92, width=51, height=51)
        if self.info_usuario['acesso']=='NIVEL 2':
            self.bt_delete_registro.place(x=1033, y=92, width=169, height=43)


        #tabela
        colunas = [
                    'id',
                    'matricula',
                    'usuario',
                    'produto',
                    'descricao',
                    'categoria',
                    'data_recebimento',
                    'hora_recebimento',
                    'data_fabricacao',
                    'data_vencimento',
                    'data_min_rec',
                    'alerta_comercial',
                    'descri_status',
                    'status_de_recebimento'

        ]

        self.tr_scroll = Scrollbar(self.root)
        self.tr_vw_historico = ttk.Treeview(self.root, columns=colunas, show='headings',yscrollcommand=self.tr_scroll.set)
        self.tr_scroll.config(command=self.tr_vw_historico.yview)

        self.tr_vw_historico.column('id', width=1)
        self.tr_vw_historico.column('matricula', width=50)
        self.tr_vw_historico.column('usuario', width=25)
        self.tr_vw_historico.column('produto', width=25)
        self.tr_vw_historico.column('descricao', width=200)
        self.tr_vw_historico.column('categoria', width=50)
        self.tr_vw_historico.column('data_recebimento', width=50)
        self.tr_vw_historico.column('hora_recebimento', width=50)
        self.tr_vw_historico.column('data_fabricacao', width=50)
        self.tr_vw_historico.column('data_vencimento', width=50)
        self.tr_vw_historico.column('data_min_rec', width=50)
        self.tr_vw_historico.column('alerta_comercial', width=50)
        self.tr_vw_historico.column('descri_status', width=50)
        self.tr_vw_historico.column('status_de_recebimento', width=50)


        self.tr_vw_historico.heading('id',text= 'ID')
        self.tr_vw_historico.heading('matricula',text= 'MATRICULA')
        self.tr_vw_historico.heading('usuario',text= 'USUARIO')
        self.tr_vw_historico.heading('produto',text= 'PRODUTO')
        self.tr_vw_historico.heading('descricao',text= 'DESCRI????O')
        self.tr_vw_historico.heading('categoria',text= 'CATEGORIA')
        self.tr_vw_historico.heading('data_recebimento',text= 'DATA_RECEBIMENTO')
        self.tr_vw_historico.heading('hora_recebimento',text= 'HORA_RECEBIMENTO')
        self.tr_vw_historico.heading('data_fabricacao',text= 'FABRICA????O')
        self.tr_vw_historico.heading('data_vencimento',text= 'VENCIMENTO')
        self.tr_vw_historico.heading('data_min_rec',text= 'MIN_REC')
        self.tr_vw_historico.heading('alerta_comercial',text= 'ALERTA_COMERCIAL')
        self.tr_vw_historico.heading('descri_status',text= 'DESCRI_STATUS')
        self.tr_vw_historico.heading('status_de_recebimento',text= 'STATUS_RECEBIMENTO')

        self.tr_vw_historico.place(x=62, y=171, width=1303, height=552)
        self.tr_scroll.place(x=1365, y=171, width=25, height=552)
        
        self.popular_tabela_historico(data_rec, data_rec)

        self.style_treeview()

    def componentes_produtos(self):
        self.destroi_widget()
        self.lista_valida_comp_produtos = []
        bd =DataBase(2)
        sql="SELECT categoria FROM tb_categoria ORDER BY categoria ASC"
        lista = bd.selectAll(sql)
        nova_lista = [item[0] for item in lista]
        

        self.componentes_menu_bar()

        
        lb_image = Label(self.root,image=self.imagem_produtos)
        lb_image.place(x=0, y=0)

        self.id_produto = ''
        self.txt_cd_produto = Entry(self.root,
                                    font=FONT_INIT

                                    
        )

        self.txt_cd_descri_produto = Entry(self.root,
                                    font=FONT_INIT
 
                                    
        )
        
        self.cbx_cd_categoria_produto = ttk.Combobox(self.root,
                                                     font= FONT_INIT,
                                                     values=nova_lista
                                                     
                                                            
        )

        self.ajd_massivo = Label(self.root,
                                        text='?',
                                        font=('Poppins', 10))

        self.ajd_massivo.bind('<Enter>',lambda e:self.widget_de_ajuda(3))
        self.ajd_massivo.bind('<Leave>',lambda e:self.lb_image_ajuda.destroy())

        self.ajd_massivo.place(x=244, y=393, width=13, height=13)
       
        self.lista_valida_comp_produtos.append(self.txt_cd_produto)
        self.lista_valida_comp_produtos.append(self.txt_cd_descri_produto)
        self.lista_valida_comp_produtos.append(self.cbx_cd_categoria_produto)

        self.cbx_cd_filtro = ttk.Combobox(self.root,
                                         font= FONT_INIT,
                                         values=['PRODUTO','DESCRI????O','CATEGORIA']
                                        
                                                           
        )

        self.txt_campo_pesquisa = Entry(self.root,
                                    font=FONT_INIT,

                                    
        )

        self.txtArea_produtos = Text(self.root, font=FONT_INIT_TXT_AREA, wrap='word')


        self.txt_cd_produto.place(x=61, y=145, width=197, height=43)
        self.txt_cd_descri_produto.place(x=61, y=230, width=632, height=43)
        self.cbx_cd_categoria_produto.place(x=61, y=314, width=290, height=43)
        self.txt_campo_pesquisa.place(x=776, y=224, width=500, height=43)
        self.cbx_cd_filtro.place(x=777, y=140, width=253, height=43)
        self.txtArea_produtos.place(x=61, y=420, width=632, height=211)

        self.btn_inserir = Button(self.root,
                                 text='INSERIR', 
                                 font=FONT_INIT, 
                                 bg='#676AA9', 
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 command=lambda:self.insert_produtos()

                                  )

        self.btn_update = Button(self.root,
                                 text='ATUALIZAR', 
                                 font=FONT_INIT, 
                                 bg='#676AA9', 
                                 fg='#ffffff',
                                 justify='center',
                                  cursor='hand2',
                                  command=lambda:self.update_produtos()
                                  )

        self.btn_delete = Button(self.root,
                                 text='DELETAR', 
                                 font=FONT_INIT, 
                                 fg='#ffffff',
                                 bg='#676AA9', 
                                 justify='center',
                                  cursor='hand2',
                                  command=lambda:self.delete_produtos()
                                  )
        self.btn_filtro_produto = Button(self.root,
                                 text='FILTRO', 
                                 font=FONT_INIT_TXT_AREA, 
                                 fg='#ffffff',
                                 bg='#676AA9', 
                                 justify='center',
                                  cursor='hand2',
                                  command=lambda:self.filtro_dados_produtos()
                                  )


        self.btn_inserir.place(x=75, y=665, width=169, height=51)
        self.btn_update.place(x=279, y=665, width=169, height=51)
        self.btn_delete.place(x=483, y=665, width=169, height=51)
        self.btn_filtro_produto.place(x=1305, y=225, width=70, height=43)

        self.scroll_produtos = Scrollbar(self.root)
        self.tr_vw_produtos = ttk.Treeview(self.root,
                                                    columns=['id','produto','descri????o','categoria'],
                                                    show='headings',
                                                    yscrollcommand=self.scroll_produtos.set)

        self.scroll_produtos.config(command=self.tr_vw_produtos.yview)
        self.tr_vw_produtos.bind('<Double-1>', self.duplo_click_tabela_produtos)

        self.tr_vw_produtos.column('id', width=1)
        self.tr_vw_produtos.column('produto', width=70)
        self.tr_vw_produtos.column('descri????o', width=330)
        self.tr_vw_produtos.column('categoria', width=100)

        self.tr_vw_produtos.heading('id',text='')
        self.tr_vw_produtos.heading('produto',text='PRODUTO')
        self.tr_vw_produtos.heading('descri????o',text='DESCRI????O')
        self.tr_vw_produtos.heading('categoria',text='CATEGORIA')

        self.tr_vw_produtos.place(x=777, y=333, width=557, height=383)
        self.scroll_produtos.place(x=1335, y=333, width=28, height=383)

        self.style_treeview()
        self.popular_tabela_produtos()

        if self.info_usuario['acesso'] == 'NIVEL 1':
            self.btn_inserir.config(state='disabled')
            self.btn_update.config(state='disabled')
            self.btn_delete.config(state='disabled')

    def componentes_usuarios(self, primeiro_acesso:bool = True, nivelAcesso: str = 'NIVEL 2'):
        self.destroi_widget()
        self.lista_valida_comp_usuario = []
        if primeiro_acesso:
            self.componentes_menu_bar()


        lb_image = Label(self.root,image=self.imagem_usuarios)
        lb_image.place(x=0, y=0)


        self.var_matricula = StringVar()
        self.var_nome_usu = StringVar()
        self.var_cargo = StringVar()
        self.var_setor = StringVar()
        self.var_nivel_acesso = StringVar()
        self.var_senha = StringVar()

        self.txt_matricula = Entry(self.root, 
                                    font=FONT_INIT, 
                                    validate='key',
                                    validatecommand=self.campo_matricula,
                                    textvariable=self.var_matricula)

        self.txt_nome_usu = Entry(self.root, 
                                    font=FONT_INIT, 
                                    textvariable=self.var_nome_usu)

        lista_cargo =  ['CONFERENTE', 'ASSIS ADM', 'SUPERVISOR', 'COORDENADOR', 'OPERADOR', 'OUTROS']
        self.cb_cargo = ttk.Combobox(self.root,
                                    values=lista_cargo, 
                                    state='readonly',
                                    font=FONT_INIT, 
                                    textvariable=self.var_cargo)

        lista_setor =  ['RECEBIMENTO', 'ARMAZENAGEM', 'QUALIDADE', 'PICKING', 'PACKING', 'EXPEDI????O', 'INSUCESSO', 'OUTROS']
        self.cb_setor = ttk.Combobox(self.root,
                                        values=lista_setor, 
                                        font=FONT_INIT,
                                        state='readonly',
                                        textvariable=self.var_setor)

        lista_acesso = ['NIVEL 1', 'NIVEL 2']
        self.cb_nivel_acesso = ttk.Combobox(self.root,
                                            values=lista_acesso, 
                                            font=FONT_INIT,
                                            state='readonly',
                                            textvariable=self.var_nivel_acesso)

        self.lb_senha = Entry(self.root,
                                font=FONT_INIT,
                                justify='center',
                                show='???',
                                textvariable=self.var_senha)

        self.lista_valida_comp_usuario.append(self.txt_matricula)
        self.lista_valida_comp_usuario.append(self.txt_nome_usu)
        self.lista_valida_comp_usuario.append(self.cb_cargo)
        self.lista_valida_comp_usuario.append(self.cb_setor)
        self.lista_valida_comp_usuario.append(self.cb_nivel_acesso)
        self.lista_valida_comp_usuario.append(self.lb_senha)

        self.cb_cargo.set('')
        self.cb_setor.set('')
        self.cb_nivel_acesso.set('')

        self.txt_matricula.place(x=68, y=150, width=197, height=43)
        self.txt_nome_usu.place(x=68, y=243, width=680, height=43)
        self.cb_cargo.place(x=68, y=327, width=680, height=43)
        self.cb_setor.place(x=68, y=412, width=680, height=43)
        self.cb_nivel_acesso.place(x=68, y=497, width=215, height=43)
        self.lb_senha.place(x=316, y=497, width=215, height=43)

        if not primeiro_acesso:
                self.var_senha.set(self.nova_senha)
                self.var_matricula.set(self.novo_matricula)
                self.cb_nivel_acesso.set('NIVEL 2')
                self.cb_nivel_acesso.config(state='readonly')


        if primeiro_acesso:
            self.btn_inserir_usu =Button(self.root,
                                    text='INSERIR', 
                                    font=FONT_INIT, 
                                    bg='#676AA9', 
                                    fg='#ffffff',
                                    justify='center',
                                    cursor='hand2',
                                    command=lambda:self.inserir_usuario()

                                    )
        else:
            self.btn_inserir_usu =Button(self.root,
                                    text='INSERIR', 
                                    font=FONT_INIT, 
                                    bg='#676AA9', 
                                    fg='#ffffff',
                                    justify='center',
                                    cursor='hand2',
                                    command=lambda:self.inserir_primeiro_usuario()

                                    )

        self.btn_delete_usu =Button(self.root,
                                 text='DELETAR', 
                                 font=FONT_INIT, 
                                 bg='#676AA9', 
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 command=lambda:self.deleta_usuario()

                                  )

        self.btn_update_usu =Button(self.root,
                                 text='ATUALIZAR', 
                                 font=FONT_INIT, 
                                 bg='#676AA9', 
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 command=lambda:self.atualiza_usuario()

                                  )

        self.btn_reset_senha =Button(self.root,
                                 text='Resetar Senha', 
                                 font=FONT_INIT_TXT_AREA, 
                                 bg='#676AA9', 
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 command=lambda:self.resetar_senha_usuario()

                                  )

        self.btn_ver_senha =Button(self.root,
                                 image=self.imagem_v_senha,
                                 bg='#ffffff', 
                                 justify='center',
                                 cursor='hand2',
                                 border=False,
                                 command=lambda:self.mostra_senha(self.lb_senha)

                                  )


        self.btn_inserir_usu.place(x=94, y=627, width=169, height=51)
        self.btn_delete_usu.place(x=298, y=627, width=169, height=51)
        self.btn_update_usu.place(x=502, y=627, width=169, height=51)
        self.btn_reset_senha.place(x=602, y=497, width=146, height=45)
        self.btn_ver_senha.place(x=536, y=497, width=50, height=43)

        if not primeiro_acesso:
            self.btn_delete_usu.config(state='disabled')
            self.btn_update_usu.config(state='disabled')
            self.btn_reset_senha.config(state='disabled')
            

        if primeiro_acesso:
            self.scroll_usu = Scrollbar(self.root)
            self.tr_vw_usuarios = ttk.Treeview(self.root,
                                                columns=['id','usuario', 'cargo', 'nivel_acesso'], 
                                                show='headings', 
                                                yscrollcommand=self.scroll_usu.set)

            self.tr_vw_usuarios.bind('<Double-1>', self.duplo_click_tabela_usuarios)
            self.scroll_usu.config(command=self.tr_vw_usuarios.yview)

            self.tr_vw_usuarios.column('id',width=0)
            self.tr_vw_usuarios.column('usuario',width=300)
            self.tr_vw_usuarios.column('cargo',width=100)
            self.tr_vw_usuarios.column('nivel_acesso',width=100)

            self.tr_vw_usuarios.heading('id', text='ID')
            self.tr_vw_usuarios.heading('usuario', text='USUARIO')
            self.tr_vw_usuarios.heading('cargo', text='CARGO')
            self.tr_vw_usuarios.heading('nivel_acesso', text='NIVEL_ACESSO')

            self.tr_vw_usuarios.place(x=791, y=122, width=568, height=599)
            self.scroll_usu.place(x=1360, y=123, width=29, height=599)
            
            self.style_treeview()
            self.popular_tabela_usuario()
        
        if nivelAcesso == 'NIVEL 1':
            self.btn_inserir_usu.config(state='disabled')
            self.btn_delete_usu.config(state='disabled')
            self.btn_reset_senha.config(state='disabled')

            valores = self.select_usuario(self.info_usuario['id'])
            self.popular_tabela_usuario(valores)
            
    def componentes_primeiro_acesso(self):
        self.destroi_widget()
        
        lb_image = Label(self.root,image=self.imagem_acesso)
        lb_image.place(x=0, y=0)

        self.btn_primeiro_acesso = Button(self.root, 
                                            text='Clique aqui', 
                                            bg="#ffffff",
                                            fg=BT_COLOR,
                                            border=False,
                                            cursor='hand2',
                                            activebackground="#ffffff",
                                            activeforeground=BT_COLOR,
                                            font=('Poppins', 40, 'bold'),
                                            command=lambda:self.primeiro_acesso())

        self.btn_login_acesso = Button(self.root, 
                                            text='Clique aqui', 
                                            bg=BT_COLOR,
                                            fg='#FFFFFF',
                                            border=False,
                                            cursor='hand2',
                                            activebackground=BT_COLOR,
                                            activeforeground='#ffffff',
                                            font=('Poppins', 40, 'bold'),
                                            command=lambda:self.primeiro_login_acesso())

        self.btn_primeiro_acesso.place(x=220, y=403, width=300, height=110)
        self.btn_login_acesso.place(x=952, y=403, width=300, height=110)

    def inserir_produto_massivo(self, dados: str):

        # dados = self.txtArea_produtos.get("1.0","end - 1c")
        lista_final: list = []
        erros: list = []
        lista_dados = dados.split(',')
        # import ipdb; ipdb.set_trace()
        if lista_dados:
            for registro in lista_dados:
                n_registro = registro
                if registro != '':

                    if '\n' in registro:
                        registro = registro.strip('\n')
                    try:
                        produto, descri, careg = registro.split(';')
                        dados = (None, produto, descri, careg.upper())

                        lista_final.append(dados)
                        dados = ()
                    except ValueError as error:
                        print(n_registro)
                        erros.append(n_registro)
                        dados = ()

            self.insert_produto(lista_final)
            self.txtArea_produtos.delete("1.0","end - 1c")
            if erros:
                [self.txtArea_produtos.insert(END, erro) for erro in erros]
                # self.txtArea_produtos.insert(END, erro)
                messagebox.showerror('Erro dados', 'Dados com formato incorreto, verifique e tente novamente.')
                  
    def insert_produto(self, listaDados: list):
        if len(listaDados)> 0:
            try:
                bd = DataBase(2)
                sql = f'INSERT INTO tb_produtos VALUES (?, ?, ?, ?)'
                bd.insert(sql, listaDados)
                messagebox.showinfo('Inser????o','Dados inseridos com sucesso')
            except:
                messagebox.showerror('Inser????o','N??o foi possivel inserir os dados, verifique e tente novamente.')


    def tela(self):
        self.root.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))

        if self.validando_primeiro_acesso():
            try:
                self.componentes_primeiro_acesso()
                self.info_usuario['acesso'] = 'NIVEL 2'
                bd = DataBase(1)
                sql ="""UPDATE tb_primeiro_acesso SET valor = 1 WHERE id = 1"""
                bd.update(sql)
            except:
                messagebox.showerror('Erro Cadastro', 'Ocorreu um erro no cadastro!\nVerifique e tente novamente')
                bd = DataBase(1)
                sql ="""UPDATE tb_primeiro_acesso SET valor = 0 WHERE id = 1"""
                bd.update(sql)

        else:
            self.componentes_login_usuario()



    def insere_registros_rec(self):
        self.variaveis_tela_inicial()
        lista_dados = []

        dados = (
                None,
                self.matricula_v,
                self.usuario_v,
                self.numSku_v,
                self.descri_produto_v,
                self.rec_minimo_v,
                self.alerta_comercial_v,
                self.receber_v,
                self.dta_fab_v,
                self.dta_venc_v,
                self.dta_recebimento_v,
                self.hra_recebimento_v,
                self.status_recebimento,
                self.categoria_v,
                self.valor_rec_minimo,
                self.valor_ale_comercial
            )

        lista_dados.append(dados)
        sql = """INSERT INTO tb_dataBase VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        bd = DataBase(2)
        bd.insert(sql, lista_dados)

    def select_dados_rec(self):
        self.tr_vw.delete(*self.tr_vw.get_children())
        bd = DataBase(2)
        sql =""" SELECT 
                    id,
                    conferente,
                    produto,
                    descricao,
                    data_fabricacao,
                    data_vencimento,
                    data_min_rec,
                    alerta_comercial,
                    descri_status,
                    status_de_recebimento
                FROM tb_dataBase WHERE data_recebimento = '{}' ORDER BY id DESC """.format(datetime.now().date())

        dados_rec = bd.selectAll(sql)
        for dados in dados_rec:
            self.tr_vw.insert('','end',values=dados)

    def select_dados_historico(self,dta_inicio:date, dta_fim: date):
        
        try:
            bd = DataBase(2)
            sql =""" SELECT 
                        id,
                        matricula,
                        conferente,
                        produto,
                        descricao,
                        categoria,
                        data_recebimento,
                        hora_recebimento,
                        data_fabricacao,
                        data_vencimento,
                        data_min_rec,
                        alerta_comercial,
                        descri_status,
                        status_de_recebimento,
                        percent_rec_minimo,
                        percent_ale_comercial            
                    FROM tb_dataBase WHERE data_recebimento BETWEEN '{}' AND '{}' ORDER BY id DESC """.format(dta_inicio, dta_fim)

            self.dados_rec = bd.selectAll(sql)
            return self.dados_rec
        except:
            messagebox.showerror('Erro de dados','N??o foi possivel carregar os dados')
            return

    def select_dados_produtos(self, sqlString:str =''):
        if sqlString:
            sql = sqlString
        else:
            sql =""" SELECT 
                id,
                produto,
                descricao,
                categoria 
            FROM tb_produtos ORDER BY id DESC """

        
        try:
            bd = DataBase(2)
            self.dados_produtos = bd.selectAll(sql)
            return self.dados_produtos
        except:
            messagebox.showerror('Erro de dados','N??o foi possivel carregar os dados do produto')
            return
            
    def popular_tabela_historico(self,dtaInicio:date, dtaFim: date):
            if isstring(dtaInicio) :
                dta_inicio = datetime.strptime(dtaInicio,'%d/%m/%Y').date()
                dtaInicio = datetime.strftime(dta_inicio,'%Y-%m-%d')
                dta_fim = datetime.strptime(dtaFim,'%d/%m/%Y').date()
                dtaFim = datetime.strftime(dta_fim,'%Y-%m-%d')
            

            if self.valida_campos_vazios(self.lista_valida_comp_historico):
                dados_rec = self.select_dados_historico(dta_inicio, dta_fim)
                self.tr_vw_historico.delete(*self.tr_vw_historico.get_children())
                try:
                    for dados in dados_rec:
                        self.tr_vw_historico.insert('','end',values=dados)
                except:
                    pass

    def deletar_registro_historico(self):
        if self.valida_campos_vazios(self.lista_valida_comp_historico):
            self.tr_vw_historico.selection()
            lista = [self.tr_vw_historico.item(n, 'values') for n in self.tr_vw_historico.selection()]
            id = lista[0][0]
            opc = messagebox.askyesnocancel('Deletar Registro',F'Confirmar exclus??o do registro?')

            if opc:
                sql = """DELETE FROM tb_dataBase WHERE id = {}""".format(id)
                bd = DataBase(2)
                bd.delete(sql)
                self.popular_tabela_historico(
                                        datetime.strptime(self.dta_inicio.get(),'%Y-%m-%d').date(),
                                         datetime.strptime(self.dta_fim.get(),'%Y-%m-%d').date())
            


    def popular_tabela_produtos(self, lista_dados:list =[]):
        if lista_dados:
            dados_prod = lista_dados
        else:
            dados_prod = self.select_dados_produtos()

        self.tr_vw_produtos.delete(*self.tr_vw_produtos.get_children())
        try:
            for dados in dados_prod:
                self.tr_vw_produtos.insert('','end',values=dados)
        except:
            pass

    def selecao_de_item_historico(self):
            try:
                item = self.tr_vw_historico.selection()[0]
                valores = self.tr_vw_historico.item(item,'values')
                # import ipdb;ipdb.set_trace()
                gerarPdf = Relatorios(
                                        numSku = valores[3],
                                        descri_produto = valores[4],
                                        categoria = valores[5],
                                        dta_fab = valores[8],
                                        dta_venc = valores[9],
                                        rec_minimo = valores[10],
                                        alerta_comercial = valores[11],
                                        dta_recebimento = valores[6],
                                        usuario = valores[2],
                                        matricula = valores[1],
                                        nome_arquivo = self.nome_saida_pdf

                )
                gerarPdf.gerar_relatorio()    

            except TypeError as err:
                messagebox.showwarning('Itens',f'Nenhum item foi selecionado!\n\n{err}')

    def selecao_item_produto(self) -> list:
        item = self.tr_vw_produtos.selection()[0]
        valores = self.tr_vw_produtos.item(item,'values')
        return valores
        
    #========configura????es============
    def select_dados_config(self,sql:str, numDataBase: int):
        try:
            bd = DataBase(numDataBase)
            config = bd.selectAll(sql)
            return config
        except:
            messagebox.showerror('Erro Banco', 'N??o foi possivel carregar os dados...\nVerifique e tente novamente.')
            return

    def carrega_dados_config(self):

        try:
            sql = """SELECT * FROM tb_config WHERE id = 1"""
            config1 =self.select_dados_config(sql, 1)

            self.nome_rel = config1[0][3]
            self.nome_saida_pdf = config1[0][2]
            self.diretorio_bd = config1[0][1]

            # self.nome_relatorio.set(config1[0][3])
            # self.nome_pdf.set(config1[0][2])
            # self.dir_bd.set(config1[0][1])

        except:
            pass
        try:

            sql = """SELECT * FROM tb_periodo_rec WHERE id = 1"""
            config2 =self.select_dados_config(sql, 2)

            self.valor_ale_comercial = config2[0][2]
            self.valor_rec_minimo = config2[0][1]

            # self.scl_alert_comercial.set(config2[0][2])
            # self.scl_rec_minimo.set(config2[0][1])

        except:
            pass

    def atualiza_dados_config(self, lista_acesso = []):
            if len(lista_acesso)> 0:
                nome_relatorio = lista_acesso[0]
                nome_pdf = lista_acesso[1]
                dir_bd = lista_acesso[2]    
                scl_rec_minimo = lista_acesso[3]
                scl_alert_comercial = lista_acesso[4]

                if self.valida_campos_vazios(self.lista_valida_comp_config) or len(lista_acesso)> 0:
                    sql = """UPDATE tb_config SET dir_bd = '{}', nome_pdf = '{}', nome_rel = '{}' WHERE id = 1
                            """.format(dir_bd, nome_pdf, nome_relatorio)
                    bd = DataBase(1)
                    bd.update(sql)

                # if scl_rec_minimo <= scl_alert_comercial:
                #     messagebox.showwarning('Erro de Periodo','Recebimento minimo menor que alerta Comercial.')
                # elif scl_rec_minimo == 0 or scl_alert_comercial == 0:
                #     messagebox.showwarning('Erro de Periodo','Defina valores Maiores que 0.')
                # else:
                #     sql2 = """UPDATE tb_periodo_rec SET r_minimo = {}, a_comercial = {} WHERE id = 1""".format(scl_rec_minimo, scl_alert_comercial)
                #     bd = DataBase(2)
                #     bd.update(sql2)
            else:

                nome_relatorio = self.nome_relatorio.get()
                nome_pdf = self.nome_pdf.get()
                dir_bd = self.dir_bd.get()    
                scl_alert_comercial = self.scl_alert_comercial.get()
                scl_rec_minimo = self.scl_rec_minimo.get()

                if self.valida_campos_vazios(self.lista_valida_comp_config) or len(lista_acesso)> 0:
                    sql = """UPDATE tb_config SET dir_bd = '{}', nome_pdf = '{}', nome_rel = '{}' WHERE id = 1
                            """.format(dir_bd, nome_pdf, nome_relatorio)
                    bd = DataBase(1)
                    bd.update(sql)

                if scl_rec_minimo <= scl_alert_comercial:
                    messagebox.showwarning('Erro de Periodo','Recebimento minimo menor que alerta Comercial.')
                elif scl_rec_minimo == 0 or scl_alert_comercial == 0:
                    messagebox.showwarning('Erro de Periodo','Defina valores Maiores que 0.')
                else:
                    sql2 = """UPDATE tb_periodo_rec SET r_minimo = {}, a_comercial = {} WHERE id = 1""".format(scl_rec_minimo, scl_alert_comercial)
                    bd = DataBase(2)
                    bd.update(sql2)

            self.carrega_dados_config()

    def gerar_relatorio_rec(self, dtaInicio: date, dtaFim: date):

        if isstring(dtaInicio) :
            dta_inicio = datetime.strptime(dtaInicio,'%d/%m/%Y').date()
            dtaInicio = datetime.strftime(dta_inicio,'%Y-%m-%d')
            dta_fim = datetime.strptime(dtaFim,'%d/%m/%Y').date()
            dtaFim = datetime.strftime(dta_fim,'%Y-%m-%d')


        database = self.select_dados_historico(dtaInicio, dtaFim)
        dados = pd.DataFrame(data=database)
        dados.columns = [
                        'ID','MATRICULA','USUARIO','PRODUTO','DESCRI????O','CATEGORIA','DATA_RECEBIMENTO',
                         'HORA_RECEBIMENTO','DATA_FABRICA????O','DATA_VENCIMENTO','DATA_MIN_REC', 'ALERTA_COMERCIAL',
                         'DESCRI_STATUS','STATUS_RECEBIMENTO','PERCENT_REC_MINIMO','PERCENT_ALE_COMERCIAL'
                        ]
        colunas_datas= ['DATA_MIN_REC','ALERTA_COMERCIAL','DATA_FABRICA????O','DATA_VENCIMENTO','DATA_RECEBIMENTO']
        
        dados[colunas_datas] = dados[colunas_datas].astype('datetime64[ns]')

        hora_rel = time.strftime('%H%M%S')
        diretorio: str = askdirectory()
        if diretorio:
            dados.to_excel(diretorio +'\\' + self.nome_rel + f'_{hora_rel}.xlsx','Relat??rio',index=None)
            messagebox.showinfo('Arquivo','Arquivo Gerado com Sucesso.')

    def style_treeview(self):
        self.estilo_treeview = ttk.Style()
        self.estilo_treeview.theme_use('clam')

    def delete_produtos(self):
        if self.valida_campos_vazios(self.lista_valida_comp_produtos):
            valores =  self.selecao_item_produto()
            bd = DataBase(2)
            sql = f"""DELETE FROM tb_produtos WHERE id = {valores[0]}"""
            bd.delete(sql)
            self.popular_tabela_produtos()

    def update_produtos(self):
        dados = (self.id_produto, self.txt_cd_produto.get(), self.txt_cd_descri_produto.get(), self.cbx_cd_categoria_produto.get())
        valid = [True if value != '' else False for value in dados]
        if False not in valid:
            if self.valida_campos_vazios(self.lista_valida_comp_produtos):
                db = DataBase(2)
                sql = """UPDATE tb_produtos SET produto = '{}', 
                            descricao = '{}', categoria = '{}' WHERE id = {}
                    """.format(self.txt_cd_produto.get(), 
                            self.txt_cd_descri_produto.get(), 
                            self.cbx_cd_categoria_produto.get(),
                            self.id_produto)
                db.update(sql)
                self.popular_tabela_produtos()
                self.txt_cd_produto.delete(0, END)
                self.txt_cd_descri_produto.delete(0, END)
                self.cbx_cd_categoria_produto.delete(0, END)

    def insert_produtos(self):
        lista: list = []
        dados = (None, self.txt_cd_produto.get(), self.txt_cd_descri_produto.get(), self.cbx_cd_categoria_produto.get())
        valid = [True if value != '' else False for value in dados]
        dados_massivo = self.txtArea_produtos.get("1.0","end - 1c")

        if False not in valid:
            if self.valida_campos_vazios(self.lista_valida_comp_produtos):
                lista.append(dados) 
                db=DataBase(2)
                sql="""INSERT INTO tb_produtos VALUES(?,?,?,?)"""
                db.insert(sql, lista)
                self.popular_tabela_produtos()
                # messagebox.showwarning('Erro Dados', 'Verifique os dados e tente novamente.')

        if dados_massivo:
            self.inserir_produto_massivo(dados= dados_massivo)
            self.popular_tabela_produtos()

    def filtro_dados_produtos(self):
        tipo = self.cbx_cd_filtro.get()
        proc = self.txt_campo_pesquisa.get()
        if tipo:
            if tipo =='PRODUTO':
                n_tipo = 'produto'
            elif tipo =='DESCRI????O':
                n_tipo = 'descricao'
            elif tipo =='CATEGORIA':
                n_tipo = 'categoria'

            sql = """SELECT              
                id,
                produto,
                descricao,
                categoria 
                FROM tb_produtos WHERE {} LIKE '%{}%'
                ORDER BY id DESC """.format(n_tipo, proc)

            dados = self.select_dados_produtos(sql)
            self.popular_tabela_produtos(dados)

    #a????es
    def duplo_click_tabela_produtos(self, event):
            self.tr_vw_produtos.selection()
            self.txt_cd_produto.delete(0, END)
            self.txt_cd_descri_produto.delete(0, END)
            self.cbx_cd_categoria_produto.delete(0, END)

            for n in self.tr_vw_produtos.selection():
                self.id_produto, col2, col3, col4 = self.tr_vw_produtos.item(n, 'values')
                self.txt_cd_produto.insert(END, col2)
                self.txt_cd_descri_produto.insert(END, col3)
                self.cbx_cd_categoria_produto.insert(END, col4)
        
    #USUARIOS
    def variaveis_usuarios(self):
        if self.info_usuario['acesso'] == 'NIVEL 1':
            self.v_matric_usu = self.info_usuario['matricula']
            self.v_nome_usu =self.info_usuario['usuario']
            self.v_cargo_usu =self.info_usuario['cargo']
            self.v_setor_usu =self.info_usuario['setor']
            self.v_nivel_usu =self.info_usuario['acesso']
            self.v_senha_usu = self.var_senha.get()
            self.id_usu = self.info_usuario['id']
        else:
            self.v_matric_usu = self.var_matricula.get()
            self.v_nome_usu =self.var_nome_usu.get()
            self.v_cargo_usu =self.var_cargo.get()
            self.v_setor_usu =self.var_setor.get()
            self.v_nivel_usu =self.var_nivel_acesso.get()
            self.v_senha_usu =self.var_senha.get()

            try:
                valores = self.selecao_item_usuario()
                self.id_usu = valores[0]
            except:
                pass

    def limpa_campos_usuarios(self):
            self.txt_matricula.delete(0, END)
            self.txt_nome_usu.delete(0, END)
            self.var_senha.set('')
            self.cb_cargo.set('')
            self.cb_setor.set('')
            self.cb_nivel_acesso.set('')

    def duplo_click_tabela_usuarios(self, event):
            # valores: list = []
            self.cb_setor.config(state='normal')
            self.cb_cargo.config(state='normal')
            self.cb_nivel_acesso.config(state='normal')
            self.tr_vw_usuarios.selection()
            self.limpa_campos_usuarios()


            for n in self.tr_vw_usuarios.selection():
                lista_valores = self.tr_vw_usuarios.item(n, 'values')
                valores = self.select_usuario(lista_valores[0])
                self.txt_matricula.insert(END, valores[0][1])
                self.txt_nome_usu.insert(END, valores[0][2])
                self.cb_cargo.insert(END, valores[0][3])
                self.cb_setor.insert(END, valores[0][4])
                self.cb_nivel_acesso.insert(END, valores[0][5])
                self.var_senha.set(valores[0][6])
                
            self.cb_setor.config(state='readonly')
            self.cb_cargo.config(state='readonly')
            self.cb_nivel_acesso.config(state='readonly')

            if valores[0][0] == self.info_usuario['id']:
                self.btn_ver_senha.config(state='normal')
            else:
                self.btn_ver_senha.config(state='disabled')
                self.lb_senha.config(show='???')

    def selecao_item_usuario(self):
        item = self.tr_vw_usuarios.selection()[0]
        valores = self.tr_vw_usuarios.item(item, 'values')
        return valores  

    def inserir_usuario(self, senhaPadrao: str = 'validade1'):
        
        if self.valida_campos_vazios(self.lista_valida_comp_usuario):
            self.variaveis_usuarios()
            bd = DataBase(2)
            valid_sql = """SELECT matricula FROM tb_usuarios WHERE matricula = '{}'""".format(self.v_matric_usu)
            resposta = bd.selectAll(valid_sql)

            try:
                n_resposta = resposta[0][0]
            except IndexError:
                n_resposta = 'novo_usuario'

            if n_resposta == self.v_matric_usu:
                messagebox.showwarning('Erro de Cadastro', 'Matricula ja cadastrada no Sistema!!\nVerifique os dados e tente novamente.')
            else:
                bd = DataBase(2)
                sql = """INSERT INTO tb_usuarios VALUES(?,?,?,?,?,?,?)"""
                bd.insert(sql,[(None,
                                self.v_matric_usu, 
                                self.v_nome_usu.upper(), 
                                self.v_cargo_usu, 
                                self.v_setor_usu, 
                                self.v_nivel_usu,
                                senhaPadrao)]
                                )
                self.popular_tabela_usuario()
                self.limpa_campos_usuarios()

    def deleta_usuario(self):
        if self.valida_campos_vazios(self.lista_valida_comp_usuario):
            valores =  self.selecao_item_usuario()
            bd = DataBase(2)
            sql = f"""DELETE FROM tb_usuarios WHERE id = {valores[0]}"""
            bd.delete(sql)
            self.popular_tabela_usuario()
            self.limpa_campos_usuarios()

    def atualiza_usuario(self):
        if self.valida_campos_vazios(self.lista_valida_comp_usuario):
            self.variaveis_usuarios()
            dados = ( self.v_matric_usu,
                    self.v_nome_usu, 
                    self.v_cargo_usu, 
                    self.v_setor_usu, 
                    self.v_nivel_usu,
                    self.v_senha_usu,
                    self.id_usu)

            valid = [True if value != '' else False for value in dados]
            if False not in valid:
                db = DataBase(2)
                sql = """UPDATE tb_usuarios SET matricula = '{}', 
                            usuario = '{}', cargo = '{}', setor = '{}', 
                            acesso = '{}', senha = '{}' WHERE id = {}
                    """.format(self.v_matric_usu,
                                self.v_nome_usu.upper(), 
                                self.v_cargo_usu, 
                                self.v_setor_usu, 
                                self.v_nivel_usu,
                                self.v_senha_usu,
                                self.id_usu
                    )
                db.update(sql)
                if self.info_usuario['acesso'] == 'NIVEL 1':
                    valores = self.select_usuario(self.info_usuario['id'])
                    self.popular_tabela_usuario(valores)
                else:
                    self.popular_tabela_usuario()
                    self.limpa_campos_usuarios()

    def select_usuario(self, id:int):
        bd = DataBase(2)
        sql = """SELECT * FROM tb_usuarios WHERE id = {}""".format(id)
        valores = bd.selectAll(sql)
        return valores

    def popular_tabela_usuario(self, lista_dados: list =[]): 
        if lista_dados:
            dados_prod = lista_dados
        else:
            dados_prod = self.select_dados_usuarios()

        try:
            self.tr_vw_usuarios.delete(*self.tr_vw_usuarios.get_children())
            for dados in dados_prod:
                self.tr_vw_usuarios.insert('','end',values=dados)
        except:
            pass

    def select_dados_usuarios(self, sqlString:str =''):
        if sqlString:
            sql = sqlString
        else:
            sql =""" SELECT 
                id,
                usuario,
                cargo,
                acesso 
            FROM tb_usuarios ORDER BY id DESC """

        
        try:
            bd = DataBase(2)
            self.dados_produtos = bd.selectAll(sql)
            return self.dados_produtos
        except:
            messagebox.showerror('Erro de dados','N??o foi possivel carregar os dados do produto')
            return

    def resetar_senha_usuario(self):

        self.variaveis_usuarios()
        db = DataBase(2)
        sql = """UPDATE tb_usuarios SET senha = '{}' WHERE id = {}""".format('validade1', self.id_usu)
        db.update(sql)
        self.popular_tabela_usuario()
        self.limpa_campos_usuarios()

    def oculta_senha(self, senha:str):
        cript_senha = "".join(['???' for letra in senha])
        return cript_senha

    # PRIMEIRO ACESSO USUARIO
    def validando_primeiro_acesso(self):
        try:
            bd = DataBase(1)
            sql = """SELECT valor FROM tb_primeiro_acesso"""
            valores = bd.selectAll(sql)
            if valores[0][0] == 0:
                return True
            return False 
        except:
            messagebox.showerror('Erro Banco', 'N??o foi possivel conectar ao banco.')
            return False 

    def dados_acesso_usuario(self, usuario: str, senha: str) -> list:
        print(usuario, senha, '==================================')
        bd = DataBase(2)
        sql = """SELECT * FROM tb_usuarios WHERE matricula = '{}' AND senha = '{}'
        """.format(usuario, senha)

        self.dados_usuario = bd.selectAll(sql)
        print(self.dados_usuario)
        if len(self.dados_usuario)> 0:
            self.info_usuario['id'] = self.dados_usuario[0][0]
            self.info_usuario['matricula'] = self.dados_usuario[0][1]
            self.info_usuario['usuario'] = self.dados_usuario[0][2]
            self.info_usuario['cargo'] = self.dados_usuario[0][3]
            self.info_usuario['setor'] = self.dados_usuario[0][4]
            self.info_usuario['acesso'] = self.dados_usuario[0][5]
            self.info_usuario['senha'] = self.dados_usuario[0][6]

        return self.dados_usuario

    def primeiro_acesso(self):
        opc = messagebox.askyesnocancel('Banco de Dados', 'Localize o banco de dados "dataBaseGlobal.db" para continuar.')

        if opc:
            try:
                diretorio = askopenfilename()
                bd = DataBase(2)
                caminho_dir = os.path.dirname(diretorio)
                v_conexao = bd.teste_de_conexao(diretorio)
                if v_conexao:
                    sql = """SELECT r_minimo, a_comercial FROM tb_periodo_rec"""
                    valores = bd.selectAll(sql)
                    lista_acesso = ['RELAT??RIO_REC', 'PDF', caminho_dir, valores[0][0], valores[0][1]]
                    self.atualiza_dados_config(lista_acesso)
                    self.componentes_cadastro_usuario()
                else:
                    messagebox.showerror('Erro conex??o', 'Erro de conex??o!\nVerifique os dados e tente novamente.')
            except:
                pass

    def primeiro_login_acesso(self):
        opc = messagebox.askyesnocancel('Banco de Dados', 'Localize o banco com o nome de "'"dataBaseGlobal.db"'" para continuar.')

        if opc:
            try:
                diretorio = askopenfilename()
                bd = DataBase(2)
                caminho_dir = os.path.dirname(diretorio)
                v_conexao = bd.teste_de_conexao(diretorio)
                if v_conexao:
                    sql = """UPDATE tb_config SET dir_bd = '{}', nome_pdf = '{}', nome_rel = '{}' WHERE id = 1
                            """.format(caminho_dir, 'PDF', 'RELAT??RIO_REC')
                    bd = DataBase(1)
                    bd.update(sql)
                    self.componentes_login_usuario()
                    
                else:
                    messagebox.showerror('Erro conex??o', 'Erro de conex??o!\nVerifique os dados e tente novamente.')
            except:
                pass

    def validacao_senha(self,usuario, senha, v_senha):
        
        if senha == v_senha and usuario !='':
            return True
        elif senha =='' or v_senha =='' or usuario =='':
            messagebox.showerror('Erro Senha','Campos de senha ou matricula em branco!!!\nVerifique e tente novamente.')
            return False
        else:
            messagebox.showerror('Erro Senha','Senhas n??o conferem!!\nVerifique e tente novamente.')
            return False

    def logar_usuario(self, tipoAcesso: int):

        if tipoAcesso == 1:
            resultado = self.validacao_senha(self.lg_cad_usuario.get(), self.lg_cad_senha.get(), self.lg_rept_senha.get())
            if resultado:
                n_valores = ''
                try:
                    sql = """SELECT matricula FROM tb_usuarios"""
                    valores = self.select_dados_usuarios(sql)
                    n_valores = valores[0][0]
                except:
                    n_valores = 'novo usuario'

                # import ipdb; ipdb.set_trace()
                if n_valores != self.lg_cad_usuario.get():
                    self.nova_senha = self.lg_cad_senha.get()
                    self.novo_matricula = self.lg_cad_usuario.get()
                    self.componentes_usuarios(False, nivelAcesso='NIVEL 2')
                else:
                    messagebox.showerror('Usuario Existente', 'Usuario ja Existe em nosso sistema!!\nVerifique os dados e tente novamente.')

        elif tipoAcesso == 2:
            resultado = self.validacao_senha(self.lg_usuario.get(), self.lg_senha.get(), self.lg_senha.get())
            if resultado:
                dados = self.dados_acesso_usuario(str(self.lg_usuario.get()), str(self.lg_senha.get()))
                if len(dados)> 0:
                    self.componentes_tela_inicial()
                else:
                    messagebox.showerror('Erro Login', 'Usuario n??o localizado!\nVerifique seus dados e tente novamente.')

    def mostra_senha(self, campo: Tk):
        try:
            if campo.cget('show') == '':
                campo.config(show='???')
            else:
                campo.config(show='')   
        except:
            pass           

    def inserir_primeiro_usuario(self):
        self.inserir_usuario(self.nova_senha)
        self.componentes_login_usuario()

    #calendario
    def calendario(self, campo):
        self.componentes_celendario(campo)

    def componentes_celendario(self, campo):
        self.master = Toplevel(self.root)
        self.master.title('Calendario')
        p = self.centralizacao_tela(352, 377, self.master)
        self.master.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))
        self.master.resizable(False, False)
        self.master.grab_set()

        lb_image = Label(self.master,image=self.imagem_calendario)
        lb_image.place(x=0, y=0)
 
        # App's private variables
        self._months = self._get_month_names()
        self._months_days = self._get_months_days_dict()
        self._clicked_button = None
        self._date = ''
        self._time = ''
        self.date_time = {}
 
        # Configures style for app's widgets
        self._configure_style()
 
        # Date fields
        self._create_date_fields()

 
        ttk.Button(self.master, text='SELECIONAR', command=lambda:self._select_date_time(campo), \
            style='Select.TButton')\
            .place(x=119, y=336, width=124, height=26)
 
    def _get_month_names(self):
        '''Returns list of month names'''
 
        return ('Janeiro', 'Fevereiro', 'Mar??o', 'Abril', 'Maio', 'Junho', \
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
    
    def _get_months_days_dict(self):
        '''
        Returns a dictionary where keys are months and values are their
        number of days
        '''
 
        months_days = {}
        months_days['Janeiro'] = 31
        months_days['Fevereiro'] = 28
        months_days['Mar??o'] = 31
        months_days['Abril'] = 30
        months_days['Maio'] = 31
        months_days['Junho'] = 30
        months_days['Julho'] = 31
        months_days['Agosto'] = 31
        months_days['Setembro'] = 30
        months_days['Outubro'] = 31
        months_days['Novembro'] = 30
        months_days['Dezembro'] = 31
 
        return months_days
 
    def _configure_style(self):
        '''Contains all style configurations'''
 
        style = ttk.Style()

 
        # Custom style
 
        style.configure('TCombobox', selectbackground=[('normal', 'white')])
        style.configure('TCombobox', selectforeground=[('normal', 'black')])
 
        style.configure('Day.TButton', background="#D9D9D9", relief='groove',font=('', 12, 'bold'))
        style.configure('Day.Clicked.TButton',font=('', 15, 'bold'),foreground='#ffffff', background='#888AC1', \
            relief='groove')
        style.configure('Select.TButton', background='#676AA9', \
            foreground='#ffffff', font=('', 10, 'bold'))
 
    def _create_date_fields(self):
        '''Creates all relevant to date fields'''
 
        # Month selection fields
        self._month = StringVar()
        month_combobox = ttk.Combobox(self.master, \
            textvariable=self._month,font=('', 10, 'bold'))
        month_combobox.place(x=56, y=67, width=88, height=21)
        month_combobox.bind('<<ComboboxSelected>>', self._enable_month_days)
        self._month_combobox = month_combobox
        self._load_months()
 
        # Year selection fields
        self._year = StringVar()
        year_combobox = ttk.Combobox(self.master, \
            textvariable=self._year,font=('', 12, 'bold'))
        year_combobox.place(x=243, y=69,width=92, height=21)
        year_combobox.bind('<<ComboboxSelected>>', self._enable_month_days)
        self._year_combobox = year_combobox
        self._load_years()
 
        # Days of the month buttons
        days_buttons = []
        days = 31
        x = 38
        y = 105
        for i in range(1, days+1):
            # Creates a button with disabled state
            button = ttk.Button(self.master, text=str(i), style='Day.TButton')
            button.configure(command=lambda btn=button: \
                self._day_button_callback(btn))
            button.place(x=x, y=y, width=40, height=40)
            button.state(['disabled'])
            days_buttons.append(button)
 
            # Updates the x,y location
            x += 40
            if i % 7 == 0:
                x = 38
                y += 40
        self._days_buttons = days_buttons

    def _load_months(self):
        '''Loads months names into combobox'''
                
        self._month_combobox.configure(values=self._months)
  
    def _load_years(self):
        '''Loads years into combobox beggining from 1990'''
 
        now = datetime.now()
 
        years = [*range(now.year-10, now.year+30)]
        years.reverse()
        
        self._year_combobox.configure(values=years)
        self._year_combobox.current(29)
 
    def _enable_month_days(self, event=None):
        '''Enables relevant days of a selected month'''
 
        month = self._month_combobox.get()
        year = self._year_combobox.get()
 
        if month and year:
            # Fields are not empty
            days = self._months_days[month]
 
            year = int(year)
            if month == 'Fevereiro' and year % 4 == 0:
                # Leap year - 29 days
                days += 1
            
            i = 0
            while i <= days-1:
                # Enables days of a month
                self._days_buttons[i].state(['!disabled'])
                self._days_buttons[i].configure(style='Day.TButton')
                i += 1
            
            while i < 31:
                # Disables days that exceed the number of days in a month
                self._days_buttons[i].state(['disabled'])
                self._days_buttons[i].configure(style='Day.TButton')
                i += 1
     
    def _day_button_callback(self, button):
        '''A callback of a days of the month button'''
 
        if self._clicked_button:
            self._clicked_button.configure(style='Day.TButton')
        
        button.configure(style='Day.Clicked.TButton')
        self._clicked_button = button
 
        # Updates selected_date_label text
        month = self._month_combobox.get()
        month = str(self._months.index(month)+1)
        day = button.cget('text')
        year = self._year_combobox.get()
        # if int(month) < 10: month = "0" + month 
        # if int(day) < 10: day = "0" + day 

        date = month + '/' + day + '/' + year
        self._date = date

    def _select_date_time(self, campo):
        '''Creates and saves a dictionary of date and time.
        
        After a dictionary is created the window is closed.
        '''
        
        month = self._month_combobox.get()
        year = self._year_combobox.get()
 
        day = ''
        if self._clicked_button:
            day = self._clicked_button.cget('text')
  
        if month and year and day:
        # if month and year and day and hour and minutes and seconds:
 
            date_time = {}
        
            month = str(self._months.index(month)+1)
            if int(month) < 10:
                month = '0' + month
 
            if int(day) < 10:
                day = '0' + day
 
            date_time['month'] = month
            date_time['year'] = year
            date_time['day'] = day
 
            self.date_time = date_time
            nova_data = day + '/' + month + '/' + year
            self.master.destroy()
            # return self.date_time
            campo.delete(0, END)
            campo.insert(0, nova_data)

    def get_date_time(self):
        '''Returns a dictionary of date and time elements'''
        print('get_date_time', self.date_time)
        return self.date_time



if __name__ == '__main__':
    TelaPrincipal()
