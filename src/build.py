import json, os, re, shutil, html
from pathlib import Path
S=str(Path(__file__).resolve().parents[1])   # repo root
D=f'{S}/src/data'
pins=json.load(open(f'{D}/venues.json'))
research=[]
for f in ['research_1.json','research_2.json','research_3.json']: research+=json.load(open(f'{D}/{f}'))
research.append(json.load(open(f'{D}/research_27.json')))
pins.append({"name":"Six Flags Magic Mountain","lat":34.4253,"lon":-118.5971})
th=json.load(open(f'{D}/research_theater.json'))
lm=dict(th['la_mirada']); deh=th['dear_evan_hansen']
lm['facts']=[f"Dear Evan Hansen plays here through Nov 22, 2026. On your weekend: Sat Nov 7 at 2pm and 8pm, Sun Nov 8 at 1:30pm and 6:30pm. About 2.5 hours with one intermission.",
 "Dear Evan Hansen is recommended for ages 13 and up. It has adult language and deals with depression and suicide.",
 "The theatre opened in 1977 in a converted movie house and is owned and run by the City of La Mirada.",
 "McCoy Rigby Entertainment produces its Broadway Series of five professional shows a year. The 2026-27 season also has Little Shop of Horrors and Les Miserables.",
 "About 1,250 seats, so it feels big but not cavernous.",
 "Parking is free in the lot next door, shared with a shopping center. It fills up, so arrive early."]
lm['what_it_is']="A city-run performing arts theatre in La Mirada that stages a five-show Broadway Series with McCoy Rigby Entertainment. Dear Evan Hansen runs here Oct 30 to Nov 22, 2026."
lm['price']="Single-ticket face value not posted online. Season-package seats run about $109 to $356. Resale sites quote more. Online orders add a 10% fee per ticket."
lm['hours_note']="Show times only. Box office 714-994-6310."
lm['booking_note']="Book direct at lamiradatheatre.com/tickets. Skip resale sites."
lm['neighborhood']="La Mirada"
research.append(lm)
pins.append({"name":"La Mirada Theatre","lat":33.9169,"lon":-118.0117})
# show-specific lines for the other three theater cards (index = venue number - 1)
research[9]['facts'].insert(0,"The Music Man national tour plays the Ahmanson through Sunday Nov 8, 2026, its first big LA run since 1980. Your weekend catches its last two days. Resale from about $38.")
research[9]['what_it_is']="The Music Center's big Broadway-style house, run by Center Theatre Group. The Music Man plays Oct 27 to Nov 8, 2026, then Oh, Mary! Nov 10 to Dec 6 and Christmas Carol Goes Wrong Dec 12 to Jan 10."
research[10]['facts'].insert(0,"Come From Away runs through its closing performance Sunday Nov 1, 2026 at 2pm. No extension was found. A Christmas Carol follows Nov 28 to Dec 24.")
research[10]['what_it_is']="A professional classical repertory theatre in Pasadena. Come From Away closes Nov 1, 2026. A Christmas Carol runs Nov 28 to Dec 24."
research[3]['facts'].insert(0,"Weekly improv: Thursdays 8pm Cookin' with GAS (all improv, running since 1992), Fridays and Saturdays 7:30pm main-stage sketch and improv, 9:30pm The Completely Different Late Show. Confirm on the live calendar.")
sm=research[12]
sm['name']=pins[12]['name']="Sunshine Makers Market"
sm['what_it_is']="A free outdoor makers market that sets up in the courtyard of The Shops at Sportsmen's Lodge in Studio City on select Saturdays. Local makers sell handmade goods, art, jewelry and clothing, with the center's cafes and shops open around it."
sm['facts']=["Free entry. Past markets ran 10am to 4pm on a Saturday in the center's open-air courtyard.",
 "Dozens of local makers sell handmade jewelry, clothing, art, ceramics, candles and food.",
 "Same organizer runs markets at the Helms Design District in Culver City, including a dog-adoption mini market with Pup Culture Rescue."]+sm['facts'][1:4]
