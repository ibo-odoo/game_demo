from datetime import timedelta
from odoo import models, fields,api,exceptions

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"


#Button
    @api.multi
    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    @api.multi
    def button_reset(self):
       for rec in self:
           rec.state='draft'

    @api.multi
    def button_cancel(self):
       for rec in self:
           rec.write({'state': 'cancel'})

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),
        ('cancel', 'Cancelled'), ], required=True, default='draft')


    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")
#Duplication

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)


#SQL constraint

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
#DEFAULT VALUE
    start_date = fields.Date(default=fields.Date.today)
    #start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
#kanban view
    color = fields.Integer()
#image
    image = fields.Binary()
#drop down menu by selection
    tax_id = fields.Integer()
#radio button
    recommended_activity_type_id = fields.Many2one('openacademy.course',string="Activity")
#many2one
    currency_id = fields.Many2one('openacademy.course',string="Currencyid")
#many2many tag
    category_id = fields.Many2many('res.users',string="category")
#one2many
    # turtles = fields.One2many('res.users',string="Turtle")
#floattoggle
    days_to_close = fields.Float()
#datepicker
    datefield = fields.Date()
#datetime
    datetimefield = fields.Datetime()
#monetary
    value = fields.Monetary()
#integer
    int_value = fields.Integer()
#float
    factor = fields.Float()
#active
    activate = fields.Boolean()
#stateinfo
    payslip_count = fields.Float()
#percentpie
    replied_ratio = fields.Float()

    instructor_id = fields.Many2one('res.partner', string="Instructor")
#DOMAIN
    #instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True),
                     #('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',
        ondelete='cascade', string="Course") #required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

#DEPENDENCIES
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

#For calendar view
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')

#Gantt view
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')

#Graph view
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

#ONCHANGE
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
#For Calendar View
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

#Gantt view
    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

#Graph view

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

#PYTHON Constraint

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")  


#teacher
class Teachers(models.Model):
    _name = 'academy.teachers'
    _inherit = 'mail.thread'

    name = fields.Char()
    biography = fields.Html()
    #course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")
    course_ids = fields.One2many('product.template', 'teacher_id', string="Courses")

class Courses(models.Model):
    #_name = 'academy.courses'
    _inherit = 'product.template'

    #name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")
          