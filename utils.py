import re
import requests
from fastapi.responses import HTMLResponse, FileResponse
from playwright.sync_api import sync_playwright

def render(template_file, var_dict={}):
    with open("./templates/{}.html".format(template_file), "r", encoding="utf-8") as f:
        content = f.read()
        for keyword in list(var_dict.keys()):
            try:
                value = var_dict[keyword]
            except:
                raise ValueError("keyword not match")
            content = content.replace("{{" + keyword + "}}", value)
        return HTMLResponse(content=content)

def statics(file_name):
    return FileResponse("./statics/{}".format(file_name))

def get_content(url, driver):
    playwright = sync_playwright().start()
    brower = playwright.chromium.launch()
    page = brower.new_page()
    page.goto(url)
    res = page.content()
    brower.close()
    playwright.stop()
    return res

def filter(string):
    re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>',re.I)
    re_button = re.compile('<s*button[^>]*>[^<]*<s*/s*button*>',re.I)#style
    re_comment = re.compile('<!--[^>]*-->')
    blank_line = re.compile('n+')
    s = re_script.sub('',string)
    s = re_button.sub('',s)
    s = re_comment.sub('',s)
    s = blank_line.sub('n',s)
    return s

def preprocess(params, driver):
    page_source = get_content(params['target_url'], driver)  # page_source must be string represent the web page's source and in UTF-8 encoding
    resp = {}
    url_head = params['target_url'].replace("https://", "").replace("http://", "").split("/")[0]
    url_head = ("https://" if "https://" in params['target_url'] else "http://") + url_head

    if params["target_head"] == "":
        params["target_head"] = "<div id=\"content\">"
    if params["target_tail"] == "":
        params["target_tail"] = "</div>"
    if params["pre_name"] == "":
        params["pre_name"] = "preview_page"
    if params["next_name"] == "":
        params["next_name"] = "next_page"
    
    resp['text'] = page_source.split(params['target_head'])[1].split(params['target_tail'])[0]
    resp['pre'] = page_source.split("var " + params['pre_name'] + " = \"")[1].split("\"")[0]
    resp['next'] = page_source.split("var " + params['next_name'] + " = \"")[1].split("\"")[0]
    if resp['next'][:4] != "http":
        resp['next'] = url_head + resp['next']
    if resp['pre'][:4] != "http":
        resp['pre'] = url_head + resp['pre']
    # menu_text = get_content("/".join(params['target_url'].split("/")[:-1]) + "/", driver)
    # resp["title"] = menu_text.split(params['target_url'].split("/")[-1] + "\">")[1].split("</a>")[0]
    resp["title"] = page_source.split("<title>")[1].split("</title>")[0]
    resp["text"] = filter(resp["text"])
    return resp