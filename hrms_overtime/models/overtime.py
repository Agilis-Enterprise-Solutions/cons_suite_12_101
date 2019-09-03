# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import pytz
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DT
import math

def compute_hour_difference(date_from, date_to):
    res = 0
    if date_from and date_to:
        time_diff = (date_to - date_from).total_seconds()
        res = time_diff / 60.0 / 60.0
    return res

def compute_night_differential(nd_start, nd_end, time_in, time_out):
    """Paremeters should be datetime.time() type"""
    t = datetime.combine(date.min, time_out) - datetime.min
    tx_out = t.total_seconds() / 3600 / 24

    t1 = datetime.combine(date.min, time_in) - datetime.min
    tx_in = t1.total_seconds() / 3600 / 24

    t2 = datetime.combine(date.min, nd_start) - datetime.min
    tx_start = t2.total_seconds() / 3600 / 24

    t3 = datetime.combine(date.min, nd_end) - datetime.min
    tx_end = t3.total_seconds() / 3600 / 24

    if (time_in < time_out):
        rec = min(2, tx_out) - max(tx_start, tx_in)
        res = max(rec,0) + max(min(tx_end, tx_out) - max(0, tx_in), 0)
    else:
        rec = min(1.25, tx_out + 1) - max(tx_start, tx_in)
        res = max(rec,0) + max((tx_end- tx_in),0)
    final_res = round(res * 24, 2)
    return abs(final_res)


class HROvertimeLine(models.Model):
    _name = 'hr.overtime.line'

    overtime_id = fields.Many2one('hr.overtime', ondelete='cascade')
    start_date = fields.Datetime(string="Start", required=True)
    end_date = fields.Datetime(string="End", required=True)
    hours = fields.Float(string="Duration")
    work_type_id = fields.Many2one('hr.overtime.type', string="Overtime Type")


