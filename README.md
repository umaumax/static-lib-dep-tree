# static-lib-dep-tree

static libraries link dependency visualization tool

maybe you can get proper link order by `-v` option

## how to install
```
# for avoiding 'pip Installing collected packages: UNKNOWN'
pip3 install setuptools --upgrade
pip3 install https://github.com/umaumax/static-lib-dep-tree/archive/master.tar.gz
```

```
# required library
pip3 install graphviz
```

## how to run
```
static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a

static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a liba.a

static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a liba.a libc.a
static-lib-dep-tree -l -o out.svg liba.a libb.a libc.a libd.a libe.a
```

__you can use below python script to find circular reference__

* [misc\-scripts/dot\_find\_cycles\.py at master · jantman/misc\-scripts]( https://github.com/jantman/misc-scripts/blob/master/dot_find_cycles.py )
  * WARN: required python3 script but shebang is `#!/usr/bin/env python`

```
$ static-lib-dep-tree -l -o out.dot liba.a libb.a libc.a libd.a libe.a
$ ./dot_find_cycles.py out.dot
['libe.a', 'liba.a', 'libd.a', 'libc.a']
['libe.a', 'liba.a', 'libc.a']
['libe.a', 'liba.a', 'libb.a', 'libc.a']
['libd.a', 'libc.a']
```

```
$ static-lib-dep-tree -l -o opencv-dep.svg /usr/local/lib/libopencv*.a --enable-multi-edges
WIP
```

### how to run test
```
cd $(git rev-parse --show-toplevel)
# run all
python -m unittest discover tests
# run with filter
python -m unittest discover -p 'test*.py'
```

個別のモジュールをテストする場合(このときは，`./tests/__init__.py`を作成する必要がある)
```
cd $(git rev-parse --show-toplevel)
# <test dir name>.<test_target python file name without ext>
python -m unittest tests.test_static_lib_dep_tree
python -m unittest tests.test_static_lib_dep_tree.TestStaticLibDepTree
python -m unittest tests.test_static_lib_dep_tree.TestStaticLibDepTree.test_filter_defined_symbol_normal
```

### color output
```
pip install green
```

```
green
green -v
green -vv
green -vvv

green tests.test_static_lib_dep_tree.TestStaticLibDepTree.test_filter_defined_symbol_normal
```

## how to run coverage
[Djangoメモ\(26\) : coverage\.pyでカバレッジ（網羅率）を計測 \- もた日記]( https://wonderwall.hatenablog.com/entry/2018/03/26/003000 )

```
pip install coverage
```

```
coverage run --source='.' --omit='*/tests/*' -m unittest discover tests
```

you can use `.coveragerc`

```
coverage report -m
coverage report -m --omit='*/tests/*'

coverage report -m static_lib_dep_tree/static_lib_dep_tree.py
```

```
coverage html static_lib_dep_tree/static_lib_dep_tree.py
open htmlcov/index.html
coverage erase
```

----

## figures
* `[x]` -> `[y]`: x depends y

![out.dot.svg](./static_lib_dep_tree/examples/out.dot.svg)

## how to build static libs
```
for f in `ls *.cpp`; do g++ -std=c++11 $f -c -o ${f%.cpp}.o; ar r lib${f%.cpp}.a ${f%.cpp}.o; done

for f in `ls *.cpp`; do g++ -std=c++11 $f -c -o ${f%.cpp}.o; done

g++ -std=c++11 add.cpp -c -o add.o
ar r libadd.a add.o
g++ -std=c++11 sub.cpp -c -o sub.o
ar r libsub.a sub.o

ar r libabced.a a.o b.o c.o d.o e.o
```

## nm command output examples
```
# Max OS X
$ nm -A libadd.a
libadd.a:add.o: 0000000000000000 T __Z3addii
libadd.a:add.o:                  U __Z3subii
$ nm -A libsub.a
libsub.a:sub.o: 0000000000000000 T __Z3subii

# Ubuntu 16.04
$ nm -A libadd.a
libadd.a:add.o:0000000000000000 T __Z3addii
libadd.a:add.o:                 U __Z3subii
$ nm -A libsub.a
libsub.a:sub.o:0000000000000000 T __Z3subii
```

## FMI
### check list
* [x] .aの中の.oの依存関係による自己ループ
* [x] .aの中の.oの仕様の確認
* [x] .aから他の.aへの複数の依存エッジ
* [x] ループしてリンク先を検索した際に見つかる定義とそうでないものを分ける
  * 1.ループなしでlinkを行う
  * 2.ループありでlinkを行う(このときに，新規にlinkできたものに対してflagをONとし，これは，ループすれば見つかるシンボルを表す)
  * NOTE: 1.と2.は指定ライブラリをすべて一巡せずにその場で行っても問題ない(liba.a libb.a liba.aという重複パターンにおいても)
* [x] 可視化したsvgを上から順番に見ていけば、依存関係の解決が可能だが，CUI的なoutputは?
  * `networkx` libraryを利用?
* [x] 依存性のないライブラリに色を付ける
  * [Graphviz/Python: Recoloring a single node after it has been generated \- Stack Overflow]( https://stackoverflow.com/questions/44337180/graphviz-python-recoloring-a-single-node-after-it-has-been-generated )
  * そもそも，`graphviz`ライブラリはedit向けではないので，`networkx`で書き直すとよい
* [ ] `networkx`で書き直し
* [ ] 複数エッジ表現を本数以外に，太さで表現したい(描画の幅の省略ため)
  * `penwidth`を利用

### NOTE
* [Library order in static linking \- Eli Bendersky's website]( https://eli.thegreenplace.net/2013/07/09/library-order-in-static-linking )
* コンパイル時の引数の`.o`のリンク順番は関係あるが，`.o`を`.a`にした際には内部のリンクの順番は関係ない?

## unittest links
### 基本(ディレクトリ構成/コマンド)
* [Python 3 標準の unittest でテストを書く際のディレクトリ構成 \- Qiita]( https://qiita.com/hoto17296/items/fa0166728177e676cd36 )
* [Python標準のunittestの使い方メモ \- Qiita]( https://qiita.com/aomidro/items/3e3449fde924893f18ca )
* [Pythonのunittestでハマったところと、もっと早くに知りたかったこと \- Qiita]( https://qiita.com/jesus_isao/items/f93c11248192645eb25d )

### 書き方
* [Python の 単体テストで 大量の入力パターンを効率よくテストする方法 \- Qiita]( https://qiita.com/Asayu123/items/61ef72bb829dd8baba9f )
