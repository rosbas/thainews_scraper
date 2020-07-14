import unittest

class TestStrings(unittest.TestCase):
    def setUp(self):
        # the first to be called in the testunit
        print("hi")

    # def tearDown(self):
    #     # will get called after setUP regardless of its successfullness
    #     print("hi again")

    def test_sth(self):
        self.assertEqual("hello".upper(),"HELLO")

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    print('test start')
    unittest.main(exit=False)
    print('test end')