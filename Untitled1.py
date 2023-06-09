#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import dash
import country_converter as coco
from flask import Flask


# In[2]:


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])


# In[3]:


df = pd.read_csv("globalterrorismdb_0718dist.tar.bz2", compression="bz2")
data= df[['eventid','suicide','success','iyear','imonth','country_txt','nkill',
          'gname','nperps','target1','natlty1_txt','weaptype1_txt','attacktype1_txt','latitude','longitude']]


# In[4]:


avea= data.groupby('iyear').count()['eventid'].reset_index()
round(avea[avea['eventid']!=0].mean()['eventid'])


# In[5]:


data.loc[data['country_txt'] == 'West Germany (FRG)', 'country_txt'] = 'Germany'
data.loc[data['country_txt'] == 'East Germany (GDR)', 'country_txt'] = 'Germany'


# In[6]:


data_country= data['country_txt'].unique().tolist()
data_country=sorted(data_country)
data_year= data['iyear'].unique().tolist()
data_attack_type = data['attacktype1_txt'].unique().tolist()
data_group= data['gname'].unique().tolist()


# In[ ]:





# In[7]:


def generate_chart(data, x_column, y_column, chart_type, tebal=None):
    if chart_type == 'bar':
        fig = px.bar(data_frame=data, x=x_column, y=y_column,text_auto=True)
        fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    elif chart_type == 'scatter':
        fig = px.scatter(data_frame=data, x=x_column, y=y_column)
    elif chart_type == 'line':
        fig = px.line(data_frame=data, x=x_column, y=y_column)
        fig.update_layout(xaxis={'tickangle': 60},yaxis_title=None)
    elif chart_type == 'pie':
        fig= px.pie(data_frame=data, values=x_column,names=y_column)
    elif chart_type=='treemap':
        fig= px.treemap(data_frame=data, path=x_column, values=y_column)
    elif chart_type=='choropleth':
        fig= px.choropleth(data_frame=data, locations=x_column,locationmode=location_mode ,color=y_column,color_continuous_scale=['white','black'])
    else:
        raise ValueError("Invalid chart type. Please choose 'bar', 'scatter', or 'line'.")
    fig.update_layout(width=1300, height=850, title={'x':0.5,'y':0.975},title_font=dict(size=30),
                      xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),plot_bgcolor='black',paper_bgcolor='gray')
    fig.update_traces(marker=dict(line=dict(color='blue', width=2)))
    return fig


# In[8]:


fig2_data= data.groupby(['iyear','imonth']).agg({'eventid': 'count', 'nkill': 'sum'}).reset_index()
fig2_data['yearsize']= fig2_data['iyear'].astype(str) +"-"+ fig2_data["imonth"].astype(str)
fig3_data= data.groupby(['country_txt','attacktype1_txt']).count()['eventid'].reset_index()
data4= data.pivot_table(index='country_txt',values='eventid',columns='iyear',aggfunc='count') 
data4.pct_change(axis=1)*100
fig4_data= data4.mean(axis=1).reset_index().sort_values(0,ascending=False)
fig5_data= fig2_data.groupby('iyear').sum()['nkill'].reset_index()


# In[9]:


fig1= generate_chart(data, data['iyear'].unique(),
                     data.groupby('iyear')['eventid'].count().reset_index()['eventid'],'line')
fig2= generate_chart(fig2_data,'eventid', 'nkill','scatter')
fig3= generate_chart(fig3_data,['country_txt','attacktype1_txt'], 'eventid','treemap')
#fig4= generate_chart(fig4_data, 'country_txt',0,'choropleth','country names')
fig4= px.choropleth(fig4_data, locations='country_txt',locationmode='country names' ,color=0,color_continuous_scale=['white','black'])
fig4.update_layout(
    width=2620, 
    height=800)
fig4.update_layout(coloraxis_showscale=False)
fig4.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig5= generate_chart(fig5_data, 'iyear','nkill','bar')


# In[10]:


card_total_case = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Total Terrorism Case",style={'text-align':'center','font-size':'50px',
                                                  'text-decoration': 'underline'}),
            html.P(id='jumlah-kasus', style={'font-size': '60px', 'text-align': 'center'}),
        ]
    ),
    style={"width": "580px","height":'235px','margin-top':'20px','outline': '8px solid white'},
    id='cardstotalcase'
)


# In[11]:


card_average_case = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Avearage Case per Year",style={'text-align':'center','font-size':'50px',
                                                    'text-decoration': 'underline'}),
            html.P(id='average-kasus', style={'font-size': '60px', 'text-align': 'center'}),
        ]
    ),
    style={"width": "580px","height":'235px','margin-top':'20px','outline': '8px solid white'},
    id='cardaveragecase'
)


# In[12]:


