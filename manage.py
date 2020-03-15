from flask import Flask
from flask import render_template
from flask import jsonify
import flickrapi
from flask import request,redirect
from flask import session
from flask import url_for
app = Flask(__name__)
app.secret_key = b"my_secret_key"



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'stringval' in request.form:
        keywords = request.form.get('stringval')
        return redirect("pictures/" + keywords)
    return render_template("home.html")

@app.route('/pictures/<keyword>')
def hello(keyword=None):
    flickr = flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)

    photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         tags=keyword,
                         extras='url_c',
                         per_page=100,  
                         sort='relevance')
    urls = []
    count = 0
    for i, photo in enumerate(photos):

        url = photo.get('url_c')
        if url is None:
            continue
        count += 1
        urls.append(url)

        if count > 31:
            break
    #return jsonify(urls)
    session['urls'] = urls
    return render_template('pictures.html', urls=urls)

@app.route('/picturestext/<link>', methods=['GET', 'POST'])
def text(link):
    url = session['urls'][int(link)]
    dict = {"up": -10, "middle": 40, "bottom": 95}
    if request.method == 'POST':
        text = request.form.get('Text')
        position = request.form.get('Select')
        num = dict[position]
        return render_template('combine.html', text = text, num = num, url = url)
    
    return render_template('text.html', url = url)


if __name__ == '__main__':
    app.debug = True
    app.run()