sm['price']="Free entry to the market. Goods and food cost what the makers charge."
sm['hours_note']="Market days are select Saturdays, 10am to 4pm. The 2026 date for this market was not posted online as of Oct 31, 2026. Confirm on sunshinemakersmarket.com."
sm['booking_note']="Walk in. No ticket."
sm['website']="https://www.sunshinemakersmarket.com/"
assert len(research)==28
CATS=[
 {"id":"hair","label":"Hair cut or color","exclusive":True,"blurb":"A cut or a color. Four hours on Monday with a stylist who does bold work."},
 {"id":"thrift","label":"Thrift and vintage stores","blurb":"Rack digging in stores that are open any day. Cheap finds, weird finds, a shop cat or two."},
 {"id":"market","label":"Markets that only happen that day","blurb":"Pop-up markets that exist for one day. Vintage vendors, makers, food, live music."},
 {"id":"anime","label":"Anime or maid cafe","blurb":"Themed drinks and desserts, live shows, photos with the cast."},
 {"id":"books","label":"Books and anime shops","blurb":"Walls of manga, used-book stacks with cats, and the first US store of Japan's biggest anime chain."},
 {"id":"show","label":"See a show","blurb":"Live theater. The improv house that fed Saturday Night Live, a Broadway tour, a regional premiere."},
 {"id":"eat","label":"Eat somewhere fun","blurb":"Drag brunch, a 1931 deli inside an old movie theater, teddy bear desserts."},
 {"id":"kbeauty","label":"K-beauty facial","blurb":"A Korean glass-skin facial with a tea ceremony."},
 {"id":"park","label":"Rollercoasters!","blurb":"Magic Mountain. Twenty coasters, the most on earth. Sunday only, full or half day."},
]
for c in CATS: c["img"]=f"images/cat-{c['id']}.png"
cat_of={1:"thrift",2:"hair",3:"books",4:"show",5:"books",6:"eat",7:"market",8:"hair",9:"hair",10:"show",11:"show",12:"skate",13:"market",14:"eat",15:"anime",16:"anime",17:"cats",18:"anime",19:"kbeauty",20:"thrift",21:"thrift",22:"thrift",23:"market",24:"thrift",25:"books",26:"eat",27:"park",28:"show"}
DROP=re.compile(r'(Yelp shows|Review sites rate|Discover Upland|The owner is Dan|4\.9 rating|Facebook shows|90 percent recommend)',re.I)
PAL=[('#0f6f73','#f6efe2'),('#e8603c','#fffaf0'),('#e9b23a','#23211d'),('#23211d','#e9b23a')]
def svg_fallback(i,name):
    bg,fg=PAL[i%4]; a=['#e8603c','#e9b23a','#0f6f73','#fffaf0'][(i+1)%4]
    initials=''.join(w[0] for w in re.findall(r"[A-Za-z]+",name)[:2]).upper()
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400"><rect width="600" height="400" fill="{bg}"/><circle cx="{470+(i%3)*20}" cy="{120+(i%5)*15}" r="{90+(i%4)*12}" fill="{a}" opacity=".9"/><rect x="-40" y="{300+(i%3)*10}" width="700" height="140" fill="{fg}" opacity=".18" transform="rotate(-6 300 330)"/><text x="48" y="330" font-family="Avenir Next,Helvetica,Arial,sans-serif" font-size="150" font-weight="800" fill="{fg}">{html.escape(initials)}</text></svg>'''
    return 'data:image/svg+xml;utf8,'+svg.replace('#','%23').replace('"',"'").replace('<','%3C').replace('>','%3E')

