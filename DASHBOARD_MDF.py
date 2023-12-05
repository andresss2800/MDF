# **DASH**

# %%
"""Importar Librerias"""

import pandas as pd
import numpy as np
import plotly.express as px
from statistics import mean
from dash import dash, html, dcc
import plotly.graph_objs as go # Renderiza objetos de plotly
from dash.dependencies import Input, Output # Para usar en los callbacks
import openpyxl

# %%
"Leer Archivo"
Tiempos = pd.read_excel('data_MDF.xlsx',engine='openpyxl')
# Extraer de la fecha el mes
Tiempos['Mes'] = Tiempos['Fecha'].dt.to_period('M')
Tiempos['Mes_texto'] = Tiempos['Mes'].astype( str )
Tiempos['Novedad']= np.where(Tiempos['Falla']!= 'Sin novedad','Novedad','Sin novedad')
Tiempos['Dia de la semana']= Tiempos['Fecha'].dt.dayofweek
Tiempos['Dia de la semana'] = Tiempos['Dia de la semana'].replace({0: 'Lunes', 1: 'Martes',2: 'Miércoles',3: 'Jueves',4: 'Viernes'})
Tiempos['Cuenta']= 1

# %%
Tiempos_por_mes = Tiempos.groupby(['Mes'])['Tiempo'].mean().reset_index()
Tiempos_por_mes['mean']= Tiempos_por_mes['Tiempo'].mean()
Tiempos_por_mes["Mes"]= Tiempos_por_mes["Mes"].dt.strftime('%Y-%m')

# %%
Tiempos_por_mes['Tiempo'] = Tiempos_por_mes['Tiempo'].round(2)
x = Tiempos_por_mes['Tiempo'].mean()

# %%
Fallas = Tiempos['Falla'].str.split(',',expand=True)
columnas = Fallas.columns.values
columnas

lista=[]
for i in columnas:
    
    lista1 =Fallas[i].tolist()
    lista.extend(lista1)

Fallas_MDF = pd.DataFrame(lista,columns=['Falla'])
Fallas_MDF['Cuenta'] = 1

Fallas_MDF = Fallas_MDF.groupby('Falla')['Cuenta'].count().reset_index()
Fallas_MDF = Fallas_MDF.sort_values('Cuenta',ascending=False)
Fallas_MDF['Novedad']= np.where(Fallas_MDF['Falla']!= 'Sin novedad','Novedad','Sin novedad')

