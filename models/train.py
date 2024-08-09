from odoo import models, fields, api

class TrainCity(models.Model):
    _name = 'train.city'
    _description = 'Train City'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)


class TrainStation(models.Model):
    _name = 'train.station'
    _description = 'Train Station'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    city_id = fields.Many2one('train.city', string='City', required=True)
    address = fields.Text(string='Address')


class TrainTrain(models.Model):
    _name = 'train.train'
    _description = 'Train'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    state = fields.Selection([
        ('ready', 'Ready'),
        ('not_ready', 'Not Ready'),
        ('maintenance', 'Maintenance')
    ], string='State', default='ready')
    active = fields.Boolean(string='Active', default=True)
    schedule_line_ids = fields.One2many('train.schedule', 'train_id', string='Schedules')


class TrainSchedule(models.Model):
    _name = 'train.schedule'
    _description = 'Train Schedule'

    code = fields.Char(string='Code', readonly=True, copy=False, default=lambda self: self._generate_code())
    origin_id = fields.Many2one('train.station', string='Origin', required=True)
    destination_id = fields.Many2one('train.station', string='Destination', required=True)
    schedule_time = fields.Datetime(string='Schedule Time', required=True)
    duration = fields.Float(string='Duration (hours)', required=True)
    arrival_time = fields.Datetime(string='Arrival Time', compute='_compute_arrival_time', store=True)
    train_id = fields.Many2one('train.train', string='Train', required=True)
    capacity = fields.Integer(string='Capacity', related='train_id.capacity')

    @api.depends('schedule_time', 'duration')
    def _compute_arrival_time(self):
        for record in self:
            if record.schedule_time and record.duration:
                record.arrival_time = fields.Datetime.add(record.schedule_time, hours=record.duration)

    @api.model
    def _generate_code(self):
        return self.env['ir.sequence'].next_by_code('train.schedule.code') or '/'
    

        
class TrainPassenger(models.Model):
    _name = 'train.passenger'
    _description = 'Train Passenger'

    name = fields.Char(string='Name', required=True)
    train_id = fields.Many2one('train.train', string='Train', required=True)

class TrainMachinist(models.Model):
    _name = 'train.machinist'
    _description = 'Train Machinist'

    name = fields.Char(string='Name', required=True)
    train_id = fields.Many2one('train.train', string='Train', required=True)

class TrainScheduleWizard(models.TransientModel):
    _name = 'train.schedule.wizard'
    _description = 'Train Schedule Wizard'

    train_id = fields.Many2one('train.train', string='Train', required=True)
    schedule_lines = fields.One2many('train.schedule.wizard.line', 'wizard_id', string='Schedule Lines')

    def add_schedules(self):
        for line in self.schedule_lines:
            self.env['train.schedule'].create({
                'code': self.env['ir.sequence'].next_by_code('train.schedule.code'),
                'origin_id': line.origin_id.id,
                'destination_id': line.destination_id.id,
                'schedule_time': line.schedule_time,
                'duration': line.duration,
                'train_id': self.train_id.id,
            })

class TrainScheduleWizardLine(models.TransientModel):
    _name = 'train.schedule.wizard.line'
    _description = 'Train Schedule Wizard Line'

    wizard_id = fields.Many2one('train.schedule.wizard', string='Wizard Reference', required=True)
    origin_id = fields.Many2one('train.station', string='Origin Station', required=True)
    destination_id = fields.Many2one('train.station', string='Destination Station', required=True)
    schedule_time = fields.Datetime(string='Schedule Time', required=True)
    duration = fields.Float(string='Duration (hours)', required=True)