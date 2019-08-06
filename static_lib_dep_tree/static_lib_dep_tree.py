#!/usr/bin/env python3

import sys
import os.path
import subprocess
import argparse

from graphviz import Digraph


def filterDefinedSymbol(lines):
    filtered_lines = []
    for no, line in enumerate(lines):
        if line.find(' T _') >= 0:
            undefined_symbol = line.split(' ')[-1]
            filtered_lines.append(undefined_symbol)
    return filtered_lines


def filterUndefinedSymbol(lines):
    filtered_lines = []
    for no, line in enumerate(lines):
        if line.find(' U _') >= 0:
            undefined_symbol = line.split(' ')[-1]
            filtered_lines.append(undefined_symbol)
    return filtered_lines


class LibArchive:
    def __init__(self):
        self.init()

    def init(self):
        self.parsed = False
        self.filepath = ""
        self.output_lines = []
        self.undefined_symbol_dict = {}
        self.defined_symbol_dict = {}

    def is_parse(self, filepath):
        return self.parsed == True

    def parse(self, filepath):
        self.filepath = filepath
        try:
            output = subprocess.check_output(["nm", "-A", self.filepath], stderr=subprocess.DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            print("Failed to execute '{0}'".format(' '.join(e.cmd)), file=sys.stderr)
            return False
        self.output_lines = output.splitlines()
        undefined_symbols = filterUndefinedSymbol(self.output_lines)
        self.undefined_symbol_dict = dict(zip(undefined_symbols, [None] * len(undefined_symbols)))
        defined_symbols = filterDefinedSymbol(self.output_lines)
        self.defined_symbol_dict = dict(zip(defined_symbols, [self.filepath] * len(defined_symbols)))
        return True

    def link(self, lib_archive):
        for undefined_symbol, depend in self.undefined_symbol_dict.items():
            if undefined_symbol in lib_archive.defined_symbol_dict:
                self.undefined_symbol_dict[undefined_symbol] = lib_archive.filepath

    def links(self, lib_archives):
        for index, lib_archive in enumerate(lib_archives):
            self.link(lib_archive)

    def get_resolved_symbol_dict(self):
        ret = {}
        ret.update(**self.defined_symbol_dict, **dict(filter(lambda v: v[1] is not None, self.undefined_symbol_dict.items())))
        return ret

    def get_unresolved_symbol_dict(self):
        return dict(filter(lambda v: v[1] is None, self.undefined_symbol_dict.items()))

    def get_depend_filepath_list(self):
        return list(dict(filter(lambda v: v[1] is not None, self.undefined_symbol_dict.items())).values())

    def is_resolved(self):
        return len(self.get_unresolved_symbol_dict()) == 0

    def __str__(self):
        ret = "[LibArchive]:{0}".format(self.filepath)
        ret += "\n  [undefined_symbols]"
        for undefined_symbol, depend in self.undefined_symbol_dict.items():
            ret += "\n  {0}:{1}".format(undefined_symbol, depend)
        ret += "\n  [defined_symbols]"
        for defined_symbol, depend in self.defined_symbol_dict.items():
            ret += "\n  {0}:{1}".format(defined_symbol, depend)
        return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True, type=str)
    parser.add_argument('--format', default="svg", type=str, help="svg,png,dot,jpg,pdf,bmp")
    parser.add_argument('--nodesep', default=1.0, type=float)
    parser.add_argument('--ranksep', default=1.0, type=float)
    parser.add_argument('-l', '--loop', action='store_true', help="enable gcc's '-Wl,--start-group ... -Wl,--end-group' like option")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--visible-self-loop', action='store_true', help="show .a self link edge loop (e.g. a1.o -> a2.o in a.a)")
    parser.add_argument('args', nargs='*')

    args, extra_args = parser.parse_known_args()

    lib_archive_dict = {}
    target_file_list = args.args
    uniq_target_file_list = sorted(set(target_file_list), key=target_file_list.index)
    for index, target_file in enumerate(uniq_target_file_list):
        lib_archive = LibArchive()
        ret = lib_archive.parse(target_file)
        if not ret:
            print("Failed to parse '{0}'".format(target_file), file=sys.stderr)
            return 1
        lib_archive_dict[target_file] = lib_archive

    # NOTE: 実行時引数で指定した順番にリンクを行う(ライブラリのファイルパスは重複する可能性があり，さｒに順番にも意味がある)
    for index, src_file in enumerate(target_file_list):
        lib_archive = lib_archive_dict[src_file]
        link_target_list = target_file_list[index + 1:]
        if args.loop:
            # NOTE: left shift (loop)
            link_target_list = target_file_list[index + 1:] + target_file_list[:index + 1]
        for _, target_file in enumerate(link_target_list):
            target_lib_archive = lib_archive_dict[target_file]
            lib_archive.link(target_lib_archive)

    main_graph = Digraph(format=args.format)
    main_graph.attr("graph", nodesep=str(args.nodesep), ranksep=str(args.ranksep))
    graph = main_graph

    for index, target_file in enumerate(uniq_target_file_list):
        lib_archive = lib_archive_dict[target_file]
        depend_filepath_list = lib_archive.get_depend_filepath_list()
        if args.verbose:
            print(index, lib_archive)
            print("depend_filepath_list", depend_filepath_list)
            print("resolved_symbol_dict", lib_archive.get_resolved_symbol_dict())
            print("unresolved_symbol_dict", lib_archive.get_unresolved_symbol_dict())
            print()
        style = "solid"
        if not lib_archive.is_resolved():
            style = "dotted"
            # NOTE: 複数の.aでunresolvedのときには複数個の'?'nodeが生成される?
            graph.node("?", shape="circle", color="black", style=style, label="?")
            graph.edge(lib_archive.filepath, "?", label="")
        graph.node(lib_archive.filepath, shape="circle", color="black", style=style, label=lib_archive.filepath)
        for depend_filepath in depend_filepath_list:
            if not args.visible_self_loop:
                if lib_archive.filepath == depend_filepath:
                    continue
            graph.edge(lib_archive.filepath, depend_filepath, label="")

    if args.verbose:
        print("[resolved_library_archives]")
        for index, target_file in enumerate(uniq_target_file_list):
            lib_archive = lib_archive_dict[target_file]
            if lib_archive.is_resolved():
                print(target_file)
        print("[unresolved_library_archives]")
        for index, target_file in enumerate(uniq_target_file_list):
            lib_archive = lib_archive_dict[target_file]
            if not lib_archive.is_resolved():
                print(target_file)

    # NOTE: to avoid xxx.svg -> xxx.svg.svg by using graphviz render() method
    output_filepath = args.output
    output_without_ext, ext = os.path.splitext(output_filepath)
    if ext == "." + args.format:
        output_filepath = output_without_ext
    main_graph.render(output_filepath)


if __name__ == '__main__':
    main()
