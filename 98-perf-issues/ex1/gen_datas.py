import openerplib
import names
import random

connection = openerplib.get_connection(hostname="localhost",
           port=80,
           database="ex1",
           login="admin",
           password="admin",
           protocol="jsonrpc")
           
co_model = connection.get_model('openacademy.course')
se_model = connection.get_model('openacademy.session')
reg_model = connection.get_model('openacademy.registration')
prtn_model = connection.get_model('res.partner')
prtn_ids = prtn_model.search([])

def _get_attendee():
    if random.randint(1,5)>4:
        new_prtn = prtn_model.create({'name': names.get_full_name()})
        prtn_ids.append(new_prtn)
        return new_prtn
    else:
        return prtn_ids[random.randint(0,len(prtn_ids)-1)]
        
def gen_datas():
    for course in range(1, 100):
        co = co_model.create({'name' : 'Course %s' % course})
        for sess in range(0, random.randint(80, 120)):
            se = se_model.create({
                'name' : 'Session %s of Course %s' % (sess, course),
                'duration': random.randint(1, 10),
                'course_id': co,
                'state': 'draft',
            })
            for att in range(0, random.randint(8, 64)):
                reg_model.create({
                    'session_id': se,
                    'attendee_id': _get_attendee(),
                })
                
def gen_attendees():
    for course in range(4, 300000):
        prtn_model.create({'name': names.get_full_name()})

# gen_attendees()
gen_datas()
