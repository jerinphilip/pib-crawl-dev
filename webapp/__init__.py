from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from flask_migrate import Migrate
from datetime import datetime, timedelta 
from sqlalchemy import and_
from collections import Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


from . import models as M

migrate = Migrate(app, db)


@app.route('/')


@app.route('/entry/<id>')
def entry(id):
	x =  M.Entry.query.get(id)
	return render_template('entry.html', entry=x)


@app.route('/entry')
def listing():
	x =  M.Entry.query
	# x = x.filter_by(id=id)
	x = x.order_by(M.Entry.date)
	x = x.limit(5)
	x = x.all()
	print(x)
	return render_template('listing.html', entries=x)


@app.route('/parallel')
def parallel():
	src = request.args.get('src')
	tgt = request.args.get('tgt')
	src_entry =  M.Entry.query.get(src)
	tgt_entry =  M.Entry.query.get(tgt)
	return render_template('parallel.html', entries=[src_entry,tgt_entry])


@app.route('/entry2/<id>')
def entry2(id):
	x =  M.Entry.query.get(id)
	delta = timedelta(days = 1)
	start = x.date - delta
	end = x.date + delta 
	qry = M.Entry.query.filter(
        and_(M.Entry.date <= end, M.Entry.date >= start , M.Entry.lang!=x.lang)).all()
	print(len(qry))
	lang_list = []
	for i in qry:
		lang_list.append(i.lang)
	_list = Counter(lang_list).keys()
	count = Counter(lang_list).values()
	print(_list,'\n',count)
	return render_template('entry.html', entry=x)