#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import MeCab


def sent_splitter_ja(text, fix_parenthesis=False): # unicode
    sents = re.sub(ur'([。．？！\n\r]+)', r'\1|', text).split('|')
    sents = [s for s in sents if len(s) > 0]
    if fix_parenthesis:
        # 開いた括弧は必ず閉じる．
        parenthesis = u'（）「」『』()'
        close2open = dict(zip(parenthesis[1::2], parenthesis[0::2]))
        fixed_sents = []
        pstack = []
        buff = u''
        for sent in sents:
            pattern = re.compile(u'[' + parenthesis + u']')
            ps = re.findall(pattern, sent)
            if len(ps) > 0:
                for p in ps:
                    if p in close2open.values(): # open
                        pstack.append(p)
                    elif len(pstack) > 0 and pstack[-1] == close2open[p]: # close
                        pstack.pop()
            # ここでpstackが空なら括弧の対応がとれている．
            if len(pstack) == 0:
                buff += sent
                if len(buff) > 0:
                    fixed_sents.append(buff)
                buff = u''
            else:
                buff += sent
        if len(buff) > 0:
            fixed_sents.append(buff)

        sents = fixed_sents
    return sents


_mecab = MeCab.Tagger()

def _mecab_node2seq(node):
    while node:
        yield node
        node = node.next


def nodes2words(nodes):
    '''
    mecab nodes -> [word]
      - 原形を返す．
      - 名詞句はまとめる．
    '''
    words = []
    noun_buff = ''
    for n in nodes:
        feat = n.feature.split(',')
        word = feat[6] if feat[6] != '*' else n.surface # 原形
        if feat[0] == '名詞':
            noun_buff += word
            if feat[1] == '接尾':
                words.append(noun_buff)
                noun_buff = ''
        else:
            if len(noun_buff) > 0:
                words.append(noun_buff)
                noun_buff = ''
            words.append(word)
    return words


def word_segmenter_ja(sent):
    if type(sent) == unicode:
        sent = sent.encode('utf-8')
    nodes = list(_mecab_node2seq(_mecab.parseToNode(sent)))
    words = nodes2words(nodes)
    words = [w.decode('utf-8') for w in words]
    return words


if __name__ == '__main__':

    text = u'''
    利根川は大水上山を水源として関東地方を北から東へ流れ、太平洋に注ぐ河川。河川法に基づく国土交通省政令により1965年（昭和40年）に指定された一級河川・利根川水系の本流である。「坂東太郎」の異名を持つ。河川の規模としては日本最大級の規模を持ち、東京都を始めとした首都圏の水源として日本の経済活動上重要な役割を有する、日本を代表する河川の一つである。

    また彼の弟子達の多種多様な思想展開からもわかるように、着眼点によって様々な解釈が可能な、多面的な性格を持ち合わせていた思想家であったとも言える。ちなみに、相当皮肉屋な人物であったようで、死刑が確定し、妻のクサンティッペが「無実の罪で死ぬなんて！」と嘆いた時も、「じゃあ僕が有罪で死んだほうがよかったのかい？」といったといわれる。
    '''
    sents = sent_splitter_ja(text, fix_parenthesis=True)
    for s in sents:
        s = s.strip()
        if len(s) == 0:
            continue
        words = word_segmenter_ja(s)
        print u'|'.join(words).encode('utf-8')
