# blog/routes.py
from blog.forms import EntryForm, LoginForm
from flask import render_template, request, session, Blueprint
import functools
from flask import redirect, url_for, flash
from blog.models import Entry, db


bp = Blueprint('blog', __name__)


def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('blog.login', next=request.path))
   return check_permissions


@bp.route('/')
def index():
    # Query published posts from the database
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()

    # Pass the list of posts to the template
    return render_template('homepage.html', all_posts=all_posts)


@bp.route('/drafts/', methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@bp.route("/new-form/", methods=["GET", "POST"])
@login_required
def create_entry():
    return entry_form(entry_id=None)


@bp.route("/edit-post/<int:entry_id>/", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    return entry_form(entry_id)


def entry_form(entry_id=None):
    entry = None
    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        if entry_id:
            entry.title = form.title.data
            entry.body = form.body.data
            entry.is_published = form.is_published.data
            db.session.commit()
        else:
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
        return redirect(url_for('blog.index'))

    return render_template("entry_form.html", form=form)


@bp.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('blog.index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@bp.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('blog.index'))


@bp.route('/delete_entry/<int:entry_id>', methods=['POST', 'DELETE'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('blog.list_drafts'))







