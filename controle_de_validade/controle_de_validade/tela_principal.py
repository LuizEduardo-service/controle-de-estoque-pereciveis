from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from turtle import update
import easygui
from tkcalendar import DateEntry
from datetime import date, datetime
from controle_de_validade.layout_pdf import Relatorios
from controle_de_validade.dataBase import DataBase
import pandas as pd
import time



root = Tk()
FONT_INIT =('Poppins', 15)
FONT_INIT_TXT_AREA =('Poppins', 10)

class TelaPrincipal:

    def __init__(self) -> None:
        self.nome_saida_pdf =''
        self.nome_rel =''
        self.diretorio_bd = ''
        self.valor_rec_minimo = 0
        self.valor_ale_comercial = 0
        self.root = root
        self.data_recebimento = datetime.now().date()
        self.tela()
        self.root.mainloop()

    def centralizacao_tela(self,largura, altura,root):
        param = []
        # dimensão tela computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()
        # posição da janela
        posX = (largura_screen/2) - (largura/2)
        posY = (altura_screen/2) - (altura/2)
        # definir posição
        param.append(largura);param.append(altura);param.append(posX);param.append(posY)
        return param

    def convert_data_str(self, data):
        return format(data,'%d/%m/%Y')

    def limpa_campos(self, tipo: int):
        """limpa os campos da tela"""
        if tipo == 1:
            self.rec_minimo.set('')
            self.alerta_comercial.set('')
            self.dta_fab._set_text('')
            self.dta_venc._set_text('')
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
            self.dta_fab._set_text('')
            self.dta_venc._set_text('')
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
            else:
                self.msg.set('PRODUTO NÃO LOCALIZADO')
                self.descri_produto.set('')
                self.categoria.set('')
                self.txt_produto.configure(bg='#FA8072')
                self.limpa_campos(2)
                self.numSku.set('')
                self.txt_produto.focus
        except:
            messagebox.showerror('Erro consulta', 'Não foi possivel conectar ao banco de  dados, por favor verifique a conexão.')
           
    def define_alerta_comercial(self,dta_venc, dta_fab, percent):
        """ define a data do alerta comercial"""
        data_final = dta_venc - ((dta_venc - dta_fab) * (percent/100))

        # return format(data_final,'%d/%m/%Y')
        return data_final

    def define_minimo_recebimento(self,dta_venc, dta_fab, percent):
        """Define a data minima para recebimento do produto"""
        data_final = dta_venc - ((dta_venc - dta_fab) * (percent/100))
        # return format(data_final,'%d/%m/%Y')
        return data_final

    def variaveis_tela_inicial(self):
        self.numSku_v = self.numSku.get()
        self.descri_produto_v = self.descri_produto.get()
        self.categoria_v = self.categoria.get()
        self.dta_fab_v = self.dta_fab.get_date()
        self.dta_venc_v = self.dta_venc.get_date()
        self.rec_minimo_v = self.r_minimo
        self.alerta_comercial_v = self.a_comercial
        self.dta_recebimento_v = self.data_recebimento
        self.hra_recebimento_v = time.strftime('%H:%M')
        self.usuario_v = self.usuario
        self.matricula_v = self.matricula
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
                                    dta_recebimento = self.data_recebimento_v,
                                    usuario = self.l_usuario_v,
                                    matricula = self.l_matricula_v,
                                    nome_arquivo = self.nome_saida_pdf

            )
            gerarPdf.gerar_relatorio()
            
    def executa_calculos(self):
        self.status_recebimento: str = ''
        self.data_fab = self.dta_fab.get_date()
        self.data_venc = self.dta_venc.get_date()
        self.r_minimo = self.define_minimo_recebimento(self.data_venc, self.data_fab, self.valor_rec_minimo)
        self.a_comercial = self.define_alerta_comercial(self.data_venc, self.data_fab, self.valor_ale_comercial)
        status_rec = self.btReceber.get()


        if self.data_fab >= self.data_venc:
            self.btReceber.set('DATA DE FABRICAÇÃO MAIOR OU IGUAL AO VENCIMENTO')
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
            self.btReceber.set('PRODUTO NÃO LIBERADO PARA RECEBIMENTO')
            self.bt_receber.configure(bg='#FA8072')
            self.rec_minimo.set(self.convert_data_str(self.r_minimo))
            self.alerta_comercial.set(self.convert_data_str(self.a_comercial))
            # self.rec_minimo.set('')
            # self.alerta_comercial.set('')
            

        status_rec_validado = self.btReceber.get()

        if status_rec == 'PRODUTO LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO LIBERADO PARA RECEBIMENTO':
            self.status_recebimento = 'RECEBIDO'
            self.insere_registros_rec()
            self.gerar_pdf()
            self.select_dados_rec()
            self.txt_produto.focus()
            self.limpa_campos(1)
            self.btReceber.set('RECEBIMENTO FINALIZADO')
            self.configura_btn_receber()

        elif status_rec == 'PRODUTO NÃO LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO NÃO LIBERADO PARA RECEBIMENTO':
            opc = messagebox.askyesnocancel("Recebimento de Mercadoria", 
                                            'Mercadoria não esta nos parametros de recebimento.\nContinuar recebimento?')
            if opc:
                messagebox.showinfo('Recebimento','Produto recebido!')
                self.status_recebimento = 'RECEBIDO'
                self.insere_registros_rec()
                self.select_dados_rec()
                self.txt_produto.focus()
                self.limpa_campos(1)
                self.btReceber.set('RECEBIMENTO FINALIZADO')
                self.configura_btn_receber()

            elif opc is None:
                pass
            else:
                messagebox.showerror('Recebimento','Produto não recebido!')
                self.limpa_campos(1)
                self.txt_produto.focus()
                self.status_recebimento = ' NÃO RECEBIDO'
                self.configura_btn_receber()
        else:
            pass


    def define_diretorio(self, tipo: str) -> str:
            diretorio = easygui.diropenbox()
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
        self.imagem_tela = PhotoImage(file=r'..\image\tela1.png')

    def configura_btn_receber(self):
        self.bt_receber.configure(bg='#676AA9', fg='#ffffff')

    def componentes_tela_inicial(self):
        self.destroi_widget()
        self.carrega_dados_config()
        self.imagem_tela = PhotoImage(file=r'..\image\tela1.png')
        self.imagem_pesquisa = PhotoImage(file=r'..\image\pesquisar.png',width=64,height=30)
        self.componentes_menu_bar()
       
        lb_image = Label(self.root,image=self.imagem_tela)
        lb_image.place(x=0, y=0)

        # relogio
        self.relogio_h = Label(self.root, font=FONT_INIT)
        self.relogio_h.place(x=683, y=92, width=169, height=43)
        self.relogio()

       #label data
        self.dta_fab = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')

        self.dta_venc = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')

        self.dta_fab.place(x=60, y=263, width=307, height=43)
        self.dta_venc.place(x=399, y=263, width=307, height=43)
        self.dta_fab._set_text('')
        self.dta_venc._set_text('')

        #botões
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

        #label
        self.dta_recebimento = StringVar()
        self.rec_minimo = StringVar()
        self.alerta_comercial = StringVar()
        self.descri_produto = StringVar()
        self.categoria = StringVar()
        self.l_usuario = StringVar()
        self.l_matricula = StringVar()
        self.msg = StringVar()


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
                                text='Usuario: ' + self.usuario,
                                font=('Poppins', 15),  
                                justify='center',
                                bg='#ffffff',
                                textvariable=self.l_usuario)

        self.lb_matricula =Label(self.root,
                                    text="Matricula: " + self.matricula, 
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
        self.lb_dta_recebimento.place(x=1197, y=140,width=211, height=37)
        self.lb_usuario.place(x=1177, y=64, width=251, height=37)
        self.lb_matricula.place(x=1179, y=99, width=251, height=37)
        self.lb_msg.place(x=345, y=80, width=554, height=43)

        #tabela
        colunas = [
                    'id',
                    'usuario',
                    'produto',
                    'descricao',
                    'data_min_rec',
                    'alerta_comercial',
                    'descri_status',
                    'data_fabricacao',
                    'data_vencimento'

        ]
        self.tr_scroll_inicial = Scrollbar(self.root)
        self.tr_vw = ttk.Treeview(self.root,columns=colunas, show='headings',yscrollcommand=self.tr_scroll_inicial.set)
        self.tr_scroll_inicial.config(command=self.tr_vw.yview)

        self.tr_vw.column('id', minwidth=0, width=0)
        self.tr_vw.column('usuario', minwidth=0, width=25)
        self.tr_vw.column('produto', minwidth=0, width=25)
        self.tr_vw.column('descricao', minwidth=0, width=200)
        self.tr_vw.column('data_min_rec', minwidth=0, width=50)
        self.tr_vw.column('alerta_comercial', minwidth=0, width=50)
        self.tr_vw.column('descri_status', minwidth=0, width=50)
        self.tr_vw.column('data_fabricacao', minwidth=0, width=50)
        self.tr_vw.column('data_vencimento', minwidth=0, width=50)


        self.tr_vw.heading('id',text= 'ID')
        self.tr_vw.heading('usuario',text= 'USUARIO')
        self.tr_vw.heading('produto',text= 'PRODUTO')
        self.tr_vw.heading('descricao',text= 'DESCRIÇÃO')
        self.tr_vw.heading('data_min_rec',text= 'DATA_MIN_REC')
        self.tr_vw.heading('alerta_comercial',text= 'ALERTA_COMERCIAL')
        self.tr_vw.heading('descri_status',text= 'DESCRI_STATUS')
        self.tr_vw.heading('data_fabricacao',text= 'DATA_FABRICAÇÃO')
        self.tr_vw.heading('data_vencimento',text= 'DATA_VENCIMENTO')


        self.tr_vw.place(x=62, y=400, width=1299, height=323)
        self.tr_scroll_inicial.place(x=1361, y=400, width=25, height=323)

        self.select_dados_rec()

    def componentes_tela_config(self):
        self.destroi_widget()
        self.image_config = PhotoImage(file=r'../image/config.png')
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

        self.ajd_alert_comercial = Label(self.root,
                                        text='?',
                                        font=('Poppins', 10))

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

    def componentes_usuarios(self):
        self.destroi_widget()
        self.componentes_menu_bar()
        self.image_usuario = PhotoImage(file=r'../image/usuarios.png')
        self.lb_img_usuario = Label(self.root,image=self.image_usuario)
        self.lb_img_usuario.place(x=0, y=0)

    def componentes_menu_bar(self):
        self.menubar = Menu(self.root)
        self.menu = Menu(self.menubar)
        self.menuBd = Menu(self.menubar)

        self.menubar.add_command(label='Inicio',command=self.componentes_tela_inicial)
        self.menubar.add_command(label='Configurações',command=self.componentes_tela_config)
        self.menubar.add_command(label='Relatório',command=self.componentes_historico)

        self.menubar.add_cascade(label='Banco', menu=self.menuBd)
        self.menuBd.add_command(label='Produtos', command=self.componentes_produtos)
        self.menuBd.add_command(label='Usuario', command=self.componentes_usuarios)

        self.root.config(menu=self.menubar)

    def componentes_login_usuario(self):
        self.destroi_widget()
        self.image_login = PhotoImage(file=r'../image/telaLogin.png')
        self.lb_img_login = Label(self.root,image=self.image_login)
        self.lb_img_login.place(x=0, y=0)
       
        self.lg_usuario = IntVar()
        self.lg_senha = StringVar()
        self.txt_usuario = Entry(self.root,
                                font=('Poppins', 25),
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                textvariable=self.lg_usuario)

        self.txt_senha = Entry(self.root,
                                font=('Poppins', 25),
                                show='•',
                                bg='#ffffff',
                                justify='center',
                                border=False,
                                textvariable=self.lg_senha)

        self.txt_usuario.place(x=930, y=350, width=393, height=45)
        self.txt_senha.place(x=930, y=462, width=393, height=45)
        self.lg_usuario.set('')

        self.btn_entrar = Button(self.root,
                                 text='Entrar',
                                 bg='#676AA9',
                                 fg='#ffffff',
                                 justify='center',
                                 cursor='hand2',
                                 border=False,
                                 font=('Poppins', 25),
                                 command=lambda:self.componentes_tela_inicial())
        
        self.btn_entrar.place(x=983, y=590, width=230, height=40)
        
    def componentes_historico(self):
        self.imagem_historico = PhotoImage(file=r'..\image\historico.png')
        self.imagem_excel = PhotoImage(file=r'..\image\b_excel.png')
        self.imagem_ficha = PhotoImage(file=r'..\image\g_ficha.png')

        self.componentes_menu_bar()
        lb_image = Label(self.root,image=self.imagem_historico)
        lb_image.place(x=0, y=0)
       #label data

        self.relogio_h = Label(self.root, font=FONT_INIT)
        self.relogio_h.place(x=683, y=92, width=169, height=43)
        self.relogio()

        self.dta_inicio = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')

        self.dta_fim = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')

        self.dta_inicio.place(x=180, y=92, width=157, height=43)
        self.dta_fim.place(x=462, y=92, width=157, height=43)

        self.bt_pesquisa_data = Button(self.root,
                            text='PESQUISAR',
                            cursor='hand2',
                            font=('Poppins', 15),
                            bg='#676AA9',
                            fg='#ffffff',
                            compound=LEFT,
                            justify='left',
                            border=False,
                            command=lambda:self.popular_tabela_historico(self.dta_inicio.get_date(),self.dta_fim.get_date()))

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
                                    self.dta_inicio.get_date(),
                                    self.dta_fim.get_date()
                                    ))

        self.bt_pesquisa_data.place(x=683, y=92, width=169, height=43)
        self.bt_gera_pdf.place(x=1260, y=92, width=51, height=51)
        self.bt_gera_rel.place(x=1339, y=92, width=51, height=51)

        #tabela
        colunas = [
                    'id',
                    'matricula',
                    'usuario',
                    'produto',
                    'descricao',
                    'categoria',
                    'data_min_rec',
                    'alerta_comercial',
                    'descri_status',
                    'data_fabricacao',
                    'data_vencimento',
                    'data_recebimento',
                    'hora_recebimento',
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
        self.tr_vw_historico.column('data_min_rec', width=50)
        self.tr_vw_historico.column('alerta_comercial', width=50)
        self.tr_vw_historico.column('descri_status', width=50)
        self.tr_vw_historico.column('data_fabricacao', width=50)
        self.tr_vw_historico.column('data_vencimento', width=50)
        self.tr_vw_historico.column('data_recebimento', width=50)
        self.tr_vw_historico.column('hora_recebimento', width=50)
        self.tr_vw_historico.column('status_de_recebimento', width=50)


        self.tr_vw_historico.heading('id',text= 'ID')
        self.tr_vw_historico.heading('matricula',text= 'MATRICULA')
        self.tr_vw_historico.heading('usuario',text= 'USUARIO')
        self.tr_vw_historico.heading('produto',text= 'PRODUTO')
        self.tr_vw_historico.heading('descricao',text= 'DESCRIÇÃO')
        self.tr_vw_historico.heading('categoria',text= 'CATEGORIA')
        self.tr_vw_historico.heading('data_min_rec',text= 'DATA_MIN_REC')
        self.tr_vw_historico.heading('alerta_comercial',text= 'ALERTA_COMERCIAL')
        self.tr_vw_historico.heading('descri_status',text= 'DESCRI_STATUS')
        self.tr_vw_historico.heading('data_fabricacao',text= 'DATA_FABRICAÇÃO')
        self.tr_vw_historico.heading('data_vencimento',text= 'DATA_VENCIMENTO')
        self.tr_vw_historico.heading('data_recebimento',text= 'DATA_RECEBIMENTO')
        self.tr_vw_historico.heading('hora_recebimento',text= 'HORA_RECEBIMENTO')
        self.tr_vw_historico.heading('status_de_recebimento',text= 'STATUS_RECEBIMENTO')

        self.tr_vw_historico.place(x=62, y=171, width=1303, height=552)
        self.tr_scroll.place(x=1365, y=171, width=25, height=552)
        self.popular_tabela_historico(self.data_recebimento, self.data_recebimento)

        self.style_treeview()

    def componentes_produtos(self):
        bd =DataBase(2)
        sql="SELECT categoria FROM tb_categoria"
        lista = bd.selectAll(sql)
        self.imagem_produtos = PhotoImage(file=r'..\image\produtos.png')

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
                                                     values=lista
                                                     
                                                            
        )

        self.cbx_cd_filtro = ttk.Combobox(self.root,
                                         font= FONT_INIT,
                                         values=['PRODUTO','DESCRIÇÃO','CATEGORIA']
                                        
                                                           
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
                                                    columns=['id','produto','descrição','categoria'],
                                                    show='headings',
                                                    yscrollcommand=self.scroll_produtos.set)

        self.scroll_produtos.config(command=self.tr_vw_produtos.yview)
        self.tr_vw_produtos.bind('<Double-1>', self.duplo_click_tabela_produtos)

        self.tr_vw_produtos.column('id', width=1)
        self.tr_vw_produtos.column('produto', width=70)
        self.tr_vw_produtos.column('descrição', width=330)
        self.tr_vw_produtos.column('categoria', width=100)

        self.tr_vw_produtos.heading('id',text='')
        self.tr_vw_produtos.heading('produto',text='PRODUTO')
        self.tr_vw_produtos.heading('descrição',text='DESCRIÇÃO')
        self.tr_vw_produtos.heading('categoria',text='CATEGORIA')

        self.tr_vw_produtos.place(x=777, y=333, width=557, height=383)
        self.scroll_produtos.place(x=1335, y=333, width=28, height=383)

        self.style_treeview()
        self.popular_tabela_produtos()
        
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
                messagebox.showinfo('Inserção','Dados inseridos com sucesso')
            except:
                messagebox.showerror('Inserção','Não foi possivel inserir os dados, verifique e tente novamente.')


    def tela(self):
        self.usuario ='Luiz Eduardo'
        self.matricula = '3896595'
        self.root.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))

        #tela inicial:
        self.componentes_produtos()




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
                    data_min_rec,
                    alerta_comercial,
                    descri_status,
                    data_fabricacao,
                    data_vencimento
                FROM tb_dataBase ORDER BY id DESC """

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
                        data_min_rec,
                        alerta_comercial,
                        descri_status,
                        data_fabricacao,
                        data_vencimento,
                        data_recebimento,
                        hora_recebimento,
                        status_de_recebimento,
                        percent_rec_minimo,
                        percent_ale_comercial            
                    FROM tb_dataBase WHERE data_recebimento BETWEEN '{}' AND '{}' ORDER BY id DESC """.format(dta_inicio, dta_fim)

            self.dados_rec = bd.selectAll(sql)
            return self.dados_rec
        except:
            messagebox.showerror('Erro de dados','Não foi possivel carregar os dados')
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
            messagebox.showerror('Erro de dados','Não foi possivel carregar os dados do produto')
            return
            
    def popular_tabela_historico(self,dtaInicio:date, dtaFim: date):
            dados_rec = self.select_dados_historico(dtaInicio, dtaFim)
            self.tr_vw_historico.delete(*self.tr_vw_historico.get_children())
            try:
                for dados in dados_rec:
                    self.tr_vw_historico.insert('','end',values=dados)
            except:
                pass

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
                                        dta_fab = valores[9],
                                        dta_venc = valores[10],
                                        rec_minimo = valores[6],
                                        alerta_comercial = valores[7],
                                        dta_recebimento = valores[11],
                                        usuario = valores[2],
                                        matricula = valores[1],
                                        nome_arquivo = self.nome_saida_pdf

                )
                gerarPdf.gerar_relatorio()       
            except:
                messagebox.showwarning('Itens','Nenhum item foi selecionado!')

    def selecao_item_produto(self) -> list:
        item = self.tr_vw_produtos.selection()[0]
        valores = self.tr_vw_produtos.item(item,'values')
        return valores
        
    #========configurações============
    def select_dados_config(self,sql:str, numDataBase: int):
        try:
            bd = DataBase(numDataBase)
            config = bd.selectAll(sql)
            return config
        except:
            messagebox.showerror('Erro Banco', 'Não foi possivel carregar os dados...\nVerifique e tente novamente.')
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

    def atualiza_dados_config(self):

            nome_relatorio = self.nome_relatorio.get()
            nome_pdf = self.nome_pdf.get()
            dir_bd = self.dir_bd.get()    
            scl_alert_comercial = self.scl_alert_comercial.get()
            scl_rec_minimo = self.scl_rec_minimo.get()

            sql = """UPDATE tb_config SET dir_bd = '{}', nome_pdf = '{}', nome_rel = '{}' WHERE id = 1""".format(dir_bd, nome_pdf, nome_relatorio)
            bd = DataBase(1)
            bd.update(sql)

            if scl_rec_minimo>= scl_alert_comercial:
                messagebox.showwarning('Erro de Periodo','Recebimento minimo maior que alerta Comercial.')
            elif scl_rec_minimo == 0 or scl_alert_comercial == 0:
                messagebox.showwarning('Erro de Periodo','Defina valores Maiores que 0.')
            else:
                sql2 = """UPDATE tb_periodo_rec SET r_minimo = {}, a_comercial = {} WHERE id = 1""".format(scl_rec_minimo, scl_alert_comercial)
                bd = DataBase(2)
                bd.update(sql2)

            self.carrega_dados_config()

    def gerar_relatorio_rec(self, dtaInicio: date, dtaFim: date):
        database = self.select_dados_historico(dtaInicio, dtaFim)
        dados = pd.DataFrame(data=database)
        dados.columns = ['ID','MATRICULA','USUARIO','PRODUTO','DESCRIÇÃO','CATEGORIA','DATA_MIN_REC',
                        'ALERTA_COMERCIAL','DESCRI_STATUS','DATA_FABRICAÇÃO','DATA_VENCIMENTO',
                        'DATA_RECEBIMENTO','HORA_RECEBIMENTO','STATUS_RECEBIMENTO','PERCENT_REC_MINIMO','PERCENT_ALE_COMERCIAL'
                        ]
        colunas_datas= ['DATA_MIN_REC','ALERTA_COMERCIAL','DATA_FABRICAÇÃO','DATA_VENCIMENTO','DATA_RECEBIMENTO']
        
        dados[colunas_datas] = dados[colunas_datas].astype('datetime64[ns]')
        dados['DATA_RECEBIMENTO']= pd.to_datetime(dados['DATA_RECEBIMENTO'],format='%d/%m/%Y')
        # dados['DATA_RECEBIMENTO'].dt.str.__format__("%d/%m/%Y")
        hora_rel = time.strftime('%H%M%S')
        diretorio: str = askdirectory()
        if diretorio:
            dados.to_excel(diretorio +'\\' + self.nome_rel + f'_{hora_rel}.xlsx','Relatório',index=None)
            messagebox.showinfo('Arquivo','Arquivo Gerado com Sucesso.')

    def style_treeview(self):
        self.estilo_treeview = ttk.Style()
        self.estilo_treeview.theme_use('clam')

    def delete_produtos(self):
        valores =  self.selecao_item_produto()
        bd = DataBase(2)
        sql = f"""DELETE FROM tb_produtos WHERE id = {valores[0]}"""
        bd.delete(sql)
        self.popular_tabela_produtos()

    def update_produtos(self):
        dados = (self.id_produto, self.txt_cd_produto.get(), self.txt_cd_descri_produto.get(), self.cbx_cd_categoria_produto.get())
        valid = [True if value != '' else False for value in dados]
        if False not in valid:
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
            elif tipo =='DESCRIÇÃO':
                n_tipo = 'descricao'
            elif tipo =='CATEGORIA':
                n_tipo = 'categoria'

            sql = """SELECT              
                id,
                produto,
                descricao,
                categoria 
                FROM tb_produtos WHERE {} LIKE '{}%'
                ORDER BY id DESC """.format(n_tipo, proc)

            print(sql)
            dados = self.select_dados_produtos(sql)
            print(dados)
            self.popular_tabela_produtos(dados)

    #ações
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
        

            
if __name__ == '__main__':
    TelaPrincipal()
