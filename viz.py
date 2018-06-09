import os
import sqlite3
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure, show


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect('./test.db')
db.row_factory = dict_factory
cur = db.cursor()
cur.execute('''SELECT GPU_ID, MEM FROM TEST;''')
res = cur.fetchmany(10)

data_source = {'GPU_ID': [], 'MEM': []}
for ele in res:
    data_source['GPU_ID'].append(ele['GPU_ID'])
    data_source['MEM'].append(ele['MEM'])

source = ColumnDataSource(data=data_source)

plot = figure()
plot.step(x='GPU_ID', y='MEM', source=source, mode='center')

slider = Slider(start=10, end=100, value=50, step=10, title='Number')

def callback(attr, old, new):
    N = slider.value
    # db = sqlite3.connect('./test.db')
    # db.row_factory = dict_factory
    cur = db.cursor()
    cur.execute('SELECT GPU_ID, MEM FROM TEST;')
    res = cur.fetchmany(N)
    data_source = {'GPU_ID': [], 'MEM': []}

    for ele in res:
        data_source['GPU_ID'].append(ele['GPU_ID'])
        data_source['MEM'].append(ele['MEM'])

    source.data = data_source

slider.on_change('value', callback)

layout = column(slider, plot)
curdoc().add_root(layout)
