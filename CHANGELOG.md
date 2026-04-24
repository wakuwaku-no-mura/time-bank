# 変更ログ

## 2026-04-24 — ゆいまわすへのリンク追加

### 概要

トップページ（`index.html`）に、時間銀行の活動管理アプリ「ゆいまわす」へのリンクを2か所追加した。

- **権利関係の方針**: ゆいまわすは永和システムマネジメント社が開発。画像・スクリーンショットの利用許諾が未確定のため、ボタンのみの実装とした。
- **動線の優先順位**: 既存メンバーの使いやすさを重視。

### 変更内容

#### 1. インラインCTA（`#about` セクション末尾）

ステップフロー（Step 1〜5）の直後に、文脈に沿った誘導ブロックを追加。

**`index.html`**
```html
<div class="yuimawasu-cta scroll_right">
    <p>困り事の相談や参加の呼びかけはこちらから</p>
    <a class="yuimawasu-btn" href="https://yuimalwasu--yuimalwasu.asia-east1.hosted.app/home"
       target="_blank" rel="noopener noreferrer">ゆいまわすを開く →</a>
</div>
```

**`static/css/main.css`** — `.yuimawasu-cta` / `.yuimawasu-btn` スタイル追加（オレンジ丸角ボタン、ホバーで浮き上がり）

#### 2. フローティングアクションボタン（FAB）

ページを開いてすぐアクセスできるよう、画面右下に固定表示するFABを追加。

**`index.html`**（`<footer>` 直前）
```html
<a class="fab-yuimawasu" href="https://yuimalwasu--yuimalwasu.asia-east1.hosted.app/home"
   target="_blank" rel="noopener noreferrer">ゆいまわす</a>
```

**`static/css/main.css`** — `.fab-yuimawasu` スタイル追加（`position: fixed; bottom: 2rem; right: 2rem; z-index: 1100`）

### 没になったアプローチ

ナビゲーションバーへのリンク追加を試みたが、ヘッダーが `width: 1200px` 固定 + `margin-left: 500px` の構造のため、4つ目のナビ項目を追加するとビューポート幅によってレイアウトが崩れた。FAB方式に切り替えることで解決。
