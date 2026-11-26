# AnyCompany Air

> この文書は [samples/anycompany-air/README.md](../../../../samples/anycompany-air/README.md) の日本語訳です。内容が食い違う場合は原文を優先します。

AI-DLC Discovery 用の架空のサンプルです。航空会社のウェブサイトとアプリについて、顧客のフィードバック、運航データ、テレメトリーがあります。AnyCompany Air、その顧客、ここにあるすべてのレコードは作りものです。

このフォルダは、実際のチームの作業フォルダと同じ配置です。

- `discovery/kickoff.md`: チームがワークショップの前に記入したキックオフページ。プロダクト、チームとそれぞれの役割が考えていること、ベースラインつきのビジネス指標、5 つの候補のユースケース、データが書かれています。日本語訳は [kickoff.md](kickoff.md) です。
- `discovery/data/`: チームが持ち込むエクスポート。テレメトリーは `discovery/data/telemetry/` にあります。

## 実行方法

1. アプリにこのフォルダ（`samples/anycompany-air`）へのアクセスを許可する。AWS Quick ではローカルフォルダとして追加し、Claude Cowork では新しいタスクに接続する。
2. Discovery を開始する。
   ```text
   AI-DLC Discovery を開始してください。プロジェクト: anycompany-air。
   ```
   アシスタントは `discovery/kickoff.md` からセットアップを下書きし、確認を求めます。
3. チームを演じる。`discovery/kickoff.md` を読み、そこに書かれた役として答え、分析を見る前に自分たちの予想を書く。

仕込んだ正解は、解答集 [facilitator/ja/anycompany-air.md](../../anycompany-air.md) にあります。実行の前ではなく、実行のあとに読んでください。
