from odoo import fields, models

class Subtype(models.Model):
    _name = "subtype"


    type = fields.Many2one('helpdesk.ticket.type', string = "Type")
    priority = fields.Selection([
        ('0', 'Low Priority'), ('1', 'Medium Priority'),
        ('2', 'High Priority'), ('3', 'Urgent')],
        'Priority',      default='1')
    
    name  = fields.Char('Name')
    count = fields.Integer(string="Count", compute="cal_count")

    def cal_count(self):
        for rec in self:
            rec['count'] = 0
            t1 = self.env['helpdesk.ticket'].search_count([('subtype', '=', rec.id)])
            if t1:
                rec['count'] = t1