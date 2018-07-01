from conductor.tests import TestCase

from support.templatetags import support_tags


class TestStartswith(TestCase):

    def test_single_match(self):
        match = support_tags.startswith('University of Virginia', 'University')
        self.assertTrue(match)

    def test_single_no_match(self):
        match = support_tags.startswith('University of Virginia', 'The')
        self.assertFalse(match)

    def test_multiple_match(self):
        match = support_tags.startswith('College of Charleston', 'University,College')
        self.assertTrue(match)

    def test_multiple_no_match(self):
        match = support_tags.startswith('College of Charleston', 'The,A')
        self.assertFalse(match)
