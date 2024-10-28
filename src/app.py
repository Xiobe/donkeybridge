import os

from flask import Flask, request, redirect, url_for, abort, render_template
import markdown


app = Flask(__name__)
FLASK_DEBUG = True
FLASK_HOST_IP = "0.0.0.0"
FLASK_PORT = 5000

PAGES_DIR = "pages"
MARKDOWN_EXTENSIONS = [ 'abbr', # abbreviations
                       'attr_list', # attribute list
                       'def_list', # definition list
                       'fenced_code', # fenced code blocks
                       'footnotes', # footnotes
                       'md_in_html', # markdown in html
                       'tables', # tables
                       'admonition', # admonition
                       'codehilite', # code hilite
                       'legacy_attrs', # legacy attributes
                       'legacy_em', # legacy emphasis
                       'meta', # meta data
                       'nl2br', # new line to break
                       'sane_lists', # sane lists
                       'smarty', # smarty pants
                       'toc', # table of contents
                       'wikilinks', # wikilinks
                      ]

def load_markdown_file(page: str) -> str:
    """
    Function to load Markdown content from file on disk.
    
    Parameters:
    page (str)    file to load from disk
    """
    filepath = f"{PAGES_DIR}/{page}.md"
    
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()        
    return None

def list_pages() -> list:
    """
    Function to list all markdown files (pages)
    
    Returns:
    list    list of pages
    """
    files = os.listdir(PAGES_DIR)
    return [f.replace(".md","") for f in files if f.endswith(".md")]

@app.route("/")
def index():
    """
    Returns the homepage, listing all available pages.
    """
    return render_template("index.html", name="index", pages=list_pages())

@app.route("/<page>")
def read_page(page):
    """
    Returns a specific page.
    """
    markdown_data = load_markdown_file(page)
    html_data = markdown.markdown(markdown_data, extensions=MARKDOWN_EXTENSIONS)
    return render_template('data.html', page=page, data=html_data)

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
