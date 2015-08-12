#!/usr/bin/env python2.7
import unittest
import main

class TestLogicObjects(unittest.TestCase):

    def setUp(self):
        self.actor = main.Actor('test actor','test actor description')
        self.area = main.Area('test area','test area description')

    def tearDown(self):
        pass


    def test_actor(self):
        self.assertTrue(self.actor.name == 'test actor')
        self.assertTrue(self.actor.description == 'test actor description')
        self.assertTrue(self.actor.type == 'being')

    def test_area(self):
        self.assertTrue(self.area.name == 'test area')
        self.assertTrue(self.area.description == 'test area description')
        self.assertTrue(self.area.type == 'place')


class TestGUIWindows(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_foo(self):
        pass


if __name__ == '__main__':
    unittest.main()