class HROvertime(models.Model):
    _name = 'hr.overtime'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin']

    employee_id = fields.Many2one(string="Employee", comodel_name="hr.employee", required=True)
    request_date = fields.Date(string="Request Date", default= date.today())
    work_type_ids = fields.One2many('hr.overtime.line', 'overtime_id',
                                    string="Work Type", readonly=True,
                                    states={'draft': [('readonly', False)]})
    overtime_start = fields.Datetime(string="Start of Overtime", required=True)
    overtime_end = fields.Datetime(string="End of Overtime", required=True)
    hours = fields.Float(string="Total Hours")
    name = fields.Text(string="Reason", required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Waiting for Confirmation'),
                              ('confirmed', 'Waiting for Approval'),
                              ('approved', 'Approved'),
                              ('rendered', 'Rendered'),
                              ('canceled', 'Cancelled')], string="Status",
                             default='draft', readonly=True, copy=False)
    submitted_by = fields.Many2one('res.users', string="Submitted By", readonly=True)
    submitted_date = fields.Datetime('Submitted Date', readonly=True)
    verified_by = fields.Many2one('res.users', string="Verified By", readonly=True)
    verified_date = fields.Datetime('Verified Date', readonly=True)
    confimed_by = fields.Many2one('res.users', string="Confirmed By", readonly=True)
    confirmed_date = fields.Datetime('Confirmed Date', readonly=True)
    approved_by = fields.Many2one('res.users', string="Approved By", readonly=True)
    approved_date = fields.Datetime('Approved Date', readonly=True)
    canceled_by = fields.Many2one('res.users', string="Cancelled By", readonly=True)
    canceled_date = fields.Datetime('Cancelled Date', readonly=True)

    # def convert_to_correct_tz(date, )

    @api.model
    def get_contract(self, employee, date_from, date_to):
        """
        @param employee: recordset of employee
        @param date_from: date field
        @param date_to: date field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        # a contract is valid if it ends between the given dates
        clause_1 = ['&', ('date_end', '<=', date_to), ('date_end', '>=', date_from)]
        # OR if it starts between the given dates
        clause_2 = ['&', ('date_start', '<=', date_to), ('date_start', '>=', date_from)]
        # OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&', ('date_start', '<=', date_from), '|', ('date_end', '=', False), ('date_end', '>=', date_to)]
        clause_final = [('employee_id', '=', employee.id), ('state', '=', 'open'), '|', '|'] + clause_1 + clause_2 + clause_3
        return self.env['hr.contract'].search(clause_final).ids


    def _holiday_type(date, empployee):
        holidays = self.env['company.holiday'].search([('date','=',date)])
        holiday_type = ''
        holiday_count = 0
        for i in holidays:
            for rec in i.company_ids:
                if employee.contract_id.company_id.id == rec.id:
                    holiday_count += 1
                    holiday_type = i.holiday_type
        if holiday_count == 0: return holiday_type
        if holiday_count >= 2: return "DHD"
        elif holiday_type == 'Regular': return "SHD"
        else: return "SHD"

    @api.multi
    def get_date_schedule(self, employee, date):
        schedule = self.employee_id.contract_id.resource_calendar_id
        sched_line = self.env['resource.calendar.attendance'].search([('calendar_id', '=', schedule.id), ('dayofweek', '=', date.weekday())], limit=1)
        return sched_line

    # @api.multi
    # def _check_filed_time(self):
    #     schedule = self.employee_id.contract_id.resource_calendar_id
    #     nd_start = self.env.user.company_id.nightdiff_hour_start
    #     nd_end = self.env.user.company_id.nightdiff_hour_end
    #     start = self.overtime_start + timedelta(hours=schedule.utc_offset)
    #     end = self.overtime_end + timedelta(hours=schedule.utc_offset)
    #     start_float = timedelta(hours=start.hour,minutes=start.minute,seconds=0.00).total_seconds()/60.00/60.00
    #     end_float = timedelta(hours=end.hour,minutes=end.minute,seconds=0.00).total_seconds()/60.00/60.00
    #     current_att_date = datetime(start.year, start.month, start.day, 0,0,0)
    #     nd_start_hours, nd_start_minutes = divmod((nd_start*60),60)
    #     nd_start_datetime = datetime(start.year, start.month, start.day, int(nd_start_hours), int(nd_start_minutes))
    #     nd_end_hours, nd_end_minutes = divmod((nd_end*60),60)
    #     nd_end_datetime = datetime(end.year, end.month, end.day, int(nd_end_hours), int(nd_end_minutes))
    #
    #     hd_type = _holiday_type(current_att_date, self.employee_id)
    #     overtime_limit = compute_hour_difference(start, end)
    #     work_schedules []
    #     day_schedule = self.get_date_schedule(self.employee_id, current_att_date)
    #     if day_schedule[:1]:
    #         #ordinary ot
    #         search_param = hd_type + 'OT'
    #         regular = compute_hour_difference(start, end)
    #         work_type_id = work_types.search([('code','=',search_param)])
    #         work_schedules.append([start, end, regular, work_type_id.id])
    #         #ordinary ot+nightdiff
    #         nd_sched = _ot_night_diff(start, end, nd_start, nd_end)
    #         if start_float < nd_end and end_float >= nd_end:
    #             if start.date() == end.date():
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     start.time(), nd_end_datetime.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = start, nd_end_datetime
    #                 work_type_id = work_types.search([('code','=',hd_type +'OTND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #         if start_float < nd_end and end_float < nd_end:
    #             if start.date() == end.date():
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     start.time(), end.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = start, end
    #                 work_type_id = work_types.search([('code','=',hd_type +'OTND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #         if start_float < nd_end and end_float < nd_end:
    #             if start.date() != end.date() and overtime_limit >21.00:
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     nd_start_datetime.time(), end.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = nd_start_datetime, end
    #                 work_type_id = work_types.search([('code','=',hd_type +'OTND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #         if nd_sched[2] != 0.00:
    #             search_param = search_param + "ND"
    #             work_type_id = work_types.search([('code','=',search_param)])
    #             work_schedules.append([nd_sched[0], nd_sched[1], nd_sched[2], work_type_id.id])
    #         break
    #     else:
    #         """Free-will to change the whole thing. Isa lamang po itong gabay."""
    #         search_param = hd_type +'RD'
    #         restday = compute_hour_difference(start, end)
    #         if restday < schedule.restday_hours:
    #             restday_rendered = compute_hour_difference(start, end)
    #             use_end = end
    #         else:
    #             restday_rendered = schedule.restday_hours
    #             use_end = start + timedelta(hours=(schedule.restday_hours + schedule.number_of_breaktime_hours))
    #         work_type_id = work_types.search([('code','=',search_param)])
    #         work_schedules.append([start, use_end, restday_rendered, work_type_id.id])
    #         if start_float < nd_end and end_float >= nd_end:
    #             if start.date() == end.date():
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     start.time(), nd_end_datetime.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = start, nd_end_datetime
    #                 work_type_id = work_types.search([('code','=',hd_type +'RDND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #         if start_float < nd_end and end_float < nd_end:
    #             if start.date() == end.date():
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     start.time(), end.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = start, end
    #                 work_type_id = work_types.search([('code','=',hd_type +'RDND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #
    #         if start_float < nd_end and end_float < nd_end:
    #             if start.date() != end.date() and overtime_limit >21.00:
    #                 nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                     start.time(), nd_end_datetime.time()
    #                                                     ) #overtime extended from nightdiff to regular same day
    #                 nd_occured, nd_ended = start, nd_end_datetime
    #                 work_type_id = work_types.search([('code','=',hd_type +'RDND')])
    #                 work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #
    #
    #         restday_needed_plus_breaktime = schedule.restday_hours + schedule.number_of_breaktime_hours
    #         if (restday > restday_needed_plus_breaktime): #restday rendered hours exceeded
    #             #restday+ot
    #             search_param = search_param +'OT'
    #             restday_ot_start = start_float + restday_needed_plus_breaktime #24hours
    #             restday_ot_start_date = start
    #             rd_nd_b4_ot = False
    #             if restday_ot_start > 24.00:
    #                 restday_ot_start = (start_float + restday_needed_plus_breaktime) % 24
    #                 restday_ot_start_date = start  + timedelta(days=1)
    #                 cut_nd_hours, cut_nd_minutes = divmod((restday_ot_start*60),60)
    #                 cut_nd_datetime = datetime(restday_ot_start_date.year, restday_ot_start_date.month, restday_ot_start_date.day, int(cut_nd_hours), int(cut_nd_minutes))
    #                 #restday+nightdiff that goes through the next day before the ot occurs
    #                 nd_sched = _ot_night_diff(start, cut_nd_datetime, nd_start, nd_end)
    #                 work_type_id = work_types.search([('code','=',hd_type +'RDND')])
    #                 work_schedules.append([nd_sched[0], nd_sched[1], nd_sched[2], work_type_id.id])
    #                 #restday+ot+nightdiff but only until the remaining hours
    #                 nd_sched = _ot_night_diff(cut_nd_datetime, end, nd_start, nd_end)
    #                 work_type_id = work_types.search([('code','=',hd_type +'RDOTND')])
    #                 work_schedules.append([nd_sched[0], nd_sched[1], nd_sched[2], work_type_id.id])
    #                 rd_nd_b4_ot = True
    #             rd_ot_hours,rd_ot_minutes = divmod((restday_ot_start*60),60)
    #             restday_ot_start_datetime = datetime(restday_ot_start_date.year, restday_ot_start_date.month, restday_ot_start_date.day, int(rd_ot_hours), int(rd_ot_minutes))
    #             restday_ot_hours = compute_hour_difference(restday_ot_start_datetime, end)
    #             work_type_id = work_types.search([('code','=',search_param)])
    #             work_schedules.append([restday_ot_start_datetime, end, restday_ot_hours, work_type_id.id])
    #             #restday+ot+nightdiff
    #             if not rd_nd_b4_ot:
    #                 nd_sched = _ot_night_diff(start, end, nd_start, nd_end)
    #                 if nd_sched[2] != 0.00:
    #                     search_param = search_param +"ND"
    #                     work_type_id = work_types.search([('code','=',search_param)])
    #                     work_schedules.append([nd_sched[0], nd_sched[1], nd_sched[2], work_type_id.id])
    #             if start_float < nd_end and end_float < nd_end:
    #                 if start.date() != end.date() and overtime_limit >21.00:
    #                     nd_hours=compute_night_differential(nd_start_datetime.time(), nd_end_datetime.time(),
    #                                                         nd_start_datetime.time(), end.time()
    #                                                         ) #overtime extended from nightdiff to regular same day
    #                     nd_occured, nd_ended = nd_start_datetime, end
    #                     work_type_id = work_types.search([('code','=',hd_type +'RDOTND')])
    #                     work_schedules.append([nd_occured, nd_ended, nd_hours, work_type_id.id])
    #         else: #restday rendered hours was not exceeded but goes through nightdiff
    #             #restday+nightdiff
    #             nd_sched = _ot_night_diff(start, end, nd_start, nd_end)
    #
    #             if nd_sched[2] != 0.00:
    #                 search_param = search_param + "ND"
    #                 work_type_id = work_types.search([('code','=',search_param)])
    #                 work_schedules.append([nd_sched[0], nd_sched[1], nd_sched[2], work_type_id.id])
    #
    #     for x in work_schedules:
    #         if x[2] == 0.00:
    #             work_schedules.remove(x)
    #     for i in work_schedules:
    #         work_schedule_data.append([0, 0,{'start_date': i[0] -timedelta(hours=self.employee_id.company_id.utc_offset),#datetime fields
    #                                          'end_date': i[1] -timedelta(hours=self.employee_id.company_id.utc_offset),#datetime fields
    #                                          'hours': i[2],
    #                                          'work_type_id':i[3]
    #                                          }
    #                                    ])
    #     return work_schedule_data


    @api.onchange('overtime_start', 'overtime_end', 'employee_id')
    def _onchange_work_parameter(self):
        if self.overtime_start and self.overtime_end and self.employee_id:
            #Check if there is a valid contract.
            contract = self.get_contract(self.employee_id, self.overtime_start, self.overtime_end)
            if not contract:
                raise ValidationError(_("No valid employment contract found for %s."%(self.employee_id.name)))
            schedule= self.env['hr.contract'].browse(contract[0])


            # self.work_type_ids = self._check_filed_time()
            # start = datetime.strptime(self.overtime_start, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=self.employee_id.company_id.utc_offset)
            # end = datetime.strptime(self.overtime_end, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=self.employee_id.company_id.utc_offset)
            # start_float = timedelta(hours=start.hour,minutes=start.minute,seconds=0.00).total_seconds()/60.00/60.00
            # current_att_date = datetime(start.year, start.month, start.day, 0,0,0)
            # current_att_date2 = datetime(end.year, end.month, end.day, 0,0,0)
            # for line in schedule.attendance_ids:
            #     if str(current_att_date.weekday()) == line.dayofweek:
            #         out_time = "%02d:%02d:00"%(line.hour_to, math.modf(line.hour_to)[0]*60)
            #         out_datetime = datetime.strptime("%s %s"%(start.strftime(DEFAULT_SERVER_DATE_FORMAT), out_time), DEFAULT_SERVER_DATETIME_FORMAT)
            #         if (out_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT) > start.strftime(DEFAULT_SERVER_DATETIME_FORMAT)):
            #             raise Warning(_('Employee is still in regular schedule. Overtime should start after regular schedule. Please check and try again.'))
            #     if str(current_att_date2.weekday()) == line.dayofweek:
            #         out_time2 = "%02d:%02d:00"%(line.hour_from, math.modf(line.hour_from)[0]*60)
            #         out_datetime2 = datetime.strptime("%s %s"%(end.strftime(DEFAULT_SERVER_DATE_FORMAT), out_time2), DEFAULT_SERVER_DATETIME_FORMAT)
            #         if (out_datetime2.strftime(DEFAULT_SERVER_DATETIME_FORMAT) < end.strftime(DEFAULT_SERVER_DATETIME_FORMAT)) and start.date() != end.date():
            #             raise Warning(_('Employee is still in regular schedule. Overtime should start after regular schedule. Please check and try again.'))