# %%
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.layout = html.Div(className='two-thirds',children =[

#Título y subtítulo


html.Div([
    
            
            html.H1('Generación Monitor diario de FIC',style={'text-align':'center','color':'blue'}), # Título
            html.Span(children=[
                "Desarrollado por ",
                html.B('Omar Andrés Montañez, '),
                html.I('Analista de Datos.'),
                html.Br()
            ]),
               html.Br(style={"line-height": "20"}) ]),

#"Lista desplegable"
        
html.Div(className='row',children=  [ dcc.Dropdown(id='Select_year',
                     options= 
                        
                            Tiempos['Mes_texto'].unique()

                        ,
                        optionHeight=35,
                        multi = False,
                        searchable = True,
                        value=None,
                        placeholder = 'Seleccione un mes',
                        clearable = True,
                        style = {'width':'50%'}
                            ),html.Br(style={"line-height": "20"})]),

#"KPI 1"

html.Div(
    # className='five columns',
    children=[  
            dcc.Graph(id = 'KPI1',figure={})
        
            ],style={'width':'25%','height':'1%','border':'1px','padding':'50px','margin':'100 px auto','display':'inline-block'}) ,

#"KPI 2"

html.Div(
    # className='five columns',
         children=[  
            dcc.Graph(id = 'KPI2',figure={}),
            # html.Br(style={"line-height": "20"})
            ],style={'width':'25%','height':'1%','border':'1px','padding':'50px','margin':'100 px auto','display':'inline-block'}) ,


#"KPI 3"

html.Div(children=[  
            dcc.Graph(id = 'KPI3',figure={}),
            # html.Br(style={"line-height": "20"})
            ],style={'width':'25%','height':'1%','border':'1px','padding':'50px','margin':'100 px auto','display':'inline-block'}) ,

#"Título distribución de tiempos"


html.Div([
    
          html.Br(style={"line-height": "20"}),  
          html.H2('Distribución de  Tiempos',style={'text-align':'left','color':'blue'}),
          html.Br(style={"line-height": "20"}) ]),
 
#"Box plot" 
                      
html.Div(className='five columns',children=[  
            dcc.Graph(id = 'my_graph',figure={})
        
            ],style={'width':'45%'}) ,

#"Histograma probabilidad"
 
html.Div(className='five columns',
        
           children=[ dcc.Graph(id='histogram',figure={}),
                     html.Br(style={"line-height": "20"})
        
            ],style={'width':'45%'}),

#"Título Promedio de tiempo"

html.Div(className='five columns',children=[
          
          html.Br(style={"line-height": "20"}),  
          html.H2('Promedio de Tiempos',style={'text-align':'left','color':'blue'}),
          html.Br(style={"line-height": "20"}) ]),

#"Gráfico de líneas promedio de tiempos "

html.Div(className='six columns',
        
           children=[ dcc.Graph(id='lineplot',figure={})
        
            ],style={'width':'92%'}),

# Título Tiempo según día

html.Div(className='five columns',children=[
          
          html.Br(style={"line-height": "20"}),  
          html.H2('Tiempos por día',style={'text-align':'left','color':'blue'}),
          html.Br(style={"line-height": "20"}) ]),


html.Div(className='six columns',
        
           children=[ dcc.Graph(id='barplot_day',figure={})
        
            ],style={'width':'92%'}),    


#"Título Fallas"

html.Div(className='five columns',children=[
          
          html.Br(style={"line-height": "20"}),  
          html.H2('Tipos de falla presentadas',style={'text-align':'left','color':'blue'}),
          html.Br(style={"line-height": "20"})
        #   dcc.Graph(id = 'Pie_Fallas',figure={}),
        #   dcc.Graph(id = 'Barras_Fallas',figure={})

                ]),

# Gráfico de lineas de fallas

html.Div(className='five columns',
         children=[html.Br(style={"line-height": "100"}),
             dcc.Graph(id = 'Pie_Fallas',figure={})
            
              ],style={'width':'92%'}
    ),


html.Div(className='five columns',
         children=[html.Br(style={"line-height": "100"}),
             dcc.Graph(id = 'Barras_Fallas',figure={})
            
              ],style={'width':'45%'}
    )
          
                    ])

        

@app.callback(Output('KPI1','figure'),[Input('Select_year','value')])

def update_graph4(Select_year):
    
    if Select_year == None:
        
        Numero_de_Dias = len(Tiempos.index)
        
        KPI1 = go.Figure()

        KPI1.add_trace(go.Indicator(
        align = 'center',mode='number',value=Numero_de_Dias,
        title={
        'text':'Número de días',
        'font':{
            'size':40
            }
         }   
        )

             )
        
        
    else:       
         
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year]
        
        Numero_de_Dias = len(Grafico.index)
    
        KPI1 = go.Figure()

        KPI1.add_trace(go.Indicator(
        align = 'center',mode='number',value=Numero_de_Dias,
        title={
        'text':'Número de días',
        'font':{
            'size':40
            }
         }   
        )

             )
        
    
    return KPI1

@app.callback(Output('KPI2','figure'),[Input('Select_year','value')])

def update_graph5(Select_year):
    
    if Select_year == None:
        
        Tiempo_Promedio = round(Tiempos['Tiempo'].mean(),2)
        Max_mes= Tiempos['Mes_texto'].max()
  

        KPI2 = go.Figure()

        KPI2.add_trace(go.Indicator(
            align = 'center',mode='number',value=Tiempo_Promedio,
            title={
            'text':'Tiempo Promedio',
            'font':{
            'size':40
            }
         }   
            )
             )
        
        
    else:       
         
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year]
        Tiempo_Promedio = round(Grafico['Tiempo'].mean(),2)
        Max_mes= Grafico['Mes_texto'].max()
        
        Numero_de_Dias = len(Grafico.index)
    
        KPI2 = go.Figure()

        KPI2.add_trace(go.Indicator(
            align = 'center',mode='number',value=Tiempo_Promedio,
            title={
            'text':'Tiempo Promedio',
            'font':{
            'size':40
            }
         }   
            )
             )
        
    
    return KPI2

