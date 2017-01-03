from collections import OrderedDict

from rest_framework.test import force_authenticate

from conductor.tests import TestCase
from planner import views


class TestSchoolViewSet(TestCase):

    def test_no_create(self):
        """Sanity check that no create method is available."""
        viewset = views.SchoolViewSet()
        self.assertRaises(AttributeError, lambda: viewset.create)


class TestSemesterViewSet(TestCase):

    def test_no_create(self):
        """Sanity check that no create method is available."""
        viewset = views.SemesterViewSet()
        self.assertRaises(AttributeError, lambda: viewset.create)

    def test_active_only(self):
        semester = self.SemesterFactory.create()
        self.SemesterFactory.create(active=False)
        viewset = views.SemesterViewSet()
        self.assertEqual([semester], list(viewset.get_queryset()))


class TestStudentViewSet(TestCase):

    def _make_view(self):
        return views.StudentViewSet.as_view(
            actions={'get': 'list', 'post': 'create'})

    def test_gets_students(self):
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        self.StudentFactory.create()
        request = self.request_factory.authenticated_get(user)
        viewset = views.StudentViewSet()
        viewset.request = request
        self.assertEqual([student], list(viewset.queryset))

    def test_list(self):
        view = self._make_view()
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(user)
        response = view(request)
        self.assertEqual(200, response.status_code)

    def test_associates_user(self):
        semester = self.SemesterFactory.create()
        view = self._make_view()
        data = {
            'first_name': 'Matt',
            'last_name': 'Layman',
            'matriculation_semester': OrderedDict({
                'type': 'semesters', 'id': str(semester.id)}),
        }
        request = self.request_factory.post(data=data)
        user = self.UserFactory.create()
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(201, response.status_code)


class TestTargetSchoolViewSet(TestCase):

    def _make_view(self):
        return views.TargetSchoolViewSet.as_view(
            actions={'get': 'list', 'post': 'create'})

    def test_gets_target_schools(self):
        """For access control, a user can only get their students' schools."""
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        target_school = self.TargetSchoolFactory.create(student=student)
        self.TargetSchoolFactory.create()
        request = self.request_factory.authenticated_get(user)
        viewset = views.TargetSchoolViewSet()
        viewset.request = request
        self.assertEqual([target_school], list(viewset.queryset))

    def test_list(self):
        view = self._make_view()
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(user)
        response = view(request)
        self.assertEqual(200, response.status_code)
