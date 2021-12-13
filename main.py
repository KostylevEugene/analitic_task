from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from queries import *
from fastapi.templating import Jinja2Templates


''' В данном файле находится сервис, который выводит аналитический отчет. '''


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
@app.get("/item", response_class=HTMLResponse)
async def root(request: Request):

    functions = {
                "request": request,
                "get_freq_country": get_freq_country(),
                "get_freq_country_fresh_fish": get_freq_country_fresh_fish(),
                "count_not_paid_carts": count_not_paid_carts(),
                "get_amount_freq_users": get_amount_freq_users()}

    return templates.TemplateResponse("item.html", functions)
