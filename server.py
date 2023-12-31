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
    with sync_playwright() as p:
        brower = p.chromium.launch()
        page = brower.new_page()
        page.goto("https://www.biquge.net/197/197503/6912606.html")
        res = page.content()
        brower.close()
    print(res)
    # playwright = sync_playwright().start()
    # browser = playwright.chromium.launch()
    # global page
    # page = browser.new_page()
    uvicorn.run(app, port=16101)
    quit()
    try:
        uvicorn.run(app, port=16101)
    except KeyboardInterrupt:
        browser.close()
        playwright.stop()
        print("Server closed.")
    except Exception as e:
        print(e)
        browser.close()
        playwright.stop()