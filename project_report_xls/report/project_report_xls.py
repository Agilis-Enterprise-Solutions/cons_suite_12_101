# -*- coding: utf-8 -*-

from odoo.http import request
from odoo import models
from datetime import datetime
from collections import OrderedDict
import random


class ProjectReportXls(models.AbstractModel):
    _name = 'report.project_report_xls.project_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        wizard_record = request.env['wizard.project.report'].search([])[-1]

        user_obj = self.env['res.users'].search([('id', '=', data['context']['uid'])])
        company = user_obj.company_id.name
        runby = user_obj.name
        currency = user_obj.company_id.currency_id.symbol
        current_time = datetime.now()
        rundate = current_time.strftime('%m/%d/%Y')


        worksheet = workbook.add_worksheet()

        # Style formats

        foramt = workbook.add_format({'font_size': 10, 'font_name': 'arial'})

        bold = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1})
        italic = workbook.add_format({'font_size': 10, 'font_name': 'arial','italic': 1})

        format1 = workbook.add_format({'font_size': 18, 'font_name': 'arial','bg_color':'#CFE2F3','bold': 1})
        format1.set_align('center')

        format2 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bg_color':'#FCE5CD'})


        format3 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bg_color':'#B7E1CD','num_format': currency+'#,##0.00'})
        format3.set_align('right')

        format4 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'num_format': currency+'#,##0.00'})
        format4.set_align('right')

        format5 = workbook.add_format({'font_size': 10, 'font_name': 'arial','num_format': '0.00##\%;[Red](0.00##\%)'})
        format5.set_align('right')

        format6 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#FCE5CD'})
        format7 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#FFF2CC'})
        format8 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#B6D7A8'})

        format9  = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#EA9999','valign': 'vcenter',})
        format10  = workbook.add_format({'font_size': 10, 'font_name': 'arial','bg_color':'#EA9999','valign': 'vcenter',})

        format9.set_align('center')
        format10.set_align('center')

        format11 = workbook.add_format({'font_size': 10, 'font_name': 'arial','italic': 1,'bg_color':'#FCE5CD','valign': 'vcenter'})

        format12 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#FCE5CD','valign': 'vcenter'})

        format12.set_align('center')

        format13 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bg_color':'#FFF2CC'})

        format14 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bg_color':'#FFF2CC','num_format': '0.00##\%;[Red](0.00##\%)'})
        format14.set_align('right')

        format15 = workbook.add_format({'font_size': 10, 'font_name': 'arial','bold': 1,'bg_color':'#FCE5CD','valign': 'vcenter'})


        # Parameters

        worksheet.write('A1', 'Project Name',italic)
        worksheet.merge_range('B1:D1', wizard_record.project_id.name, bold)

        worksheet.set_column(0, 0, 32)
        worksheet.set_column(1, 3, 15)
        worksheet.set_column(4, 4, 30)
        worksheet.set_column(5, 8, 15)

        worksheet.write('A2', 'Run By',italic)
        worksheet.write('B2', runby, bold)
        as_of_date = ""
        if (wizard_record.asof_date):
            as_of_date = wizard_record.asof_date

        worksheet.write('A3', 'As of',italic)
        worksheet.write('B3', as_of_date, bold)

        worksheet.write('E1', 'Client Name',italic)
        worksheet.merge_range('F1:G1', company, bold)

        worksheet.write('E2', 'Run Date',italic)
        worksheet.write('F2', rundate, bold)

        worksheet.merge_range('A5:H5', 'Project Budget', format1)

        headings = ['', 'Budget', 'Actual Expense']
        worksheet.write_row('A7', headings, format2)

        # Tabular data for Project Budget

        worksheet.write('A8', 'Material', foramt)
        worksheet.write_number('B8', wizard_record.project_id.material_budget,format3)
        worksheet.write_number('C8', wizard_record.project_id.material_expense,format3)

        worksheet.write('A9', 'Subcontract/Outsource Services',foramt)
        worksheet.write_number('B9', wizard_record.project_id.service_budget,format3)
        worksheet.write_number('C9', wizard_record.project_id.service_expense,format3)

        worksheet.write('A10', 'Human Resource/Labor',foramt)
        worksheet.write_number('B10', wizard_record.project_id.labor_budget,format3)
        worksheet.write_number('C10', wizard_record.project_id.labor_expense,format3)

        worksheet.write('A11', 'Equipment',foramt)
        worksheet.write_number('B11', wizard_record.project_id.equipment_budget,format3)
        worksheet.write_number('C11', wizard_record.project_id.equipment_expense,format3)

        worksheet.write('A12', 'Overheads',foramt)
        worksheet.write_number('B12', wizard_record.project_id.overhead_budget,format3)
        worksheet.write_number('C12', wizard_record.project_id.overhead_expense,format3)

        worksheet.write('A13', 'Total',bold)
        worksheet.write_number('B13', wizard_record.project_id.total_budget,format4)
        worksheet.write_number('C13', wizard_record.project_id.total_expense,format4)

        # Bar graph for Project Budget

        chart1 = workbook.add_chart({'type': 'column'})

        chart1.add_series({
            'name':       '=Sheet1!$B$7',
            'categories': '=Sheet1!$A$8:$A$12',
            'values':     '=Sheet1!$B$8:$B$12',
        })

        chart1.add_series({
            'name':       '=Sheet1!$C$7',
            'categories': '=Sheet1!$A$8:$A$12',
            'values':     '=Sheet1!$C$8:$C$12',
        })

        chart1.set_title ({'name': 'Budget and Actual Expense','name_font': {'bold':0,'size': 10, 'name': 'arial', 'color':'#808080'}})
        chart1.set_x_axis({'name': 'Project Budget','name_font': {'bold':0,'size': 10, 'name': 'arial'}})

        chart1.set_style(2)

        chart1.set_legend({'position': 'top'})
        chart1.set_size({'width':600,'height' : 300})

        worksheet.insert_chart('D6:G6', chart1, {'x_offset': 20, 'y_offset': 5})

        worksheet.merge_range('J5:Q5', 'Project Status', format1)
        worksheet.set_column(9, 9, 30)
        worksheet.set_column(10, 16, 13)

        # Fetching data for Projected Accomplishment
        if wizard_record.asof_date :
            search_date = ('date','<=',wizard_record.asof_date)
        else:
            search_date = (1,'=',1)
        accomplishment = self.env['project.projection.accomplishment'].search([('id', 'in', wizard_record.project_id.projection_accomplishment_ids.ids),search_date])
        headings = []

        projected_accomplish_temp = {}
        actual_accomplish_temp = {}

        for rec in accomplishment:
            datee = rec.date
            if (not datee.strftime("%b") in headings):
                headings.append(datee.strftime("%b"))
            if projected_accomplish_temp.get(datee.strftime("%b")):
                projected_accomplish_temp[datee.strftime("%b")] =  projected_accomplish_temp[datee.strftime("%b")] + rec.projected
            else:
                projected_accomplish_temp[datee.strftime("%b")] =  rec.projected

            if actual_accomplish_temp.get(datee.strftime("%b")):
                actual_accomplish_temp[datee.strftime("%b")] =  actual_accomplish_temp[datee.strftime("%b")] + rec.actual
            else:
                actual_accomplish_temp[datee.strftime("%b")] =  rec.actual


        projected_accomplish = []
        actual_accomplish = []
        for hd in headings:
            projected_accomplish.append(projected_accomplish_temp.get(hd))
            actual_accomplish.append(actual_accomplish_temp.get(hd))

        #  Projected Accomplishment tabular
        if (len(actual_accomplish) >0 or len(projected_accomplish) > 0):
            worksheet.write('J22', "Accomplishment", format6)
            worksheet.write('J23', "Projected Accomplishment", format8)
            worksheet.write('J24', "Actual Accomplishment", format8)
            worksheet.write_row('K22', headings, format7)
            worksheet.write_row('K23', projected_accomplish, format5)
            worksheet.write_row('K24', actual_accomplish, format5)

        #  Line graph for Projected Accomplishment

        chart2 = workbook.add_chart({'type': 'line'})

        series_1_category = chr(ord('K') + len(headings))

        chart2.add_series({
            'name':       '=Sheet1!$J$23',
            'categories': '=Sheet1!$K$22:$'+series_1_category+'$22',
            'values':     '=Sheet1!$K$23:$'+series_1_category+'$23',
        })

        chart2.add_series({
            'name':       '=Sheet1!$J$24',
            'categories': '=Sheet1!$K$22:$'+series_1_category+'$22',
            'values':     '=Sheet1!$K$24:$'+series_1_category+'$24',
        })

        chart2.set_title ({'name': 'Projected Accomplishment and Actual Accomplishment','name_font': {'bold':0,'size': 10, 'name': 'arial', 'color':'#808080'}})

        chart2.set_style(2)

        chart2.set_legend({'position': 'top'})
        chart2.set_size({'width':880,'height' : 300})

        worksheet.insert_chart('J6:Q6', chart2, {'y_offset': 5})

        # Phase-wise Project Budget and Expense Tabular data

        worksheet.merge_range('A22:A23', "Phase", format9)
        worksheet.merge_range('B22:B23', "Task", format9)
        worksheet.merge_range('C22:C23', "Type", format9)
        worksheet.merge_range('D22:H22', "Categories", format10)
        worksheet.write('D23', "1. Material", bold)
        worksheet.write('E23', "2. Subcontract (Ousource Service)", bold)
        worksheet.write('F23', "3. Equipment", bold)
        worksheet.write('G23', "4. Overheads", bold)
        worksheet.write('H23', "Total", bold)


        tasks = self.env['project.task'].search([('project_id', '=', wizard_record.project_id.id)],order="phase_id,create_date")
        row_number = 24
        cnt = 0
        temp_phase_id = -1
        start_row_number = 24
        for task in tasks:
            if (temp_phase_id != task.phase_id.id and temp_phase_id != -1):
                phase = self.env['project.phase'].search([('id', '=', temp_phase_id)])
                worksheet.merge_range('A'+str(start_row_number)+':A'+str(start_row_number-1 + cnt * 2), "Project "+phase.name if phase else "", format11)
                start_row_number = row_number
                cnt = 0
            temp_phase_id = task.phase_id.id
            worksheet.write('C'+str(row_number), "Budget", format2)
            worksheet.write('D'+str(row_number), task.material_budget, format3)
            worksheet.write('E'+str(row_number), task.service_budget, format3)
            worksheet.write('F'+str(row_number), task.equipment_budget, format3)
            worksheet.write('G'+str(row_number), task.overhead_budget, format3)
            worksheet.write('H'+str(row_number), task.total_budget, format3)

            worksheet.merge_range('B'+str(row_number)+':B'+str(row_number+1), task.name, format11)

            row_number += 1

            worksheet.write('C'+str(row_number), "Actual Expense", format2)
            worksheet.write('D'+str(row_number), task.material_expense, format3)
            worksheet.write('E'+str(row_number), task.service_expense, format3)
            worksheet.write('F'+str(row_number), task.equipment_expense, format3)
            worksheet.write('G'+str(row_number), task.overhead_expense, format3)
            worksheet.write('H'+str(row_number), task.total_expense, format3)

            cnt += 1
            row_number += 1

        worksheet.merge_range('A'+str(start_row_number)+':A'+str(start_row_number-1 + cnt * 2), "Project "+ task.phase_id.name if task.phase_id else "", format11)

        #Fetching data for Task-wise and Phase-wise Accomplishment

        visual_headings = []
        task_accomplishment = OrderedDict()
        phase_accomplishment = {}
        for task in tasks:
            visual_list = self.env['project.visual.inspection'].search([('id', 'in', task.visual_inspection.ids),search_date],order="date")
            for vis in visual_list:
                datee = vis.date
                if (not datee.strftime("%b") in visual_headings):
                    visual_headings.append(datee.strftime("%b"))
                if (task_accomplishment.get(task.id) and task_accomplishment[task.id].get(datee.strftime("%b"))):
                    task_accomplishment[task.id][datee.strftime("%b")] = task_accomplishment[task.id][datee.strftime("%b")] + vis.actual_accomplishment
                elif (task_accomplishment.get(task.id)):
                    task_accomplishment[task.id][datee.strftime("%b")] = vis.actual_accomplishment
                else:
                    task_accomplishment[task.id] = ({datee.strftime("%b") : vis.actual_accomplishment})

                if (phase_accomplishment.get(task.phase_id.id) and phase_accomplishment[task.phase_id.id].get(datee.strftime("%b"))):
                    phase_accomplishment[task.phase_id.id][datee.strftime("%b")] = phase_accomplishment[task.phase_id.id][datee.strftime("%b")] + vis.actual_accomplishment
                elif (phase_accomplishment.get(task.phase_id.id)):
                    phase_accomplishment[task.phase_id.id][datee.strftime("%b")] = vis.actual_accomplishment
                else:
                    phase_accomplishment[task.phase_id.id] = ({datee.strftime("%b") : vis.actual_accomplishment})



        # Phase-wise Accomplishment
        colors = ['#B7E1CD','#CFE2F3']
        rand = lambda: random.randint(200, 255)
        if (len(phase_accomplishment) > 0):
            start_number = 28
            phase_colors = {}
            phase_cnt = 0
            for phase_id, values in phase_accomplishment.items():
                actual_accomplish = []
                phase = self.env['project.phase'].search([('id', '=', phase_id)])
                phase_colors[phase_id] =  colors[phase_cnt] if phase_cnt < 2 else '#%02X%02X%02X' % (rand(), rand(), rand())
                worksheet.write('J'+str(start_number), phase.name,format7)
                worksheet.write('K'+str(start_number), phase.phase_weight,format14)
                for hd in visual_headings:
                    if values.get(hd):
                        actual_accomplish.append(values.get(hd))
                    else:
                        actual_accomplish.append("")

                format_phase = workbook.add_format({'font_size': 10, 'font_name': 'arial','num_format': '0.00##\%;[Red](0.00##\%)','bg_color':phase_colors[phase_id]})
                format_phase.set_align('right')
                worksheet.write_row('L'+str(start_number), actual_accomplish,format_phase)
                start_number += 1
                phase_cnt += 1

            if len(visual_headings) == 1:
                worksheet.write('L26', "Accomplishment",format12)
            else:
                worksheet.merge_range('L26:'+chr(ord('L') + len(visual_headings)-1)+'26', "Accomplishment",format12)
            worksheet.merge_range('J26:J27', "Phase",format15)
            worksheet.merge_range('K26:K27', "Phase Weight",format15)
            worksheet.write_row('L27', visual_headings,bold)


        # Task-wise Accomplishment
        if (len(task_accomplishment) > 0):
            start_number += 1

            if len(visual_headings) == 1:
                worksheet.write('L'+str(start_number), "Accomplishment",format12)
            else:
                worksheet.merge_range('L'+str(start_number)+':'+chr(ord('L') + len(visual_headings)-1)+str(start_number), "Accomplishment",format12)
            worksheet.merge_range('J'+str(start_number)+':J'+str(start_number+1), "Task",format15)
            worksheet.merge_range('K'+str(start_number)+':K'+str(start_number+1), "Task Weight",format15)
            worksheet.write_row('L'+str(start_number+1), visual_headings,bold)

            start_number += 2

            for task_id, values in task_accomplishment.items():
                actual_accomplish = []
                tasks = self.env['project.task'].search([('id', '=', task_id)])
                worksheet.write('J'+str(start_number), tasks.name,format13)
                worksheet.write('K'+str(start_number), tasks.task_weight,format14)
                for hd in visual_headings:
                    if values.get(hd):
                        actual_accomplish.append(values.get(hd))
                    else:
                        actual_accomplish.append("")
                phase_col = phase_colors.get(tasks.phase_id.id) if phase_colors.get(tasks.phase_id.id) else '#%02X%02X%02X' % (rand(), rand(), rand())
                format_phase = workbook.add_format({'font_size': 10, 'font_name': 'arial','num_format': '0.00##\%;[Red](0.00##\%)','bg_color':phase_col})
                format_phase.set_align('right')

                worksheet.write_row('L'+str(start_number), actual_accomplish,format_phase)
                start_number += 1
