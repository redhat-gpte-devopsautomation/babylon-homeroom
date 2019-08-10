from flask_wtf import FlaskForm
from wtforms import SubmitField

class ResourceForm(FlaskForm):
    btn_start = SubmitField('Start')
    btn_stop = SubmitField('Stop')
    btn_delete = SubmitField('Delete', 
                             render_kw={'data-toggle': 'modal',
                                        'data-target': '#confirm-delete',
                                        'type': 'button'
                                                  })
    btn_update = SubmitField('Info')
