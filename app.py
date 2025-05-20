from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Data Discovery API",
    version="1.0.0",
    description="Search for dashboards, datasets, or reports based on a user's query."
)

@app.get("/api/search", operation_id="searchController_getSearchResults")
def search_data_assets(
    query: str = Query(..., description="The user's natural language question, like 'sales data by region' or 'warranty claim dashboard'.")
):
    results = [
        {
            "title": "Regional Sales Dashboard",
            "type": "Dashboard",
            "link": "https://internal.url/dashboards/sales-region"
        },
        {
            "title": "Warranty Claims Report",
            "type": "Report",
            "link": "https://internal.url/reports/warranty-claims"
        },
    ]
    return {"query": query, "results": results}

# ✅ Proper OpenAPI override with version and servers
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.2"  # <- Force 3.0.2 version
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000"}  # <- Required for some OpenAPI consumers
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
