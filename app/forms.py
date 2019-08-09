from flask_wtf import FlaskForm
from wtforms import SubmitField

class ResourceForm(FlaskForm):
    btn_start = SubmitField('Start')
    btn_stop = SubmitField('Stop')
    btn_delete = SubmitField('Delete')
    btn_update = SubmitField('Info')

class ConfirmDeleteForm(FlaskForm):
    btn_confirm = SubmitField('Delete')
    btn_cancel  = SubmitField('Cancel')

