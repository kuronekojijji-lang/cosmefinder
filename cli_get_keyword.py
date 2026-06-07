"""
コスメサイト用 次のキーワードを取得するCLIヘルパー
Usage:
  python cli_get_keyword.py            # next pending keyword
  python cli_get_keyword.py --id 5     # specific ID
Output: JSON  (empty dict {} if none)
"""
import sqlite3, json, sys, os

DB_PATH = os.path.join(os.path.dirname(__file__), "keywords.db")

def get_keyword(id_=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if id_:
        row = c.execute("SELECT * FROM keywords WHERE id=?", (id_,)).fetchone()
    else:
        row = c.execute(
            "SELECT * FROM keywords WHERE status='pending' ORDER BY monthly_volume DESC LIMIT 1"
        ).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}

if __name__ == "__main__":
    id_ = None
    if "--id" in sys.argv:
        idx = sys.argv.index("--id")
        id_ = int(sys.argv[idx + 1])
    result = get_keyword(id_)
    # UTF-8 output (redirect-safe on Windows)
    sys.stdout.buffer.write((json.dumps(result, ensure_ascii=False) + "\n").encode("utf-8"))
