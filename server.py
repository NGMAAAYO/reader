import json
import uvicorn
from fastapi import FastAPI

from playwright.sync_api import sync_playwright

from utils import render, statics, preprocess

app = FastAPI()

@app.get("/")
def get_index():
    return render("index")

@app.get("/reader")
def get_reader(target_url: str, target_head: str, target_tail: str, pre_name: str, next_name: str):
    params = {
        "target_url": target_url,
        "target_head": target_head,
        "target_tail": target_tail,
        "pre_name": pre_name,
        "next_name": next_name
    }
    return render("reader", preprocess(params, None))

@app.get("/statics/{file}")
def get_statics(file):
    return statics(file)

if __name__ == "__main__":
    try:
        uvicorn.run(app, port=16101)
    except KeyboardInterrupt:
        print("Server closed.")
    except Exception as e:
        print(e)