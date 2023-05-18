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

@router.get("/pricefetcher", response_class=HTMLResponse)
def form_get(request: Request):
    key = os.getenv("unsplash_key")
    print(key)
    result = "Type a number"
    return templates.TemplateResponse('pricefetcher.html', context={'request': request, 'result': result})


@router.post("/form1", response_class=HTMLResponse)
def form_post1(request: Request, ticker: str = Form(...), period: str = Form(...), interval: str = Form(...)):
    price = trading.dl_stock(ticker=ticker, period=period, interval=interval)[0]
    dates = trading.dl_stock(ticker=ticker, period=period, interval=interval)[1]
    return templates.TemplateResponse('pricefetcher.html', context={'request': request, 'ticker': ticker, 'graph_div': plot_graph(xv=dates, yv=price, title=ticker, xtitle="Time", ytitle="Stock Price")})