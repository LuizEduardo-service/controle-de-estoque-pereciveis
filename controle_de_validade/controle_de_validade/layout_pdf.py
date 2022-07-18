import datetime as dt
import os
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import webbrowser
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')

class Relatorios:
    def __init__(self, **kwargs) -> None:
        self.absolutepath = os.path.abspath(__file__)
        self.fileDirectory = os.path.dirname(self.absolutepath)
        self.parentDirectory = os.path.dirname(self.fileDirectory)
        self.dir_pdf = os.path.join(self.parentDirectory, 'pdf\\')

        f_data_fab = dt.datetime.strftime(kwargs.get('dta_fab'),'%Y-%m-%d')
        f_data_venc = dt.datetime.strftime(kwargs.get('dta_venc'),'%Y-%m-%d')

        self.numSku = kwargs.get('numSku')
        self.descri_produto = kwargs.get('descri_produto')
        self.categoria = kwargs.get('categoria')
        self.dta_fab = dt.datetime.strptime(f_data_fab,'%Y-%m-%d')
        self.dta_venc = dt.datetime.strptime(f_data_venc,'%Y-%m-%d')
        self.rec_minimo = dt.datetime.strptime(str(kwargs.get('rec_minimo')),'%Y-%m-%d')
        self.alerta_comercial = dt.datetime.strptime(str(kwargs.get('alerta_comercial')),'%Y-%m-%d')
        self.dta_recebimento = dt.datetime.strptime(str(kwargs.get('dta_recebimento')),'%Y-%m-%d')
        self.usuario = kwargs.get('usuario')
        self.matricula = kwargs.get('matricula')
        self.nome_arquivo = kwargs.get('nome_arquivo')
        # self.nome_arquivo = 'validade.pdf'
        


    def mostra_cliente(self):
        webbrowser.open(self.dir_pdf + self.nome_arquivo + '.pdf')

    def gerar_relatorio(self):
        FONT_PRINCIPAL = 'Helvetica-Bold'

        self.c = canvas.Canvas(self.dir_pdf + self.nome_arquivo + '.pdf')


        #faixa limite de expedição
        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(120)
        self.c.line(30,730,550,730)

        alerta_comercial = dt.datetime.strftime(self.alerta_comercial,'%d/%m/%Y')
        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=750,text='LIMITE EXPEDIÇÃO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=700,text=alerta_comercial)

        #faixa data de vencimento
        self.c.setStrokeColor(colors.black)
        self.c.setLineWidth(120)
        self.c.line(30,620,550,620)
        

        data_venc = dt.datetime.strftime(self.dta_venc,'%d/%m/%Y')
        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=640,text='DATA VENCIMENTO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=590,text=data_venc)
        # self.c.drawCentredString(x=300, y=590,text=format(self.dta_venc,'%d/%m/%Y'))


        #faixa sku
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=80,y=495,text='SKU:')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(50)
        self.c.line(150,510,550,510)

        self.c.setFillColor(colors.black)
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=370,y=495, text= str(self.numSku))

        #faixa de recebimento
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=430,text='DATA RECEBIMENTO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,400,550,400)

        dta_recebimento = dt.datetime.strftime(self.dta_recebimento,'%d/%m/%Y')
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=393, text= dta_recebimento)

        #faixa de fabricação
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=330,text='DATA FABRICAÇÃO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,300,550,300)

        dta_fab = dt.datetime.strftime(self.dta_fab,'%d/%m/%Y')
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=293, text= dta_fab)
        # self.c.drawCentredString(x=300, y=293, text= format(self.dta_fab,'%d/%m/%Y'))


        mes = dt.datetime.strftime(self.dta_venc,'%B')
        ano = dt.datetime.strftime(self.dta_venc,'%Y')

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=230,text='DATA MIN RECEBIMENTO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,200,550,200)

        rec_minimo = dt.datetime.strftime(self.rec_minimo,'%d/%m/%Y')
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=193, text= rec_minimo)

        #faixa de mes e ano
        self.c.setFont(FONT_PRINCIPAL,25)
        self.c.drawCentredString(x=110, y=110,text='Vence em:' )
        self.c.setFont(FONT_PRINCIPAL,40)
        self.c.drawCentredString(x=110, y=60,text= mes.upper())
        self.c.setFont(FONT_PRINCIPAL,120)
        self.c.drawCentredString(x=370, y=50,text=str(ano))


        self.c.showPage()
        self.c.save()
        self.mostra_cliente()


if __name__ == '__main__':
    pdf = Relatorios()
    pdf.gerar_relatorio()

