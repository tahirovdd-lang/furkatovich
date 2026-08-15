from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacements = {
    "mkFood('salad_ruletiki_baklazhan',{ru:'Рулетики из баклажана'},'',10000,'salads')": "mkFood('salad_ruletiki_baklazhan',{ru:'Рулетики из баклажана',uz:'Baqlajon ruletlari',en:'Eggplant rolls',tj:'Рулетҳои бодинҷон'},'',10000,'salads')",
    "mkFood('salad_shef',{ru:'Салат от шефа'},'',18000,'salads')": "mkFood('salad_shef',{ru:'Салат от шефа',uz:'Shef salati',en:'Chef salad',tj:'Салати шеф'},'',18000,'salads')",
    "mkFood('salad_yaichnitsa_shuba',{ru:'Яичница под шубой'},'',17000,'salads')": "mkFood('salad_yaichnitsa_shuba',{ru:'Яичница под шубой',uz:'Shuba ostidagi tuxum',en:'Egg under a fur coat',tj:'Тухм зери шуба'},'',17000,'salads')",
}
for old, new in replacements.items():
    s = s.replace(old, new)

anchor = "function formatSum(x){ const n=Number(x)||0; return n.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,' '); }"
if 'function localizedMeta(' not in s:
    helper = anchor + "\n" + """function localizedMeta(meta,targetLang=lang){
  let v=String(meta||'').trim();
  if(!v)return '';
  const units={ru:{g:'гр',ml:'мл',kg:'кг',l:'л'},uz:{g:'g',ml:'ml',kg:'kg',l:'l'},en:{g:'g',ml:'ml',kg:'kg',l:'l'},tj:{g:'г',ml:'мл',kg:'кг',l:'л'}};
  const u=units[targetLang]||units.en;
  v=v.replace(/(\\d+(?:[.,]\\d+)?)\\s*(гр|г|g)/gi,(_,n)=>n+' '+u.g);
  v=v.replace(/(\\d+(?:[.,]\\d+)?)\\s*(мл|ml)/gi,(_,n)=>n+' '+u.ml);
  v=v.replace(/(\\d+(?:[.,]\\d+)?)\\s*(кг|kg)/gi,(_,n)=>n+' '+u.kg);
  v=v.replace(/(\\d+(?:[.,]\\d+)?)\\s*(л|l)/gi,(_,n)=>n+' '+u.l);
  return v;
}"""
    s = s.replace(anchor, helper)

s = s.replace("const id=it.id,qty=cart[id]||0,meta=it.meta?String(it.meta):'';", "const id=it.id,qty=cart[id]||0,meta=localizedMeta(it.meta);")
s = s.replace("${escapeHtml(it.meta)}", "${escapeHtml(localizedMeta(it.meta))}")
s = s.replace("${it.meta||'—'}\\n${UI[lang].price}", "${localizedMeta(it.meta)||'—'}\\n${UI[lang].price}")
s = s.replace("it.meta?`<div class=\"cart-item-meta\">${escapeHtml(it.meta)}</div>`:''", "it.meta?`<div class=\"cart-item-meta\">${escapeHtml(localizedMeta(it.meta))}</div>`:''")

p.write_text(s, encoding='utf-8')