card_average_victim = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Total Victim",style={'text-align':'center','font-size':'50px',
                                                    'text-decoration': 'underline'}),
            html.P(id='totalvictim', style={'font-size': '60px', 'text-align': 'center'}),
        ]
    ),
    style={"width": "580px","height":'235px','margin-top':'20px','outline': '8px solid white'},
    id='totalvictimkilled'
)


# In[13]:


radioitem= dcc.RadioItems(options=[
                                    {'label': 'Country', 'value': 'Country'},
                                    {'label': 'Year', 'value': 'Year'},
                                    #{'label': 'Attack Type', 'value': 'Attack Type'},
                                    {'label': 'Group Terrorist', 'value': 'Group Terrorist'}],value= 'Year', id='radiobutton',
                          style={'font-size':'40px', 'margin-bottom':'40px'},
                         inputStyle={'width': '40px', 'height': '40px','margin-left': '20px','margin-right': '20px'})


# In[14]:


dropdown= dcc.Dropdown([{'label':name ,'value': name} for name in data_country],value=None,id='iddropdown', 
                       placeholder='Please Choose',style={'height':'60px','margin-left':'10px','margin-right':'40px',
                                                          'margin-bottom':'20px','font-size':'25px'}
                       )


# In[15]:


menu = html.Div(
    children=[
        html.H2('FILTERS', style={'font-size': '54px', 'text-align': 'center','margin-bottom': '30px'}),
        dbc.Row(
            [
                dbc.Col(radioitem),
            ],
            style={'width': '100%'}
            ),
        dbc.Row([dbc.Col(dropdown)],style={'width':'100%'}),
        dbc.Button('Submit', id='button',n_clicks=0,style={
            'font-size': '40px',
            'background-color': 'blue',
            'color': 'white',
            'text-align': 'center',
            'width': '200px',
            'height': '100px',
            'margin': '20px'})
    ],
     style={'margin-left':'30px','outline': '8px solid white','background-color': 'rgba(125, 125, 125, 0.5)'}
)


# In[16]:


title= html.Div('Terrorism Hotspots Dashboard',style=
                {'font-size':'80px','text-align':'center'})


# In[17]:


app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(title, width={"size": 12}),
            justify="center",
            style={"padding-top": "20px", "padding-bottom": "20px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([menu],
                                style={'margin-bottom': '20px','margin-right':'45px'}),
                        dbc.Row([card_total_case], 
                                style={'margin-left': '15px', 'margin-right': '20px', 'margin-bottom': '20px'}),
                        dbc.Row([card_average_case], 
                                style={'margin-left': '15px', 'margin-right': '20px', 'margin-bottom': '20px'}),
                        dbc.Row([card_average_victim], 
                                style={'margin-left': '15px', 'margin-right': '20px', 'margin-bottom': '20px'})
        
                    ],
                    width=2,
                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([dcc.Graph(id="chart4", figure=fig4)], width=10)
                                ],
                                style={"padding": "40px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col([dcc.Graph(id="chart3", figure=fig3)]),
                                    dbc.Col([dcc.Graph(id="chart5", figure=fig5)])
                                ],
                                style={"padding": "40px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col([dcc.Graph(id="chart1", figure=fig1)]),
                                    dbc.Col([dcc.Graph(id="chart2", figure=fig2)])
                                ],
                                style={"padding": "40px"},
                            ),
                        ],
                        style={'padding': "40px", 'outline': '8px solid white'}
                    ),
                    width={"size": '10'},
                    style={'background-color': 'rgba(125, 125, 125, 0.5)'}
                )
            ],
            justify="center",
            style={"padding-bottom": "20px"},
        ),
    ],
    fluid=True
)


# In[18]:


@app.callback(
    Output('iddropdown', 'options'),
    Output('iddropdown', 'style'),
    Input('radiobutton', 'value')
)

def value_dropdown(input_radio):
    if input_radio=='Country':
        a= [{'label':name,'value':name} for name in data_country]
        b= {'font-size':'40px'}
        return a,b
    elif input_radio=='Year':
        a=  [{'label':name,'value':name} for name in data_year]
        b= {'font-size':'40px'}
        return a,b
    elif input_radio=='Group Terrorist':
        a= [{'label':name,'value':name} for name in data_group]
        b= {'font-size':'20px'}
        return a,b
        
    


# In[19]:


@app.callback(
    Output('chart1', 'figure'),
    Output('chart2', 'figure'),
    Output('chart3', 'figure'),
    Output('chart5', 'figure'),
    Output('jumlah-kasus', 'children'),
    Output('average-kasus', 'children'),
    Output('totalvictim', 'children'),
    Output('chart4', 'figure'),
    Input('radiobutton','value'),
    Input('button','n_clicks'),
    State('iddropdown','value')
)
    
