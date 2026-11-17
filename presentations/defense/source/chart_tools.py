"""Preserve measured XY points in editable chart workbooks."""
from pathlib import Path
from io import BytesIO
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
from deck_tools import *
from pptx.oxml.xmlchemy import OxmlElement
from pptx.enum.chart import XL_DATA_LABEL_POSITION, XL_TICK_LABEL_POSITION

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'


def vc(proposal, key):
    return next(block['text'] for block in proposal['visible_content'] if block['id'] == key)


def separate_xy_columns(chart, groups):
    """Use a shared X grid and blank unmeasured Y cells for renderer compatibility."""
    currents = sorted({point['iout_a'] for group in groups for point in group['points']})
    stream = BytesIO()
    book = xlsxwriter.Workbook(stream, {'in_memory': True})
    sheet = book.add_worksheet('Measurements')
    for i, (native, group) in enumerate(zip(chart.series, groups)):
        cx, cy = i*2, i*2+1
        observed = {point['iout_a']: point['error_pct'] for point in group['points']}
        sheet.write(0, cx, 'Output load current (A)')
        sheet.write(0, cy, group['name'])
        for row, current in enumerate(currents, 1):
            sheet.write_number(row, cx, current)
            if current in observed:
                sheet.write_number(row, cy, observed[current])
        end = len(currents)+1
        native._element.xpath('./c:tx/c:strRef/c:f')[0].text = f'Measurements!${xl_col_to_name(cy)}$1'
        for tag, column in [('xVal', cx), ('yVal', cy)]:
            letter = xl_col_to_name(column)
            native._element.xpath(f'./c:{tag}/c:numRef/c:f')[0].text = f'Measurements!${letter}$2:${letter}${end}'
            cache = native._element.xpath(f'./c:{tag}/c:numRef/c:numCache')[0]
            cache.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}ptCount').set('val', str(len(currents)))
            for element in list(cache):
                if element.tag.endswith('}pt'): cache.remove(element)
            for row, current in enumerate(currents):
                if tag == 'yVal' and current not in observed: continue
                point = OxmlElement('c:pt');point.set('idx', str(row))
                value = OxmlElement('c:v');value.text = str(current if tag == 'xVal' else observed[current])
                point.append(value);cache.append(point)
    # Lines join observed points; blank cells remain unmeasured, never zero.
    root = chart._chartSpace
    blanks = root.xpath('./c:chart/c:dispBlanksAs')
    if blanks: blanks[0].set('val', 'span')
    else:
        element = OxmlElement('c:dispBlanksAs');element.set('val', 'span')
        root.xpath('./c:chart')[0].append(element)
    sheet.set_column(0, 7, 24)
    book.close()
    chart.part.chart_workbook.update_from_xlsx_blob(stream.getvalue())


