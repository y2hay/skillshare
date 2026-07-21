<div align="center">
  <img src="./docs/public/proxmox-skill-mark.svg" alt="Proxmox Skill mark" width="110" />
  <h1>Proxmox Skill</h1>
  <p><strong>Codex から安全に Proxmox VE を操作するための公開向け skill リポジトリです。</strong></p>
  <p>
    再利用しやすい <code>uv run</code> ベースの CLI と Codex skill を組み合わせ、
    クラスタ確認、ゲスト起動、VM 作成、テンプレート clone、LXC 作成までを一つの repo にまとめています。
  </p>
  <p>
    <img src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/proxmox-skill/ci.yml?branch=main&style=flat-square&label=ci" alt="CI badge" />
    <img src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/proxmox-skill/deploy-docs.yml?branch=main&style=flat-square&label=docs" alt="Docs badge" />
    <img src="https://img.shields.io/github/license/Sunwood-ai-labs/proxmox-skill?style=flat-square" alt="License badge" />
    <img src="https://img.shields.io/badge/runtime-uv-0f766e?style=flat-square" alt="uv badge" />
  </p>
  <p>
    <a href="./README.md"><strong>English</strong></a>
    ·
    <a href="./README.ja.md"><strong>日本語</strong></a>
  </p>
</div>

<p align="center">
  <img src="./docs/public/proxmox-skill-hero.svg" alt="Proxmox Skill hero" width="100%" />
</p>

## ✨ 特徴

- Codex 用の [SKILL.md](./SKILL.md) と、実行用の [proxmox_vm.py](./scripts/proxmox_vm.py) を同じ repo で管理できます。
- `.env` に接続情報を閉じ込め、公開時は `.env.example` だけを配布できます。
- QEMU VM の確認、起動、作成、clone に対応しています。
- LXC の確認、作成、起動にも対応しています。
- `root` を `root@pam` に補正し、ticket 認証と CSRF header を自動処理します。
- Python 標準ライブラリ中心なので、`uv run` ですぐ使えます。

## 🚀 クイックスタート

1. リポジトリを clone します。
2. `.env.example` を `.env` としてコピーします。
3. Proxmox の接続先、ユーザー名、パスワードを設定します。
4. 変更系コマンドの前に、必ず確認系コマンドを実行します。

```powershell
Copy-Item .env.example .env
uv run .\scripts\proxmox_vm.py nodes
uv run .\scripts\proxmox_vm.py nextid
uv run .\scripts\proxmox_vm.py list-vms --node pve
uv run .\scripts\proxmox_vm.py list-cts --node pve
```

PowerShell 以外では `./scripts/proxmox_vm.py` 形式でも実行できます。

## 🧠 Skill の入口

Codex が読む skill 定義は [SKILL.md](./SKILL.md) にあります。ここには、`.env` の安全な扱い方、inspect-first の基本フロー、次の代表操作がまとまっています。

- 既存 VM の起動
- 空の VM シェル作成
- VM テンプレートからの clone
- LXC コンテナの作成と起動

補助実装は [scripts/proxmox_vm.py](./scripts/proxmox_vm.py)、API メモは [references/api-notes.md](./references/api-notes.md) にあります。

## 🧪 サンプルスクリプト

検証時に使った確認系の流れは、場当たり的な shell 履歴で終わらせず [scripts/examples/](./scripts/examples/) に内包しました。repo を clone したあと、そのまま再利用できます。

cluster と node の概況確認:

```powershell
uv run .\scripts\examples\cluster_probe.py --node pve --content-storage local
```

guest の状態と設定スナップショット取得:

```powershell
uv run .\scripts\examples\guest_snapshot.py --kind lxc --node pve --vmid 230
```

これらは破壊的な変更を伴わないサンプルに寄せてあり、必要に応じてコピーして拡張しやすいようにしています。

## 🛠️ よく使うコマンド

ノード確認:

```powershell
uv run .\scripts\proxmox_vm.py nodes
```

VM シェル作成:

```powershell
uv run .\scripts\proxmox_vm.py create `
  --node pve `
  --vmid 220 `
  --name app-220 `
  --memory 4096 `
  --cores 4 `
  --bridge vmbr0 `
  --storage local-lvm `
  --disk-gb 32 `
  --wait
```

テンプレート clone:

```powershell
uv run .\scripts\proxmox_vm.py clone `
  --node pve `
  --source-vmid 9000 `
  --newid 221 `
  --name app-221 `
  --full `
  --wait
```

LXC を作成して起動:

```powershell
uv run .\scripts\proxmox_vm.py create-ct `
  --node pve `
  --vmid 230 `
  --hostname codex-230 `
  --ostemplate local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst `
  --storage local-lvm `
  --memory 512 `
  --swap 512 `
  --cores 1 `
  --disk-gb 8 `
  --bridge vmbr0 `
  --ip dhcp `
  --wait `
  --start-after-create
```

## 🔐 安全設計

- `.env` は shell source せず、ファイルとして読み込みます。
- `.env` は ignore し、公開するのは `.env.example` のみです。
- 変更前に node、VM ID、storage、bridge、template を必ず確認します。
- 実タスク結果が必要な場合は `--wait` を付けます。
- 自分用の自動化に cluster 固有名を埋め込まず、環境変数や引数で切り替える前提にします。

## 🧪 検証状況

LXC フローについては、実際の Proxmox VE 環境で以下を確認済みです。

- node と既存 guest の確認
- 次の空き ID の取得
- Proxmox template からの LXC 作成
- 作成した LXC の起動
- `running` の確認
- 同一 LXC の停止と `stopped` の確認

公開資料では、環境固有のホスト名や IP は伏せたまま、再現しやすい操作手順に整理しています。

## 📚 ドキュメント

- docs ソース: [docs/](./docs/)
- 英語ガイド入口: [docs/guide/getting-started.md](./docs/guide/getting-started.md)
- 日本語ガイド入口: [docs/ja/guide/getting-started.md](./docs/ja/guide/getting-started.md)
- GitHub Pages 想定 URL: `https://sunwood-ai-labs.github.io/proxmox-skill/`

## 🗂️ リポジトリ構成

```text
.
|-- SKILL.md
|-- scripts/
|   |-- examples/
|   |   |-- cluster_probe.py
|   |   `-- guest_snapshot.py
|   `-- proxmox_vm.py
|-- references/
|   `-- api-notes.md
|-- docs/
|   |-- .vitepress/
|   |-- guide/
|   `-- ja/
|-- agents/
|   `-- openai.yaml
|-- .env.example
`-- pyproject.toml
```

## 📄 ライセンス

[MIT License](./LICENSE) で公開しています。
