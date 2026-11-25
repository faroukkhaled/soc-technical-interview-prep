import csv
import html
import io
import json


def anki_csv(questions):
    """Tab-separated, importable by Anki: front, back, tags."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    for q in questions:
        w.writerow([q.text, q.answer, "soc %s level%d" % (q.domain, q.level)])
    return buf.getvalue()


def flashcards_html(questions):
    data = [{"q": q.text, "a": q.answer, "d": q.domain, "l": q.level} for q in questions]
    blob = json.dumps(data).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    domains = sorted({q.domain for q in questions})
    opts = "".join('<option value="%s">%s</option>' % (html.escape(d), html.escape(d)) for d in domains)
    return """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOC interview flashcards</title>
<style>body{font:16px system-ui;max-width:720px;margin:2rem auto;padding:0 1rem}.card{border:1px solid #ccc;border-radius:10px;padding:1.5rem;min-height:140px;cursor:pointer}
.tag{color:#666;font-size:13px}button,select{font:inherit;padding:.4rem .8rem;margin:.3rem .3rem .3rem 0}</style>
<h1>SOC interview flashcards</h1>
<select id="dom"><option value="">all domains</option>%s</select> <button id="shuffle">Shuffle</button> <span id="count"></span>
<div class="card" id="card"></div><p><button id="prev">Prev</button><button id="flip">Show answer</button><button id="next">Next</button></p>
<script>
const DATA=%s;let list=DATA.slice(),i=0,show=false;
const el=id=>document.getElementById(id);
function render(){const c=list[i];el('count').textContent=(i+1)+' / '+list.length;
 el('card').innerHTML='';const t=document.createElement('div');t.className='tag';t.textContent=c.d+' | level '+c.l;
 const b=document.createElement('p');b.textContent=show?c.a:c.q;b.style.fontWeight=show?'normal':'600';
 el('card').append(t,b);el('flip').textContent=show?'Show question':'Show answer';}
function go(d){i=(i+d+list.length)%%list.length;show=false;render()}
el('next').onclick=()=>go(1);el('prev').onclick=()=>go(-1);el('flip').onclick=el('card').onclick=()=>{show=!show;render()};
el('shuffle').onclick=()=>{list.sort(()=>Math.random()-.5);i=0;show=false;render()};
el('dom').onchange=e=>{list=DATA.filter(c=>!e.target.value||c.d===e.target.value);i=0;show=false;render()};
render();
</script>""" % (opts, blob)
