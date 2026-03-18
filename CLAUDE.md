# CLAUDE.md

## プロジェクト概要

GitHub Pages向け静的サイト。
リモート: https://github.com/wakuwaku-no-mura/time-bank.git

## jj（Jujutsu）の使い方

このプロジェクトはjjとgitを併用（colocate）しています。

### zshrcのエイリアス定義

```zsh
jj() {
    case "$1" in
        init)  command jj git init --colocate "${@:2}" ;;
        clone) command jj git clone --colocate "${@:2}" ;;
        push)  command jj git push "${@:2}" ;;
        fetch) command jj git fetch "${@:2}" ;;
        *)     command jj "$@" ;;
    esac
}
```

### よく使うコマンド

| コマンド | 内容 |
|---|---|
| `jj status` | 状態確認 |
| `jj diff` | 差分確認 |
| `jj describe -m "メッセージ"` | 変更にメッセージをつける |
| `jj push` | GitHubにプッシュ（エイリアス経由） |
| `jj git push --allow-new` | 新しいブランチを初めてプッシュ |
| `jj fetch` | リモートから取得（エイリアス経由） |
| `jj log` | 履歴確認 |
| `jj git remote add origin <URL>` | リモート追加 |

## ファイル構成

```
index.html       # メインHTML
static/
  css/           # スタイルシート
  images/        # 画像
.gitignore       # .DS_Store を除外
```