@app.callback(Output('KPI3','figure'),[Input('Select_year','value')])

def update_graph6(Select_year):
    
    if Select_year == None:
        
        Ultima_Semana = Tiempos.tail(5)
        Tiempo_Promedio_Ultima_Semana= round(Ultima_Semana['Tiempo'].mean(),2)


        KPI3 = go.Figure()

        KPI3.add_trace(go.Indicator(
            align = 'center',mode='number',value=Tiempo_Promedio_Ultima_Semana,
            title={
            'text':'Tiempo prom última semana',
            'font':{
            'size':25
            }
         }   
            )
             )
        
        
    else:       
         
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year]
        Ultima_Semana = Grafico.tail(5)
        Tiempo_Promedio_Ultima_Semana= round(Ultima_Semana['Tiempo'].mean(),2)
    
        KPI3 = go.Figure()

        KPI3.add_trace(go.Indicator(
            align = 'center',mode='number',value=Tiempo_Promedio_Ultima_Semana,
            title={
            'text':'Tiempo prom última semana',
            'font':{
            'size':25
            }
         }   
            )
             )
        
    
    return KPI3
   
@app.callback(Output('my_graph','figure'),[Input('Select_year','value')])

def update_graph(Select_year):
    
    if Select_year == None:
        
        boxplot = px.box(Tiempos,y=Tiempos['Tiempo'],color= Tiempos['Mes'],title= 'Distribución Tiempos MDF')
        
        boxplot.update_layout(legend=dict(
        orientation="v",
     
        ))
        
        
    else:       
         
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year]
    
        boxplot = px.box(Grafico,y=Grafico['Tiempo'],points="all",color_discrete_sequence = ['green'],title= 'Distribución Tiempos MDF')
        
    
    return boxplot


@app.callback(Output('histogram','figure'),[Input('Select_year','value')])

def update_graph_2(Select_year):
    
    if Select_year == None:
        
     histogram = px.histogram(Tiempos, x="Tiempo",title='Histograma de probabilidad de tiempos MDF',nbins= 8,labels={'Tiempo':'Tiempo (min)', 'count':'Frecuencia'},text_auto='.2f',histnorm='probability',color_discrete_sequence=['gray'])
     
    
     
    else: 
    
     Grafico2 = Tiempos[Tiempos['Mes_texto']==Select_year]
        
     histogram = px.histogram(Grafico2, x="Tiempo",title='Histograma de probabilidad de tiempos MDF',nbins= 8,labels={'Tiempo':'Tiempo (min)', 'count':'Frecuencia'},text_auto='.2f',histnorm='probability',color_discrete_sequence=['gray'])
            
    return histogram


@app.callback(Output('lineplot','figure'),[Input('Select_year','value')])

