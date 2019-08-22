#!/usr/bin/env python3

import unittest
import static_lib_dep_tree


class TestStaticLibDepTree(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_filter_defined_symbol_normal(self):
        dataset = [
            ([], []),
            ([''], []),
            # Mac OS X
            (['libadd.a:add.o: 0000000000000000 T __Z3addii', 'libadd.a:add.o:                  U __Z3subii'], ['__Z3addii']),
            (['libsub.a:sub.o: 0000000000000000 T __Z3subii'], ['__Z3subii']),
            # Ubuntu 16.04
            (['libadd.a:add.o:0000000000000000 T __Z3addii',
              'libadd.a:add.o:                 U __Z3subii'], ['__Z3addii']),
            (['libsub.a:sub.o:0000000000000000 T __Z3subii'], ['__Z3subii']),
        ]
        # NOTE: this index may be useful to find input data index
        for index, element in enumerate(dataset):
            input, expected = element
            with self.subTest(index=index, input=input, expected=expected):
                result = static_lib_dep_tree.filter_defined_symbol(input)
                self.assertEqual(result, expected)

    def test_filter_defined_symbol_error(self):
        dataset = [
            (['xxx'], []),
        ]
        for index, element in enumerate(dataset):
            input, expected = element
            with self.subTest(index=index, input=input, expected=expected):
                result = static_lib_dep_tree.filter_defined_symbol(input)
                self.assertEqual(result, expected)

    def test_filter_undefined_symbol_normal(self):
        dataset = [
            ([], []),
            ([''], []),
            # Mac OS X
            (['libadd.a:add.o: 0000000000000000 T __Z3addii', 'libadd.a:add.o:                  U __Z3subii'], ['__Z3subii']),
            (['libsub.a:sub.o: 0000000000000000 T __Z3subii'], []),
            # Ubuntu 16.04
            (['libadd.a:add.o:0000000000000000 T __Z3addii',
              'libadd.a:add.o:                 U __Z3subii'], ['__Z3subii']),
            (['libsub.a:sub.o:0000000000000000 T __Z3subii'], []),
        ]
        for index, element in enumerate(dataset):
            input, expected = element
            with self.subTest(index=index, input=input, expected=expected):
                result = static_lib_dep_tree.filter_undefined_symbol(input)
                self.assertEqual(result, expected)

    def test_filter_undefined_symbol_error(self):
        dataset = [
            (['xxx'], []),
        ]
        for index, element in enumerate(dataset):
            input, expected = element
            with self.subTest(index=index, input=input, expected=expected):
                result = static_lib_dep_tree.filter_undefined_symbol(input)
                self.assertEqual(result, expected)

# NOTE: we cannot test codes with main function when treated as test modules
# because relative filepath is differ between current path and library modules


"""
if __name__ == "__main__":
    unittest.main()
"""
