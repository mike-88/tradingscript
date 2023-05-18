from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scripts import trading
import os
import plotly.graph_objects as go
from fastapi.staticfiles import StaticFiles

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

def plot_graph(xv, yv, title, xtitle, ytitle):
    fig = go.Figure(data=go.Scatter(x=xv, y=yv))
    fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title=ytitle)
    return fig.to_html(full_html=False)

@router.get("/twoforms", response_class=HTMLResponse)
def form_get(request: Request):
    key = os.getenv("unsplash_key")
    print(key)
    result = "Type a number"
    return templates.TemplateResponse('twoforms.html', context={'request': request, 'result': result})

@router.post("/form2", response_class=HTMLResponse)
def form_post2(request: Request, ticker2: str = Form(...), period: str = Form(...), interval: str = Form(...)):
    tradingscript = trading.trade_stock(ticker=ticker2, period=period, interval=interval)

    result_dict = {
        'Total Trades': tradingscript["Total Trades"],
        'Average Return': round(tradingscript["Average Return"], 2),
        'Sum of all trades': round(tradingscript["Sum"], 2),
        'End balance': round(tradingscript["Balance"], 2)}
    pl_list = tradingscript["TradeList"]

    return templates.TemplateResponse('twoforms.html', context={'request': request, 'ticker2': ticker2, 'trader_div': result_dict, 'pl_list':pl_list})