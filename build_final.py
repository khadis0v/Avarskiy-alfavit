"""Build the selected offline trainer; syllable and word share one source recording."""
from pathlib import Path
import base64,json,subprocess,wave

root=Path(__file__).parent
items=[
    {'letter':'Гъ','syllable':'гъу','syllableAudio':'01-1.wav','words':[('рагъ','война, бой','01-3.wav'),('гъветӏ','дерево','01-2.wav'),('тӏагъур','шапка','08-1.wav')]},
    {'letter':'Гь','syllable':'гьа','syllableAudio':'02-1.wav','words':[('мугь','зёрнышко','02-3.wav'),('гьан','мясо','02-1.wav'),('вегьи','приход','extra-vegyi.wav')]},
    {'letter':'ГӀ','syllable':'гӏе','syllableAudio':'03-1.wav','words':[('рагӏи','слово','03-2.wav'),('нугӏ','свидетель','extra-nugi.wav'),('гӏеч','яблоко','03-1.wav')]},
    {'letter':'Къ','syllable':'къу','syllableAudio':'04-1.wav','words':[('бакъ','солнце','extra-bak.wav'),('ункъо','четыре','extra-unko.wav'),('къо','день','04-2.wav')]},
    {'letter':'Кь','syllable':'кье','syllableAudio':'05-1.wav','words':[('вакьад','тесть','extra-vakyad.wav'),('некь','след','extra-neky.wav'),('кьибил','корень, основа','05-3.wav')]},
    {'letter':'КӀ','syllable':'кӏа','syllableAudio':'06-1.wav','words':[('букӏине','быть','extra-bukine.wav'),('накӏкӏ','облако','extra-nakk.wav'),('кӏул','ключ','06-2.wav')]},
    {'letter':'Лъ','syllable':'лъа','syllableAudio':'07-1.wav','words':[('нилъ','серп','07-3.wav'),('лъор','душа','07-2.wav'),('балъ','обычай','extra-bal.wav')]},
    {'letter':'ТӀ','syllable':'тӏа','syllableAudio':'08-1.wav','words':[('лӏутӏ','кол','08-2.wav'),('тӏагъур','шапка','08-1.wav'),('гъветӏ','дерево','08-3.wav')]},
    {'letter':'Хъ','syllable':'хъе','syllableAudio':'09-1.wav','words':[('рахъ','канал','extra-rah.wav'),('хъал','слой, шелуха','09-2.wav'),('рахъу','зола','extra-rahu.wav')]},
    {'letter':'Хь','syllable':'хьа','syllableAudio':'10-1.wav','words':[('рахь','молоко','10-3.wav'),('хьибил','бок','10-2.wav'),('чехь','живот','extra-cheh.wav')]},
    {'letter':'ХӀ','syllable':'хӏа','syllableAudio':'11-1.wav','words':[('гохӏ','холм','11-3.wav'),('хӏан','сыр','11-1.wav'),('махӏ','запах','extra-mah.wav')]},
    {'letter':'ЦӀ','syllable':'цӏе','syllableAudio':'12-1.wav','words':[('мацӏ','язык','extra-mac.wav'),('цӏер','лёд, стекло','12-1.wav'),('бацӏ','волк','extra-bac.wav')]},
    {'letter':'ЧӀ','syllable':'чӏа','syllableAudio':'13-1.wav','words':[('мачӏу','кремень','13-4.wav'),('бачӏин','приезд','extra-bachin.wav'),('чӏор','стрела','13-3.wav')]},
]
out=root/'assets/pairs'
out.mkdir(exist_ok=True)
normal=root/'assets/normalized'
normal.mkdir(exist_ok=True)
for i,item in enumerate(items,1):
    source_names=[entry[2] for entry in item['words'] if entry[2]]
    norm_paths=[]
    for source_name in source_names:
        norm=normal/source_name
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(root/'assets/words3'/source_name),'-af','loudnorm=I=-18:LRA=7:TP=-2','-ar','24000','-ac','1',str(norm)],check=True)
        norm_paths.append(norm)
    pair=out/f'{i:02}.wav'
    word_segments=''.join(f'[{n}:a]' for n in range(len(norm_paths)))
    filters=f'{word_segments}concat=n={len(norm_paths)}:v=0:a=1[out]'
    command=['ffmpeg','-y','-loglevel','error']
    for path in norm_paths: command.extend(['-i',str(path)])
    command.extend(['-filter_complex',filters,'-map','[out]','-ar','24000','-ac','1',str(pair)])
    subprocess.run(command,check=True)
    durations=[]
    for path in norm_paths:
        with wave.open(str(path)) as sound:
            durations.append(round(sound.getnframes()/sound.getframerate(),3))
    starts=[0, durations[0], round(durations[0]+durations[1],3)]
    item.update(wordStarts=starts,audio='data:audio/wav;base64,'+base64.b64encode(pair.read_bytes()).decode())

