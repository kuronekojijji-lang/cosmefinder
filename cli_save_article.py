"""
コスメサイト用 記事保存CLIヘルパー
Usage:
  python cli_save_article.py \
    --keyword_id 1 \
    --keyword "プチプラ リップ おすすめ" \
    --title "タイトル" \
    --description "メタ説明" \
    --slug "slug-name" \
    --category "リップ" \
    --zone "lip" \
    --look "natural" \
    --budget "low" \
    --article_type "ranking" \
    --content_file C:/tmp/cosme_article.md
Output: "OK article_id=N | WORD_COUNT words | TITLE"
"""
import sqlite3, json, sys, os, argparse, re
from datetime import datetime

DB_PATH     = os.path.join(os.path.dirname(__file__), "keywords.db")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content", "posts")

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s[:60]

def save_article(args):
    # Read article body
    with open(args.content_file, encoding="utf-8") as f:
        body = f.read().strip()

    word_count = len(body.split())
    today      = datetime.now().strftime("%Y-%m-%d")

    # Build Hugo front matter
    tags = [args.category]
    if args.budget == "low":   tags.append("プチプラ")
    if args.budget == "high":  tags.append("デパコス")
    if args.look:              tags.append(args.look)

    frontmatter = f"""---
title: "{args.title}"
date: {today}
description: "{args.description}"
categories: ["{args.category}"]
tags: {json.dumps(list(set(tags)), ensure_ascii=False)}
icon: "{'💋' if args.zone=='lip' else '👁' if args.zone=='eye' else '✨' if args.zone=='skin' else '🌸' if args.zone=='cheek' else '🖊' if args.zone=='eyebrow' else '💄'}"
zone: "{args.zone}"
look: "{args.look}"
budget: "{args.budget}"
article_type: "{args.article_type}"
---
"""

    slug = args.slug or slugify(args.title)
    filename = f"{today}-{slug}.ja.md"
    filepath = os.path.join(CONTENT_DIR, filename)

    os.makedirs(CONTENT_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + "\n" + body)

    # Update DB
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE keywords SET status='written', article_path=?, updated_at=datetime('now','localtime') WHERE id=?",
        (filepath, args.keyword_id)
    )
    conn.commit()

    # Get new article_id (row_id from keywords is keyword_id; article is just the file)
    conn.close()

    sys.stdout.buffer.write(
        f"OK article_id={args.keyword_id} | {word_count} words | {args.title}\nFile: {filepath}\n"
        .encode("utf-8")
    )

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--keyword_id",   type=int, required=True)
    p.add_argument("--keyword",      required=True)
    p.add_argument("--title",        required=True)
    p.add_argument("--description",  required=True)
    p.add_argument("--slug",         default="")
    p.add_argument("--category",     required=True)
    p.add_argument("--zone",         default="all")
    p.add_argument("--look",         default="all")
    p.add_argument("--budget",       default="all")
    p.add_argument("--article_type", default="ranking")
    p.add_argument("--content_file", required=True)
    save_article(p.parse_args())
