# ktnhtmg

その時々の素直な心情を包み隠さず、juliusの音声認識用文法ファイルを例文ファイルから自動で生成する。

OSXで動作を確認済み。

## Dependencies
- julius
- MeCab
- MeCab-Python

## Usage
- `git submodule init`
- 設定ファイルを編集
- `convert.command`をダブルクリック
- 生成された文法ファイルをテストする際は`voice_text.command`をダブルクリック

## 設定ファイル
- sentence.txt
  - 例文ファイル。ここに認識させたい文章を一行ずつ記述する。
- common_grammar.txt
  - 共通で認識する文法を記述する。common_word.txtと組み合わせて使う。
- common_word.txt
  - 文頭に共通で認識する文章を記述する。common_grammar.txtと組み合わせて使う。
- list.txt
  - 固有名詞を記述する。固有名詞と読み方（ひらがな）を`,`区切りで記述する。

## その他
生成されたgrammarファイルはresult以下に展開されます。

# License
3-clause BSD License.