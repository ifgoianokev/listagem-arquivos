from flask import Flask
from markupsafe import escape
import os

#caminho para a pasta
PATH = r""


#tipos de arquivo que voce quer que apareca
EXT = (      
    ".html",
    ".css",
    ".js",
    ".py",
    ".lua",
    ".java"
)


app = Flask(__name__)

@app.route('/file/<path:name>')
def file(name):
    path = f"{PATH}\{name}"
    with open(path, encoding="UTF-8") as file:
        texto = file.read()
    return f"""<html>
    <head><meta charset="UTF-8"></head>
    <body>
        <pre>{escape(texto)}</pre>
    </body>
</html>
    """


def return_html_folder(path, relative):
    pad = 0
    if relative != '':
        pad = 30
    html = f'<div  style="padding-left:{pad}px">'
    for file in os.listdir(path):
        p = path+'\\'+file
        relative_file = relative+'\\'+file
        if os.path.isfile(p):
            if file.endswith(EXT):
                html += f'<a href="/file{relative_file}">{file}</a>\n'
        elif os.path.isdir(p):
            html += f'<details><summary>{file}</summary>'
            html += return_html_folder(p, relative_file)
            html += '</details>'
    html += '</div>'
    return html


@app.route('/')
def index():
    folder_name = PATH.split('\\')[-1]
    return f"<h1 style='font-size: 60px'>{folder_name}</h1><pre style='font-size: 40px'>{return_html_folder(PATH, '')}</pre>"