# Schedule rules. Blocks: sat-am sat-pm sat-night sun-am sun-pm sun-night mon-am mon-pm. slots: 2 = whole block, 1 = half.
AM=['sat-am','sun-am','mon-am']; PM=['sat-pm','sun-pm','mon-pm']; NIGHT=['sat-night','sun-night']
DAY=AM+PM; ANY=DAY+NIGHT
SCHED={
 1:(DAY,1,"Open daily from 11:30am"),            # Sunday's Best
 2:(['mon-am','mon-pm'],2,"Hair is Monday, 4 hours"),
 3:(DAY,1,"Open 10am to 8pm"),                    # Kinokuniya
 4:(['sat-night'],2,"Saturday 9:30pm show"),      # Groundlings
 5:(['sat-am','sat-pm'],1,"Closed Sunday and Monday"),  # Iliad
 6:(['sat-am','sun-am'],2,"Drag brunch, weekend mornings"),
 7:(['sat-am','sat-pm'],1,"Saturday market"),     # Pickwick
 8:(['mon-am','mon-pm'],2,"Hair is Monday, 4 hours"),
 9:(['mon-am','mon-pm'],2,"Hair is Monday, 4 hours"),
 10:(['sat-pm','sat-night','sun-pm','sun-night'],2,"The Music Man closes Sunday Nov 8"),
 13:(['sun-am','sun-pm'],1,"Sunday market, 10am to 4pm"),
 14:(PM+NIGHT,1,"Opens at noon"),                 # Somemore
 15:(ANY,1,"Open 11:30am to 9pm"),                # Dreamland
 16:(['sat-pm','sat-night','sun-pm','sun-night'],1,"Lunch and dinner seatings"),  # Asayoru
 18:(DAY,1,"Coffee shop hours"),                  # Anteiku
 19:(DAY,2,"Facial by appointment"),              # Hanok
 20:(DAY,1,"Open daily"),                         # St Vincent
 21:(DAY,1,"Open daily"),                         # TROVE
 22:(DAY,1,"Call for hours"),                     # Lemon Frog
 23:(['sun-am','sun-pm'],1,"Sunday market, 10am to 5pm"),  # Melrose
 24:(ANY,1,"Open daily, late on Saturday"),       # Squaresville
 25:(DAY,1,"Open daily"),                         # Animate
 26:(ANY,1,"Open 24 hours"),                      # Canter's
 27:(['sun-am'],2,"Sunday morning, or a full Sunday"),  # Magic Mountain (full = morning + afternoon)
 28:(['sat-pm','sat-night','sun-pm','sun-night'],2,"Sat 2pm or 8pm, Sun 1:30pm or 6:30pm"),
}
BLOCK_NAMES={'sat-am':'Sat morning','sat-pm':'Sat afternoon','sat-night':'Sat night','sun-am':'Sun morning','sun-pm':'Sun afternoon','sun-night':'Sun night','mon-am':'Mon morning','mon-pm':'Mon afternoon'}
pins[8]['name']="Little Shop of Hairdos"
GALLERY={
 9:"https://www.instagram.com/littleshopofhairdos?xtok=MW44bmU5bXppdndiZQ==",
 8:"https://www.instagram.com/flamingoloungehair?exln=bzc2MnJybWdseWdr",
}
DROP_VENUES={2,11,12,17}  # Come From Away closed Nov 1; ice rink opens Nov 12; CatCafe dropped by Jenna
HOOKS={
 1:"Color-coded thrift racks, a $1 rack out front, and a shop cat named Sunday.",
 2:"Gender-neutral barbershop from New York known for bold, affirming cuts.",
 3:"Japan's big bookstore chain. A new 14,000 square foot flagship packed with manga.",
 4:"The improv theater that trained a long line of Saturday Night Live cast members.",
 5:"100,000 used books in crooked stacks, plus two resident cats, Apollo and Zeus.",
 6:"Burgers with a live drag show at the oldest Hamburger Mary's still running.",
 7:"40 to 50 curated vintage vendors under one roof, one Saturday a month.",
 8:"A Y2K-decor salon doing rainbow color, flash tattoos and tooth gems.",
 9:"Vivid color and creative hair art in a salon reviewers call a great vibe.",
 10:"LA's big Broadway house. The Music Man plays through Sunday Nov 8.",
 13:"A free Sunday makers market in an open-air courtyard, with Erewhon next door.",
 14:"Teddy-bear cups, bear ice cubes and mille crepe cake. Built to be photographed.",
 15:"America's largest indie maid cafe, with live idol shows and cheki photos.",
 16:"A permanent maid cafe with high-energy shows and Japanese comfort food.",
 18:"A Tokyo Ghoul themed coffee shop with anime drinks and onigiri.",
 19:"Korean glass-skin facials with a tea ceremony and a hanbok fitting.",
 20:"LA's largest thrift store. Room after room of odd finds and bargains.",
 21:"Department-store-style consignment, from Zara to Prada.",
 22:"A closet-sized shop stuffed floor to ceiling with 50s to 90s vintage.",
 23:"A Sunday flea market with vintage, art and live music that funds school arts programs.",
 24:"Two floors of buy-sell-trade vintage. Bring old clothes for cash or trade.",
 25:"The first US store of Japan's biggest anime retailer. Figures, cards, manga.",
 26:"A 1931 Jewish deli inside an old movie theater, with a late-night music bar attached.",
 27:"20 roller coasters, the most of any theme park on earth.",
 28:"Dear Evan Hansen, regional premiere. Sat 2pm and 8pm, Sun 1:30pm and 6:30pm.",
}
out=[]; missing=[]
for n,(p,r) in enumerate(zip(pins,research),1):
    if n in DROP_VENUES: continue
    if os.path.exists(f'{S}/images/{n:02d}.jpg'): src=f'images/{n:02d}.jpg'
    else: src=svg_fallback(n,p['name']); missing.append(n)
    what=r.get('what_it_is','').strip()
    hook=HOOKS[n]
    out.append({"id":f"v{n:02d}","name":p['name'],"cat":cat_of[n],"typeLabel":r.get('type',''),"neighborhood":r.get('neighborhood','').split(' (')[0],
        "address":r.get('address'),"what":what,"hook":hook,"facts":[f for f in r.get('facts',[]) if not DROP.search(f)],
        "price":r.get('price'),"hours":r.get('hours_note'),"age":r.get('age_note'),"booking":r.get('booking_note'),"website":r.get('website'),
        "img":src,"lat":p['lat'],"lon":p['lon'],
        "blocks":SCHED[n][0],"slots":SCHED[n][1],"when":SCHED[n][2],"spanOption":(n==27),
        "whenText":', '.join(BLOCK_NAMES[b] for b in SCHED[n][0]),"gallery":GALLERY.get(n)})
data={"categories":CATS,"venues":out,"blocks":[{"id":k,"label":v} for k,v in BLOCK_NAMES.items()]}
tpl=open(f'{S}/src/page_template.html').read()
page=tpl.replace('/*__DATA__*/',json.dumps(data,ensure_ascii=False))
cut=page.index('</style>')+len('</style>')
head=page[:cut]; body=page[cut:]
html=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
      +head+'</head><body>'+body+'</body></html>')
open(f'{S}/index.html','w').write(html)
print('wrote index.html; svg fallbacks for:',missing,'size KB:',len(html)//1024)
