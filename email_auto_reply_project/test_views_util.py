import unittest
from views_util import extract_receiver_name, extract_sender_name

class TestExtractReceiverName(unittest.TestCase):
    
    def test_extract_receiver_name_hi(self):
        self.assertEqual(extract_receiver_name("Hi John,"), "John")

    def test_extract_receiver_name_hello(self):
        self.assertEqual(extract_receiver_name("Hello Lisa,"), "Lisa")

    def test_extract_receiver_name_dear(self):
        self.assertEqual(extract_receiver_name("Dear Smith,"), "Smith")

    def test_extract_receiver_name_hey(self):
        self.assertEqual(extract_receiver_name("Hey Alex,"), "Alex")

    def test_extract_receiver_name_no_greeting(self):
        self.assertIsNone(extract_receiver_name("No greeting here"))

    def test_extract_receiver_name_miss(self):
        self.assertEqual(extract_receiver_name("Miss Jane,"), "Jane")

    def test_extract_receiver_name_mrs(self):
        self.assertEqual(extract_receiver_name("Mrs. Robinson,"), "Robinson")

    def test_extract_receiver_name_dr(self):
        self.assertEqual(extract_receiver_name("Dr. Strange,"), "Strange")

    def test_extract_receiver_name_case_insensitive(self):
        self.assertEqual(extract_receiver_name("hi john,"), "john")
        self.assertEqual(extract_receiver_name("HELLO LISA,"), "LISA")


class TestExtractSenderName(unittest.TestCase):

    def test_extract_sender_name_regards(self):
        self.assertEqual(extract_sender_name("Regards, John"), "John")

    def test_extract_sender_name_best(self):
        self.assertEqual(extract_sender_name("Best, Alice"), "Alice")

    def test_extract_sender_name_thanks(self):
        self.assertEqual(extract_sender_name("Thanks, Max"), "Max")

    def test_extract_sender_name_yours(self):
        self.assertEqual(extract_sender_name("Yours, Emma"), "Emma")

    def test_extract_sender_name_no_closing(self):
        self.assertIsNone(extract_sender_name("No closing phrase here"))