'''
Created on 31 August 2019

@author: Dennis
'''

from odoo import models
import pandas3 as pd

def workbook_table_header(workbook):
    table_header = workbook.add_format()
    table_header.set_bold(True)
    table_header.set_font_color('black')
    table_header.set_font_name('Arial')
    table_header.set_font_size(13)
    table_header.set_bg_color('#b5e9ff')
    return table_header

def workbook_table_row(workbook):
    table_row = workbook.add_format()
    table_row.set_bold(True)
    table_row.set_font_color('black')
    table_row.set_font_name('Arial')
    table_row.set_font_size(12)
    table_row.set_bg_color('#cceeff')
    return table_row


df = pd.DataFrame({'Date and time': [datetime(2015, 1, 1, 11, 30, 55),
                                     datetime(2015, 1, 2, 1,  20, 33),
                                     datetime(2015, 1, 3, 11, 10    ),
                                     datetime(2015, 1, 4, 16, 45, 35),
                                     datetime(2015, 1, 5, 12, 10, 15)],
                   'Dates only':    [date(2015, 2, 1),
                                     date(2015, 2, 2),
                                     date(2015, 2, 3),
                                     date(2015, 2, 4),
                                     date(2015, 2, 5)],
                   })

# Create a Pandas Excel writer using XlsxWriter as the engine.
# Also set the default datetime and date formats.
writer = pd.ExcelWriter("pandas_datetime.xlsx",
                        engine='xlsxwriter',
                        datetime_format='mmm d yyyy hh:mm:ss',
                        date_format='mmmm dd yyyy')

# Convert the dataframe to an XlsxWriter Excel object.
# df.to_excel(writer, sheet_name='Sheet1')
#
# # Get the xlsxwriter workbook and worksheet objects in order to set the column
# # widths, to make the dates clearer.
# workbook  = writer.book
# worksheet = writer.sheets['Sheet1']
#
# worksheet.set_column('B:C', 20)
#
# # Close the Pandas Excel writer and output the Excel file.
# writer.save()




class ProjectAccomplishment(models.AbstractModel):
    _name = 'report.construction_project_management_base.pa'
    _inherit = 'report.report_xlsx.abstract'



    def generate_xlsx_report(self, workbook, data, line):
        table_header = workbook_table_header(workbook)
        table_row = workbook_table_row(workbook)
        for obj in line:
            print(df)
            project_stat = workbook.add_worksheet("Project Status")
            project_stat.set_column('B:B', 23)
            project_stat.write(0, 1, "Accomplishment", table_header)
            project_stat.write(1, 1, "Projected Accomplishment", table_row)
            project_stat.write(2, 1, "Actual Accomplishment", table_row)
