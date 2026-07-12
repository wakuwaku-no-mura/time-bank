---
name: manage-activities
description: 時間銀行（じかんぎんこう）の活動実績を追加・管理する
---

# manage-activities

このスキルは、時間銀行の「活動実績」に新しいイベント記事を追加するための手順と自動化スクリプトを提供します。

## 主な機能

- `/activities/<slug>/index.html` の個別記事ページの自動生成。
- `/activities/index.html`（一覧ページ）への活動カードの自動挿入。
- 追加される画像の自動リサイズ・圧縮（macOS `sips` コマンド使用）。
- `CHANGELOG.md` への変更履歴の自動追記。

## 使用方法

### 1. 新しい活動実績を追加する

エージェントは、本スキルに同梱されている自動生成スクリプト `scripts/add_activity.py` を使用して、新規追加タスクを実行してください。

```bash
python3 .agents/skills/manage-activities/scripts/add_activity.py \
  --date "2026.05.10" \
  --slug "2026-05-10-schongarten-cleanup" \
  --title "シェーンガルテン周辺のゴミ拾い" \
  --description "地域の子どもたちと一緒に、シェーンガルテン周辺の清掃活動を行いました。" \
  --image-sources "/path/to/img1.JPG,/path/to/img2.JPG,/path/to/img3.JPG"
```

#### 引数の詳細
- `--date`: 表示用の日付。`YYYY.MM.DD` 形式。
- `--slug`: 記事フォルダのディレクトリ名。`YYYY-MM-DD-キーワード`（半角英数字とハイフンのみ、URL用）。
- `--title`: 活動実績のタイトル。
- `--description`: 活動内容の短い概要。
- `--image-sources`: 元画像ファイルの絶対パスまたは相対パス（カンマ区切り）。指定された画像は自動的に 1200px (または1000px) にリサイズ・圧縮され、`static/images/activities/<slug>/` 配下にコピーされます。

### 2. 手動での確認・テスト

スクリプト実行完了後、以下のファイルが正しく更新されていることを確認します：
- [activities/index.html](file:///Users/kat/src/github.com/wakuwaku-no-mura/time-bank/activities/index.html) (カードの追加)
- `/activities/<slug>/index.html` (個別記事ページの生成)
- `static/images/activities/<slug>/` (圧縮画像の保存)
- [CHANGELOG.md](file:///Users/kat/src/github.com/wakuwaku-no-mura/time-bank/CHANGELOG.md) (ログの追記)
