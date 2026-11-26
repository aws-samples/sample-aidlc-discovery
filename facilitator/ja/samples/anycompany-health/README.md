# AnyCompany Health: 課題を抱える加入者ポータル

> この文書は [samples/anycompany-health/README.md](../../../../samples/anycompany-health/README.md) の日本語訳です。内容が食い違う場合は原文を優先します。

AI-DLC Discovery 用の架空のサンプルです。医療保険会社の加入者ポータルとアプリを扱います。データは規制の対象で、自社の環境の外に出せません。そのため、チームは生のレコードの代わりに、Signal Brief（匿名化したシグナルの要約）と集計統計を持ち込みます。AnyCompany Health、その加入者、ここにあるすべてのレコードは作りものです。

このフォルダは、実際のチームの作業フォルダと同じ配置です。

- `discovery/kickoff.md`: チームがワークショップの前に記入したキックオフページ。プロダクト、チームとそれぞれの役割が考えていること、ベースラインつきのビジネス指標、5 つの候補のユースケース、データが書かれています。日本語訳は [kickoff.md](kickoff.md) です。
- `discovery/signal-briefs/`: チームが持ち込む Signal Brief と集計値。

## 実行方法

1. アプリにこのフォルダ（`samples/anycompany-health`）へのアクセスを許可する。AWS Quick Desktop では、**設定**（Settings）、**マイコンピュータ**（My computer）、**ローカルフォルダ**（Local folders）の順に開いて追加し、Claude Cowork では新しいタスクに接続する。
2. Discovery を開始する。
   ```text
   AI-DLC Discovery を開始してください。プロジェクト: member-portal。
   ```
   アシスタントは `discovery/kickoff.md` からセットアップを下書きし、確認を求めます。
3. チームを演じる。`discovery/kickoff.md` を読み、そこに書かれた役として答え、分析の前にチームの予想を書く。

仕込んだ正解は、解答集 [facilitator/ja/anycompany-health.md](../../anycompany-health.md) にあります。実行の前ではなく、実行のあとに読んでください。
