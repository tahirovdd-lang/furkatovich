from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

start = s.index('const CATEGORY_LABELS = {')
end = s.index('\nlet mainGroup=', start)
block = """const CATEGORY_LABELS = {
  sides:{ru:'Гарниры',uz:'Garnirlar',en:'Sides',tj:'Гарнирҳо'},
  salads:{ru:'Салаты',uz:'Salatlar',en:'Salads',tj:'Хӯришҳо'},
  soups:{ru:'Супы',uz:'Sho‘rvalar',en:'Soups',tj:'Шӯрбоҳо'},
  hot_dishes:{ru:'Горячие блюда',uz:'Issiq taomlar',en:'Hot dishes',tj:'Таомҳои гарм'},
  plov:{ru:'Плов',uz:'Osh',en:'Plov',tj:'Оши палав'},
  bistro:{ru:'Бистро',uz:'Bistro',en:'Bistro',tj:'Бистро'},
  sets:{ru:'Сеты',uz:'Setlar',en:'Sets',tj:'Сетҳо'},
  hot_dog:{ru:'Хот-Дог',uz:'Hot-Dog',en:'Hot Dog',tj:'Хот-Дог'},
  cold_drinks:{ru:'Холодные напитки',uz:'Sovuq ichimliklar',en:'Cold drinks',tj:'Нӯшокиҳои хунук'},
  hot_drinks:{ru:'Горячие напитки',uz:'Issiq ichimliklar',en:'Hot drinks',tj:'Нӯшокиҳои гарм'},
  desserts:{ru:'Десерты',uz:'Desertlar',en:'Desserts',tj:'Шириниҳо'}
};
const GROUPS={menu:['sides','salads','soups','hot_dishes','plov','bistro','sets','hot_dog','cold_drinks','hot_drinks','desserts']};"""
s = s[:start] + block + s[end:]

menu_start = s.index('const MENU = {')
menu_end = s.index('\n};\n\nconst ITEM_INDEX', menu_start) + 3
old = s[menu_start:menu_end]

def extract(key):
    m = re.search(r'^  ' + re.escape(key) + r':\[(.*)\],?$', old, re.M)
    return m.group(1) if m else ''

vals = {k: extract(k) for k in ['sides','salads','soups','cold_drinks']}
order = ['sides','salads','soups','hot_dishes','plov','bistro','sets','hot_dog','cold_drinks','hot_drinks','desserts']
lines = ['const MENU = {']
for i, k in enumerate(order):
    body = vals.get(k, '')
    comma = ',' if i < len(order)-1 else ''
    lines.append(f'  {k}:[{body}]{comma}')
lines.append('};')
new_menu = '\n'.join(lines)
s = s[:menu_start] + new_menu + s[menu_end:]

p.write_text(s, encoding='utf-8')
