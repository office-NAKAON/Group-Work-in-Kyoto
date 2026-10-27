from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pathlib import Path
import pypdfium2 as pdfium

OUT=Path('output/pdf'); OUT.mkdir(parents=True,exist_ok=True)
QA=Path('tmp/pdfs'); QA.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('JP','C:/Windows/Fonts/YuGothM.ttc'))
pdfmetrics.registerFont(TTFont('JPB','C:/Windows/Fonts/YuGothB.ttc'))
W,H=A4

def make(kind):
    adventure=kind=='adventure'
    name='京都探究ワークシート_'+('冒険ボードゲーム風' if adventure else '京都探検マップ風')+'_京都イラスト版'
    c=canvas.Canvas(str(OUT/(name+'.pdf')),pagesize=A4)
    c.setTitle(name)
    accent=HexColor('#245D85' if adventure else '#38685C')
    gold=HexColor('#D88A25' if adventure else '#AF8655')
    pale=HexColor('#EEF5FB' if adventure else '#F5F3EC')
    ink=HexColor('#202D35')
    def txt(x,y,s,size=10,bold=False,color=None):
        c.setFillColor(color or ink); c.setFont('JPB' if bold else 'JP',size); c.drawString(x,H-y-size,s)
    def line(x,y,x2,y2,col=None,width=0.6):
        c.setStrokeColor(col or HexColor('#C3CDCC')); c.setLineWidth(width); c.line(x,H-y,x2,H-y2)
    def rect(x,y,w,h,fill=white,stroke=None,r=9):
        c.setFillColor(fill); c.setStrokeColor(stroke or accent); c.setLineWidth(.8); c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=1)
    def lines(x,y,w,n=2):
        for i in range(n): line(x,y+i*22,x+w,y+i*22)
    def badge(x,y,n):
        c.setFillColor(gold if adventure else accent); c.circle(x,H-y,13,fill=1,stroke=0)
        txt(x-5,y-10,str(n),13,True,white)
    def tile(n,y,h,title,hint):
        rect(63,y,499,h)
        badge(46,y+22,n)
        txt(77,y+9,title,13,True)
        txt(77,y+31,hint,9)
    def route():
        c.setStrokeColor(HexColor('#E1C78F' if adventure else '#C9D4C5')); c.setLineWidth(7)
        p=c.beginPath(); p.moveTo(46,H-180)
        for yy in range(180,744,94):
            p.curveTo(15,H-yy-28,24,H-yy-60,46,H-yy-94)
        c.drawPath(p)
        if adventure:
            for i,yy in enumerate(range(220,750,37)):
                xx=24 if i%2 else 32
                c.setFillColor(white); c.setStrokeColor(gold); c.setLineWidth(1)
                c.roundRect(xx-6,H-yy-7,12,14,3,fill=1,stroke=1)
        for yy in range(205,750,52):
            c.setFillColor(gold); p=c.beginPath(); p.moveTo(42,H-yy); p.lineTo(50,H-yy); p.lineTo(46,H-yy-6); p.close(); c.drawPath(p,fill=1,stroke=0)
    def scene():
        # Small vector skyline: pagoda, machiya and hills.
        x,y=485,48
        if adventure:
            line(514,36,514,91,accent,2)
            c.setFillColor(gold)
            p=c.beginPath(); p.moveTo(515,H-37); p.lineTo(550,H-44); p.lineTo(515,H-60); p.close(); c.drawPath(p,fill=1,stroke=0)
            for xx,yy in [(491,66),(544,80)]:
                c.setFillColor(white); c.setStrokeColor(accent); c.setLineWidth(1)
                c.roundRect(xx-7,H-yy-7,14,14,3,fill=1,stroke=1)
                c.setFillColor(gold); c.circle(xx,H-yy,2,fill=1,stroke=0)
        else:
            for level in range(3):
                yy=60+level*12; ww=38-level*8
                line(511-ww/2,yy,511+ww/2,yy,accent,2)
                line(511-ww/2,yy,511,yy-8,accent,1)
                line(511,yy-8,511+ww/2,yy,accent,1)
            line(511,47,511,94,accent,1)
    def header(page):
        c.setFillColor(pale); c.rect(0,0,W,H,fill=1,stroke=0)
        c.drawImage('output/assets/kyoto-'+('adventure' if adventure else 'map')+'-background.png',0,0,W,H)
        c.saveState(); c.setFillAlpha(.94); c.setFillColor(pale)
        c.roundRect(24,H-101,385,86,9,fill=1,stroke=0)
        c.roundRect(24,H-163,548,65,9,fill=1,stroke=0)
        c.restoreState()
        c.saveState(); c.setFillAlpha(.96); c.setFillColor(pale)
        c.roundRect(71,H-798,491,50 if page==1 else 72,7,fill=1,stroke=0)
        c.restoreState()
        txt(33,22,'京都 班別自主研修  /  中学2年',9,True,accent)
        txt(33,43,'京都探究 '+('クエスト' if adventure else 'さんぽマップ'),23,True)
        txt(33,78,'問いを見つける旅' if page==1 else '確かめる作戦を立てる旅',14,True,accent)
        txt(33,105,'2年（　　）組（　　）番　氏名（　　　　　　　　　）　班（　　）')
        txt(33,128,'まず自分で考える → 班で相談する → 決まった内容を自分の用紙にも書く',9)
        txt(33,146,'書けたら次へ。迷ったら前のマスに戻ってOK。サイコロは使いません。',9)
        route()
        c.saveState(); c.setFillAlpha(.94); c.setFillColor(pale); c.roundRect(25,20,548,22,4,fill=1,stroke=0); c.restoreState()
        txt(33,807,('冒険ボードゲーム風' if adventure else '京都探検マップ風')+'　｜　班全員で相談し、一人ひとりが記録する',8,color=accent)
        txt(524,807,f'{page} / 2',9,True,accent)
    header(1)
    txt(26,170,'START',9,True,accent)
    tile(1,190,86,'気になる分野を選ぼう','気になるものに○。班で相談して、ひとつを出発点にしよう。')
    txt(79,242,'建築　／　食　／　工芸　／　暮らし　／　その他（　　　　　　）',11)
    tile(2,289,109,'調べる対象を具体的にしよう','分野の中で、何を調べたい？　もの・建物・技術・場所などを書こう。')
    txt(79,338,'ヒント：食 → 和菓子　／　建築 → 町家　／　工芸 → 西陣織',9,color=accent)
    lines(79,380,465,1)
    tile(3,411,148,'不思議のカードを選ぼう','対象について知りたいことに○。自分たちでカードをつくってもOK。')
    for x,y,w,s in [(79,463,220,'A　なぜ今も続いている？'),(315,463,230,'B　続けるための工夫は？'),(79,501,220,'C　何を守り、何を変えている？'),(315,501,230,'D　今の暮らしでどう生かす？')]:
        rect(x,y,w,29,pale,HexColor('#CCD6D5'),5); txt(x+8,y+8,s,9)
    txt(79,539,'自分たちのカード：',9); line(170,552,544,552)
    tile(4,572,171,'組み合わせて 班の問いをつくろう','「②の対象」＋「③のカード」で、たたき台をつくってみよう。')
    txt(79,622,'例：和菓子は、今の人に選ばれるためにどんな工夫をしているのか。',9,color=accent)
    txt(79,645,'班の問い',10,True); lines(79,681,465,2)
    txt(79,719,'「変えているはず」と決めつけず、変えない工夫や予想との違いにも注目。',8.5)
    txt(78,756,'中間ゴール　問いができたら2枚目へ！',13,True,accent)
    txt(78,780,'□ 対象が具体的　　□「何が有名」「いつできた」から一歩進んだ',9)
    c.showPage()
    header(2)
    txt(22,170,'RESTART',8,True,accent)
    tile(5,190,126,'今の予想と理由を書こう','1枚目の班の問いを見ながら、「たぶんこうだ」を言葉にしよう。')
    txt(79,239,'予想：',10,True); lines(112,261,432,1)
    txt(79,272,'理由：',10,True); lines(112,298,432,1)
    tile(6,329,112,'現地で確かめたいことを決めよう','何を見たり、聞いたりすれば、予想を確かめられる？　2つ考えよう。')
    txt(79,379,'①',10); lines(98,397,446,1)
    txt(79,407,'②',10); lines(98,426,446,1)
    tile(7,454,156,'調べ方と訪問候補をつなごう','⑥の①②それぞれに合う方法と場所を考えよう。候補はあとで確認してOK。')
    txt(79,501,'方法のヒント：観察・展示や説明板・公式資料・事前に依頼する聞き取り',8.5,color=accent)
    txt(79,522,'① 方法と場所：',9); line(158,541,544,541)
    txt(79,548,'② 方法と場所：',9); line(158,567,544,567)
    txt(79,576,'聞けない場合は：',9); line(165,597,544,597)
    tile(8,623,98,'役割を決めて 記録を共有しよう','例：班長・時間・交通・会計・記録（6人班は記録2人など）。判断は全員で。')
    txt(79,670,'自分の担当：',9); line(145,689,280,689)
    txt(300,670,'記録の共有方法：',9); line(388,689,544,689)
    txt(79,699,'班員全員の担当を確認しよう。担当が違っても、集めた記録は全員で使う。',8.5)
    txt(78,733,'GOAL　班の探究計画が完成！',14,True,accent)
    txt(78,758,'□ 現地で確かめられる問い　　□ 問いと調べ方がつながっている',9)
    txt(78,776,'□ 全員に担当がある　　　　　□ 聞き取りができない場合も考えた',9)
    c.save()
    doc=pdfium.PdfDocument(str(OUT/(name+'.pdf')))
    assert len(doc)==2
    for i,p in enumerate(doc):
        p.render(scale=1.4).to_pil().save(QA/(kind+f'-illustrated-{i+1}.png'))
    return str(OUT/(name+'.pdf'))

for k in ['map','adventure']: print(make(k))
