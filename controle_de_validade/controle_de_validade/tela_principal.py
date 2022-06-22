import os
from tkinter import * 
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
        self.caminho = os.getcwd()
        print(self.caminho, '************')
        self.root.title('Controle de Validade')
        p = self.centralizacao_tela(1440,750,self.root)
        self.root.geometry("%dx%d+%d+%d" % (p[0],p[1],p[2],p[3]))
        self.imagem_tela = PhotoImage(file=r'..\image\tela1.png')
        lb_image = Label(self.root,image=self.imagem_tela)
        lb_image.place(x=0, y=0)
        calendario = DateEntry(self.root,selectmode='day')
        calendario.place(x=400, y=300)
        val = calendario.get_date()
        print(val)


if __name__ =='__main__':
    TelaPrincipal()
