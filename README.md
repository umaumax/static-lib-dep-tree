# static-lib-dep-tree

static libraries link dependency visualization tool

maybe you can get proper link order by `-v` option

## how to install
``` bash
# for avoiding 'pip Installing collected packages: UNKNOWN'
pip3 install setuptools --upgrade
pip3 install https://github.com/umaumax/static-lib-dep-tree/archive/master.tar.gz
```

``` bash
# required library
pip3 install graphviz
```

## how to run
``` bash
static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a

static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a liba.a

static-lib-dep-tree -o out.svg liba.a libb.a libc.a libd.a libe.a liba.a libc.a
static-lib-dep-tree -l -o out.svg liba.a libb.a libc.a libd.a libe.a
```

__you can use below python script to find circular reference__

* [misc\-scripts/dot\_find\_cycles\.py at master · jantman/misc\-scripts]( https://github.com/jantman/misc-scripts/blob/master/dot_find_cycles.py )
  * WARN: required python3 script but shebang is `#!/usr/bin/env python`

``` bash
$ static-lib-dep-tree -l -o out.dot liba.a libb.a libc.a libd.a libe.a
$ ./dot_find_cycles.py out.dot
['libe.a', 'liba.a', 'libd.a', 'libc.a']
['libe.a', 'liba.a', 'libc.a']
['libe.a', 'liba.a', 'libb.a', 'libc.a']
['libd.a', 'libc.a']
```

``` bash
$ static-lib-dep-tree -l -o opencv-dep.svg /usr/local/lib/libopencv*.a --enable-multi-edges -v
/usr/local/lib/libopencv_superres.a /usr/local/lib/libopencv_optflow.a /usr/local/lib/libopencv_bgsegm.a /usr/local/lib/libopencv_xobjdetect.a /usr/local/lib/libopencv_stereo.a /usr/local/lib/libopencv_face.a /usr/local/lib/libopencv_videostab.a /usr/local/lib/libopencv_tracking.a /usr/local/lib/libopencv_ximgproc.a /usr/local/lib/libopencv_stitching.a /usr/local/lib/libopencv_ccalib.a /usr/local/lib/libopencv_video.a /usr/local/lib/libopencv_aruco.a /usr/local/lib/libopencv_rgbd.a /usr/local/lib/libopencv_objdetect.a /usr/local/lib/libopencv_shape.a /usr/local/lib/libopencv_sfm.a /usr/local/lib/libopencv_structured_light.a /usr/local/lib/libopencv_datasets.a /usr/local/lib/libopencv_calib3d.a /usr/local/lib/libopencv_xfeatures2d.a /usr/local/lib/libopencv_videoio.a /usr/local/lib/libopencv_xphoto.a /usr/local/lib/libopencv_text.a /usr/local/lib/libopencv_surface_matching.a /usr/local/lib/libopencv_imgcodecs.a /usr/local/lib/libopencv_img_hash.a /usr/local/lib/libopencv_line_descriptor.a /usr/local/lib/libopencv_highgui.a /usr/local/lib/libopencv_dpm.a /usr/local/lib/libopencv_freetype.a /usr/local/lib/libopencv_gapi.a /usr/local/lib/libopencv_hfs.a /usr/local/lib/libopencv_features2d.a /usr/local/lib/libopencv_plot.a /usr/local/lib/libopencv_reg.a /usr/local/lib/libopencv_saliency.a /usr/local/lib/libopencv_photo.a /usr/local/lib/libopencv_dnn.a /usr/local/lib/libopencv_quality.a /usr/local/lib/libopencv_bioinspired.a /usr/local/lib/libopencv_dnn_objdetect.a /usr/local/lib/libopencv_fuzzy.a /usr/local/lib/libopencv_flann.a /usr/local/lib/libopencv_imgproc.a /usr/local/lib/libopencv_ml.a /usr/local/lib/libopencv_phase_unwrapping.a /usr/local/lib/libopencv_core.a
$ pkg-config --libs opencv4
-L/usr/local/Cellar/opencv/4.1.1_2/lib -lopencv_gapi -lopencv_stitching -lopencv_aruco -lopencv_bgsegm -lopencv_bioinspired -lopencv_ccalib -lopencv_dnn_objdetect -lopencv_dpm -lopencv_face -lopencv_freetype -lopencv_fuzzy -lopencv_hfs -lopencv_img_hash -lopencv_line_descriptor -lopencv_quality -lopencv_reg -lopencv_rgbd -lopencv_saliency -lopencv_sfm -lopencv_stereo -lopencv_structured_light -lopencv_phase_unwrapping -lopencv_superres -lopencv_optflow -lopencv_surface_matching -lopencv_tracking -lopencv_datasets -lopencv_text -lopencv_highgui -lopencv_dnn -lopencv_plot -lopencv_videostab -lopencv_video -lopencv_videoio -lopencv_xfeatures2d -lopencv_shape -lopencv_ml -lopencv_ximgproc -lopencv_xobjdetect -lopencv_objdetect -lopencv_calib3d -lopencv_imgcodecs -lopencv_features2d -lopencv_flann -lopencv_xphoto -lopencv_photo -lopencv_imgproc -lopencv_core
```

### how to run test
``` bash
cd $(git rev-parse --show-toplevel)
# run all
python -m unittest discover tests
# run with filter
python -m unittest discover -p 'test*.py'
```

個別のモジュールをテストする場合(このときは，`./tests/__init__.py`を作成する必要がある)
``` bash
cd $(git rev-parse --show-toplevel)
# <test dir name>.<test_target python file name without ext>
python -m unittest tests.test_static_lib_dep_tree
python -m unittest tests.test_static_lib_dep_tree.TestStaticLibDepTree
python -m unittest tests.test_static_lib_dep_tree.TestStaticLibDepTree.test_filter_defined_symbol_normal
```

### color output
``` bash
pip install green
```

``` bash
green
green -v
green -vv
green -vvv

green tests.test_static_lib_dep_tree.TestStaticLibDepTree.test_filter_defined_symbol_normal
```

## how to run coverage
[Djangoメモ\(26\) : coverage\.pyでカバレッジ（網羅率）を計測 \- もた日記]( https://wonderwall.hatenablog.com/entry/2018/03/26/003000 )

``` bash
pip install coverage
```

``` bash
coverage run --source='.' --omit='*/tests/*' -m unittest discover tests
```

you can use `.coveragerc`

``` bash
coverage report -m
coverage report -m --omit='*/tests/*'

coverage report -m static_lib_dep_tree/static_lib_dep_tree.py
```

``` bash
coverage html static_lib_dep_tree/static_lib_dep_tree.py
open htmlcov/index.html
coverage erase
```

----

## figures
* `[x]` -> `[y]`: x depends y

![out.dot.svg](./static_lib_dep_tree/examples/out.dot.svg)

## how to build static libs
``` bash
for f in `ls *.cpp`; do g++ -std=c++11 $f -c -o ${f%.cpp}.o; ar r lib${f%.cpp}.a ${f%.cpp}.o; done

for f in `ls *.cpp`; do g++ -std=c++11 $f -c -o ${f%.cpp}.o; done

g++ -std=c++11 add.cpp -c -o add.o
ar r libadd.a add.o
g++ -std=c++11 sub.cpp -c -o sub.o
ar r libsub.a sub.o

ar r libabced.a a.o b.o c.o d.o e.o
```

## nm command output examples
``` bash
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
* [x] 共有ライブラリへの対応
  * lddtreeで、依存はしているが実は不使用な共有ライブラリの洗い出しが可能

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

## other tools?
* [ojroques/staticdep: A tool to compute the dependencies among object files of a static library]( https://github.com/ojroques/staticdep )
  * `.a`から`.json`形式で結果を出力する
    * それを利用して，単一の`.a`の中の`.o`同士の依存関係を調査するツール
  * Ubuntu 16.04で動作確認済
  * Mac OS Xでは`nm -s`が実行できず，オプションを変更すると想定した出力とならず，parse errorとなる

* [jameysharp/static\-ldd: Library and command\-line tool for inferring dependencies between static libraries\.]( https://github.com/jameysharp/static-ldd )

``` bash
cargo install --git https://github.com/jameysharp/static-ldd
```

では，buildエラーとなるので，下記のpatchを当てて，`cargo install`とするとビルドはできるが，想定通りの挙動とならず

``` diff
diff --git a/Cargo.toml b/Cargo.toml
index a8e88d2..02c2baf 100644
--- a/Cargo.toml
+++ b/Cargo.toml
@@ -10,5 +10,5 @@ description = """A library and command-line tool for inferring
 dependencies between static libraries."""
 
 [dependencies]
-filebuffer = "0.2.0"
+filebuffer = "0.4.0"
 goblin = "0.0.10"
```
