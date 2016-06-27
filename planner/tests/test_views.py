from conductor.tests import TestCase
from planner import views


class TestSchoolViewSet(TestCase):

    def test_no_create(self):
        """Sanity check that no create method is available."""
        viewset = views.SchoolViewSet()
        self.assertRaises(AttributeError, lambda: viewset.create)


class TestStudentViewSet(TestCase):

    def test_gets_students(self):
        student = self.StudentFactory.create()
        self.assertIn(student, views.StudentViewSet.queryset)

    def test_list(self):
        view = views.StudentViewSet.as_view(actions={'get': 'list'})
        request = self.request_factory.get()
        response = view(request)
        self.assertEqual(200, response.status_code)
