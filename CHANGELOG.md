# 変更ログ

## 2026-04-24 — 協力サイトバナーセクションの追加

### 概要

ページ最下部（`#member` セクション後、フッター直前）に「協力サイト」セクションを新設。関連サービスのバナーリンクを横並びで表示するグリッドレイアウトを実装。今後バナーを追加しやすい構造とした。

### 変更内容

#### 1. 長野データ探検隊バナー（初回追加）

**`index.html`** — `.partner-links` セクションと `.partner-links-grid` を追加。

```html
<section class="partner-links scroll_up">
    <h2>協力サイト</h2>
    <div class="partner-links-grid">
        <a class="partner-link-item" href="https://nagano-data.willbefree-k-m.workers.dev/" target="_blank" rel="noopener noreferrer">
            <img src="static/images/compressed_banner_nagano_data.jpg" alt="長野データ探検隊 — 地域のデータを、みんなで発見しよう！">
        </a>
    </div>
</section>
```

**`static/css/main.css`** — `.partner-links` / `.partner-links-grid` / `.partner-link-item` スタイル追加。バナー幅360px固定、`flex-wrap` で複数バナー対応。

- バナーサイズを控えめな360pxに（初期実装時は960pxで大きすぎたため修正）
- 他セクションと統一した白半透明カード＋角丸スタイル
- ホバーで浮き上がり＋シャドウ強調

#### 2. OMI NEWS 麻績ニュースバナー追加

**`index.html`** — `.partner-links-grid` 内に2つ目のバナーを追加。

```html
<a class="partner-link-item" href="https://miyagawake1019.github.io/omi-news/" target="_blank" rel="noopener noreferrer">
    <img src="static/images/banner_omi_news.png" alt="OMI NEWS 麻績ニュース — 麻績村の最新情報をチェック！">
</a>
```

画像ファイル: `static/images/banner_omi_news.png`

---

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
