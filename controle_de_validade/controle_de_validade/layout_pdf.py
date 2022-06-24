import datetime as dt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib import colors
import webbrowser
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
except:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')

class Relatorios:
    def __init__(self, **kwargs) -> None:
        self.numSku = kwargs.get('numSku')
        self.descri_produto = kwargs.get('descri_produto')
        self.categoria = kwargs.get('categoria')
        self.dta_fab = kwargs.get('dta_fab')
        self.dta_venc = kwargs.get('dta_venc')
        self.rec_minimo = kwargs.get('rec_minimo')
        self.alerta_comercial = kwargs.get('alerta_comercial')
        self.dta_recebimento = kwargs.get('dta_recebimento')
        self.usuario = kwargs.get('usuario')
        self.matricula = kwargs.get('matricula')
        self.nome_arquivo = kwargs.get('nome_arquivo')

        self.lmt_exp = kwargs.get('lmt_exp')
        self.recebimento = kwargs.get('recebimento')
        self.min_recebimento = kwargs.get('min_recebimento')
        self.validade = kwargs.get('validade')
        self.sku = kwargs.get('sku')
        self.descricao = kwargs.get('descricao')
        self.ano = 2022

    def mostra_cliente(self):
        webbrowser.open(self.nome_arquivo)

    def gerar_relatorio(self):
        self.nome_arquivo = 'validade.pdf'
        self.lmt_exp = '10/10/2022'
        self.recebimento = '22/06/2022'
        self.min_recebimento = '25/05/2022'
        self.validade = '18/10/2023'
        self.sku = 123456
        self.mes = 'JUNHO'
        self.ano = 2022
        FONT_PRINCIPAL = 'Helvetica-Bold'

        self.c = canvas.Canvas(self.nome_arquivo)


        #faixa limite de expedição
        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(120)
        self.c.line(30,730,550,730)

        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=750,text='LIMITE EXPEDIÇÃO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=700,text=self.alerta_comercial)

        #faixa data de vencimento
        self.c.setStrokeColor(colors.black)
        self.c.setLineWidth(120)
        self.c.line(30,620,550,620)

        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=640,text='DATA VENCIMENTO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=590,text=format(self.dta_venc,'%d/%m/%Y'))

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

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=393, text= self.dta_recebimento)

        #faixa de fabricação
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=330,text='DATA FABRICAÇÃO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,300,550,300)

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=293, text= format(self.dta_fab,'%d/%m/%Y'))

        #faixa de recebimento minimo
        mes = dt.datetime.strftime(self.dta_venc,'%B')
        ano = dt.datetime.strftime(self.dta_venc,'%Y')

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=230,text='DATA MIN RECEBIMENTO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,200,550,200)

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=193, text= self.rec_minimo)

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

