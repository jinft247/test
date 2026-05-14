import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import random

# 1. 메뉴 데이터 정의
MENU_DATA = {
    "한식": ["김치찌개", "비빔밥", "제육볶음", "불고기", "된장찌개"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "볶음밥"],
    "일식": ["돈카츠", "초밥", "라멘", "규동", "소바"],
    "양식": ["파스타", "피자", "스테이크", "햄버거", "샐러드"],
    "분식": ["떡볶이", "튀김", "순대", "라면", "김밥"]
}

app = dash.Dash(__name__)

# 2. 레이아웃 설정
app.layout = html.Div([
    # 사이드바
    html.Div([
        html.H2("카테고리 선택", style={'textAlign': 'center'}),
        html.Hr(),
        html.Div([
            html.Div([
                html.Label(f"[{cat}]", style={'fontWeight': 'bold', 'marginTop': '10px', 'display': 'block'}),
                dcc.Checklist(
                    id={'type': 'menu-check', 'index': cat},
                    options=[{'label': m, 'value': m} for m in menus],
                    value=menus[:2],
                    style={'marginBottom': '15px'}
                )
            ]) for cat, menus in MENU_DATA.items()
        ])
    ], style={
        'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0,
        'width': '250px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'overflowY': 'auto'
    }),

    # 본문 영역
    html.Div([
        html.H1("오늘의 점심 룰렛", style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='roulette-graph', config={'displayModeBar': False}),
        ], style={'display': 'flex', 'justifyContent': 'center'}),
        
        html.Div([
            html.Button('룰렛 돌리기!', id='spin-button', n_clicks=0, 
                        style={'fontSize': '20px', 'padding': '10px 30px', 'cursor': 'pointer', 
                               'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'borderRadius': '5px'}),
        ], style={'textAlign': 'center', 'marginTop': '20px'}),
        
        html.Div(id='result-display', style={'textAlign': 'center', 'marginTop': '30px', 'fontSize': '24px', 'color': '#e44d26'})
    ], style={'marginLeft': '300px', 'padding': '20px'})
])

# 3. 콜백 함수
@app.callback(
    [Output('roulette-graph', 'figure'),
     Output('result-display', 'children')],
    [Input('spin-button', 'n_clicks'),
     Input({'type': 'menu-check', 'index': dash.ALL}, 'value')]
)
def update_roulette(n_clicks, selected_lists):
    all_selected = [menu for sublist in selected_lists for menu in sublist]
    
    if not all_selected:
        return go.Figure().update_layout(title="메뉴를 선택해주세요!"), "메뉴를 선택하세요."

    # 룰렛 차트 구성
    fig = go.Figure(data=[go.Pie(
        labels=all_selected,
        values=[1] * len(all_selected),
        hole=.3,
        showlegend=False,
        textinfo='label',
        marker=dict(colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FFD700'] * 10)
    )])

    result_text = ""
    if n_clicks > 0:
        winner = random.choice(all_selected)
        rotation = random.randint(0, 360)
        fig.update_layout(rotation=rotation)
        result_text = f"오늘의 추천 메뉴: {winner}!"
    
    fig.update_layout(width=500, height=500, margin=dict(t=0, b=0, l=0, r=0))
    return fig, result_text

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)