from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(
    title="HTML Content Fetcher",
    description="This API fetches and returns the HTML content of a provided URL.",
    version="1.0.0",
    servers=[
        {
            "url": "https://project1-1-7tyj.onrender.com",  # 🔁 Replace with your deployed server address
            "description": "Production Server"
        }
    ]
)

class URLData(BaseModel):
    """Model containing the URL to fetch HTML from."""
    url: str = Field(..., description="The URL to fetch HTML content from.")

@app.post("/fetch-html/", response_description="HTML content of the provided URL")
def fetch_html(data: URLData):
    """
    Fetch and return HTML from a given URL using HTTP GET.

    Args:
        data (URLData): JSON body with 'url' field.

    Returns:
        dict: A dictionary with key 'html_content'.
    """
    try:
        response = requests.get(data.url)
        response.raise_for_status()
        return {"html_content": response.text}
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")

