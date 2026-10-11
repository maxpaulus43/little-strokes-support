"""Family-facing dictionary derivative; original licensed records stay intact.

Suppress the entire English definition when it contains an unsuitable term,
so trimming clauses cannot accidentally change a character's meaning. Hanzi,
pinyin, stroke geometry, and exportable original JSON are preserved.
"""
import re

# These are whole-word matches, including listed inflections. For example,
# "opium" matches, while the chemical element "europium" does not.
TERMS = (
    r"fuck\w*|shit\w*|bitch\w*|bastard\w*|asshole\w*|cunt\w*|damn\w*|"
    r"piss\w*|crap|whore\w*|slut\w*|profan\w*|obscen\w*|vulgar(?:ity)?|"
    r"penis|penises|vagina\w*|genital\w*|testicl\w*|scrot\w*|phall\w*|"
    r"sexual\w*|sex|intercourse|copulat\w*|coitus|erotic\w*|porn\w*|"
    r"prostitut\w*|brothel\w*|rape(?:d|s)?|rapist\w*|molest\w*|incest\w*|"
    r"masturbat\w*|semen|sperm\w*|ejaculat\w*|orgasm\w*|sodom\w*|"
    r"adulter(?:y|er|ers|ous)|concubin\w*|castrat\w*|eunuch\w*|naked\w*|nude|nudity|"
    r"breast\w*|nipple\w*|buttock\w*|anus|anal|fec\w*|faec\w*|excrement\w*|"
    r"alcohol\w*|wine\w*|beer\w*|liquor\w*|whisk(?:ey|y|ies)|vodka|drunk\w*|"
    r"intoxicat\w*|brew\w*|tobacco|cigaret\w*|cigar\w*|opium|heroin|"
    r"cocaine|cannabis|marijuana|narcotic\w*|drug\w*|gambl\w*|casino\w*|"
    r"weapon\w*|guns?|gunfire|gunpowder|gunshot\w*|gunboat\w*|pistol\w*|rifle\w*|firearm\w*|ammunition|bullet\w*|"
    r"cannon\w*|bomb\w*|grenade\w*|sword\w*|spear\w*|dagger\w*|"
    r"knife|knives|blade\w*|arrow\w*|crossbow\w*|halberd\w*|lance\w*|saber\w*|sabre\w*|harpoon\w*|bayonet\w*|"
    r"kill\w*|murder\w*|slaughter\w*|massacr\w*|tortur\w*|suicid\w*|"
    r"execut\w*|behead\w*|decapitat\w*|corpse\w*|cadaver\w*|gore|"
    r"violent\w*|violence|war|warfare|warrior\w*|combat\w*|battle\w*|"
    r"assault\w*|assassin\w*|terror\w*|cruel\w*|abuse\w*|racis\w*|slurs?|"
    r"slay\w*|slew|slain|artillery|blunderbuss\w*|harlot\w*|lewd\w*|"
    r"licentious\w*|kinky|orgies|orgy|homicid\w*|fart\w*|defecat\w*|"
    r"lust(?:s|ful|fully)?|lecher\w*|seduc\w*|pervert\w*|libido|bawdy|"
    r"stab(?:s|bed|bing)?|strangl\w*|dismember\w*|noose\w*|hangover\w*|"
    r"spirits|blood sacrifice|hang a criminal|bows?|archer\w*|armou?r\w*|armed|"
    r"armament\w*|axe\w*|hatchet\w*|clubs?|mace\w*|dirk\w*|darts?|"
    r"missile\w*|torpedo\w*|musket\w*|ordnance|rapier\w*|scabbard\w*"
)
UNSUITABLE = re.compile(r"\b(?:" + TERMS + r")\b", re.IGNORECASE)

# Carefully chosen neutral meanings keep common learning searches useful.
FAMILY_MEANINGS = {
    "乳": "milk; to suckle", "奶": "milk; nurse, grandmother",
    "匈": "chest; Hungary", "胸": "chest; heart, mind",
    "怀": "to hold in one's heart; to carry", "懷": "to hold in one's heart; to carry",
    "色": "color, tint, hue, shade; beauty, form",
    "性": "nature, character", "俗": "social customs", "村": "village, hamlet",
    "辣": "pepper; hot, spicy", "汁": "juice, fluid; sap; gravy, sauce",
    "博": "rich, plentiful, extensive; wide, broad", "宠": "to love; to favor, to pamper, to spoil",
    "寵": "to love; to favor, to pamper, to spoil", "執": "to grasp, to hold; to keep",
    "执": "to grasp, to hold; to keep", "措": "to arrange; to manage",
    "药": "medicine; the leaf of the Dahurian angelica plant",
    "藥": "medicine; the leaf of the Dahurian angelica plant",
    "赤": "red, scarlet; blushing", "竿": "bamboo pole", "粒": "grain, granule",
    "械": "tools; instruments", "箭": "a type of bamboo", "芒": "ray; silvergrass, Miscanthus sinensis",
    "莛": "stalks of grass", "靳": "a strap on a horse's chest",
    "触": "to touch", "觸": "to touch", "斟": "to deliberate, to gauge; to pour tea",
    "殘": "incomplete", "残": "incomplete", "膺": "chest; to bear, to undertake",
    "臆": "chest; thoughts, feelings", "魯": "foolish, rash", "鲁": "foolish, rash",
    "葑": "turnip", "亢": "high, proud; skilled; surname",
    "春": "springtime; joyful", "妍": "beautiful, handsome",
    "娇": "lovable, tender; pampered; frail", "嬌": "lovable, tender; pampered; frail",
    "刺": "to prick; to prod", "勒": "to tighten", "戳": "stamp, seal",
    "絞": "intertwined; to twist, to wring", "绞": "intertwined; to twist, to wring",
    "呱": "to wail, to cry", "妖": "strange, weird; enchanting",
    "低": "low; to lower; to bend", "俯": "to face down, to look down",
    "叩": "to ask; to knock", "折": "to break, to snap; to fold, to bend; humble",
    "拜": "to salute; to worship, to pay respects", "拱": "to salute; arched; arch",
    "揖": "to salute; to defer, to yield", "躬": "personally, in person; oneself",
    "鞠": "to bend; to nourish, to rear", "頓": "to pause; to arrange", "顿": "to pause; to arrange",
    "弓": "curved, arched", "弦": "string instrument; hypotenuse", "弧": "arc, crescent",
    "弛": "to loosen, to relax", "挽": "to pull, to lead; to pull back",
    "輓": "to pull, to lead; to pull back", "库": "treasury, warehouse", "庫": "treasury, warehouse",
    "斤": "a catty (about 500 grams); keen, shrewd", "甲": "shell; fingernails; first heavenly stem",
    "介": "agent, go-between, intermediary; to introduce; shell", "棒": "stick; strong, smart",
    "梃": "stalk; straight", "莞": "to smile", "飛": "to fly; high", "飞": "to fly; high",
}

def family_definition(definition, character=None):
    if character in FAMILY_MEANINGS:
        return FAMILY_MEANINGS[character]
    return "" if UNSUITABLE.search(definition) else definition
