import datetime
import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

STATIC_FOLDER = Path(__file__).parent / "static"
TEMPLATES_FOLDER = Path(__file__).parent / "templates"
DATA_FOLDER = Path(__file__).parent / "data"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)


def load_data(fname: str):
    with (DATA_FOLDER / fname).open() as data_file:
        return json.load(data_file)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/index.html.jinja",
    )


@app.get("/admin/modal", response_class=HTMLResponse)
async def admin_modal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/modal.html.jinja",
    )


@app.get("/admin/tabs/account_requests", response_class=HTMLResponse)
async def admin_account_requests_tab(request: Request):
    data = load_data("account_requests.json")

    def count_entries_with_state(state):
        return len([entry for entry in data if entry["account_request_state"] == state])

    summary = {
        "total": len(data),
        "requested": count_entries_with_state("requested"),
        "pending": count_entries_with_state("pending"),
        "accepted": count_entries_with_state("accepted"),
    }
    return templates.TemplateResponse(
        request=request,
        name="admin/tab_account_requests.html.jinja",
        context={"summary": summary},
    )


@app.get("/admin/tabs/server_status", response_class=HTMLResponse)
async def admin_server_status_tab(request: Request):
    return templates.TemplateResponse(
        request=request, name="admin/tab_server_status.html.jinja", context={}
    )


@app.get("/admin/server/daemons", response_class=HTMLResponse)
async def admin_server_daemons(request: Request):
    daemons = load_data("server_daemons.json")
    # randomize some more interesting data
    for daemon in daemons:
        import random

        if random.random() < 0.1:
            daemon["pids"] = [
                random.randint(100, 1000) for _ in range(random.randint(1, 3))
            ]
            daemon["status"] = "running"
        elif random.random() < 0.2:
            daemon["pids"] = []
            daemon["status"] = "not_running"
    return templates.TemplateResponse(
        request=request,
        name="admin/server_daemons.html.jinja",
        context={"server_daemons": daemons, "now": datetime.datetime.now()},
    )


@app.get("/admin/server/logs", response_class=HTMLResponse)
async def admin_server_logs(request: Request):
    logs = load_data("server_logs.json")
    last_lines = 10
    try:
        last_lines = int(request.query_params.get("server_logs_last_lines", "10"))
    except ValueError:
        pass

    return templates.TemplateResponse(
        request=request,
        name="admin/server_logs.html.jinja",
        context={"log_entries": logs[-last_lines:]},
    )


@app.get("/admin/tabs/site_stats", response_class=HTMLResponse)
async def admin_site_stats_tab(request: Request):
    return templates.TemplateResponse(
        request=request, name="admin/tab_site_stats.html.jinja", context={}
    )


@app.get("/admin/site/stats", response_class=HTMLResponse)
async def admin_site_stats(request: Request):
    data = load_data("site_stats.json")
    return templates.TemplateResponse(
        request=request,
        name="admin/site_stats.html.jinja",
        context={"site_stats": data},
    )


@app.get("/admin/account_requests/table", response_class=HTMLResponse)
async def admin_account_requests_table(request: Request):
    fields = ["organization", "country"] 
    if any(key.startswith("fields.") for key in request.query_params):
        fields = [
            key.removeprefix("fields.")
            for key, value in request.query_params.items()
            if key.startswith("fields.") and value == "on"
        ]
    account_requests = load_data("account_requests.json")

    # filter by query
    if query := request.query_params.get("query"):
        account_requests = filter(
            lambda entry: any(
                query.lower() in str(val).lower() for val in entry.values()
            ),
            account_requests,
        )

    # filter by state
    if state := request.query_params.get("state"):
        account_requests = filter(
            lambda entry: entry["account_request_state"] == state, account_requests
        )

    # select fields
    filter_fields = fields + ["full_name", "email"]
    account_requests = [
        {key: value for key, value in entry.items() if key in filter_fields}
        for entry in account_requests
    ]

    return templates.TemplateResponse(
        request=request,
        name="admin/account_requests_table.html.jinja",
        context={"entries": account_requests, "fields": fields, "state": state},
    )


@app.get("/admin/account_requests/table_config", response_class=HTMLResponse)
async def admin_account_requests_table_config(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/account_requests_table_config.html.jinja",
        context={},
    )
