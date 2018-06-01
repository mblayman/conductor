from collections import OrderedDict

import mock
from rest_framework.test import force_authenticate

from conductor.tests import TestCase
from planner import views


class TestApplicationStatusViewSet(TestCase):

    def _make_view(self):
        return views.ApplicationStatusViewSet.as_view(
            actions={'get': 'list', 'post': 'create'})

    def test_create(self):
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        view = self._make_view()
        data = {
            'student': OrderedDict({
                'type': 'students', 'id': str(student.id)}),
        }
        request = self.request_factory.post(data=data, format='json')
        force_authenticate(request, user)

        response = view(request)

        self.assertEqual(201, response.status_code)

    def test_create_different_student(self):
        """A user may only create an application status for their student."""
        user = self.UserFactory.create()
        student = self.StudentFactory.create()
        view = self._make_view()
        data = {
            'student': OrderedDict({
                'type': 'students', 'id': str(student.id)}),
        }
        request = self.request_factory.post(data=data, format='json')
        force_authenticate(request, user)

        response = view(request)

        self.assertEqual(422, response.status_code)


class TestMilestoneViewSet(TestCase):

    def test_no_create(self):
        """Sanity check that no create method is available."""
        viewset = views.MilestoneViewSet()
        self.assertRaises(AttributeError, lambda: viewset.create)

    def test_active_only(self):
        milestone = self.MilestoneFactory.create()
        self.MilestoneFactory.create(active=False)
        viewset = views.MilestoneViewSet()
        self.assertEqual([milestone], list(viewset.get_queryset()))


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
        request = self.request_factory.post(data=data, format='json')
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

    def test_validates_unique_school_student(self):
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        target_school = self.TargetSchoolFactory.create(student=student)
        view = self._make_view()
        data = {
            'school': OrderedDict({
                'type': 'schools', 'id': str(target_school.school.id)}),
            'student': OrderedDict({
                'type': 'students', 'id': str(target_school.student.id)}),
        }
        request = self.request_factory.post(data=data, format='json')
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(422, response.status_code)

    @mock.patch('planner.views.tasks')
    def test_triggers_school_audit(self, tasks):
        user = self.UserFactory.create()
        student = self.StudentFactory.create(user=user)
        school = self.SchoolFactory.create()
        view = self._make_view()
        data = {
            'school': OrderedDict({
                'type': 'schools', 'id': str(school.id)}),
            'student': OrderedDict({
                'type': 'students', 'id': str(student.id)}),
        }
        request = self.request_factory.post(data=data, format='json')
        force_authenticate(request, user)
        response = view(request)
        self.assertEqual(201, response.status_code)
        tasks.audit_school.delay.assert_called_once_with(school.id)


class TestAddStudent(TestCase):

    def test_get(self):
        request = self.request_factory.get()

        response = views.add_student(request)

        self.assertEqual(200, response.status_code)

    @mock.patch('planner.views.render')
    def test_has_form(self, render):
        request = self.request_factory.get()

        views.add_student(request)

        context = render.call_args[0][2]
        self.assertIn('form', context)
