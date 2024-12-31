from datetime import datetime
from werkzeug.exceptions import NotFound

from flask_login import current_user
from app.model import Schedule
from flask import request, flash
from sqlalchemy.exc import SQLAlchemyError
from app.model import db


# Function to handle editing an existing schedule
def edit_schedule(sch_id: int):
    try:
        # Fetching by ID
        schedule_to_edit = Schedule.query.get_or_404(sch_id)

        schedule_to_edit.cs = request.form["cs"]
        schedule_to_edit.week = int(request.form["week"])
        schedule_to_edit.carrier = request.form["carrier"]
        schedule_to_edit.service = request.form["service"]
        schedule_to_edit.mv = request.form["mv"]
        schedule_to_edit.pol = request.form["pol"]
        schedule_to_edit.pod = request.form["pod"]
        schedule_to_edit.routing = request.form["routing"]
        schedule_to_edit.cyopen = datetime.strptime(request.form["cyopen"], "%Y-%m-%d")
        schedule_to_edit.sicutoff = datetime.strptime(
            "{year} {time}".format(
                year=request.form["sicutoff"],
                time=request.form["sicutoff_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        schedule_to_edit.cycvcls = datetime.strptime(
            "{year} {time}".format(
                year=request.form["cycvcls"],
                time=request.form["cycvcls_time"],
            ),
            "%Y-%m-%d %H:%M",
        )
        schedule_to_edit.etd = datetime.strptime(request.form["etd"], "%Y-%m-%d")
        schedule_to_edit.eta = datetime.strptime(request.form["eta"], "%Y-%m-%d")
        schedule_to_edit.owner = current_user.id
        db.session.commit()
        flash("Schedule updated successfully!", "success")
        return True
    except NotFound:
        flash(
            "Schedule not found, please try again. No changes were made to the database."
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return False
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return False
