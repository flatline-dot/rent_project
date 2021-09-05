from flask import Blueprint, render_template, request
from webapp.model import Flat
from webapp.ads.forms import FilterForm


blueprint = Blueprint('ads', __name__)


@blueprint.route('/index', methods=["GET"])
def index():
    form = FilterForm()
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1
    query = Flat.query.paginate(page=page, per_page=25)
    return render_template('index.html', flats=query, form=form)


@blueprint.route('/result', methods=["POST", "GET"])
def result():
    form = FilterForm(request.form)
    query = Flat.query

    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1
    url = 'result'
    if request.method == "POST":
        if form.price_min.data:
            print(form.price_min.data)
            query = query.filter(Flat.price >= form.price_min.data)
        if form.price_max.data:
            query = query.filter(Flat.price <= form.price_max.data)
        if form.rooms.data:
            query = query.filter(Flat.num_rooms.in_(form.rooms.data))
        if form.area_min.data:
            query = query.filter(Flat.area >= form.area_min.data)
        if form.area_max.data:
            query = query.filter(Flat.area <= form.area_max.data)
        if form.material.data:
            query = query.filter(Flat.material.in_(form.material.data))
        if form.commission.data:
            query = query.filter(Flat.commission == 0)
        if form.deposit.data:
            query = query.filter(Flat.deposit == 0)

    query = query.paginate(page=page, per_page=25)
    return render_template('index.html', flats=query, form=form)
