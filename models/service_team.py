from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Service Team'

    name = fields.Char(string='Team Name', required=True)
    team_leader = fields.Many2one(comodel_name='res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
   
