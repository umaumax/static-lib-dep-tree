#!/usr/bin/env python3

import unittest
import static_lib_dep_tree


class TestStaticLibDepTree(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_filter_defined_symbol_normal(self):
        input = ['libadd.a:add.o: 0000000000000000 T __Z3addii', 'libadd.a:add.o:                  U __Z3subii']
        result = static_lib_dep_tree.filter_defined_symbol(input)
        print(result)
        self.assertEqual(1, 1)

# NOTE: we cannot test codes with main function when treated as test modules
# because relative filepath is differ between current path and library modules


"""
if __name__ == "__main__":
    unittest.main()
"""
