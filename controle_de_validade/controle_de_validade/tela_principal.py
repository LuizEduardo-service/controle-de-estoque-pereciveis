import os
from tkinter import *
from tkinter import font
from turtle import width 
from tkcalendar import DateEntry



root = Tk()

class TelaPrincipal:

    def __init__(self) -> None:
        self.root = root
        self.tela_inicial()
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

    def tela_inicial(self):
        self.root.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))
        self.imagem_tela = PhotoImage(file=r'..\image\tela1.png')
        self.imagem_pesquisa = PhotoImage(file=r'..\image\pesquisa.png',width=43,height=43)
       
        lb_image = Label(self.root,image=self.imagem_tela)
        lb_image.place(x=0, y=0)

        dta_fab = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')
        dta_venc = DateEntry(self.root,
                            selectmode='day',
                            font=('Poppins',20), 
                            justify='center')

        dta_fab.place(x=60, y=263, width=307, height=43)
        dta_venc.place(x=399, y=263, width=307, height=43)

        #botões
        bt_receber = Button(self.root,
                            text='Aguardando analise...',
                            cursor='hand2')
        bt_pesquisa_sku = Button(self.root,
                            text='',
                            cursor='hand2',
                            image=self.imagem_pesquisa)


        bt_receber.place(x=60, y=333,width=1328, height=50)
        bt_pesquisa_sku.place(x=280, y=82,width=42, height=39)

        txt_produto =Text(self.root,
                            font=('Poppins', 20))

        txt_produto.place(x=60, y=79,width=197,height=43)



if __name__ =='__main__':
    TelaPrincipal()
