日本語Wikipediaのダンプデータからword2vecのモデルを作成する。(gensim)

## 必要なもの

- [jawiki-20150805-pages-articles.xml.bz2](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
- [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor)

## 手順

### テキストのみを抽出

```
python script/WikiExtractor.py -c -o data/extracted data/jawiki-20150805-pages-articles.xml.bz2
```

### モデル作成

```
python script/learn.py data/jawiki_word2vec.pkl.gz
```

## テスト