def filter_input(data_filter,klik,input_filter):
    filtered_data= data.copy()
    input_filter=input_filter or []
    
    
    if data_filter=='Country' and input_filter is not None and klik>0:
        filtered_data = filtered_data[filtered_data['country_txt']==input_filter]
    if data_filter=='Year'and input_filter is not None and klik>0:
        filtered_data = filtered_data[filtered_data['iyear']==input_filter]
    if data_filter =='Group Terrorist'and input_filter is not None and klik>0:
        filtered_data = filtered_data[filtered_data['gname']==input_filter]
    
    fig2_data= filtered_data.groupby(['iyear','imonth']).agg({'eventid': 'count', 'nkill': 'sum'}).reset_index()
    fig2_data['yearsize']= fig2_data['iyear'].astype(str) +"-"+ fig2_data["imonth"].astype(str)
    fig3_data= filtered_data.groupby(['country_txt','attacktype1_txt']).count()['eventid'].reset_index()
    fig5_data= fig2_data.groupby('iyear').sum()['nkill'].reset_index()
    average_case= filtered_data.groupby('iyear').count()['eventid'].reset_index()
    data4= filtered_data.pivot_table(index='country_txt',values='eventid',columns='iyear',aggfunc='count') 
    data4.pct_change(axis=1)*100
    fig4_data= data4.mean(axis=1).reset_index().sort_values(0,ascending=False)
    
    fig1 = generate_chart(filtered_data, filtered_data['iyear'].unique(),
                     filtered_data.groupby('iyear')['eventid'].count().reset_index()['eventid'],'line')
    fig1.update_layout(title={'text': f'Trend of Terrorism in {input_filter}'},title_font={'size': 40})
    fig1.update_traces(line={'width': 10})
    fig1.update_layout(
    xaxis=dict(
        tickfont=dict(size=20)  # Ubah ukuran font pada sumbu x
    ),
    yaxis=dict(
        tickfont=dict(size=20)  # Ubah ukuran font pada sumbu y
    ))

    fig2 = generate_chart(fig2_data,'eventid', 'nkill','scatter')
    fig2.update_layout(title={'text': f'Correlation Number and Victim of Terrorism in  {input_filter}'},title_font={'size': 40})
    fig2.update_traces(marker=dict(size=15,
                              line=dict(width=4,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
    fig3 = generate_chart(fig3_data,['country_txt','attacktype1_txt'], 'eventid','treemap')
    fig3.update_layout(title={'text': f'Distribution of Country and Attack Type in {input_filter}'},title_font={'size': 40})
    fig3.update_layout(font=dict(
        family="Arial",  # Ubah font family sesuai yang diinginkan
        size=30  # Ubah ukuran font sesuai yang diinginkan
    ))
    fig3.update_traces(textfont=dict(size=30))
    fig3.update_layout(
    xaxis=dict(
        tickfont=dict(size=12)  # Ubah ukuran font pada sumbu x
    ),
    yaxis=dict(
        tickfont=dict(size=12)  # Ubah ukuran font pada sumbu y
    ))
    fig5= generate_chart(fig5_data, 'iyear','nkill','bar')
    fig5.update_layout(title={'text': f'Total Victims of Terrorism in {input_filter}'},title_font={'size': 40},font=dict(
        family="Arial",  # Ubah font family sesuai yang diinginkan
        size=30  # Ubah ukuran font sesuai yang diinginkan
    ))
    fig5.update_traces(textfont_size=30, textangle=0, textposition="outside", cliponaxis=False)
    total_case = len(filtered_data['eventid'])
    averages= round(average_case[average_case['eventid'] != 0]['eventid'].mean())
    total_victim= filtered_data['nkill'].sum()
    fig4= px.choropleth(fig4_data, locations='country_txt',locationmode='country names' ,color=0,color_continuous_scale=['white','blue','red'])
    fig4.update_layout(paper_bgcolor='black',title={'text': f'Distribution Terrorism {input_filter}'},title_font={'size': 40},font=dict(
        family="Arial",  # Ubah font family sesuai yang diinginkan
        size=30  # Ubah ukuran font sesuai yang diinginkan
    ),
    margin=dict(l=3, r=3, t=3, b=3, pad=1),
    coloraxis_colorbar=dict(
        x=0.9,  # Ubah posisi horisontal legenda sesuai yang diinginkan
        y=0.5,  # Ubah posisi vertikal legenda sesuai yang diinginkan
        lenmode="fraction",
        len=0.7  # Ubah panjang legenda sesuai yang diinginkan
    )
)
    return fig1,fig2,fig3,fig5,total_case,averages,total_victim,fig4


# In[ ]:


server = app.server


# In[ ]:




