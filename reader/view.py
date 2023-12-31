from django.shortcuts import render
import requests
import chardet
import re

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

def view(request):
	return render(request, 'view.html')

def reader(request):
	ctx = {}
	if request.GET:
		r = requests.get(request.GET['target_url'])
		r.encoding = "utf-8"
		if "���" in r.text:
			r.encoding = "gbk"
		content = r.text
		url_head = request.GET['target_url'].replace("https://","").replace("http://","").split("/")[0]
		if "https://" in request.GET['target_url']:
			url_head = "https://" + url_head
		elif "http://" in request.GET['target_url']:
			url_head = "http://" + url_head
		if request.GET['target_head']:
			ctx['text'] = content.split(request.GET['target_head'])[1].split(request.GET['target_tail'])[0]
		else:
			ctx['text'] = content.split("<div id=\"content\">")[1].split("</div>")[0]
		if request.GET['pre_name']:
			ctx['pre'] = content.split("var " + request.GET['pre_name'] + " = \"")[1].split("\";")[0]
		else:
			ctx['pre'] = content.split("var preview_page = \"")[1].split("\";")[0]
		if request.GET['next_name']:
			ctx['next'] = content.split("var " + request.GET['next_name'] + " = \"")[1].split("\";")[0]
		else:
			ctx['next'] = content.split("var next_page = \"")[1].split("\";")[0]
		if "http" not in ctx['next'] and "http" not in ctx['pre']:
			ctx['next'] = url_head + ctx['next']
			ctx['pre'] = url_head + ctx['pre']
		rt = requests.get(request.GET['target_url'].replace(request.GET['target_url'].split("/")[-1], ""))
		rt.encoding = chardet.detect(rt.content)["encoding"]
		rct = rt.text
		ctx["title"] = rct.split(request.GET['target_url'].split("/")[-1] + "\">")[1].split("</a>")[0]
		ctx["text"] = filter(ctx["text"])
		return render(request, 'reader.html', ctx)
	return render(request, 'view.html', ctx)