def update_graph_3(Select_year):
    
    if Select_year == None:
        
     Line = px.line(Tiempos_por_mes,x = 'Mes', y = 'Tiempo',title = "Tiempo promedio generación MDF por mes",markers = True,text='Tiempo')

     x0 = Tiempos_por_mes['Mes'].iloc[0]            
     x1 = Tiempos_por_mes['Mes'].iloc[-1] 
     xm = Tiempos_por_mes['Mes'].iloc[len(Tiempos_por_mes)//2] 
     Media_tiempos = mean(Tiempos_por_mes['mean'])

     Line.add_shape(type="line",
     x0=x0, y0=Media_tiempos, x1=x1, y1=Media_tiempos,
     line=dict(color="Green",width=3))

     Line.add_annotation(x=xm, y=Media_tiempos,
     text=f'Tiempo Promedio={round(Media_tiempos,2)} min',
     showarrow=False,
     yshift=10)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                        x=Tiempos_por_mes['Mes'].iloc[1] , y=35.8,
            text='No traer todos los datos',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[1] , y=35.8,
            text='No traer todos los datos',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[2] , y=28.1,
            text='Ajuste Scripts <br> Web Scrapping',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[3] , y=26.8,
            text='Script para <br> archivo SFC',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[4] , y=28.2,
            text='Script para <br> completar sondeo',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

     Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[6] , y=32.2,
            text='Fallas scripts <br> y memoria',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)
              
     Line.update_traces(textposition= 'top center')
     
    
     
    else: 
    
        Line = px.line(Tiempos_por_mes,x = 'Mes', y = 'Tiempo',title = "Tiempo promedio generación MDF por mes",markers = True,text='Tiempo')

        x0 = Tiempos_por_mes['Mes'].iloc[0]            
        x1 = Tiempos_por_mes['Mes'].iloc[-1] 
        xm = Tiempos_por_mes['Mes'].iloc[len(Tiempos_por_mes)//2] 
        Media_tiempos = mean(Tiempos_por_mes['mean'])

        Line.add_shape(type="line",
        x0=x0, y0=Media_tiempos, x1=x1, y1=Media_tiempos,
        line=dict(color="Green",width=3))

        Line.add_annotation(x=xm, y=Media_tiempos,
        text=f'Tiempo Promedio={round(Media_tiempos,2)} min',
        showarrow=False,
        yshift=10)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                        x=Tiempos_por_mes['Mes'].iloc[1] , y=35.8,
            text='No traer todos los datos',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[1] , y=35.8,
            text='No traer todos los datos',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[2] , y=28.1,
            text='Ajuste Scripts <br> Web Scrapping',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[3] , y=26.8,
            text='Script para <br> archivo SFC',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[4] , y=28.2,
            text='Script para <br> completar sondeo',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)

        Line.add_annotation(font=dict(color='black',size=8,family="Arial Black"),
                         x=Tiempos_por_mes['Mes'].iloc[6] , y=32.2,
            text='Fallas scripts <br> y memoria',
            showarrow=False,
            yshift=20,
            bordercolor='black',
            bgcolor="#CFECEC"
            , opacity=0.8)
              
        Line.update_traces(textposition= 'top center')
            
    return Line

@app.callback(Output('Barras_Fallas','figure'),[Input('Select_year','value')])


def update_graph7(Select_year):
    
    if Select_year == None:
        
        fallas = px.bar(Fallas_MDF,x='Cuenta',y= 'Falla',title='Fallas presentadas durante la generación del MDF',color='Falla',text= 'Cuenta'
                        ,height=1000,
        width=1330
        )
        fallas.update_traces(textfont_size = 100, textangle = 0, textposition = "outside")
        fallas.update_layout(showlegend=False)
        
        
    else:       
         
        fallas = px.bar(Fallas_MDF,x='Cuenta',y= 'Falla',title='Fallas presentadas durante la generación del MDF',color='Falla',text= 'Cuenta',height=1000,
        width=1330)
        fallas.update_traces(textfont_size = 100, textangle = 0, textposition = "outside")
        fallas.update_layout(showlegend=False)
        
    
    return fallas

@app.callback(Output('Pie_Fallas','figure'),[Input('Select_year','value')])

def update_graph8(Select_year):
    
    if Select_year == None:
        
        pie = px.pie(Tiempos,values='Cuenta',names='Novedad',title='Generación de MDF',hole=.3)
        pie.update_traces(textposition='inside', textinfo='percent+label')
        pie.update_layout(showlegend=False)
        
        
    else:       
        
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year] 
        pie = px.pie(Grafico,values='Cuenta',names='Novedad',title='Generación de MDF',hole=.3)
        pie.update_traces(textposition='inside', textinfo='percent+label')
        pie.update_layout(showlegend=False)
        
    
    return pie

@app.callback(Output('barplot_day','figure'),[Input('Select_year','value')])

def update_graph9(Select_year):
    
    if Select_year == None:
        
        dia = px.bar(Tiempos.groupby(['Dia de la semana'])['Tiempo'].mean().reset_index(),x='Dia de la semana',y= 'Tiempo',title='Promedio tiempos por día'
             ,color='Dia de la semana'
        )

        dia.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'},showlegend=False)
        
        
    else:       
        Grafico = Tiempos[Tiempos['Mes_texto']==Select_year] 
        dia = px.bar(Grafico.groupby(['Dia de la semana','Mes'])['Tiempo'].mean().reset_index(),x='Dia de la semana',y= 'Tiempo',title='Promedio tiempos por día'
             ,color='Mes'
        )
        dia.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        
    return dia   

if __name__ == '__main__':
    app.run_server(debug=True)
    

   
    


