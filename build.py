"""Build a self-contained, offline design preview. No network at runtime."""
from pathlib import Path
import base64, json, re

root = Path(__file__).parent
letters = ['Гъ','Гь','ГӀ','Къ','Кь','КӀ','Лъ','ТӀ','Хъ','Хь','ХӀ','ЦӀ','ЧӀ']
fonts = [('Golos Text','golos-text'),('PT Sans','pt-sans'),('Manrope','manrope'),('IBM Plex Sans','ibm-plex-sans'),('Literata','literata')]
font_css = ''.join("@font-face{font-family:'%s';src:url(data:font/ttf;base64,%s);font-display:swap}" % (name, base64.b64encode((root/'assets'/f'{slug}.ttf').read_bytes()).decode()) for name,slug in fonts)
sounds = {int(p.stem)-1:'data:audio/wav;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (root/'assets').glob('*.wav')}
buttons = ''.join(f'<button class="letter" data-index="{i}" aria-label="Прослушать {l}" aria-pressed="false"><span lang="av">{l}</span></button>' for i,l in enumerate(letters))
html = '''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Предварительный выбор тёмного оформления страницы с 13 особыми буквами аварского алфавита."><meta name="color-scheme" content="dark"><title>Аварский алфавит | Выбор оформления</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2317252d'/%3E%3Ctext x='8' y='45' fill='white' font-size='35'%3EГъ%3C/text%3E%3C/svg%3E">
<style>FONT_CSS
*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#101a20;color:#f0f4f5;font-family:'Golos Text',sans-serif}button,a{-webkit-tap-highlight-color:transparent}button{font:inherit;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #fff;outline-offset:5px}::selection{background:#aac9d8;color:#14232c}
.chooser{padding:24px max(20px,calc((100vw - 1120px)/2));background:#101a20}.chooser h1{font-size:22px;line-height:1.2;font-weight:500;margin:0 0 12px;text-wrap:balance}.intro{color:#bcc8ce;font-size:14px;line-height:1.6;max-width:65ch;margin:0 0 18px}.choices{display:flex;gap:8px;flex-wrap:wrap}.choice{min-height:44px;padding:10px 16px;border:1px solid #53636b;border-radius:8px;background:transparent;color:#d4dfe4}.choice[aria-pressed=true]{background:#d1e3ed;border-color:#d1e3ed;color:#17252d}.hint{font-size:13px;color:#b7c5cc;line-height:1.6;margin:16px 0 0}.stage{--bg:#17252d;--surface:#243842;--ink:#edf4f6;--muted:#b2c6d0;--accent:#c3dce8;--font:'Golos Text';background:var(--bg);color:var(--ink);min-height:600px;padding:44px max(20px,calc((100vw - 1120px)/2)) 36px;font-family:var(--font),sans-serif;transition:background 160ms}.heading{display:flex;justify-content:space-between;align-items:baseline;gap:24px;margin-bottom:32px}.heading h2{font-size:clamp(25px,3.6vw,42px);font-weight:500;margin:0;line-height:1.15;text-wrap:balance;letter-spacing:-.025em}.heading p{color:var(--muted);font-size:14px;margin:0;white-space:nowrap}.letters{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px}.letter{min-height:128px;border:0;border-radius:14px;background:var(--surface);color:var(--ink);font-size:clamp(38px,4.5vw,60px);font-weight:500;line-height:1;transition:background 130ms,color 130ms,transform 130ms;touch-action:manipulation}.letter:hover{background:color-mix(in srgb,var(--surface),var(--ink) 14%)}.letter[aria-pressed=true]{background:var(--accent);color:var(--bg)}.letter:active{transform:scale(.97)}.status{min-height:48px;margin:24px 0 0;font-size:15px;color:var(--muted);line-height:1.6;max-width:65ch}.source{padding:24px max(20px,calc((100vw - 1120px)/2)) 32px;font-size:13px;color:#b7c5cc;line-height:1.7}.source a{color:#d1e3ed;text-underline-offset:4px}.source p{margin:0 0 10px;max-width:65ch}
.stage[data-theme="2"]{--bg:#252728;--surface:#3a3e3f;--ink:#f1f0ec;--muted:#c5c6c2;--accent:#d9cec0;--font:'PT Sans'}.stage[data-theme="2"] .letters{grid-template-columns:repeat(7,minmax(0,1fr));gap:20px}.stage[data-theme="2"] .letter{aspect-ratio:1;border-radius:50%;min-height:0}.stage[data-theme="2"] .heading{margin-bottom:44px}
.stage[data-theme="3"]{--bg:#192c2c;--surface:#2d4544;--ink:#e9f2ed;--muted:#b8ccc5;--accent:#c3d6ca;--font:'Manrope'}.stage[data-theme="3"] .letters{grid-template-columns:repeat(5,minmax(0,1fr));gap:2px}.stage[data-theme="3"] .letter{border-radius:0;min-height:112px}.stage[data-theme="3"] .heading{display:block}.stage[data-theme="3"] .heading p{margin-top:14px}
.stage[data-theme="4"]{--bg:#242c3b;--surface:#354054;--ink:#eef0f6;--muted:#bdc6d9;--accent:#c9d4ed;--font:'IBM Plex Sans'}.stage[data-theme="4"] .letters{grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.stage[data-theme="4"] .letter{min-height:94px;border-radius:6px;text-align:left;padding-left:28px}.stage[data-theme="4"] .heading{margin-bottom:24px}
.stage[data-theme="5"]{--bg:#302a28;--surface:#443b37;--ink:#f4eee8;--muted:#cfc2b9;--accent:#e1c8b8;--font:'Literata'}.stage[data-theme="5"] .letters{grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}.stage[data-theme="5"] .letter{background:transparent;border:1px solid #79675e;min-height:124px;border-radius:12px}.stage[data-theme="5"] .letter[aria-pressed=true]{background:var(--accent)}.stage[data-theme="5"] .letter:hover{background:var(--surface)}.stage[data-theme="5"] .heading{display:block}.stage[data-theme="5"] .heading p{margin-top:16px}
@media(max-width:700px){.chooser{padding-top:20px}.stage{padding-top:32px;min-height:0}.heading{display:block;margin-bottom:24px}.heading p{margin-top:12px}.letters,.stage[data-theme="2"] .letters,.stage[data-theme="3"] .letters,.stage[data-theme="4"] .letters,.stage[data-theme="5"] .letters{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.letter{font-size:40px;min-height:100px}.stage[data-theme="2"] .letters{gap:16px}.stage[data-theme="3"] .letter{min-height:100px}.stage[data-theme="4"] .letter{padding-left:18px;min-height:90px}.stage[data-theme="5"] .letter{min-height:108px}.choice{padding:10px 13px}.status{min-height:78px}.intro{font-size:14px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
</style></head><body>
<header class="chooser"><h1>Выберите оформление</h1><p class="intro">Это предварительный просмотр. Отдельные звуки пока найдены для Кь, Лъ, ЦӀ и ЧӀ. Остальные кнопки показывают выбор буквы, но ещё не озвучены.</p><nav class="choices" aria-label="Варианты оформления">CHOICES</nav><p class="hint" id="design-note">Вариант 1. Крупные клавиши на сине-сером фоне. Рекомендую для частого повторения.</p></header>
<main class="stage" data-theme="1"><div class="heading"><h2>Аварский алфавит</h2><p>13 особых букв</p></div><div class="letters" role="group" aria-label="Прослушивание букв">BUTTONS</div><p class="status" id="status" role="status" aria-live="polite">Нажмите на букву.</p></main>
<footer class="source"><p>Записи отдельных звуков: <a href="https://pkholyavin.github.io/avar/" target="_blank" rel="noopener noreferrer">методическое пособие по аварскому языку</a>, составленное в СПбГУ. Четыре записи встроены в этот файл и доступны без интернета. Принадлежность всех записей одному диктору не подтверждена.</p><p>Полный набор со слогами: <a href="https://www.youtube.com/watch?v=Klo83A0OBro" target="_blank" rel="noopener noreferrer">видеоурок Сарат Мухумаевой</a>. Его звук пока не используется: для замены отдельных звуков слогами нужно ваше согласие.</p><p>Переключите варианты кнопками и сообщите номер понравившегося.</p></footer>
<script>
'use strict';
const letters=LETTERS, sounds=SOUNDS;
const stage=document.querySelector('.stage'), status=document.getElementById('status');
const notes=['Крупные клавиши на сине-сером фоне. Рекомендую для частого повторения.','Круглые кнопки на графитовом фоне.','Плотная сетка на тёмно-зелёном фоне.','Прямоугольные клавиши с буквами у левого края.','Контурные клавиши с книжными буквами.'];
let current=null, generation=0;
function stop(){generation++;if(current){current.pause();current.currentTime=0;current=null;}document.querySelectorAll('.letter').forEach(b=>b.setAttribute('aria-pressed','false'));}
document.querySelectorAll('.choice').forEach(button=>button.addEventListener('click',()=>{stop();const n=Number(button.dataset.theme);stage.dataset.theme=String(n);document.querySelectorAll('.choice').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.getElementById('design-note').textContent='Вариант '+n+'. '+notes[n-1];status.textContent='Нажмите на букву.';}));
document.querySelectorAll('.letter').forEach(button=>button.addEventListener('click',()=>{stop();const i=Number(button.dataset.index);button.setAttribute('aria-pressed','true');if(!sounds[i]){status.textContent='Для '+letters[i]+' запись отдельного звука ещё не найдена.';return;}const token=generation;const audio=new Audio(sounds[i]);current=audio;status.textContent='Звучит '+letters[i];audio.onended=()=>{if(token!==generation)return;button.setAttribute('aria-pressed','false');status.textContent='Нажмите ещё раз, чтобы повторить '+letters[i]+'.';current=null;};audio.play().catch(()=>{if(token!==generation)return;button.setAttribute('aria-pressed','false');status.textContent='Не удалось включить звук. Нажмите на букву ещё раз.';current=null;});}));
document.addEventListener('keydown',event=>{if(event.key==='Escape'){stop();status.textContent='Воспроизведение остановлено.';}});
document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();status.textContent='Нажмите на букву.';}});
</script></body></html>'''
choices=''.join(f'<button class="choice" data-theme="{i}" aria-pressed="{str(i==1).lower()}">Вариант {i}</button>' for i in range(1,6))
html=html.replace('FONT_CSS',font_css).replace('CHOICES',choices).replace('BUTTONS',buttons).replace('LETTERS',json.dumps(letters,ensure_ascii=False)).replace('SOUNDS',json.dumps(sounds,ensure_ascii=False))
(root/'variants.html').write_text(html)
# Each variant is also independently reviewable, without a build tool.
for i in range(1,6):
    folder=root/'variants'/str(i)
    folder.mkdir(parents=True,exist_ok=True)
    variant=html.replace('<main class="stage" data-theme="1">',f'<main class="stage" data-theme="{i}">')
    family,slug=fonts[i-1]
    selected_face="@font-face{font-family:'%s';src:url(data:font/ttf;base64,%s);font-display:swap}" % (family,base64.b64encode((root/'assets'/f'{slug}.ttf').read_bytes()).decode())
    accent=['#c3dce8','#d9cec0','#c3d6ca','#c9d4ed','#e1c8b8'][i-1]
    variant=variant.replace(font_css,selected_face+f":root{{--font-main:'{family}';--accent:{accent}}}")
    variant=variant.replace("font-family:'Golos Text',sans-serif",f"font-family:'{family}',sans-serif")
    variant=re.sub(r'<nav class="choices".*?</nav>','',variant)
    variant=re.sub(r'<p class="hint" id="design-note">.*?</p>',f'<p class="hint" id="design-note">Вариант {i}</p>',variant)
    (folder/'index.html').write_text(variant)
# Preview only. The selected trainer is written by build_final.py.
print('Built variants.html:',len(html.encode()),'bytes; embedded recordings:',len(sounds))
