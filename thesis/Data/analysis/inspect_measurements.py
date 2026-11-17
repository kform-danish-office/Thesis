from pathlib import Path
import json, zipfile, xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'Data/measurements'
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(s.itertext()) for s in E.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        rel=E.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets={e.attrib['Id']:e.attrib['Target'] for e in rel}
        book=E.fromstring(z.read('xl/workbook.xml'))
        result={}
        for sheet in book.find('m:sheets',NS):
            rid=sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target=targets[rid].lstrip('/')
            if not target.startswith('xl/'): target='xl/'+target
            rows=[]
            for row in E.fromstring(z.read(target)).findall('.//m:sheetData/m:row',NS):
                vals={}
                for cell in row.findall('m:c',NS):
                    typ=cell.attrib.get('t'); v=cell.find('m:v',NS)
                    if typ=='inlineStr':
                        inline=cell.find('m:is',NS)
                        value=''.join(inline.itertext()) if inline is not None else None
                    elif v is None: value=None
                    elif typ=='s': value=strings[int(v.text)]
                    else:
                        value=v.text
                        try:value=float(value)
                        except (ValueError,TypeError): pass
                    if value is not None: vals[cell.attrib['r']]=value
                if vals:rows.append({'row':int(row.attrib['r']),'cells':vals})
            result[sheet.attrib['name']]=rows
        return result

if __name__=='__main__':
    for p in DATA.glob('*.xlsx'):
        result=read_xlsx(p)
        dest=Path(__file__).parent/(p.stem+'_extracted.json')
        dest.write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(p.name,{name:len(rows) for name,rows in result.items()})
        if p.name=='Thesis_USB_PDO_3A_Limited_Test_Plan.xlsx':
            for row in result.get('Load Data',[]): print(json.dumps(row))
