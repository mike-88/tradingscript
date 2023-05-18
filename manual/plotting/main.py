import plotly.graph_objects as go
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form, Request

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/graph")
async def generate_graph(request: Request, number: int = Form(...)):
    x = [i for i in range(number)]
    y = [i ** 2 for i in range(number)]

    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.update_layout(title="Graph", xaxis_title="X", yaxis_title="Y")

    graph_div = fig.to_html(full_html=False)

    return templates.TemplateResponse(
        "graph.html",
        {"request": request, "graph_div": graph_div},
    )
