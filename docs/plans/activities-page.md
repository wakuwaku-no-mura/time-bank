# 活動実績ページの追加

## Context

時間銀行（じかんぎんこう）のサイトは現在 `index.html` 1枚のみの構成（GitHub Pages静的サイト）。今回、2026.05.10に行われた「シェーンガルテン周辺のゴミ拾い」活動を皮切りに、今後も活動実績を蓄積・公開していくための専用ページを新設する。トップページからは、既存の「協力サイト」バナーと同じ視覚言語を持つ新設バナーセクションからリンクする。実装自体はantigravity cliに依頼するため、このプランはantigravity cliへの実装依頼として使える詳細な仕様書とする。

ユーザー確認済み事項:
- 活動実績ページは**一覧形式（拡張可能なカード/タイムライン）**で作る。今回は1件のみ掲載するが、今後も同じページに追記していける構造にする。
- トップページからのリンクは、「協力サイト」セクションと同様のカードデザインで**新設バナーセクション**を作る（ナビバーへの追加はCHANGELOG記載の通り過去にレイアウト崩れが起きたため避ける）。

## 現状の技術情報（antigravity cliに引き継ぐ前提知識）

- サイトはdestyle.css + Bootstrap4 + 独自 `static/css/main.css`、Google Font「Yomogi」を使用。
- スクロールで要素をフェードインさせる `.scroll_up` / `.scroll_left` / `.scroll_right` ユーティリティクラスがあり、対象要素に付与すると `index.html:520-533` の共通スクリプトが自動的に `.on` を付けて発火する（同じscriptを新ページでも読み込めば動く）。
- 外部/内部リンクは `target="_blank" rel="noopener noreferrer"` が一貫して使われている（同一サイト内ページなので活動実績ページへのリンク自体は新規タブ不要、通常のページ遷移でよい）。
- 「協力サイト」セクション（再利用テンプレート）— [index.html:482](index.html:482):
  ```html
  <section class="partner-links scroll_up">
      <h2>協力サイト</h2>
      <div class="partner-links-grid">
          <a class="partner-link-item" href="..." target="_blank" rel="noopener noreferrer">
              <img src="static/images/..." alt="...">
          </a>
      </div>
  </section>
  ```
  対応CSSは `static/css/main.css:653-695`（`.partner-links` カード / `.partner-links-grid` flex / `.partner-link-item` 360px固定幅・ホバーで浮き上がり）。
- フッター構造 — [index.html:500](index.html:500)、対応CSSは `main.css:511-572` 付近。
- レスポンシブは単一の `@media (max-width: 700px)` ブロック（`main.css:699`以降）にまとまっている。
- サイト内に他の.htmlファイルは存在せず、複数ページ化はこれが初めての試み。

## フォルダ構成方針（今後のページ増加・記事増加に備えて）

今回が最初の複数ページ化であり、今後も「活動実績」以外のページ（お知らせ、アクセス等）や、活動実績内の個別記事が増えていく可能性を考慮し、**「1ページ=1フォルダ+index.html」方式**を採用する。さらに活動実績は**一覧ページ＋記事ごとの個別ページ**の2階層構成にする（記事を1ページに積み重ねる方式だと将来的にページが長大化し、個別URLでのシェアもできないため）。

- サイトトップレベル: `index.html`（トップページ）のみをルート直下に維持。今後別ジャンルのページを追加する場合も `news/index.html`, `access/index.html` のように同じパターンで並べる。
- 活動実績の一覧ページ: `activities/index.html`（URL `/activities/`）。各記事へのカード（サムネイル・日付・タイトル・抜粋）を新しい順に並べる。
- 活動実績の個別記事ページ: `activities/<slug>/index.html`（URL `/activities/<slug>/`）。**命名規則は `YYYY-MM-DD-キーワード`**（日付でソートしやすく、キーワードはローマ字/英語の短い単語をハイフンつなぎにする。URLに日本語を含めない）。
  - 例: 今回の記事は `activities/2026-05-10-schongarten-cleanup/`
  - 今後の例: `activities/2026-06-01-summer-festival/`, `activities/2026-07-15-farm-work/` など
