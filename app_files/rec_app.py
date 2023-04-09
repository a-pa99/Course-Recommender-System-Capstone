from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import recco
#import app3 #This is the py file that contains the reccomendation model in it.


app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])

#this will connect app to render when we're ready
server = app.server

input_types = ("text", "number",)

app.layout = html.Div(
    [
     html.H1("Course Recommender"),
     html.P('Please enter a job title and the number of recommendations you would like'),
     html.Div([
         dcc.Input(
         id = 'my_{}'.format(x),
         type = x,
         placeholder = "insert {}".format(x),
         debounce = True,
         size = 25
         
         ) for x in input_types]),
     
     html.Br(),
     
     dcc.Graph(id = 'mytable')
         
    ])

@app.callback(
    Output(component_id='mytable', component_property='figure'),
    [Input(component_id='my_{}'.format(x), component_property='value')
     for x in input_types
     ],)
#run this when I know which method produces the best results
def update_output(value):
    get1 = recco.recommender(value)
    return fig1(get1)

#create table that will be used in final app
def fig1(course_list):
    data = {'Course_Recommendations' : course_list}
    df = pd.DataFrame(data)
    
    fig1 = go.Figure(data = [go.Table(
        header = dict(
            values=["<b>Course Recommendations</b>"],
            #line_color='white', fill_color='white',
            align='center', font=dict(color='black', size=12),height=30
    ),
        cells=dict(
            values=[df['Course_Recommendations']],
            #line_color=['#000000'], fill_color=['#3b5998'],
            align='center', font=dict(color='white', size=11), height=30))])
    
    return fig1

#run app
if __name__ =='__main__':
    #app.run_server(port=8080)
    app.run_server(debug=False)

#add input component; string and number
#add title
#add instructions