import openpyxl
from openpyxl.styles import Alignment, Color, PatternFill, Font, Border, Side
from openpyxl.styles.colors import YELLOW, BLACK, DARKYELLOW

from settings.table_constants import HEADER, COLUMNS


class XlsProcessor:
    def __init__(self, data: list):
        self.data = data

    def make_table(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        header_allignment = Alignment(horizontal='center',
                                      vertical='center',
                                      text_rotation=0,
                                      wrap_text=False,
                                      shrink_to_fit=False,
                                      indent=0)

        for index, col in enumerate(HEADER, start=1):
            cell = sheet.cell(row=1, column=index, value=col)

            cell.alignment = header_allignment
            cell.border = Border(
                left=Side(border_style='thin',
                          color=BLACK),
                right=Side(border_style='thin',
                           color=BLACK),
                top=Side(border_style='thin',
                         color=BLACK),
                bottom=Side(border_style='thin',
                            color=BLACK
                            )
            )
            cell.font = Font(size=12, )
            if index % 2 == 0:
                cell.fill = PatternFill(start_color=YELLOW,
                                        end_color=YELLOW,
                                        fill_type='solid')
            else:
                cell.fill = PatternFill(start_color=DARKYELLOW,
                                        end_color=DARKYELLOW,
                                        fill_type='solid')
            sheet.column_dimensions[cell.column_letter].width = 40
        sheet.row_dimensions[1].height = 60

        for row, order in enumerate(self.data, start=2):
            for col_number, col in enumerate(COLUMNS, start=1):
                sheet.cell(row=row, column=col_number, value=order[col])

        workbook.save(filename="test_wb.xls")
