from typing import Union
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup


app = FastAPI()

class Recipe(BaseModel):
    url: str

@app.post("/recipes/summary")
def title(request : Recipe):
    URL = request.url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find(id='article-heading_1-0')
    rating = soup.find(id='mntl-recipe-review-bar__rating_1-0')
    description = soup.find(id='article-subheading_1-0')
    updated = soup.find(class_='mntl-attribution__item-date')
    details = soup.findAll(class_='mntl-recipe-details__value')

    return {"title": title.text.strip(), "rating": rating.text.strip(), "description": description.text.strip(), 
    "updated": updated.text.strip(), "Prep Time": details[0].text.strip(), "Cook Time": details[1].text.strip(), "Total Time": details[2].text.strip(), "Servings": details[3].text.strip() }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
