from flask import (render_template, request, Blueprint,
                    redirect,  flash, url_for)
from webApp import db
from webApp.models import Entry
from webApp.main.forms import EntryForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    entries = Entry.query.all()
    return render_template('index.html', title='Home', entries=entries)


@main.route("/entry/new", methods=['GET', 'POST'])
def new_entry():
    form = EntryForm()

    if form.validate_on_submit():
        entry = Entry(title=form.title.data, description=form.description.data)
        db.session.add(entry)
        db.session.commit()
        flash('Your entry has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_entry.html', title='New Entry',
                           form=form)

@main.route("/entry/<int:entry_id>/delete", methods=['POST'])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Your entry has been deleted!', 'success')
    return redirect(url_for('main.home'))


@main.route("/about")
def about():
    return render_template('about.html', title='About')

