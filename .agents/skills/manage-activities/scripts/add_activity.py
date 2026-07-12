#!/usr/bin/env python3
import argparse
import os
import subprocess
from datetime import datetime
import shutil

def main():
    parser = argparse.ArgumentParser(description="Add a new activity to time-bank.")
    parser.add_argument("--date", required=True, help="Activity date, e.g., '2026.05.10'")
    parser.add_argument("--slug", required=True, help="Directory name for the activity, e.g., '2026-05-10-schongarten-cleanup'")
    parser.add_argument("--title", required=True, help="Title of the activity")
    parser.add_argument("--description", required=True, help="Brief description of the activity")
    parser.add_argument("--image-sources", required=True, help="Comma-separated paths to original image files")
    args = parser.parse_args()

    # パス解決
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", ".."))
    
    # テンプレートパス
    detail_temp_path = os.path.join(script_dir, "..", "resources", "activity-detail-template.html")
    card_temp_path = os.path.join(script_dir, "..", "resources", "activity-card-template.html")
    
    # 出力先パス
    activities_dir = os.path.join(project_root, "activities")
    new_activity_dir = os.path.join(activities_dir, args.slug)
    images_dest_dir = os.path.join(project_root, "static", "images", "activities", args.slug)

    # 1. フォルダの作成
    os.makedirs(new_activity_dir, exist_ok=True)
    os.makedirs(images_dest_dir, exist_ok=True)

    # 2. 画像のコピー・圧縮 (sips コマンド使用)
    sources = [s.strip() for s in args.image_sources.split(",") if s.strip()]
    dest_filenames = []
    
    for i, src in enumerate(sources):
        if not os.path.exists(src):
            print(f"Warning: Image source file not found: {src}")
            continue
        ext = os.path.splitext(src)[1]
        dest_filename = f"schongarten_{args.slug.replace('-', '_')}_{i+1}{ext}"
        dest_path = os.path.join(images_dest_dir, dest_filename)
        
        print(f"Compressing {src} -> {dest_path}...")
        cmd = ["sips", "--resampleWidth", "1200", "-s", "formatOptions", "60", src, "--out", dest_path]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # サイズチェック
            sz = os.path.getsize(dest_path)
            if sz > 350000: # 350KB超えた場合、幅1000px, Quality 55% で再圧縮
                print(f"File size {sz/1024:.1f}KB exceeds 350KB. Re-compressing with smaller dimensions...")
                cmd_retry = ["sips", "--resampleWidth", "1000", "-s", "formatOptions", "55", src, "--out", dest_path]
                subprocess.run(cmd_retry, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            dest_filenames.append(dest_filename)
            print(f"Saved: {dest_path} ({os.path.getsize(dest_path)/1024:.1f} KB)")
        except subprocess.CalledProcessError as e:
            print(f"Error compressing image {src}: {e}")
            # エラーの場合は直接コピー
            shutil.copy2(src, dest_path)
            dest_filenames.append(dest_filename)

    if not dest_filenames:
        print("Error: No images were successfully processed.")
        return

    # 3. 個別詳細HTMLの生成
    with open(detail_temp_path, "r", encoding="utf-8") as f:
        detail_html = f.read()

    # photo_items の生成
    photo_items_html = ""
    for i, fname in enumerate(dest_filenames):
        photo_items_html += f'                    <div class="activity-photo-item">\n'
        photo_items_html += f'                        <img src="../../static/images/activities/{args.slug}/{fname}" alt="活動の様子 {i+1}">\n'
        photo_items_html += f'                    </div>\n'
        
    detail_html = detail_html.replace("{title}", args.title)
    detail_html = detail_html.replace("{date}", args.date)
    detail_html = detail_html.replace("{formatted_date}", args.date)
    detail_html = detail_html.replace("{description}", args.description)
    detail_html = detail_html.replace("{photo_items}", photo_items_html.rstrip())

    dest_detail_path = os.path.join(new_activity_dir, "index.html")
    with open(dest_detail_path, "w", encoding="utf-8") as f:
        f.write(detail_html)
    print(f"Created detail page: {dest_detail_path}")

    # 4. 一覧ページ (activities/index.html) へのカード追加
    list_html_path = os.path.join(activities_dir, "index.html")
    with open(card_temp_path, "r", encoding="utf-8") as f:
        card_html_template = f.read()

    thumbnail = dest_filenames[0]
    card_html = card_html_template.replace("{slug}", args.slug)
    card_html = card_html.replace("{thumbnail}", thumbnail)
    card_html = card_html.replace("{title}", args.title)
    card_html = card_html.replace("{formatted_date}", args.date)
    card_html = card_html.replace("{description}", args.description)

    # 既存の一覧HTMLの <div class="activity-grid"> の直後にカードを挿入
    with open(list_html_path, "r", encoding="utf-8") as f:
        list_html = f.read()

    target_str = '<div class="activity-grid">'
    if target_str in list_html:
        parts = list_html.split(target_str, 1)
        new_list_html = parts[0] + target_str + "\n" + card_html + parts[1]
        with open(list_html_path, "w", encoding="utf-8") as f:
            f.write(new_list_html)
        print(f"Inserted activity card into: {list_html_path}")
    else:
        print(f"Warning: could not find '{target_str}' in {list_html_path}. Card was not inserted automatically.")

    # 5. CHANGELOG.md への自動追記
    changelog_path = os.path.join(project_root, "CHANGELOG.md")
    with open(changelog_path, "r", encoding="utf-8") as f:
        changelog = f.read()

    today_str = datetime.now().strftime("%Y-%m-%d")
    log_entry = f"""## {today_str} — 活動実績の追加（{args.title}）

### 概要

新しく活動実績「{args.title}」を追加。

### 変更内容

- **`activities/{args.slug}/index.html`** — 個別詳細ページを生成。
- **`activities/index.html`** — 一覧ページへ活動実績カードを挿入。
- **`static/images/activities/{args.slug}/`** — リサイズ・圧縮された画像を配置。

---

"""
    title_marker = "# 変更ログ"
    if title_marker in changelog:
        parts = changelog.split(title_marker, 1)
        new_changelog = parts[0] + title_marker + "\n\n" + log_entry + parts[1].lstrip()
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(new_changelog)
        print("Updated CHANGELOG.md")
    else:
        print("Warning: could not find '# 変更ログ' in CHANGELOG.md")

if __name__ == "__main__":
    main()
