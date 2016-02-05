#!/usr/bin/python
# coding:utf-8

import MeCab
import sys
import string
import hashlib
import re
import os

# こちらを参考に変換表を作る http://d.hatena.ne.jp/mohayonao/20091129/1259505966
"""かな⇔ローマ字を変換する"""

def _make_kana_convertor():
    """ひらがな⇔カタカナ変換器を作る"""
    kata = {
        'ア':'あ', 'イ':'い', 'ウ':'う', 'エ':'え', 'オ':'お',
        'カ':'か', 'キ':'き', 'ク':'く', 'ケ':'け', 'コ':'こ',
        'サ':'さ', 'シ':'し', 'ス':'す', 'セ':'せ', 'ソ':'そ',
        'タ':'た', 'チ':'ち', 'ツ':'つ', 'テ':'て', 'ト':'と',
        'ナ':'な', 'ニ':'に', 'ヌ':'ぬ', 'ネ':'ね', 'ノ':'の',
        'ハ':'は', 'ヒ':'ひ', 'フ':'ふ', 'ヘ':'へ', 'ホ':'ほ',
        'マ':'ま', 'ミ':'み', 'ム':'む', 'メ':'め', 'モ':'も',
        'ヤ':'や', 'ユ':'ゆ', 'ヨ':'よ', 'ラ':'ら', 'リ':'り',
        'ル':'る', 'レ':'れ', 'ロ':'ろ', 'ワ':'わ', 'ヲ':'を',
        'ン':'ん',

        'ガ':'が', 'ギ':'ぎ', 'グ':'ぐ', 'ゲ':'げ', 'ゴ':'ご',
        'ザ':'ざ', 'ジ':'じ', 'ズ':'ず', 'ゼ':'ぜ', 'ゾ':'ぞ',
        'ダ':'だ', 'ヂ':'ぢ', 'ヅ':'づ', 'デ':'で', 'ド':'ど',
        'バ':'ば', 'ビ':'び', 'ブ':'ぶ', 'ベ':'べ', 'ボ':'ぼ',
        'パ':'ぱ', 'ピ':'ぴ', 'プ':'ぷ', 'ペ':'ぺ', 'ポ':'ぽ',

        'ァ':'ぁ', 'ィ':'ぃ', 'ゥ':'ぅ', 'ェ':'ぇ', 'ォ':'ぉ',
        'ャ':'ゃ', 'ュ':'ゅ', 'ョ':'ょ',
        'ヴ':'&#12436;', 'ッ':'っ', 'ヰ':'ゐ', 'ヱ':'ゑ',
        }

    # ひらがな → カタカナ のディクショナリをつくる
    hira = dict([(v, k) for k, v in kata.items() ])

    re_hira2kata = re.compile("|".join(map(re.escape, hira)))
    re_kata2hira = re.compile("|".join(map(re.escape, kata)))

    def _hiragana2katakana(text):
        return re_hira2kata.sub(lambda x: hira[x.group(0)], text)

    def _katakana2hiragana(text):
        return re_kata2hira.sub(lambda x: kata[x.group(0)], text)

    return (_hiragana2katakana, _katakana2hiragana)


hiragana2katakana, katakana2hiragana = _make_kana_convertor()

################################################################################

