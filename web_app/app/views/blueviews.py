"""
main blueprint to handel all requests.
"""


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

"""
Home page route. 
"""
@app_views.route('/')
def home_page():
    return 'If you are new to this api, please visit <a href="https://github.com/pyrotimux/LittleHelper">GitHub page</a> for documentation.'

"""
Given the list of HelperTable Objects format it to json with page support.
Args:
    page (int): page number to retrieve.
    limit (int): number of items in one page.
    data (list/tuple): list of helpertable objects.
Returns:
    result (json): json object with requested page.
"""
def format_returned_data(page, limit, data, base_url, title):
    start = 0 # place holder in case wrong page was requested
    end = 0
    temp_page = page - 1 # we don't want zero index page so let's increment

    # check boundaries (is start and end between 0 to len(data))
    if len(data) > temp_page * limit and temp_page >= 0:
        start = (temp_page * limit)
        if len(data) >= (temp_page + 1) * limit: 
            end = (temp_page + 1) * limit
        else:
            end = len(data)

    # get prev and next url 
    prev = None
    next = None
    query = ""
    totpages = int( math.ceil(len(data) / float(limit)) )

    if start or end:
        if title != None: 
            query = "&query=" + title
        
        if page > 1:
            prev = base_url + "?page=" + str(page-1) + "&limit=" + str(limit) + query
            
        if page < totpages:
            next = base_url + "?page=" + str(page+1) + "&limit=" + str(limit) + query 
    
    # load data to the dict so we can convert and return as json
    result = {}
    result["success"] = True
    result["pagination"] = {"count": totpages, "current": page, "limit": limit, "prev": prev, "next": next }
    result["indexes"] = { "start": start, "end": end, "total": len(data) }
    result["content-type"]= "application/json"
    result['results'] = []

    for i in range(start, end):
        row = data[i]
        rowdict = {}
        rowdict['id'] = row.Id
        rowdict['title'] = row.Title
        rowdict['plot'] = row.Plot
        rowdict['year'] = row.Year
        rowdict['type'] = row.Type
        rowdict['genre'] = row.Genre
        rowdict['rated'] = row.Rated

        result['results'].append(rowdict)

    return jsonify(result)


"""
Retrieve the data from db using either (mid and mtype) or title.
Args:
    mid (str): id to look up data with.
    mtype (str): type either movie or show.
    title (str): name of the movie or show.
    page (int): page number to retrieve.
    limit (int): number of items in one page.
Returns:
    result (json): json object with requested page.
"""
def get_data_from_db(mid=None, mtype=None, title=None, page=1, limit=5, base_url=None):
    if mid != None: # query with id 
        # query_ind = "SELECT id, title, plot, year, type, genre, rated FROM helpertable WHERE id=:mid and type=:type"
        # t_data = {'mid': mid, 'type': mtype}
        # result = db_session.execute(query_ind, t_data).fetchall()
        result = HelperTable.query.filter(and_(HelperTable.Id == mid, HelperTable.Type == mtype)).all()
    elif title != None: # query with title regex
        result = HelperTable.query.filter(HelperTable.Title.like('%'+title+'%')).all()

    if result != []:
        return format_returned_data(page, limit, result, base_url, title)
    else:
        return jsonify( {'success': False, 'error': 'No result returned.'} )


"""
Validate the request object to see if digits were passed in and 
if not provide a way to recover.
Args:
    defpage (int): default page in case user did not request it.
    deflimit (int): default limit 
    request (dict): flask request args object.
Returns:
    page (int): page from request.
    limit (int): limit from request.
    no_error (str): if there was any error in processing.
    err_msg (str): err message to indicate what happened.
"""
def validate_request(defpage, deflimit, request):
    if "page" in request and "limit" in request:
        page = request["page"]
        limit = request["limit"]

        if not page.isdigit():
            return 0, 0, False, "page is not a digit."
        if not limit.isdigit():
            return 0, 0, False, "limit is not a digit."
        
        return int(page), int(limit), True, ""
    return defpage, deflimit, True, "no page or limit request passed in."


"""
Route to look up movies using id.
Args:
    mid (str): id to look up data with.
RequestArgs:
    page (str): page number to retrieve.
    limit (str): number of items in one page.
Returns:
    result (json): json object with requested page.
"""
@app_views.route('/movie/<mid>', methods=['GET'])
def get_movie_by_id(mid):
    page, limit, no_err, err_msg = validate_request(1, 5, request.args)
    if not no_err:
        return  jsonify( {'success': False, 'error': err_msg} )
    return get_data_from_db(mid=mid, mtype="movie", page=page, limit=limit, base_url=request.base_url)


"""
Route to look up shows using id.
Args:
    mid (str): id to look up data with.
RequestArgs:
    page (str): page number to retrieve.
    limit (str): number of items in one page.
Returns:
    result (json): json object with requested page.
"""
@app_views.route('/show/<mid>', methods=['GET'])
def get_show_by_id(mid):
    page, limit, no_err, err_msg = validate_request(1, 5, request.args)
    if not no_err:
        return  jsonify( {'success': False, 'error': err_msg} )
    return get_data_from_db(mid=mid, mtype="series", page=page, limit=limit, base_url=request.base_url)


"""
Route to search movies and shows.
RequestArgs:
    query (str): name of the movie or show.
    page (str): page number to retrieve.
    limit (str): number of items in one page.
Returns:
    result (json): json object with requested page.
"""
@app_views.route('/search', methods=['GET'])
def search_movies_and_shows():
    page, limit, no_err, err_msg = validate_request(1, 5, request.args)
    if not no_err:
        return  jsonify( {'success': False, 'error': err_msg} )

    if "query" in request.args:
        query = request.args["query"]
        return get_data_from_db(title=query, page=page, limit=limit, base_url=request.base_url)
    else:
        jsonify( {'success': False, 'error': 'No query supplied.'} )



"""
Route to reimport the db.
Returns:
    result (str): result of reimport.
"""
@app_views.route('/reimportdb')
def dbupdater():
    dbimp = DbHelper()
    dbimp.dropdb()
    dbimp.importdb("./in/cacheddata.csv")
    
    return "Imported Successfully!"
