import psycopg2
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from jinja2 import Environment, FileSystemLoader
import webbrowser
from datetime import date
import os

file_loader = FileSystemLoader('template')
env = Environment(loader=file_loader)
template = env.get_template('template.html')

today = date.today()
f = open('Data_Report_{}.html'.format(today), 'w')
    
#connect to the db
con = psycopg2.connect(
    host = "pgpl-db.iii.com",
    database = "iii",
    user = "gzaarour",
    password = "gdAL3-818_",
    port = "1032"
    )
#or 54012 or 5432 for port
#or "postgres" for database

#cursor
cur = con.cursor()

#convert item type codes to strings
def code2string(num):
    conversion = ['unknown',  'Book', 'Paperback', 'Magazine', 'Audiobook', 'Music CD', 'DVD', 'VHS', 'Video Game', 'Magnetic', 'Software',
                  '', '', '', '', 'Marketplace', 'Marketplace DVD', '', '', '',
                  'No Loan', '', '', '', '', '', '', '', '', '', 'Interlibrary Loan', '', '', '', '', '', '', '', '', '', 'CD Player', '',
                  '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Laptop', '', '', '',
                  '', '', '', '', '', '', 'DVD Player', '', '', '', '', '', '', '', '', '', 'iPad', '', '', '', '', 'Hotspot',
                  'Hotspot - No Holds', '', '', '', 'Kit', '', '', '', '', '', '', '', 'Microform', 'Default/Cleanup']

    return conversion[num]

#convert patron types to strings
def type2string(num):
    conversion = ['Adaptive', 'Adult', 'Adult-Laptop', 'Teen Limited', 'Teen Limited Laptop', 'Teen Unlimited', 'Teen Unlimited Laptop', 'Juvenile Limited',
                  'Juvenile Limited Laptop', 'Juvenile Unlimited', 'Juvenile Unlimited Laptop', 'Edison Limited', 'Edison Limited Laptop', 'Edison Unlimited',
                  'Edison Unlimited Laptop', 'eCard', 'Self Registration', 'Homebound',
                  'Library Staff', 'Department', 'City Staff', 'City Staff Laptop', 'Very Important People', 'Very Important People Laptop', 'Guest',
                  'GUSD Student', '', '', '', '', 'Business Resident', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Force Collection']

    return conversion[num]

#-------------------------------------------------------------------------------------------------------------------------
#execute query
#number of users who checked out or were active this month broken down by patron type (pie chart)


cur.execute("SELECT COUNT(*) AS users, sierra_view.patron_view.ptype_code AS patrontype \
FROM sierra_view.patron_view \
WHERE patron_view.activity_gmt > '2020-1-27' \
AND sierra_view.patron_view.barcode LIKE '2901%' \
AND sierra_view.patron_view.ptype_code < '100' \
GROUP BY sierra_view.patron_view.ptype_code \
ORDER BY sierra_view.patron_view.ptype_code;")
rows = cur.fetchall()
variable = list()
data = list()

for patrons in rows:
    data.append(patrons[0])

for ptype in rows:
    variable.append(type2string(ptype[1]))
    #variable.append('Ptype ' + str(ptype[1]))

labels = [variable]
values = [data]

fig = go.Figure(data=[go.Pie(labels=variable,  values=data)])

fig.update_layout(title_text='Number of Active Users this Month by Patron Type')

code = plot(fig, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------
#execute second query
#number of items checked out over a month's time broken down by item type (pie chart)


cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.itype_code_num \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'g%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.itype_code_num \
ORDER BY sierra_view.item_view.itype_code_num;")
rows = cur.fetchall()
variable = list()
data = list()

for items in rows:
    data.append(items[0])

for itype in rows:
    variable.append(code2string(itype[1]))
    #variable.append('itype ' + str(itype[1]))

fig1 = go.Figure(data=[go.Pie(labels=variable,  values=data)])

fig1.update_layout(title_text='Item Circulation this Month by Item Type')

code1 = plot(fig1, include_plotlyjs=False, output_type='div')
#---------------------------------------------------------------------------------------------------------------------------
#execute third query
#circulation at Brand Library (by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout2 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Brand Library (by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gb%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig2 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout2)
code2 = plot(fig2, include_plotlyjs=False, output_type='div')
#---------------------------------------------------------------------------------------------------------------------------
#execute fourth query
#circulation at Central Library (by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout3 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Central Library (by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gc%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig3 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout3)
code3 = plot(fig3, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute fifth query
#circulation at Grandview Library (by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout4 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Grandview Library (by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gg%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig4 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout4)
code4 = plot(fig4, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute sixth query
#circulation at Chevy Chase Library (by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout5 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Chevy Chase Library (by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gh%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig5 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout5)
code5 = plot(fig5, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute seventh query
#circulation at Library Connection(by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout6 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Library Connection(by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gl%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig6 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout6)
code6 = plot(fig6, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute eighth query
#circulation at Montrose Library(by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout7 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Montrose Library(by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gm%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig7 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout7)
code7 = plot(fig7, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute ninth query
#circulation at Pacific Park Library(by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout8 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Pacific Park Library(by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gp%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig8 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout8)
code8 = plot(fig8, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute tenth query
#circulation at Casa Verdugo Library(by Top Five Location Codes)
#NOTE: circulation denotes items checked out


layout9 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Casa Verdugo Library(by Top Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gv%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation DESC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig9 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout9)
code9 = plot(fig9, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------
#execute eleventh query
#circulation at Pacific Park Library(by BOTTOM Five Location Codes)
#NOTE: circulation denotes items checked out


layout10 = go.Layout(
    title=go.layout.Title(
        text='Items Checked Out at Pacific Park Library(by Bottom Five Location Codes)',
        xref='paper',
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Location Code',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Items Checked Out',
            font=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )
        )
    )
)



cur.execute("SELECT COUNT(*) AS circulation, sierra_view.item_view.location_code \
FROM sierra_view.item_view \
WHERE sierra_view.item_view.last_checkout_gmt > '2020-1-27' \
AND sierra_view.item_view.location_code LIKE 'gp%' \
AND sierra_view.item_view.barcode LIKE '3901%' \
GROUP BY sierra_view.item_view.location_code \
ORDER BY circulation ASC limit 5")
rows = cur.fetchall()
variable = list()
data = list()

for circulation in rows:
    data.append(circulation[0])

for location in rows:
    variable.append(location[1])

fig10 = go.Figure(data=go.Bar(y=data,  x=variable), layout=layout10)
code10 = plot(fig10, include_plotlyjs=False, output_type='div')
#------------------------------------------------------------------------------------------------------------------------------

output = template.render(figure = code, figure1 = code1, figure2 = code2, figure3 = code3, figure4 = code4, figure5 = code5, figure6 = code6, figure7 = code7, figure8 = code8, figure9 = code9, figure10 = code10)
print >>f, output

url = "file://{}".format(os.path.realpath(f.name))
print url;
webbrowser.open(url, new=2) 

#close the cursor
cur.close()

#close the connection
con.close()
