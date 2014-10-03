
from flask import Flask, render_template, abort, request, jsonify, Response
from requests import get
from webargs import Arg
from webargs.flaskparser import FlaskParser
import json
from utils import pubdetails, pull_feed
from forms import ContactForm


app = Flask(__name__)

pub_url = "https://cida-eros-pubsdev.er.usgs.gov:8443/pubs-services/"
lookup_url = "https://pubs-test.er.usgs.gov/pubs-services/lookup/"
supersedes_url = 'http://pubs.er.usgs.gov/service/citation/json/extras?'



@app.route('/')
def index():
    return render_template('home.html')

#contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        return 'Form posted.'
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

#leads to rendered html for publication page
@app.route('/publication/<indexId>')
def publication(indexId):
    r = get(pub_url+'publication/'+indexId, params={'mimetype': 'json'}, verify=False)
    pubreturn = r.json()
    #pubdata= pubdetails(pubreturn['pub'])
    return render_template('publication.html', indexID=indexId, pubdata=pubreturn)

#leads to json for selected endpoints
@app.route('/lookup/<endpoint>')
def lookup(endpoint):
    endpoint_list = ['costcenters', 'publicationtypes', 'publicationsubtypes', 'publicationseries']
    endpoint = endpoint.lower()
    if endpoint in endpoint_list:
        r = get(lookup_url+endpoint+'?mimetype=json').json()
        return Response(json.dumps(r),  mimetype='application/json')
    else:
        abort(404)



@app.route('/documentation/faq')
def faq():
    feed_url = 'https://my.usgs.gov/confluence/createrssfeed.action?types=page&spaces=pubswarehouseinfo&title=myUSGS+4.0+RSS+Feed&labelString=pw_faq&excludedSpaceKeys%3D&sort=modified&maxResults=10&timeSpan=600&showContent=true&confirm=Create+RSS+Feed'
    faq_content = pull_feed(feed_url)
    return render_template('faq.html', faq_content=faq_content)

@app.route('/documentation/usgs_series')
def usgs_series():
    feed_url = 'https://my.usgs.gov/confluence/createrssfeed.action?types=page&spaces=pubswarehouseinfo&title=myUSGS+4.0+RSS+Feed&labelString=usgs_series&excludedSpaceKeys%3D&sort=modified&maxResults=10&timeSpan=3600&showContent=true&confirm=Create+RSS+Feed'
    usgs_series_content = pull_feed(feed_url)
    return render_template('usgs_series.html', usgs_series_content=usgs_series_content)

@app.route('/documentation/web_service_documentation')
def web_service_docs():
    feed_url = 'https://my.usgs.gov/confluence/createrssfeed.action?types=page&spaces=pubswarehouseinfo&title=myUSGS+4.0+RSS+Feed&labelString=pubs_webservice_docs&excludedSpaceKeys%3D&sort=modified&maxResults=10&timeSpan=3650&showContent=true&confirm=Create+RSS+Feed'
    web_service_docs = pull_feed(feed_url)
    return render_template('webservice_docs.html', web_service_docs=web_service_docs)

@app.route('/documentation/other_resources')
def other_resources():
    feed_url = 'https://my.usgs.gov/confluence/createrssfeed.action?types=page&spaces=pubswarehouseinfo&title=myUSGS+4.0+RSS+Feed&labelString=other_resources&excludedSpaceKeys%3D&sort=modified&maxResults=10&timeSpan=3650&showContent=true&confirm=Create+RSS+Feed'
    other_resources = pull_feed(feed_url)
    return render_template('other_resources.html', other_resources=other_resources)


#search args, will be used for the search params and generating the opensearch.xml documentation
search_args = {
    'title': Arg(str, multiple=True),
    'author': Arg(str, multiple=True),
    'year': Arg(str, multiple=True),
    'abstract': Arg(str, multiple=True)
}


#this takes advantage of the webargs package, which allows for multiple parameter entries. e.g. year=1981&year=1976
@app.route('/search/searchwebargs', methods=['GET'])
def api_webargs():
    parser = FlaskParser()
    args = parser.parse(search_args, request)

    print 'webarg param: ', args
    #TODO: map the webargs to the Pubs Warehouse Java API, generate output


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    #app.run()
    app.run(port=5000)