font=base64.b64encode((root/'assets/golos-text.ttf').read_bytes()).decode()
buttons=''.join(f'<button class="letter" type="button" data-index="{i}" aria-pressed="false" aria-label="Прослушать три слова для буквы {x["letter"]}"><span lang="av">{x["letter"]}</span></button>' for i,x in enumerate(items))
html='''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><meta name="description" content="Нажмите на одну из 13 особых букв аварского алфавита: прозвучат три простых слова с переводом. Работает без интернета."><meta name="color-scheme" content="dark"><meta name="theme-color" content="#17252d"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg" type="image/svg+xml"><title>Аварский алфавит | Слушайте и повторяйте</title>
<style>
@font-face{font-family:'Golos Text';src:url(data:font/ttf;base64,FONT);font-weight:500;font-display:swap}
:root{--bg:#17252d;--surface:#243842;--ink:#edf4f6;--muted:#b2c6d0;--accent:#c3dce8;--font-main:'Golos Text';--radius:14px}
*{box-sizing:border-box}html{color-scheme:dark;scroll-padding-bottom:110px}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-main),sans-serif;font-weight:500}::selection{background:var(--accent);color:var(--bg)}button,a{-webkit-tap-highlight-color:transparent}button{font:inherit;cursor:pointer}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:5px}
main{max-width:1200px;margin:0 auto;padding:clamp(32px,6vw,72px) 40px 0;min-height:calc(100svh - 100px)}.heading{display:flex;justify-content:space-between;align-items:baseline;gap:24px}.heading h1{font-size:clamp(28px,3.6vw,42px);font-weight:500;line-height:1.15;letter-spacing:-.025em;text-wrap:balance;margin:0}.heading p{font-size:14px;white-space:nowrap;color:var(--muted);margin:0}.instruction{font-size:15px;color:var(--muted);line-height:1.6;margin:16px 0 30px;max-width:65ch}
.letters{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px}.letter{min-height:128px;padding:20px 10px;border:0;border-radius:var(--radius);background:var(--surface);color:var(--ink);font-size:clamp(38px,4.5vw,60px);font-weight:500;line-height:1;transition:background 130ms,color 130ms,transform 130ms;touch-action:manipulation}.letter:hover{background:#314a57}.letter[aria-pressed=true]{background:var(--accent);color:var(--bg)}.letter:active{transform:scale(.97)}
.feedback{position:sticky;bottom:0;z-index:2;background:var(--bg);min-height:112px;padding:22px 0 18px;display:flex;align-items:center;gap:20px}.playing-letter{display:none;align-items:center;justify-content:center;width:54px;height:54px;flex:none;background:var(--surface);border-radius:10px;font-size:25px}.feedback[data-selected=true] .playing-letter{display:flex}.examples{display:flex;flex-wrap:wrap;gap:6px 12px;margin:0}.example{font-size:22px;line-height:1.3;overflow-wrap:anywhere}.example[data-current=true]{color:var(--accent)}.translation{margin:5px 0 0;font-size:14px;color:var(--muted);line-height:1.5}.phase{margin-left:auto;font-size:13px;color:var(--muted);max-width:18ch;text-align:right;line-height:1.5}.initial{font-size:15px;color:var(--muted)}
footer{max-width:1200px;margin:auto;padding:18px 40px 28px;color:var(--muted);font-size:12px;line-height:1.7}footer a{color:var(--accent);text-underline-offset:4px}summary{cursor:pointer;width:fit-content;min-height:32px}details p{max-width:65ch;margin:10px 0 0}audio{display:none}
@media(max-width:700px){main{padding:30px 20px 0;min-height:calc(100svh - 90px)}.heading{display:block}.heading p{margin-top:12px}.instruction{font-size:14px;margin:16px 0 24px}.letters{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.letter{min-height:100px;font-size:40px}.feedback{min-height:118px;gap:12px;padding:18px 0}.playing-letter{width:44px;height:44px;font-size:24px}.example{font-size:20px}.phase{font-size:11px;max-width:11ch}footer{padding:14px 20px 24px}}
@media(max-width:350px){.letter{min-height:88px;font-size:36px}.phase{display:none}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
</style></head><body><main><header class="heading"><h1>Аварский алфавит</h1><p>13 особых букв</p></header><p class="instruction">Нажмите на букву. Прозвучат три слова подряд.</p>
<div class="letters" role="group" aria-label="Прослушивание аварских букв">BUTTONS</div>
<section class="feedback" data-selected="false" aria-label="Выбранная буква"><span class="playing-letter" id="selected-letter" lang="av" aria-hidden="true"></span><div role="status" aria-live="polite" aria-atomic="true"><p class="examples initial" id="words">Выберите букву, чтобы начать.</p><p class="translation" id="translation"></p></div><span class="phase" id="phase" aria-hidden="true"></span></section>
<audio id="player" preload="none"></audio></main>
<footer><details><summary>О записях</summary><p>Слова и переводы взяты из <a href="https://pkholyavin.github.io/avar/" target="_blank" rel="noopener noreferrer">учебного пособия по аварскому языку</a>, составленного в СПбГУ. Для каждой буквы три слова произносятся подряд, без добавленных пауз.</p><p>Все записи и шрифт встроены в этот HTML-файл. Для прослушивания интернет не нужен. Повторное нажатие запускает запись сначала; другая буква прерывает текущую. Клавиша Escape останавливает звук.</p></details></footer>
<script>
'use strict';
const items=ITEMS;
const player=document.getElementById('player');
const buttons=[...document.querySelectorAll('.letter')];
const feedback=document.querySelector('.feedback'),words=document.getElementById('words'),translation=document.getElementById('translation'),phase=document.getElementById('phase');
let generation=0,active=-1;
function resetPlayback(){generation++;player.onended=null;player.onerror=null;player.pause();player.currentTime=0;buttons.forEach(b=>b.setAttribute('aria-pressed','false'));}
function showError(token){if(token!==generation)return;resetPlayback();phase.textContent='Повторите нажатие';translation.textContent='Не удалось воспроизвести запись. Нажмите на букву ещё раз.';}
buttons.forEach((button,index)=>button.addEventListener('click',()=>{
 resetPlayback();active=index;const item=items[index],token=generation;
 feedback.dataset.selected='true';document.getElementById('selected-letter').textContent=item.letter;
 words.classList.remove('initial');words.innerHTML=item.words.map((entry,i)=>'<span class="example" data-word="'+i+'" data-current="false" lang="av">'+entry[0]+'</span>').join('');translation.textContent=item.words.map(entry=>entry[1]).join(' · ');phase.textContent='Слово 1 из 3';
 button.setAttribute('aria-pressed','true');player.src=item.audio;
 player.onended=()=>{if(token!==generation)return;button.setAttribute('aria-pressed','false');phase.textContent='Нажмите, чтобы повторить';};
 player.onerror=()=>showError(token);
 const attempt=player.play();if(attempt)attempt.catch(()=>showError(token));
}));
player.addEventListener('timeupdate',()=>{if(active<0||player.paused)return;const item=items[active],time=player.currentTime,current=time>=item.wordStarts[2]?2:time>=item.wordStarts[1]?1:0;phase.textContent='Слово '+(current+1)+' из 3';words.querySelectorAll('[data-word]').forEach(node=>node.dataset.current=String(Number(node.dataset.word)===current));});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){resetPlayback();phase.textContent='Остановлено';}});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&!player.paused){resetPlayback();phase.textContent='Остановлено';}});
// На учебной сетке жест двумя пальцами не должен менять масштаб страницы.
document.addEventListener('gesturestart',event=>event.preventDefault(),{passive:false});
document.addEventListener('gesturechange',event=>event.preventDefault(),{passive:false});
document.addEventListener('gestureend',event=>event.preventDefault(),{passive:false});
document.addEventListener('touchmove',event=>{if(event.touches.length>1)event.preventDefault();},{passive:false});
if('serviceWorker'in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
</script></body></html>'''
html=html.replace('FONT',font).replace('BUTTONS',buttons).replace('ITEMS',json.dumps(items,ensure_ascii=False))
(root/'index.html').write_text(html)
(root/'avarsky-alfavit.html').write_text(html)
ledger=[{k:v for k,v in x.items() if k!='audio'} for x in items]
(root/'assets/pairs.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
print('Built offline trainer:',len(html.encode()),'bytes;',len(items),'three-word sequences')