- 記事固有の画像は `static/images/activities/<slug>/` に、記事と同じslugのサブフォルダへ格納する（例: `static/images/activities/2026-05-10-schongarten-cleanup/`）。共通で使う画像（ロゴ、SNSアイコン等）は従来通り `static/images/` 直下に残す。
- CSSは当面 `static/css/main.css` を一覧・個別ページ共通で利用する（ページごとにCSSを分割する必要が出てきたら改めて検討）。

## 実装方針

### 1. 活動実績 一覧ページ `activities/index.html`

- `<head>` は `index.html` と同じCDN/CSS読み込み（destyle, bootstrap, Yomogiフォント, `static/css/main.css`）。titleは「活動実績 | 時間銀行」、meta descriptionも活動実績向けに調整。
- ヘッダーは `index.html` と共通のロゴ・ナビを流用しつつ、ロゴリンクとナビの各項目は `../index.html#nature` 等トップページへの相対パスに変更（同一ページ内アンカーでは効かなくなるため）。ナビに「活動実績」項目を無理に追加しない（幅固定構造の教訓を踏襲）。ロゴから「← 時間銀行トップへ戻る」的な戻り導線を明確にする。
- メインコンテンツ: 見出し「活動実績」＋説明文一行、その下に記事カードを新しい順に並べるカード一覧（新規CSSクラス、例 `.activity-list` / `.activity-list-item`）。各カードの構成:
  - サムネイル画像（`static/images/activities/<slug>/` の軽量版サムネイル）
  - 日付（例: `2026.05.10`）
  - タイトル（例: `シェーンガルテン周辺のゴミ拾い`）
  - カード全体が個別記事ページ（`activities/<slug>/`）へのリンクになっている。
  - 今後2件目以降を追加する際は、同じカードブロックをコピーして一覧の先頭に追加していくだけで拡張できる構造にする（新しい記事が上に来る降順）。
- フッターは `index.html` と同じ内容をそのまま複製（SNSリンク・コピーライト、パスは `../` プレフィックスに調整）。
- 末尾のスクロールアニメーション用スクリプトとCloudflare Analyticsタグも `index.html` と同様に含める。

### 2. 活動実績 個別記事ページ `activities/2026-05-10-schongarten-cleanup/index.html`

- `<head>`・ヘッダー・フッターの構成は一覧ページと同様（パスは `../../index.html` 等さらに1階層深くなる点に注意）。
- パンくず的なリンク「← 活動実績一覧へ戻る」を `activities/index.html`（相対パス `../index.html`）に向けて設置。
- メインコンテンツ: タイトル「シェーンガルテン周辺のゴミ拾い」、日付「2026.05.10」、概要文（1〜2行、仮文「地域の子どもたちと一緒に、シェーンガルテン周辺の清掃活動を行いました。」程度）、写真ギャラリー（`static/images/activities/2026-05-10-schongarten-cleanup/schongarten_20260510_1.JPG` 〜 `_3.JPG` を横並びグリッドで表示）。
- 今後の記事は `activities/<slug>/index.html` を同じテンプレートでコピーして作成し、`activities/index.html` の一覧にカードを追加する2ステップで運用する。

### 3. トップページ `index.html` にバナーセクションを追加

- 「協力サイト」セクション（[index.html:482-494](index.html:482)）と同じ見た目のカードを、**別セクションとして新設**する（協力サイトのgrid内に混ぜ込まない。外部サイトと自サイトのコンテンツを区別するため）。配置は「Member」セクションの後、「協力サイト」セクションの前後どちらでも良いが、時系列的に活動を目立たせたいなら「協力サイト」の直前に置くことを推奨。リンク先は活動実績一覧ページ `activities/`（個別記事ではなく一覧への導線）。
- マークアップ例（`.partner-links` と同じCSSクラスを再利用しつつ見出しとリンク先のみ差し替え。新規CSSはほぼ不要）:
  ```html
  <section class="partner-links scroll_up">
      <h2>活動実績</h2>
      <div class="partner-links-grid">
          <a class="partner-link-item" href="activities/">
              <img src="static/images/activities/2026-05-10-schongarten-cleanup/compressed_schongarten_20260510_1.jpg" alt="2026.05.10 シェーンガルテン周辺のゴミ拾い">
          </a>
      </div>
  </section>
  ```
  - 外部リンクではないため `target="_blank"` は付けない。
  - サムネイル画像はそのままだと解像度が大きい（元写真はスマホ撮影の高解像度JPG）ため、表示用に軽量化・トリミングしたサムネイルを別途用意することを推奨（例: `static/images/compressed_banner_nagano_data.jpg` のように既存サイトも軽量版を別ファイルで用意する慣習がある）。antigravity cliに依頼する際、画像圧縮/リサイズも作業範囲に含めるかを明記する。

