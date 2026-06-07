"""
コスメサイト用 キーワードDB初期化スクリプト
Usage: python init_keywords.py
DB: C:/AI_Claude/cosme_site/keywords.db
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "keywords.db")

# ─────────────────────────────────────────────────────────────
# キーワードリスト
# columns: keyword, category, zone, look, budget, intent, monthly_volume, difficulty, status
# intent: informational / commercial / transactional
# status: pending / written / published
# ─────────────────────────────────────────────────────────────
KEYWORDS = [
    # ── リップ ──
    ("プチプラ リップ おすすめ",          "リップ", "lip",     "all",     "low",  "commercial",      8100, "medium", "written"),
    ("リップ マット おすすめ",             "リップ", "lip",     "all",     "all",  "commercial",      4400, "medium", "pending"),
    ("ティントリップ プチプラ",            "リップ", "lip",     "natural", "low",  "commercial",      3600, "low",    "pending"),
    ("グロスリップ うるうる",              "リップ", "lip",     "natural", "all",  "commercial",      2400, "low",    "pending"),
    ("CANMAKE リップ おすすめ",            "リップ", "lip",     "natural", "low",  "commercial",      2900, "low",    "pending"),
    ("KATE リップモンスター 色 選び方",    "リップ", "lip",     "trendy",  "mid",  "informational",   1900, "low",    "pending"),
    ("ヌードリップ 選び方",               "リップ", "lip",     "natural", "all",  "informational",   2200, "low",    "pending"),
    ("コーラルリップ 似合う肌色",          "リップ", "lip",     "casual",  "all",  "informational",   1600, "low",    "pending"),
    ("リップ 長持ち プチプラ",             "リップ", "lip",     "office",  "low",  "commercial",      3200, "medium", "pending"),
    ("デパコス リップ おすすめ",           "リップ", "lip",     "gorgeous","high", "commercial",      4800, "high",   "pending"),

    # ── アイシャドウ ──
    ("アイシャドウ ナチュラル 初心者",     "アイメイク","eye",   "natural", "all",  "informational",   5400, "medium", "written"),
    ("アイシャドウ プチプラ おすすめ",     "アイメイク","eye",   "all",     "low",  "commercial",      9900, "high",   "pending"),
    ("ブラウンアイシャドウ おすすめ",      "アイメイク","eye",   "natural", "all",  "commercial",      3300, "medium", "pending"),
    ("一重 アイシャドウ 選び方",           "アイメイク","eye",   "all",     "all",  "informational",   4100, "medium", "pending"),
    ("奥二重 アイシャドウ おすすめ",       "アイメイク","eye",   "all",     "all",  "commercial",      3800, "medium", "pending"),
    ("excel スキニーリッチシャドウ 色",    "アイメイク","eye",   "natural", "mid",  "informational",   2200, "low",    "pending"),
    ("CANMAKE アイシャドウ 全色",          "アイメイク","eye",   "all",     "low",  "informational",   2600, "low",    "pending"),
    ("ゴールドアイシャドウ 似合う人",      "アイメイク","eye",   "gorgeous","all",  "informational",   1800, "low",    "pending"),
    ("アイシャドウ 塗り方 初心者",         "アイメイク","eye",   "natural", "all",  "informational",   6700, "medium", "pending"),
    ("二重 アイシャドウ おすすめ 2025",    "アイメイク","eye",   "all",     "all",  "commercial",      5100, "high",   "pending"),

    # ── ファンデーション・下地 ──
    ("プチプラ ファンデ おすすめ",         "ファンデ", "skin",   "all",     "low",  "commercial",      7200, "high",   "pending"),
    ("ツヤ肌 ファンデ おすすめ",           "ファンデ", "skin",   "all",     "all",  "commercial",      5500, "medium", "pending"),
    ("乾燥肌 ファンデ おすすめ",           "ファンデ", "skin",   "all",     "all",  "commercial",      6100, "medium", "pending"),
    ("崩れない ファンデ プチプラ",         "ファンデ", "skin",   "office",  "low",  "commercial",      4300, "medium", "pending"),
    ("リキッドファンデ 初心者 選び方",     "ファンデ", "skin",   "all",     "all",  "informational",   3900, "medium", "pending"),
    ("日焼け止め プチプラ おすすめ",       "ファンデ", "skin",   "natural", "low",  "commercial",      8800, "high",   "pending"),
    ("化粧下地 毛穴 プチプラ",             "ファンデ", "skin",   "all",     "low",  "commercial",      5600, "medium", "pending"),
    ("NARS ファンデ 色 選び方",            "ファンデ", "skin",   "gorgeous","high", "informational",   2100, "low",    "pending"),
    ("CANMAKE マシュマロフィニッシュ 色",  "ファンデ", "skin",   "all",     "low",  "informational",   3400, "low",    "pending"),
    ("インテグレート ファンデ おすすめ",   "ファンデ", "skin",   "office",  "mid",  "commercial",      2800, "low",    "pending"),

    # ── チーク ──
    ("チーク おすすめ プチプラ",           "チーク",   "cheek",  "all",     "low",  "commercial",      4700, "medium", "pending"),
    ("チーク 塗り方 初心者",              "チーク",   "cheek",  "natural", "all",  "informational",   5200, "medium", "pending"),
    ("クリームチーク おすすめ",           "チーク",   "cheek",  "natural", "all",  "commercial",      3100, "low",    "pending"),
    ("オレンジチーク 似合う人",           "チーク",   "cheek",  "trendy",  "all",  "informational",   2300, "low",    "pending"),
    ("コーラルチーク 日本人 似合う",      "チーク",   "cheek",  "casual",  "all",  "informational",   1900, "low",    "pending"),
    ("NARS ブラッシュ 色 おすすめ",       "チーク",   "cheek",  "gorgeous","high", "commercial",      2600, "low",    "pending"),
    ("CANMAKE クリームチーク 全色",       "チーク",   "cheek",  "natural", "low",  "informational",   4100, "low",    "pending"),

    # ── アイブロウ ──
    ("アイブロウ 初心者 おすすめ",        "アイブロウ","eyebrow","natural", "all",  "commercial",      5800, "medium", "pending"),
    ("眉毛 整え方 初心者",               "アイブロウ","eyebrow","all",     "all",  "informational",   9200, "high",   "pending"),
    ("平行眉 書き方",                     "アイブロウ","eyebrow","trendy",  "all",  "informational",   6400, "medium", "pending"),
    ("アイブロウ パウダー 選び方",        "アイブロウ","eyebrow","natural", "all",  "informational",   3700, "medium", "pending"),
    ("CEZANNE アイブロウ おすすめ",      "アイブロウ","eyebrow","natural", "low",  "commercial",      2400, "low",    "pending"),
    ("KATE アイブロウ 3D 使い方",        "アイブロウ","eyebrow","trendy",  "mid",  "informational",   2100, "low",    "pending"),

    # ── 比較・まとめ系 ──
    ("CANMAKE CEZANNE どっち おすすめ",  "比較",    "all",    "natural", "low",  "informational",   1800, "low",    "pending"),
    ("プチプラ デパコス 違い",           "比較",    "all",    "all",     "all",  "informational",   3200, "medium", "pending"),
    ("コスメ 初心者 何から買う",         "比較",    "all",    "natural", "low",  "informational",   4500, "medium", "pending"),
    ("ナチュラルメイク コスメ 全部揃える", "比較",  "all",    "natural", "all",  "commercial",      2900, "medium", "pending"),
    ("春 メイク コスメ おすすめ 2025",   "比較",    "all",    "natural", "all",  "commercial",      5600, "high",   "pending"),
    ("韓国コスメ 日本 どっちがいい",     "比較",    "all",    "all",     "all",  "informational",   3800, "medium", "pending"),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword        TEXT NOT NULL UNIQUE,
            category       TEXT,
            zone           TEXT,
            look           TEXT,
            budget         TEXT,
            intent         TEXT,
            monthly_volume INTEGER,
            difficulty     TEXT,
            status         TEXT DEFAULT 'pending',
            article_path   TEXT,
            created_at     TEXT DEFAULT (datetime('now','localtime')),
            updated_at     TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    inserted = 0
    for row in KEYWORDS:
        try:
            c.execute("""
                INSERT INTO keywords
                    (keyword, category, zone, look, budget, intent, monthly_volume, difficulty, status)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, row)
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # already exists

    conn.commit()
    conn.close()
    print(f"[OK] DB initialized: {DB_PATH}")
    print(f"   Inserted {inserted} keywords ({len(KEYWORDS)} total)")

if __name__ == "__main__":
    init_db()
