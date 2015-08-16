日本語Wikipediaのダンプデータからword2vecのモデルを作成する。(gensim)

## 必要なもの

- [jawiki-20150805-pages-articles.xml.bz2](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
- [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor)

## 手順

### テキストのみを抽出

```
python script/WikiExtractor.py -c -o data/extracted data/jawiki-20150805-pages-articles.xml.bz2
```

途中で、'Max template recursion exceeded!'が出てきて処理が終わらなかったので、途中からやり直し。

```
bzcat data/jawiki-20150805-pages-articles.xml.bz2 | head -35 > data/jawiki-20150805-pages-articles_tail.xml
bzcat data/jawiki-20150805-pages-articles.xml.bz2 | tail -n +49536626 >> data/jawiki-20150805-pages-articles_tail.xml
bzip2 jawiki-20150805-pages-articles_tail.xml
```

```
python script/WikiExtractor.py -c -o data/extracted/sub data/jawiki-20150805-pages-articles_tail.xml.bz2
```

はじめから分割されたデータを使ったほうが良かったかも

### モデル作成

```
python script/learn.py data/jawiki_word2vec.pkl.gz
```

## テスト
