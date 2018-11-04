from flask import render_template, Blueprint, request, flash, redirect, send_file, url_for, jsonify
from DatabaseHelper import DbHelper
from werkzeug.local import LocalProxy
from database import db_session
from flask import current_app as app
import uwsgi
import math
from models import HelperTable
from sqlalchemy import and_, or_, not_


app_views = Blueprint('app_views_views', __name__)
_datastore = LocalProxy(lambda: _security.datastore)


@app_views.route('/')
def home_page():
    return "Hello World!"

def format_returned_data(page=1, limit=5, data=None):
    result = {}
    result["success"] = True
    result["Pagination-Count"] = int( math.ceil(len(data) / float(limit)) )
    result["Pagination-Page"] = page
    result["Pagination-Limit"]= limit
    result["Content-Type"]= "application/json"
    result['results'] = []

    for row in data:
        rowdict = {}
        # id, title, plot, year, type, genre, rated
        rowdict['id'] = row.Id
        rowdict['title'] = row.Title
        rowdict['plot'] = row.Plot
        rowdict['year'] = row.Year
        rowdict['type'] = row.Type
        rowdict['genre'] = row.Genre
        rowdict['rated'] = row.Rated

        result['results'].append(rowdict)

    return jsonify(result)


def get_data_from_db(mid=None, mtype=None, title=None):
    if mid != None:
        # query_ind = "SELECT id, title, plot, year, type, genre, rated FROM helpertable WHERE id=:mid and type=:type"
        # t_data = {'mid': mid, 'type': mtype}
        # result = db_session.execute(query_ind, t_data).fetchall()
        result = HelperTable.query.filter(and_(HelperTable.Id == mid, HelperTable.Type == mtype)).all()
    elif title != None:
        result = HelperTable.query.filter(HelperTable.Title.like('%'+title+'%')).all()

    if result != []:
        return format_returned_data(data=result)
    else:
        return jsonify( {'success': False, 'error': 'Not Found.'} )
         

@app_views.route('/movie/<mid>', methods=['GET'])
def get_movie_by_id(mid):
    return get_data_from_db(mid=mid, mtype="movie")


@app_views.route('/show/<mid>', methods=['GET'])
def get_show_by_id(mid):
    return get_data_from_db(mid=mid, mtype="series")

@app_views.route('/search', methods=['GET'])
def search_movies_and_shows():
    if "query" in request.args:
        query = request.args["query"]
        return get_data_from_db(title=query)


@app_views.route('/reimportdb')
def dbupdater():
    dbimp = DbHelper()
    dbimp.dropdb()
    dbimp.importdb("./in/cacheddata.csv")
    
    return "Imported Successfully!"
