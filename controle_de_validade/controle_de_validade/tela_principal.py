from cProfile import label
import os
from time import sleep
from tkinter import *


from tkinter import font
import easygui
from tkcalendar import DateEntry
from datetime import datetime



root = Tk()
FONT_INIT =('Poppins', 15)
class TelaPrincipal:

    def __init__(self) -> None:
        self.root = root
        self.data_recebimento = datetime.now().date()
        self.tela()
        self.root.mainloop()

    def centralizar_tela(self):
        pass

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
        produtos = {
            123:[
                'Smart TV LED 32" HD Philco PTV32G70RCH Roku TV','TELEVISORES'
            ],
            456:[
                'Smartphone Motorola Moto G22 Azul 128GB 4GB RAM Tela de 6.5','CELULAR'
            ],
            789:[
                'Geladeira Consul Frost Free Duplex CRM43NB com Altura Flex','LINHA BRANCA'
            ]
        }
        try:
            novo_produto = produtos[numProduto]
        except KeyError:
            novo_produto = []

        if novo_produto:
            self.descri_produto.set(novo_produto[0])
            self.categoria.set(novo_produto[1])
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
           
    def define_alerta_comercial(self,dta_venc, dta_fab, percent = 0.25):
        """ define a data do alerta comercial"""

        data_final = dta_venc - ((dta_venc - dta_fab) * percent)

        # return format(data_final,'%d/%m/%Y')
        return data_final

    def define_minimo_recebimento(self,dta_venc, dta_fab, percent = 0.75):
        """Define a data minima para recebimento do produto"""

        data_final = dta_venc - ((dta_venc - dta_fab) * percent)
        # return format(data_final,'%d/%m/%Y')
        return data_final

    def executa_calculos(self):
        data_fab = self.dta_fab.get_date()
        data_venc = self.dta_venc.get_date()
        r_minimo = self.define_minimo_recebimento(data_venc, data_fab)
        a_comercial = self.define_alerta_comercial(data_venc, data_fab)
        status_rec = self.btReceber.get()


        if data_fab >= data_venc:
            self.btReceber.set('DATA DE FABRICAÇÃO MAIOR OU IGUAL AO VENCIMENTO')
            self.bt_receber.configure(bg='#FA8072')
            self.rec_minimo.set('')
            self.alerta_comercial.set('')

        elif  r_minimo >= datetime.now().date():
            self.btReceber.set('PRODUTO LIBERADO PARA RECEBIMENTO')
            self.bt_receber.configure(bg='#3CB371')
            self.rec_minimo.set(self.convert_data_str(r_minimo))
            self.alerta_comercial.set(self.convert_data_str(a_comercial))
            # self.limpa_campos()

        else:
            self.btReceber.set('PRODUTO NÃO LIBERADO PARA RECEBIMENTO')
            self.bt_receber.configure(bg='#FA8072')
            self.rec_minimo.set('')
            self.alerta_comercial.set('')

        status_rec_validado = self.btReceber.get()

        if status_rec == 'PRODUTO LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO LIBERADO PARA RECEBIMENTO':

            self.limpa_campos(1)
            self.btReceber.set('RECEBIMENTO FINALIZADO')
            self.txt_produto.focus

        elif status_rec == 'PRODUTO NÃO LIBERADO PARA RECEBIMENTO' and status_rec_validado == 'PRODUTO NÃO LIBERADO PARA RECEBIMENTO':
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

    def componentes_tela_inicial(self):
        self.destroi_widget()
        self.imagem_tela = PhotoImage(file=r'..\image\tela1.png')
        self.imagem_pesquisa = PhotoImage(file=r'..\image\pesquisar.png',width=64,height=30)
        self.componentes_menu_bar()
       
        lb_image = Label(self.root,image=self.imagem_tela)
        lb_image.place(x=0, y=0)
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
        self.lb_usuario = StringVar()
        self.lb_matricula = StringVar()
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
                                bg='#ffffff')

        self.lb_matricula =Label(self.root,
                                    text="Matricula: " + self.matricula, 
                                    font=('Poppins', 15), 
                                    justify='center',
                                    bg='#ffffff')

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

    def componentes_tela_config(self):
        self.destroi_widget()
        self.image_config = PhotoImage(file=r'../image/config.png')
        self.lb_img_config = Label(self.root,image=self.image_config)
        self.lb_img_config.place(x=0, y=0)
        self.componentes_menu_bar()

        # campos de entrada
        self.dir_bd = StringVar()
        self.dir_pdf = StringVar()
        self.dir_relatorio = StringVar()
        self.nome_pdf =StringVar()
        self.nome_relatorio = StringVar()



        self.txt_dir_bd = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.dir_bd,
                            )

        self.txt_dir_pdf = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.dir_pdf,
                            )

        self.txt_dir_relatorio = Entry(self.root,
                            font=FONT_INIT,
                            textvariable=self.dir_relatorio,
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
        self.txt_dir_pdf.place(x=70, y=265, width=826, height=30)
        self.txt_dir_relatorio.place(x=70, y=344, width=826, height=30)
        self.txt_nome_pdf.place(x=1012, y=265, width=252, height=30)
        self.txt_nome_relatorio.place(x=1012, y=346, width=252, height=30)


        #botoes de localiza pasta
        self.bd =StringVar()
        self.pdf =StringVar()
        self.rel =StringVar()
        self.btn_dir_bd = Button(self.root,
                                text='...',
                                font=FONT_INIT,
                                justify='center',
                                command=lambda:self.define_diretorio('bd'),
                                )

        self.btn_dir_pdf = Button(self.root,
                                text='...',
                                font=FONT_INIT,
                                justify='center',
                                command=lambda:self.define_diretorio('pdf'),
                                )

        self.btn_dir_relatorio = Button(self.root,
                                        text='...',
                                        font=FONT_INIT,
                                        justify='center',
                                        command=lambda:self.define_diretorio('rel'),
                                        )

        self.btn_dir_bd.place(x=915, y=186, width=55, height=30)
        self.btn_dir_pdf.place(x=915, y=265, width=55, height=30)
        self.btn_dir_relatorio.place(x=915, y=344, width=55, height=30)

        #escala de valores
        self.scl_rec_minimo = IntVar()
        self.scl_alert_comercial = IntVar()

        self.sc_rec_minimo = Scale(self.root, 
                                    from_=0, to=100,
                                    variable=self.scl_rec_minimo, 
                                    orient='horizontal',
                                    tickinterval=5)

        self.sc_alert_comercial = Scale(self.root, 
                                        from_=0, to=100,
                                        variable=self.scl_alert_comercial, 
                                        orient='horizontal',
                                        tickinterval=5)
        
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
                        command=lambda:self.componentes_tela_inicial()
                        )

        self.btn_cancelar_config = Button(self.root,
                        text='CANCELAR',
                        font=FONT_INIT,
                        justify='center',
                        # textvariable=self.cancelar_config,
                        )
        

        self.btn_salva_config.place(x=1250, y=690, width=140, height=30)
        self.btn_cancelar_config.place(x=1073, y=690, width=140, height=30)

    def componentes_menu_bar(self):
        self.menubar = Menu(self.root)
        self.menu = Menu(self.menubar)

        self.menubar.add_command(label='Inicio',command=self.componentes_tela_inicial)
        self.menubar.add_command(label='Banco')
        self.menubar.add_command(label='Configurações',command=self.componentes_tela_config)
        self.menubar.add_command(label='Relatório')

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

    def tela(self):
        self.usuario='Luiz Eduardo'
        self.matricula = '3896595'
        self.root.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))

        #tela inicial:

        self.componentes_login_usuario()


if __name__ =='__main__':
    TelaPrincipal()
