日本語Wikipediaのダンプデータからword2vecのモデルを作成する。

## 必要なもの

- Python 2.7 (gensim, MeCab)
- [jawiki-20150805-pages-articles.xml.bz2](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
- [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor)

## (参考) 環境

- Intel(R) Xeon(R) CPU E3-1270 v3 @ 3.50GHz (8-core)
- メモリ 16GB
- Ubuntu 14.04.2 LTS

## 形態素の扱い

解析器はMeCabを使う。

- 原形を使う
- 連続する名詞は一つの単語として扱う (例: 東京|都 → 東京都)

詳細は、`script/tools.py#word_segmenter_ja`

## 手順

### テキストを抽出

(参考: 約10時間)

```
python script/WikiExtractor.py -c -o data/extracted data/jawiki-20150805-pages-articles.xml.bz2
```

**注意: 空のファイルができることがある!**

```
find data/extracted/ -type f -empty | xargs rm -i
```

---

(参考) 'Max template recursion exceeded!'が出てきて処理が終わらなかったので、途中からやり直し。

```
bzcat data/jawiki-20150805-pages-articles.xml.bz2 | head -35 > data/jawiki-20150805-pages-articles_tail.xml
bzcat data/jawiki-20150805-pages-articles.xml.bz2 | tail -n +49536626 >> data/jawiki-20150805-pages-articles_tail.xml
bzip2 jawiki-20150805-pages-articles_tail.xml
```

```
python script/WikiExtractor.py -c -o data/extracted/sub data/jawiki-20150805-pages-articles_tail.xml.bz2
```

途中でエラーが出る可能性があるなら、はじめから分割されたダンプファイルを使ったほうが良い。

### モデル作成

(参考: 約時間)

```
python script/learn.py data/jawiki_word2vec.pkl.gz
```

log:

```
...
2015-08-16 10:34:34,603 : INFO : collected 11592499 word types from a corpus of 409577477 words and 18483422 sentences
2015-08-16 10:34:39,038 : INFO : total 1313299 word types after removing those with count<5
...
```

## テスト
