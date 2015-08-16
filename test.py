#!/usr/bin/env python2.7
import main
import traceback
import unittest
import subprocess

class TestLogicObjects(unittest.TestCase):

    def setUp(self):
        self.case_name = 'TestLogicObjects'
        self.actor = main.Actor('test actor','test actor description')
        self.area = main.Area('test area','test area description')

    def tearDown(self):
        pass


    def test_actor(self):
        t_name = self.case_name + '.test_actor'
        print "\nStarting %s..." % t_name
        self.assertTrue(self.actor.name == 'test actor')
        self.assertTrue(self.actor.description == 'test actor description')
        self.assertTrue(self.actor.type == 'being')
        print t_name + " PASSED..."

    def test_area(self):
        t_name = self.case_name + '.test_area'
        print "\nStarting %s..." % t_name
        self.assertTrue(self.area.name == 'test area')
        self.assertTrue(self.area.description == 'test area description')
        self.assertTrue(self.area.type == 'place')
        print t_name + " PASSED..."


class TestDBFunctions(unittest.TestCase):

    def setUp(self):
        self.case_name = 'TestDBFunctions'
        self.db = 'test.db'
        f = open(self.db, 'w')
        f.close()

    def tearDown(self):
        try:
            subprocess.call(['del', self.db], shell=True)
        except:
            print traceback.format_exc()

    def test_create_table(self):
        t_name = self.case_name + '.test_create_table'
        print "\nStarting %s..." % t_name
        main.create_creature_table(self.db)
        if main.get_tables(self.db)[0][1] == 'creatures':
            pass
        else:
            print traceback.format_exc()
            raise Exception('Creatures table not created. Error.')
        print t_name + " PASSED..."

    def test_insert_creature(self):
        t_name = self.case_name + '.test_insert_creature'
        print "\nStarting %s..." % t_name
        main.create_creature_table(self.db)
        self.insert_statement = '''INSERT INTO creatures VALUES (
            '2006-01-05',
            'Test Creature Name 0',
            'This is a test',
            '{}',
            'being',
            0,
            'proof'
            );'''
        self.answers_tuple = (
            u'2006-01-05',
            u'Test Creature Name 0',
            u'This is a test', u'{}',
            u'being',
            0.0,
            u'proof'
        )
        main.db_commit(self.db, [self.insert_statement])
        self.query = main.db_query(self.db, ["SELECT * FROM creatures;"])[0]
        self.test_passed = True
        results_list = []
        check_name = 'tuple length '
        q_length = len(self.query)
        a_length = len(self.answers_tuple)
        if q_length == a_length:
            result = ' PASS: ' + repr(q_length) + ' == ' + repr(a_length)
            results_list.append(check_name + result)
        else:
            results_list.append(check_name + ': FAIL')
            self.test_passed = False
            raise Exception(
                'Tuple length test failed. ' +
                'Query does not return expected output.'
            )
        if self.test_passed:
            for i in xrange(len(self.answers_tuple)):
                check_name = 'value check ' + str(i)
                if self.answers_tuple[i] == self.query[i]:
                    result = (
                        ' PASS: ' +
                        repr(self.answers_tuple[i]) + 
                        ' == ' +
                        repr(self.query[i])
                    )
                    results_list.append(check_name + result)
                else:
                    results_list.append(check_name + ': FAIL')
                    self.test_passed = False
                    raise Exception(
                        'Expected value does not match actual value.' +
                        '\n' + check_name + ':\n' +
                        repr(self.answers_tuple[i]) + 
                        ' IS NOT EQUAL TO ' +
                        repr(self.query[i])
                    )
        for result in results_list:
            print result
        print t_name + " PASSED..."

class TestGUIWindows(unittest.TestCase):

    def setUp(self):
        print "WARNING: TestGUIWindows NOT YET IMPLEMENTED!"

    def tearDown(self):
        pass

    def test_foo(self):
        pass


if __name__ == '__main__':
    unittest.main()