日本語Wikipediaのダンプデータからword2vecのモデルを作成する。

## 必要なもの

- Python 2.7 (gensim, MeCab)
- [jawiki-20150805-pages-articles.xml.bz2](https://ja.wikipedia.org/wiki/Wikipedia:%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)
- [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor)

## 環境 (参考)

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
for f in $(find data/extracted/ -name "*.bz2"); do bzcat $f > /dev/null; done
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

(参考: 約1.5時間)

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

```
ls -lh data/jawiki_word2vec.pkl.gz
-rw-rw-r-- 1 nemo nemo 2.9G Aug 16 11:42 data/jawiki_word2vec.pkl.gz
```

## テスト

モデルをload。(参考) メモリを約4.5GB使う。

```
python
>>> import cPickle as pickle
>>> import gzip
>>> model = pickle.load(gzip.open('data/jawiki_word2vec.pkl.gz'))
```

### 類似語

```
>>> for w, s in model.most_similar(positive=[u'MLB']): print w, s
...
メジャーリーグ 0.69296759367
メジャーリーグベースボール 0.63514727354
傘下マイナーリーグ 0.623519837856
ワシントン・ナショナルズ傘下 0.619817733765
クリーブランド・インディアンス傘下 0.594461381435
ヤンキース 0.592985808849
ブレーブス 0.591527879238
タンパベイ・レイズ傘下 0.590766072273
コロラド・ロッキーズ傘下 0.589994132519
マイナーリーグ 0.589917302132
```

```
>>> for w, s in model.most_similar(positive=[u'イチロー']): print w, s
...
松井秀喜 0.738363087177
清原和博 0.691302418709
福留孝介 0.688463509083
ダルビッシュ有 0.682058334351
江夏豊 0.678952276707
デレク・ジーター 0.678451001644
掛布 0.675491333008
松坂大輔 0.673651516438
佐々木主浩 0.671629905701
坂本勇人 0.671455800533
```

```
>>> for w, s in model.most_similar(positive=[u'熱い']): print w, s
...
温かい 0.620217621326
冷たい 0.616167902946
辛い 0.577460348606
暖かい 0.542341768742
清々しい 0.532653987408
心地よい 0.523373246193
美味しい 0.522518217564
楽しい 0.514630615711
甘酸っぱい 0.513881921768
湿っぽい 0.507992327213
```

```
>>> for w, s in model.most_similar(positive=u'Python'.split()): print w, s
...
Perl 0.826446115971
C++ 0.803466677666
Ruby 0.802895665169
C言語 0.802019417286
Java 0.796339631081
Smalltalk 0.753612458706
Pascal 0.751491189003
JavaScript 0.741331577301
LISP 0.740336060524
Objective-C 0.722095966339
>>> for w, s in model.most_similar(positive=u'Scheme'.split()): print w, s
...
CommonLisp 0.750118553638
Haskell 0.725929439068
LISP 0.721939980984
OCaml 0.711216449738
Ada 0.710205078125
Pascal 0.704237878323
Forth 0.689190804958
Objective-C 0.684636116028
文字型 0.684105992317
正規表現 0.68187224865
```

### 足し引き

```
>>> for w, s in model.most_similar(positive=[u'王様', u'女性'], negative=[u'男性']): print w, s
...
ハイジ 0.561104953289
若様 0.553895354271
友だち 0.551104366779
テレビくん 0.525920629501
ヌレンナハール姫 0.520405471325
お姫様 0.519794046879
国ファイナルファンタジー・クリスタルクロニクル 0.514082670212
狂卓 0.512963712215
マーニー 0.50738132
王女様 0.506066501141
```

```
>>> for w, s in model.most_similar(positive=[u'東京', u'大阪'], negative=[u'横浜']): print w, s
...
名古屋 0.669375360012
神戸 0.620675981045
福岡 0.597984910011
静岡 0.588322162628
関西 0.580491423607
仙台 0.580258011818
札幌 0.56919413805
京都 0.559204399586
兵庫 0.544475376606
和歌山 0.542441129684
```