### 4. CSS追加（`static/css/main.css`）

- 新規クラス `.activity-list`, `.activity-list-item`, `.activity-article`, `.activity-photos` 等を、既存の `.partner-links` や `.stepbar` のデザイントーン（白半透明カード、角丸、Yomogiフォント見出し）に合わせて追加。
- 写真ギャラリーはflexまたはgridで3枚横並び→モバイルで縦積み（既存の `@media (max-width: 700px)` ブロックに追記）。
- トップページの新セクションは既存 `.partner-links` 系クラスをそのまま再利用するため、追加CSSはほぼ不要。

### 5. CHANGELOG.md への追記

このプロジェクトの慣習として、機能追加時は `CHANGELOG.md` に変更概要とコードスニペットを追記している（[CHANGELOG.md](CHANGELOG.md)参照）。今回の活動実績ページ追加も同様に追記する。

## 確定事項

- 活動実績は**一覧ページ＋記事ごとの個別ページ**の2階層構成とする（1ページに全記事を積み重ねる方式は不採用）。
- 記事フォルダの命名規則は `activities/<YYYY-MM-DD>-<英語/ローマ字キーワード>/`。日付でソート可能にし、URLには日本語を含めない。今回の記事は `activities/2026-05-10-schongarten-cleanup/`。
- 活動の説明文は仮文で進める。例: 「地域の子どもたちと一緒に、シェーンガルテン周辺の清掃活動を行いました。」程度の一文をantigravity cliに仮置きしてもらい、後から本文を差し替えやすい構造（テキストのみのシンプルな1〜2行、HTMLコメント等での装飾は不要）にする。正式な文面は後日ユーザーが確認・修正する。
- 写真（スマホ撮影の高解像度JPG、現在 `static/images/schongarten_20260510_1.JPG`〜`_3.JPG` に配置）は、まず `static/images/activities/2026-05-10-schongarten-cleanup/` に移動し、その配下に軽量化・トリミングした記事本文用・トップページバナーサムネイル用の画像（例: `static/images/activities/2026-05-10-schongarten-cleanup/compressed_schongarten_20260510_1.jpg`）を作成する。元の高解像度ファイルもそのまま同フォルダ配下に残す。
- ページURLは「フォルダ構成方針」の通り、一覧が `activities/index.html`（`/activities/`）、個別記事が `activities/2026-05-10-schongarten-cleanup/index.html`（`/activities/2026-05-10-schongarten-cleanup/`）とする。

## 検証方法

- ローカルで `index.html` / `activities/index.html` / `activities/2026-05-10-schongarten-cleanup/index.html` をブラウザで開き、以下を確認:
  - トップページの新セクションから活動実績一覧ページに正しく遷移する。
  - 一覧ページのカードから個別記事ページに正しく遷移し、「一覧へ戻る」リンクで一覧に戻れる。
  - 一覧・個別記事それぞれのロゴ/ナビからトップページに正しく戻れる（相対パスの階層ズレがないか特に確認）。
  - 3枚の写真が個別記事ページで正しく表示され、モバイル幅（700px以下）でレイアウトが崩れない。
  - スクロールアニメーション（`.scroll_up` 等）が新セクション・一覧ページ・個別記事ページそれぞれで正常に発火する。
  - Yomogiフォント・全体の配色・角丸カードのトーンが既存ページと統一されている。
