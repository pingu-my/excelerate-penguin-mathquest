from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from scoring import summary

def create_certificate(profile,results,run_id):
    out=BytesIO();w,h=landscape(A4);c=canvas.Canvas(out,pagesize=(w,h))
    font='Helvetica'; bold='Helvetica-Bold'
    assets=Path(__file__).parent/'assets'
    regular=assets/'CertificateFont.ttf'; strong=assets/'CertificateFont-Bold.ttf'
    if regular.exists():
        pdfmetrics.registerFont(TTFont('CertificateFont',str(regular)));font='CertificateFont'
    if strong.exists():
        pdfmetrics.registerFont(TTFont('CertificateBold',str(strong)));bold='CertificateBold'
    c.setTitle('EXCELerate MathQuest Certificate of Participation')
    c.setFillColor(HexColor('#f1fbff'));c.rect(0,0,w,h,fill=1,stroke=0)
    c.setStrokeColor(HexColor('#53a9bd'));c.setLineWidth(3);c.roundRect(25,25,w-50,h-50,20)
    c.setStrokeColor(HexColor('#bde4ee'));c.rect(35,35,w-70,h-70)
    def line(text,y,size=14,face=None):
        c.setFillColor(HexColor('#174052'));c.setFont(face or font,size);c.drawCentredString(w/2,y,text)
    # Original vector penguin: needs no external image or emoji font.
    c.setFillColor(HexColor('#203543'));c.ellipse(w/2-22,h-83,w/2+22,h-32,fill=1,stroke=0)
    c.setFillColor(HexColor('#ffffff'));c.ellipse(w/2-15,h-80,w/2+15,h-43,fill=1,stroke=0)
    c.setFillColor(HexColor('#ffffff'));c.circle(w/2,h-45,12,fill=1,stroke=0)
    c.setFillColor(HexColor('#e9aa29'));c.circle(w/2,h-47,4,fill=1,stroke=0)
    c.setFillColor(HexColor('#203543'));c.circle(w/2-7,h-42,2,fill=1,stroke=0);c.circle(w/2+7,h-42,2,fill=1,stroke=0)
    line('EXCELerate Learning Space',h-108,20,bold)
    line('CERTIFICATE OF PARTICIPATION',h-143,25,bold)
    line('This certificate is presented to',h-180)
    name=profile['name'];size=30
    while pdfmetrics.stringWidth(name,bold,size)>w-120 and size>10:size-=1
    line(name,h-223,size,bold)
    line('for completing EXCELerate Penguin MathQuest',h-257,16)
    line(f"Primary {profile['year']} | {profile['topic']} | {profile['mode']}",h-286,14)
    line(profile['syllabus'],h-310,12)
    stats=summary(results)
    line(f"Questions completed: {stats['questions']}   |   Correct: {stats['correct']}/{stats['questions']}",h-346,15)
    line(f"Total score: {stats['score']} points   |   Accuracy: {stats['accuracy']:.1f}%   |   Best streak: {stats['best_streak']}",h-373,14)
    y=h-401
    for difficulty in dict.fromkeys(r['difficulty'] for r in results):
        s=summary([r for r in results if r['difficulty']==difficulty])
        line(f"{difficulty}: {s['correct']}/{s['questions']} correct, {s['score']} points",y,12);y-=20
    line('Keep thinking, keep exploring, keep waddling forward!',82,13)
    date=datetime.now(ZoneInfo('Asia/Kuching')).strftime('%d %B %Y')
    line(f'{date} | Participation record: {run_id[:8]}',57,10)
    c.showPage();c.save();return out.getvalue()
