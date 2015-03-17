# -*- coding: utf-8 -*-
# try something like
from plugin_rating_widget import RatingWidget
from tables import *
db = DAL('sqlite:memory:')
db.define_table('rate',
    Field('rating', 'integer',
          requires=IS_IN_SET(range(1, 6)),  # "requires" is necessary for the rating widget
))

#register in events table
db.define_table('register',
                Field('name'),
                Field('event_name'),
                Field('user_id', db.auth_user),
                Field('phone'),
                Field('email'),
                Field('category'),
                Field('date_posted', 'datetime'),
                Field('prof_pic', 'upload'),
                Field('attend', 'boolean', default=False),
                Field('rating', 'integer', requires=IS_IN_SET(range(1,6))), # "requires" is necessary for the rating widget
                #format = '%(title)s',
                )

#Credit for rating plugin: http://dev.s-cubism.com/plugin_rating_widget
# Also referenced: http://ochiba77.blogspot.com/2012/01/web2py-plugin-rating-widget.html
################################ The core ######################################
# Inject the horizontal radio widget
db.register.rating.widget = RatingWidget()
################################################################################


def index():
    form = SQLFORM(db.register)
    if form.accepts(request.vars, session):
        session.flash = 'submitted %s' % form.vars
        redirect(URL('index'))
    return dict(form=form)

#to find the average for ratings
def rateEvent():

    r = db.register()
    
    form = SQLFORM(db.attending)
    if form.process().accepted:
        
        rating_val = form.vars.rating
        event_to_rate = form.vars.event_name
        
        x = db.attending.event_name == event_to_rate
        n = len(x)
        for x in n:
            s = s + x.rating
        avg = 0.0 + s/n
        
        row = db(db.register.id).select()
        db(db.register.id == event_to_rate).update(rating=avg)

        redirect(URL('default', 'index'))
        return dict(form=form)