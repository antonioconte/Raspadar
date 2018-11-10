# simple_table_html.py
 
from fpdf import FPDF, HTMLMixin
import pandas as pd
distance = [str(i) for i in range(5,45,5)]
 
class HTML2PDF(FPDF, HTMLMixin):
    pass

pdf = HTML2PDF()

def simple_table_html(m):
    data = pd.read_csv("DATA/CSV/"+m+".csv") 
 
    doc = "<h2>"+m+"</h2>"
    doc += """<table border="0" align="center" width="80%">
    <thead>
    <tr>
    <th width="5%">cm</th>
    <th width="23%">Min</th>
    <th width="23%">Max</th>
    <th width="23%">Avg</th>
    <th width="23%">Err</th>
    </tr></thead>
    <tbody>"""

    for i in range(0,8):
        row = data.loc[i]
        doc +="<tr><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td><td align='center'>{}</td></tr>".format(distance[i],row["min"],row["max"],row["avg"],row["err"])
    doc += "</tbody></table>"
 
    pdf.add_page()
    pdf.write_html(doc)

materials = ["Legno","Vetro","Plastica","Ferro","Carta"]
for m in materials:
    simple_table_html(m)
pdf.output('ReportMisure.pdf')