def _make_romaji_convertor():
    """ローマ字⇔かな変換器を作る"""
    master = {
        ' a'  :'ア', ' i'  :'イ', ' u'  :'ウ', ' e'  :'エ', ' o'  :'オ',
        ' k a' :'カ', ' k i' :'キ', ' k u' :'ク', ' k e' :'ケ', ' k o' :'コ',
        ' s a' :'サ', ' sh i':'シ', ' s u' :'ス', ' s e' :'セ', ' s o' :'ソ',
        ' t a' :'タ', ' ch i':'チ', ' t u' :'ツ', ' t e' :'テ', ' t o' :'ト',
        ' n a' :'ナ', ' n i' :'ニ', ' n u' :'ヌ', ' n e' :'ネ', ' n o' :'ノ',
        ' h a' :'ハ', ' h i' :'ヒ', ' f u' :'フ', ' h e' :'ヘ', ' h o' :'ホ',
        ' m a' :'マ', ' m i' :'ミ', ' m u' :'ム', ' m e' :'メ', ' m o' :'モ',
        ' y a' :'ヤ', ' y u' :'ユ', ' y o' :'ヨ',
        ' r a' :'ラ', ' r i' :'リ', ' r u' :'ル', ' r e' :'レ', ' r o' :'ロ',
        ' w a' :'ワ', ' w o' :'ヲ', ' N'  :'ン', ' v u' :'ヴ',
        ' g a' :'ガ', ' g i' :'ギ', ' g u' :'グ', ' g e' :'ゲ', ' g o' :'ゴ',
        ' z a' :'ザ', ' j i' :'ジ', ' z u' :'ズ', ' z e' :'ゼ', ' z o' :'ゾ',
        ' d a' :'ダ', ' d i' :'ヂ', ' d u' :'ヅ', ' d e' :'デ', ' d o' :'ド',
        ' b a' :'バ', ' b i' :'ビ', ' b u' :'ブ', ' b e' :'ベ', ' b o' :'ボ',
        ' p a' :'パ', ' p i' :'ピ', ' p u' :'プ', ' p e' :'ペ', ' p o' :'ポ',

        ' ky a':'キャ', ' ky i':'キィ', ' ky u':'キュ', ' ky e':'キェ', ' ky o':'キョ',
        ' gy a':'ギャ', ' gy i':'ギィ', ' gy u':'ギュ', ' gy e':'ギェ', ' gy o':'ギョ',
        ' sh a':'シャ',               ' sh u':'シュ', ' sh e':'シェ', ' sh o':'ショ',
        ' j a' :'ジャ',               ' j u' :'ジュ', ' j e' :'ジェ', ' j o' :'ジョ',
        ' ch a':'チャ',               ' ch u':'チュ', ' ch e':'チェ', ' ch o':'チョ',
        ' dy a':'ヂャ', ' dy i':'ヂィ', ' dy u':'ヂュ', ' dh e':'デェ', ' dy o':'ヂョ',
        ' ny a':'ニャ', ' ny i':'ニィ', ' ny u':'ニュ', ' ny e':'ニェ', ' ny o':'ニョ',
        ' hy a':'ヒャ', ' hy i':'ヒィ', ' hy u':'ヒュ', ' hy e':'ヒェ', ' hy o':'ヒョ',
        ' by a':'ビャ', ' by i':'ビィ', ' by u':'ビュ', ' by e':'ビェ', ' by o':'ビョ',
        ' py a':'ピャ', ' py i':'ピィ', ' py u':'ピュ', ' py e':'ピェ', ' py o':'ピョ',
        ' my a':'ミャ', ' my i':'ミィ', ' my u':'ミュ', ' my e':'ミェ', ' my o':'ミョ',
        ' ry a':'リャ', ' ry i':'リィ', ' ry u':'リュ', ' ry e':'リェ', ' ry o':'リョ',
        ' f a' :'ファ', ' f i' :'フィ',               'f e' :'フェ', ' f o' :'フォ',
        ' w i' :'ウィ', ' w e' :'ウェ',
        ' v a' :'ヴァ', ' v i' :'ヴィ', ' v e' :'ヴェ', ' v o' :'ヴォ',

        ' k u a':'クァ', ' k u i':'クィ', ' k u u':'クゥ', ' k u e':'クェ', ' k u o':'クォ',
        ' k u a':'クァ', ' k u i':'クィ', ' k u u':'クゥ', ' k u e':'クェ', ' k u o':'クォ',
        ' g u a':'グァ', ' g u i':'グィ', ' g u u':'グゥ', ' g u e':'グェ', ' g u o':'グォ',
        ' g u a':'グァ', ' g u i':'グィ', ' g u u':'グゥ', ' g u e':'グェ', ' g u o':'グォ',
        ' s u a':'スァ', ' s u i':'スィ', ' s u u':'スゥ', ' s u e':'スェ', ' s u o':'スォ',
        ' s u a':'スァ', ' s u i':'スィ', ' s u u':'スゥ', ' s u e':'スェ', ' s u o':'スォ',
        ' z u a':'ズヮ', ' z u i':'ズィ', ' z u u':'ズゥ', ' z u e':'ズェ', ' z u o':'ズォ',
        ' t o a':'トァ', ' t o i':'トィ', ' t o u':'トゥ', ' t o e':'トェ', ' t o o':'トォ',
        ' d o a':'ドァ', ' d o i':'ドィ', ' d o u':'ドゥ', ' d o e':'ドェ', ' d o o':'ドォ',
        ' m u a':'ムヮ', ' m u i':'ムィ', ' m u u':'ムゥ', ' m u e':'ムェ', ' m u o':'ムォ',
        ' b i a':'ビヮ', ' b i i':'ビィ', ' b i u':'ビゥ', ' b i e':'ビェ', ' b i o':'ビォ',
        ' p u a':'プヮ', ' p u i':'プィ', ' p u u':'プゥ', ' p u e':'プェ', ' p u o':'プォ',
        ' p u i':'プィ', ' p u u':'プゥ', ' p u e':'プェ', ' p u o':'フォ',
        ' q':'ッ',
        }


    romaji_asist = {
        ' sh a':'シャ', ' sh u':'シュ', ' sh o':'ショ',
        ' ch a':'チャ', ' ch u':'チュ', ' ch o':'チョ',
        ' jy a':'ジャ', ' jy u':'ジュ', ' jy o':'ジョ', ' pha':'ファ',
        ' k a' :'クァ', ' k u i' :'クィ', ' k u' :'クゥ', ' k u e' :'クェ', ' k u o':'クォ',
        }


    kana_asist = { ' a':'ァ', ' i':'ィ', ' u':'ゥ', ' e':'ェ', ' o':'ォ', }


    def __romaji2kana():
        romaji_dict = {}
        for tbl in master, romaji_asist:
            for k, v in tbl.items(): romaji_dict[k] = v

        romaji_keys = romaji_dict.keys()
        romaji_keys.sort(key=lambda x:len(x), reverse=True)

        re_roma2kana = re.compile("|".join(map(re.escape, romaji_keys)))
        # m の後ろにバ行、パ行のときは "ン" と変換
        rx_mba = re.compile("m(b|p)([aiueo])")
        # 子音が続く時は "ッ" と変換
        rx_xtu = re.compile(r"([bcdfghjklmpqrstvwxyz])\1")
        # 母音が続く時は "ー" と変換
        rx_a__ = re.compile(r"([aiueo])\1")

        def _romaji2katakana(text):
            result = text.lower()
            result = rx_mba.sub(r"ン\1\2", result)
            result = rx_xtu.sub(r"ッ\1"  , result)
            result = rx_a__.sub(r"\1ー"  , result)
            return re_roma2kana.sub(lambda x: romaji_dict[x.group(0)], result)

        def _romaji2hiragana(text):
            result = _romaji2katakana(text)
            return katakana2hiragana(result)

        return _romaji2katakana, _romaji2hiragana


    def __kana2romaji():
        kana_dict = {}
        for tbl in master, kana_asist:
            for k, v in tbl.items(): kana_dict[v] = k

        kana_keys = kana_dict.keys()
        kana_keys.sort(key=lambda x:len(x), reverse=True)

        re_kana2roma = re.compile("|".join(map(re.escape, kana_keys)))
        rx_xtu = re.compile("ッ(.)") # 小さい "ッ" は直後の文字を２回に変換
        rx_ltu = re.compile("ッ$"  ) # 最後の小さい "ッ" は消去(?)
        rx_er  = re.compile("(.)ー") # "ー"は直前の文字を２回に変換
        rx_n   = re.compile(r"n(b|p)([aiueo])") # n の後ろが バ行、パ行 なら m に修正
        rx_oo  = re.compile(r"([aiueo])\1")      # oosaka → osaka

        def _kana2romaji(text):
            result = hiragana2katakana(text)
            result = re_kana2roma.sub(lambda x: kana_dict[x.group(0)], result)
            result = rx_xtu.sub(r"\1\1" , result)
            result = rx_ltu.sub(r""     , result)
            result = rx_er.sub (r"\1\1" , result)
            result = rx_n.sub  (r"m\1\2", result)
            result = rx_oo.sub (r"\1"   , result)
            return result
        return _kana2romaji

    a, b = __romaji2kana()
    c    = __kana2romaji()

    return  a, b, c


