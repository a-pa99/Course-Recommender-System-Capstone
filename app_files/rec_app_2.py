from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
#import recommender.py. This is the py file that contains the reccomendation model we will be calling in.
import reccomender

app = Dash(__name__)

#this will connect app to render when we're ready
server = app.server

#create table that will be used in final app
def fig1(course_list):
    data = {'Course_Recommendations' : course_list}
    df = pd.DataFrame(data)
    
    fig2 = go.Figure(data = [go.Table(
        header = dict(
            values=["<b>Course Recommendations</b>"],
            line_color='light grey', fill_color='light grey',
            align='center', font=dict(color='black', size=12),height=30
    ),
        cells=dict(
            values=[df['Course_Recommendations']],
            line_color=['#000000'], fill_color=['#3b5998'],
            align='center', font=dict(color='white', size=11), height=30))])
    
    return fig2


app.layout = html.Div(
    [
     html.H1("Course Recommender"),
     html.P('Please enter a job title and the number of recommendations you would like'),
     html.Div([
         dcc.Input(
         id = 'text',
         type = 'text',
         placeholder = "enter job title here",
         debounce = True,),
         
         dcc.Input(id = 'number', type = 'number', placeholder = 'enter number here',debounce = True)
         ]),
     
     html.Br(),
     
     dcc.Graph(id = 'mytable')
         
    ])

@app.callback(
    Output(component_id='mytable', component_property='figure'),
    [Input(component_id='text', component_property='value'),
     Input(component_id='number', component_property='value')
     ],)
#run this when I know which method produces the best results
def update_output(my_text, my_number):
    
    get1 = reccommender.recommender(my_text, my_number)
    return fig1(get1)

#run app
if __name__ =='__main__':
    app.run_server(port=server, debug = True)
    
