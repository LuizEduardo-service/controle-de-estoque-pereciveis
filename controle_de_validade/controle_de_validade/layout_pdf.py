from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib import colors
import webbrowser

class Relatorios:
    def mostra_cliente(self):
        webbrowser.open("validade.pdf")

    def gerar_relatorio(self):
        self.c = canvas.Canvas('validade.pdf')

        self.lmt_exp = '10/10/2022'
        self.recebimento = '22/06/2022'
        self.min_recebimento = '25/05/2022'
        self.validade = '18/10/2023'
        self.sku = 123456
        self.mes = 'JUNHO'
        self.ano = 2022
        FONT_PRINCIPAL = 'Helvetica-Bold'

        #faixa limite de expedição
        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(120)
        self.c.line(30,730,550,730)

        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=750,text='LIMITE EXPEDIÇÃO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=700,text=self.lmt_exp)

        #faixa data de vencimento
        self.c.setStrokeColor(colors.black)
        self.c.setLineWidth(120)
        self.c.line(30,620,550,620)

        self.c.setFont(FONT_PRINCIPAL, 30)
        self.c.setFillColor(colors.white)
        self.c.drawCentredString(x=300, y=640,text='DATA VENCIMENTO')
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=300, y=590,text=self.validade)

        #faixa sku
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=80,y=495,text='SKU:')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(50)
        self.c.line(150,510,550,510)

        self.c.setFillColor(colors.black)
        self.c.setFont(FONT_PRINCIPAL, 40)
        self.c.drawCentredString(x=370,y=495, text= str(self.sku))

        #faixa de recebimento
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=430,text='DATA RECEBIMENTO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,400,550,400)

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=393, text= self.recebimento)

        #faixa de fabricação
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=330,text='DATA FABRICAÇÃO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,300,550,300)

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=293, text= self.recebimento)

        #faixa de recebimento minimo
        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300,y=230,text='DATA MIN RECEBIMENTO')

        self.c.setStrokeColor(colors.gray)
        self.c.setLineWidth(40)
        self.c.line(40,200,550,200)

        self.c.setFont(FONT_PRINCIPAL, 20)
        self.c.setFillColor(colors.black)
        self.c.drawCentredString(x=300, y=193, text= self.min_recebimento)

        #faixa de mes e ano
        self.c.setFont(FONT_PRINCIPAL,25)
        self.c.drawCentredString(x=110, y=110,text='Vence em:' )
        self.c.setFont(FONT_PRINCIPAL,40)
        self.c.drawCentredString(x=110, y=60,text=self.mes )
        self.c.setFont(FONT_PRINCIPAL,120)
        self.c.drawCentredString(x=370, y=50,text=str(self.ano))




        self.c.showPage()
        self.c.save()
        self.mostra_cliente()


if __name__ == '__main__':
    pdf = Relatorios()
    pdf.gerar_relatorio()

