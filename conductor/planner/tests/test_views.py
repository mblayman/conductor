from collections import OrderedDict
import json
from typing import Dict
from unittest import mock

from django.http import Http404
from django.urls import reverse

from conductor.planner import views
from conductor.planner.models import Milestone, SchoolApplication
from conductor.tests import TestCase


class TestSchoolDetail(TestCase):
    def test_unauthenticated(self) -> None:
        school = self.SchoolFactory.create()
        request = self.request_factory.get()

        response = views.school_detail(request, school.slug)

        self.assertEqual(200, response.status_code)

    def test_bad_school(self) -> None:
        request = self.request_factory.get()

        with self.assertRaises(Http404):
            views.school_detail(request, "bad-slug")

    @mock.patch("conductor.planner.views.render")
    def test_school_in_context(self, render: mock.MagicMock) -> None:
        school = self.SchoolFactory.create()
        request = self.request_factory.get()

        views.school_detail(request, school.slug)

        context = render.call_args[0][2]
        self.assertEqual(school, context["school"])

    @mock.patch("conductor.planner.views.render")
    def test_authenticated_teplate(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        school = self.SchoolFactory.create()
        request = self.request_factory.authenticated_get(user)

        views.school_detail(request, school.slug)

        template = render.call_args[0][1]
        self.assertEqual("planner/school.html", template)

    @mock.patch("conductor.planner.views.render")
    def test_unauthenticated_teplate(self, render: mock.MagicMock) -> None:
        school = self.SchoolFactory.create()
        request = self.request_factory.get()

        views.school_detail(request, school.slug)

        template = render.call_args[0][1]
        self.assertEqual("planner/school_unauthenticated.html", template)


class TestAddStudent(TestCase):
    def test_requires_login(self) -> None:
        request = self.request_factory.get()

        response = views.add_student(request)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_get(self) -> None:
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        response = views.add_student(request)

        self.assertEqual(200, response.status_code)

    @mock.patch("conductor.planner.views.render")
    def test_has_form(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        views.add_student(request)

        context = render.call_args[0][2]
        self.assertIn("form", context)

    @mock.patch("conductor.planner.views.render")
    def test_app_nav(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.build()
        request = self.request_factory.authenticated_get(user)

        views.add_student(request)

        context = render.call_args[0][2]
        self.assertEqual("add-student", context["app_nav"])

    def test_success(self) -> None:
        semester = self.SemesterFactory.create()
        data = {
            "first_name": "Joe",
            "last_name": "Student",
            "matriculation_semester": str(semester.id),
        }
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_post(user, data=data)

        response = views.add_student(request)

        self.assertEqual(1, user.students.count())
        student = user.students.first()
        self.assertIn(
            reverse("student-profile", args=[student.id]), response.get("Location")
        )

    @mock.patch("conductor.planner.views.render")
    def test_failure(self, render: mock.MagicMock) -> None:
        data: Dict[str, str] = {}
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_post(user, data=data)

        views.add_student(request)

        context = render.call_args[0][2]
        self.assertFalse(context["form"].is_valid())


class TestStudentProfile(TestCase):
    def test_requires_login(self) -> None:
        request = self.request_factory.get()

        response = views.student_profile(request, 1)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_valid(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        response = views.student_profile(request, student.id)

        self.assertEqual(200, response.status_code)

    def test_unauthorized_user(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory()
        request = self.request_factory.authenticated_get(user)

        with self.assertRaises(Http404):
            views.student_profile(request, student.id)

    @mock.patch("conductor.planner.views.render")
    def test_context(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        target_school = self.TargetSchoolFactory.create(student=student)
        milestone = self.MilestoneFactory.create(school=target_school.school)
        target_school.milestones.add(milestone)
        request = self.request_factory.authenticated_get(user)

        views.student_profile(request, student.id)

        context = render.call_args[0][2]
        self.assertEqual(Milestone, context["Milestone"])
        self.assertEqual(student, context["student"])
        self.assertEqual([target_school.school], list(context["schools"]))
        self.assertEqual([milestone], list(context["target_milestones"]))

    @mock.patch("conductor.planner.views.render")
    def test_schools_by_application_type(self, render: mock.MagicMock) -> None:
        """Order the schools by what application types are available.

        * The application type with the most schools will be ordered first.
        * The school will only be selected for one app type.
        * The student may also have no selected app type yet.
        """
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        school_1 = self.SchoolFactory.create(name="A University")
        school_application_1 = self.SchoolApplicationFactory.create(
            school=school_1, application_type=SchoolApplication.SCHOOL_BASED_APPLICATION
        )
        self.TargetSchoolFactory.create(
            student=student, school_application=school_application_1, school=school_1
        )
        self.SchoolApplicationFactory.create(
            school=school_1, application_type=SchoolApplication.COMMON_APP
        )
        school_2 = self.SchoolFactory.create(name="B University")
        school_application_2 = self.SchoolApplicationFactory.create(
            school=school_2, application_type=SchoolApplication.SCHOOL_BASED_APPLICATION
        )
        self.TargetSchoolFactory.create(
            student=student, school_application=school_application_2, school=school_2
        )
        school_3 = self.SchoolFactory.create(name="B University")
        self.SchoolApplicationFactory.create(
            school=school_3, application_type=SchoolApplication.COALITION_APPLICATION
        )
        self.TargetSchoolFactory.create(student=student, school=school_3)
        request = self.request_factory.authenticated_get(user)

        views.student_profile(request, student.id)

        context = render.call_args[0][2]
        expected_data = OrderedDict()
        expected_data["School Based Application"] = [
            {"school": school_1, "no_app_selected": False, "selected": True},
            {"school": school_2, "no_app_selected": False, "selected": True},
        ]
        expected_data["Common App"] = [
            {"school": school_1, "no_app_selected": False, "selected": False}
        ]
        expected_data["Coalition Application"] = [
            {"school": school_3, "no_app_selected": True, "selected": False}
        ]
        expected_data["Universal College Application"] = []
        self.assertEqual(expected_data, context["schools_by_application_type"])


class TestAddSchool(TestCase):
    def test_requires_login(self) -> None:
        request = self.request_factory.get()

        response = views.add_school(request, 1)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_valid_get(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        response = views.add_school(request, student.id)

        self.assertEqual(200, response.status_code)

    def test_valid_post(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        school = self.SchoolFactory.create()
        data = {"school": str(school.id)}
        request = self.request_factory.authenticated_post(user, data=data)

        response = views.add_school(request, student.id)

        self.assertEqual(302, response.status_code)
        self.assertIn(
            reverse("student-profile", args=[student.id]), response.get("Location")
        )

    def test_unauthorized_user(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory()
        request = self.request_factory.authenticated_get(user)

        with self.assertRaises(Http404):
            views.add_school(request, student.id)

    @mock.patch("conductor.planner.views.render")
    def test_student_in_context(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        views.add_school(request, student.id)

        context = render.call_args[0][2]
        self.assertEqual(student, context["student"])

    @mock.patch("conductor.planner.views.render")
    def test_query_in_context(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        data = {"q": "University of Virginia"}
        request = self.request_factory.authenticated_get(user, data=data)

        views.add_school(request, student.id)

        context = render.call_args[0][2]
        self.assertEqual("University of Virginia", context["q"])

    @mock.patch("conductor.planner.views.render")
    def test_form_in_context(self, render: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        views.add_school(request, student.id)

        context = render.call_args[0][2]
        self.assertIn("form", context)


class TestExportSchedule(TestCase):
    def test_requires_login(self) -> None:
        request = self.request_factory.get()

        response = views.export_schedule(request, 1)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_unauthorized_user(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory()
        request = self.request_factory.authenticated_get(user)

        with self.assertRaises(Http404):
            views.export_schedule(request, student.id)

    @mock.patch("conductor.planner.views.messages")
    def test_no_google_auth(self, messages: mock.MagicMock) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        response = views.export_schedule(request, student.id)

        messages.add_message.assert_called_once_with(request, messages.INFO, mock.ANY)
        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("settings"), response.get("Location"))

    @mock.patch("conductor.planner.views.messages")
    @mock.patch("conductor.planner.views.build_schedule")
    def test_trigger_task(
        self, build_schedule: mock.MagicMock, messages: mock.MagicMock
    ) -> None:
        user = self.UserFactory.create()
        self.GoogleDriveAuthFactory.create(user=user)
        student = self.StudentFactory(user=user)
        request = self.request_factory.authenticated_get(user)

        response = views.export_schedule(request, student.id)

        build_schedule.delay.assert_called_once_with(student.id)
        messages.add_message.assert_called_once_with(
            request, messages.SUCCESS, mock.ANY
        )
        self.assertEqual(302, response.status_code)
        self.assertIn(
            reverse("student-profile", args=[student.id]), response.get("Location")
        )


class TestSetStudentMilestone(TestCase):
    def test_requires_login(self) -> None:
        request = self.request_factory.post()

        response = views.set_student_milestone(request, 1)

        self.assertEqual(302, response.status_code)
        self.assertIn(reverse("login"), response.get("Location"))

    def test_requires_post(self) -> None:
        user = self.UserFactory.create()
        request = self.request_factory.authenticated_get(user)

        response = views.set_student_milestone(request, 1)

        self.assertEqual(405, response.status_code)

    def test_unauthorized_user(self) -> None:
        user = self.UserFactory.create()
        student = self.StudentFactory()
        request = self.request_factory.authenticated_post(user)

        with self.assertRaises(Http404):
            views.set_student_milestone(request, student.id)

    def test_no_milestone(self) -> None:
        student = self.StudentFactory()
        data = {"milestone": 1}
        request = self.request_factory.authenticated_post(student.user)
        request._body = json.dumps(data)

        with self.assertRaises(Http404):
            views.set_student_milestone(request, student.id)

    def test_no_target_school_for_student(self) -> None:
        student = self.StudentFactory()
        milestone = self.MilestoneFactory.create()
        self.TargetSchoolFactory(school=milestone.school)
        data = {"milestone": milestone.id}
        request = self.request_factory.authenticated_post(student.user)
        request._body = json.dumps(data)

        with self.assertRaises(Http404):
            views.set_student_milestone(request, student.id)

    def test_add_milestone(self) -> None:
        """A milestone is added to a target school if it's not there."""
        student = self.StudentFactory()
        milestone = self.MilestoneFactory.create()
        target_school = self.TargetSchoolFactory.create(
            student=student, school=milestone.school
        )
        data = {"milestone": milestone.id}
        request = self.request_factory.authenticated_post(student.user)
        request._body = json.dumps(data)

        response = views.set_student_milestone(request, student.id)

        self.assertEqual(200, response.status_code)
        self.assertTrue(target_school.milestones.filter(id=milestone.id).exists())
        data = json.loads(response.content)
        self.assertEqual("add", data["action"])

    def test_remove_milestone(self) -> None:
        """A milestone is removed from a target school if it is there."""
        student = self.StudentFactory()
        milestone = self.MilestoneFactory.create()
        target_school = self.TargetSchoolFactory.create(
            student=student, school=milestone.school
        )
        target_school.milestones.add(milestone)
        data = {"milestone": milestone.id}
        request = self.request_factory.authenticated_post(student.user)
        request._body = json.dumps(data)

        response = views.set_student_milestone(request, student.id)

        self.assertEqual(200, response.status_code)
        self.assertFalse(target_school.milestones.filter(id=milestone.id).exists())
        data = json.loads(response.content)
        self.assertEqual("remove", data["action"])
