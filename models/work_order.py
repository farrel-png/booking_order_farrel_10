from copy import copy
from datetime import datetime, timedelta
from email.policy import default
from odoo import models, fields, api, exceptions, _


class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'
    _rec_name = "wo_number"

    name = fields.Char(string='Name')
    wo_number = fields.Char(string='Wo Number', required=True, readonly=True, copy=False, default=lambda self: _('New'))
    #Sebagai referensi bo untuk wo
    bo_reference = fields.Many2one(comodel_name='sale.order', readonly=True)
    team = fields.Many2one(comodel_name='service.team', required=True)
    team_leader = fields.Many2one(comodel_name='res.users', string='Team Leader', required=True)
    team_members = fields.Many2many(comodel_name='res.users', string='Team Members')
    planned_start = fields.Datetime('Planned Start', required=True)
    planned_end = fields.Datetime('Planned End', required=True)
    date_start = fields.Datetime('Date Start', readonly=True)
    date_end = fields.Datetime('Date End', readonly=True)
    state = fields.Selection(
        string='State', 
        selection=[
            ('pending', 'Pending'), 
            ('in progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled')],
        default="pending", 
        track_visibility='onchange'
    )
    note = fields.Text(string='Note')
    
    @api.model
    def create(self, vals):
        if vals.get('wo_number', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['wo_number'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'work.order') or _('New')
            else:
                vals['wo_number'] = self.env['ir.sequence'].next_by_code('work.order') or _('New')
        result = super(WorkOrder, self).create(vals)
        return result

    @api.multi
    #Pembuatan Status pengerjaan
    def start_work(self):
        return self.write({'state': 'in_progress', 'date_start': str(datetime.now())})

    @api.multi
    def end_work(self):
        return self.write({'state': 'done', 'date_end': str(datetime.now())})

    @api.multi
    def reset(self):
        return self.write({'state': 'pending', 'date_start': ''})

    @api.multi
    def cancel(self):
        return self.write({'state': 'cancelled'})
    
    
    
    
    
    
