#!/usr/bin/env python2.7
import main
import traceback
import unittest
import subprocess

class TestLogicObjects(unittest.TestCase):

    def setUp(self):
        self.case_name = 'TestLogicObjects'
        print "\nTestLogicObjects "
        self.actor = main.Actor('test actor','test actor description', {})
        self.area = main.Area('test area','test area description')
        self.race_dict = main.read_yaml('monsters.yaml')['race_dict']
        self.test_name = 'Testy'
        self.test_race = 'human'
        self.test_description = 'This is a test...'

    def tearDown(self):
        print "\nEND OF TestLogicObjects "


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

    def test_gen_stats(self):
        stats = main.generate_stats('elf', self.race_dict)
        self.assertTrue(stats['st'] > 0)
        self.assertTrue(stats['dx'] > 0)
        self.assertTrue(stats['cn'] > 0)
        self.assertTrue(stats['in'] > 0)
        self.assertTrue(stats['wi'] > 0)
        self.assertTrue(stats['ch'] > 0)

    def test_create_creature(self):
        critter = (
            main.create_creature(
                self.test_name,
                self.test_race,
                self.test_description,
                self.race_dict
                )
            )
        self.assertTrue(critter.name == self.test_name)
        self.assertTrue(critter.race == self.test_race)
        self.assertTrue(critter.description == self.test_description)
        self.assertTrue(critter.stats['st'] > 0)
        self.assertTrue(critter.stats['dx'] > 0)
        self.assertTrue(critter.stats['cn'] > 0)
        self.assertTrue(critter.stats['in'] > 0)
        self.assertTrue(critter.stats['wi'] > 0)
        self.assertTrue(critter.stats['ch'] > 0)

    def test_creature_levels(self):
        critter = (
            main.create_creature(
                self.test_name,
                self.test_race,
                self.test_description,
                self.race_dict
                )
            )
        for i in xrange(2000):
            gain_exp(critter, 25)
        print critter.level


# critter = Actor('Testguy','testy')
# print "Testguy created."
# critter2 = Actor('Testguy2','testy')
# print "Testguy2 created."
# stats = generate_stats('elf', race_dict)
# stats2 = generate_stats('dwarf', race_dict)
# print stats
# print stats2
# critter.stats = stats
# critter2.stats = stats2
# for i in xrange(2000):
#     combat_round(critter, critter2)
#     gain_exp(critter, 25)

# print critter.stats
# print critter2.stats

class TestDBFunctions(unittest.TestCase):

    def setUp(self):
        self.case_name = 'TestDBFunctions'
        print "\nTestDBFunctions "
        self.db = 'test.db'
        f = open(self.db, 'w')
        f.close()

    def tearDown(self):
        try: #TODO fix for mac
            subprocess.call(['del', self.db], shell=True)
        except:
            print traceback.format_exc()
        print "\nEND OF TestDBFunctions "

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
            0
            );'''
        self.answers_tuple = (
            u'2006-01-05',
            u'Test Creature Name 0',
            u'This is a test', u'{}',
            u'being',
            0.0
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