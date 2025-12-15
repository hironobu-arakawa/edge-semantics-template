# Edge Semantics Template（Slim版）

このリポジトリは **Edge＝「接続境界 × 意味境界」** を
*読みやすく・誤解なく* 伝えるための **最小テンプレート** です。

目的は「完成した製品」ではなく、
**正しい設計判断が再現できる“型”** を共有することにあります。

---

## まず覚えること（3つだけ）

1. **Factは不変**
   - 観測データは書き換えない
   - 意味を入れない

2. **LLMは意味候補（Hypothesis）まで**
   - 確定しない
   - SCADAや制御には触れない

3. **上位が使うのはResolutionだけ**
   - Hypothesisは候補
   - 変更兆候があれば安全側へ倒す

---

## データモデル（読む順番）

1. **Fact**  
   - 生データ＋接続条件＋fingerprint（変更検知のヒント）

2. **Hypothesis**  
   - 仮の意味（source / confidence / ttl 付き）

3. **Resolution**  
   - 用途（scope）ごとに「今はこれを信じる」

※ schema/ 配下の JSON Schema を参照

---

## PoCについて（あえて簡単にしています）

`poc/resolve_cli.py` は **説明用の最小実装** です。

やっていることは **これだけ**：

- Factの `schema_hash` を baseline と比較
- 違っていたら Resolution を `degraded` にする
- 自動修正はしない

> 実運用で必要になる
> - 統計ドリフト
> - 人による昇格
> - DB / API
> は **あえて実装していません**。

---

## 実行例

```bash
python poc/resolve_cli.py   --facts examples/facts.sample.jsonl   --hypotheses examples/hypotheses.sample.jsonl   --baseline examples/baseline.sample.json   --out examples/resolutions.out.jsonl
```

---

## LLMの位置づけ

LLMは **意味候補の生成専用** です。

- `prompts/llm_system.txt`
- `prompts/llm_user_template.txt`

をそのまま使えば、
「越境しないAI」を簡単に再現できます。

---

## 拡張したくなったら

次に進むなら、**READMEに書き足すだけ**で十分です。

- fingerprintを増やす（stats drift など）
- human promotion をイベントとして扱う
- 永続化（SQLite / JSONL）

コードを増やす前に、
**この3原則が守られているか**を確認してください。
