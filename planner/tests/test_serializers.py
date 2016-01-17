from planner import serializers
from lcp.tests import TestCase


class TestSchoolSerializer(TestCase):

    def test_serializes_id(self):
        school = self.SchoolFactory.create()
        serializer = serializers.SchoolSerializer(school)
        self.assertEqual(school.id, serializer.data['id'])

    def test_serializes_name(self):
        school = self.SchoolFactory.build(name='Johns Hopkins University')
        serializer = serializers.SchoolSerializer(school)
        self.assertEqual('Johns Hopkins University', serializer.data['name'])