romaji2katakana, romaji2hiragana, kana2romaji = _make_romaji_convertor()

f = open('sentence.txt', 'r')
idx = 0
path = "./result/"
# 1行ずつ読み込む
for l in f:
    # 各文法のディレクトリを作る
    if os.path.exists(path + str(idx)) != True:
        os.mkdir(path + str(idx))

    l = l.rstrip()
    flag = ''
    if os.path.exists("./list.dic"):
        flag = '-u list.dic'
    t = MeCab.Tagger (flag)
    m = t.parseToNode (l)

    dict = {}
    syntax = []
    # 単語ごとに処理を行う
    while m:
        splited_feature = m.feature.split(',')
        feature = splited_feature[0]
        kana = splited_feature[-1]
        surface = m.surface

        # 品詞に対応するIDを生成
        w_id = hashlib.md5(str(m.id)).hexdigest()
        if surface == '？':
            m = m.next
            continue
        if surface == '、':
            surface = 'sp'
            w_id = 1000000000

        if feature != 'BOS/EOS':
            print m.surface + ":" + m.feature + " " + kana2romaji(kana)
            syntax.append(w_id)
            if w_id in dict:
                yomi = dict[w_id]
                yomi.add(surface + kana2romaji(kana))
            else:
                yomi = set([surface + kana2romaji(kana)])
                dict[w_id] = yomi
        m = m.next

    # 文章に対応する文法と読みのファイルを生成する
    grammar = open(path + str(idx) + "/" + str(idx) + ".grammar", "w")
    print >> grammar, "S : NS_B WORD NS_E"
    common = open('common_grammar.txt', 'r')
    for c in common:
        print >> grammar, c.replace('\n', '')

    keys = set([])
    key = map(str, syntax)
    keys.add(" ".join(key))

    for x in keys:
        print >> grammar, 'WORD :', x

    voca = open(path + str(idx) + "/" + str(idx) + ".voca", "w")
    common = open('common_word.txt', 'r')
    for c in common:
        print >> voca, c.replace('\n', '')
    
    for k in dict:
        print >> voca, "%", k
        for v in dict[k]:
            print >> voca, v

    idx += 1
f.close()
