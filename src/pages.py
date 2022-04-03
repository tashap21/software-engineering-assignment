from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Event
from . import db

pages = Blueprint("pages", __name__)


@pages.route("/")
@pages.route("/dashboard")
@login_required
def dashboard():
    # collect of the events in the events table
    events = Event.query.all()
    return render_template("dashboard.html", user=current_user, events=events)


@pages.route("/create-event", methods=['GET', 'POST'])
@login_required
def create_event():

    if request.method == 'POST':
        event = request.form.get("event")
        eventtime = request.form.get("eventtime")
        description = request.form.get("description")

        # the event name, time and description is required
        if not event:
            flash('Event name cannot be empty', category='error')
        elif not eventtime:
            flash('Time and date of the event cannot be empty', category='error')
        elif not description:
            flash('Description of the event cannot be empty', category='error')
        else:
            event = Event(event=event, eventtime=eventtime,
                          description=description, creator=current_user.id)
            db.session.add(event)
            db.session.commit()
            flash('Event created', category='success')
            return redirect(url_for('pages.dashboard'))

    return render_template('create_event.html', user=current_user)
