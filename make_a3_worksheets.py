from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation
import pypdfium2 as pdfium

source=Path('make_worksheets_illustrated.py').read_text(encoding='utf-8')
source=source.replace("OUT=Path('output/pdf')", "OUT=Path('tmp/pdfs/a3-source')")
source=source.replace("f'{page} / 2'", "'前半' if page==1 else '後半'")
source=source.replace('1枚目の班の問いを見ながら', '左側の班の問いを見ながら')
source=source.replace('中間ゴール　問いができたら2枚目へ！', '中間ゴール　問いができたら右側へ！')
exec(compile(source,'a3_source','exec'),{})

for kind,label in [('map','京都探検マップ風'),('adventure','冒険ボードゲーム風')]:
    name=f'京都探究ワークシート_{label}_京都イラスト版'
    reader=PdfReader(f'tmp/pdfs/a3-source/{name}.pdf')
    w=float(reader.pages[0].mediabox.width)
    h=float(reader.pages[0].mediabox.height)
    writer=PdfWriter()
    page=writer.add_blank_page(width=w*2,height=h)
    page.merge_transformed_page(reader.pages[0],Transformation())
    page.merge_transformed_page(reader.pages[1],Transformation().translate(tx=w))
    writer.add_metadata({'/Title':f'京都探究ワークシート {label} A3横1枚'})
    target=Path(f'output/pdf/京都探究ワークシート_{label}_A3横1枚.pdf')
    with target.open('wb') as f: writer.write(f)
    check=PdfReader(target)
    assert len(check.pages)==1
    doc=pdfium.PdfDocument(str(target))
    doc[0].render(scale=1.2).to_pil().save(f'tmp/pdfs/{kind}-a3.png')
    print(target)
