import datetime

from django.db import models

from conductor.tests import TestCase


class TestMilestone(TestCase):

    def test_has_date(self):
        date = datetime.datetime.now()
        milestone = self.MilestoneFactory.build(date=date)
        self.assertEqual(date, milestone.date)


class TestSchool(TestCase):

    def test_has_name(self):
        school = self.SchoolFactory.build(name='University of Virginia')
        self.assertEqual('University of Virginia', school.name)

    def test_has_slug(self):
        school = self.SchoolFactory.build(slug='university-of-virginia')
        self.assertEqual('university-of-virginia', school.slug)

    def test_has_url(self):
        school = self.SchoolFactory.build(url='http://www.virginia.edu/')
        self.assertEqual('http://www.virginia.edu/', school.url)

    def test_has_milestones_url(self):
        school = self.SchoolFactory.build(
            milestones_url='http://admission.virginia.edu/events')
        self.assertEqual(
            'http://admission.virginia.edu/events', school.milestones_url)


class TestSemester(TestCase):

    def test_factory(self):
        semester = self.SemesterFactory.build()

        self.assertIsNotNone(semester.date)
        self.assertTrue(semester.active)

    def test_has_date(self):
        today = datetime.date.today()
        semester = self.SemesterFactory.build(date=today)

        self.assertEqual(today, semester.date)

    def test_has_active(self):
        active = False
        semester = self.SemesterFactory.build(active=active)

        self.assertFalse(semester.active)


class TestStudent(TestCase):

    def test_factory(self):
        student = self.StudentFactory.build()

        self.assertIsNotNone(student.user)
        self.assertNotEqual('', student.first_name)
        self.assertNotEqual('', student.last_name)
        self.assertIsNotNone(student.matriculation_semester)

    def test_has_user(self):
        user = self.UserFactory.build()
        student = self.StudentFactory.build(user=user)

        self.assertEqual(user, student.user)

    def test_has_first_name(self):
        student = self.StudentFactory.build(first_name='Matt')

        self.assertEqual('Matt', student.first_name)

    def test_has_last_name(self):
        student = self.StudentFactory.build(last_name='Layman')

        self.assertEqual('Layman', student.last_name)

    def test_has_matriculation_semester(self):
        semester = self.SemesterFactory.create()
        student = self.StudentFactory.build(matriculation_semester=semester)

        self.assertEqual(semester, student.matriculation_semester)

    def test_protect_student(self):
        semester = self.SemesterFactory.create()
        self.StudentFactory.create(matriculation_semester=semester)

        with self.assertRaises(models.ProtectedError):
            semester.delete()

    def test_has_schools(self):
        school = self.SchoolFactory.create()
        student = self.StudentFactory.create(schools=(school,))

        self.assertEqual([school], list(student.schools.all()))


class TestTargetSchool(TestCase):

    def test_factory(self):
        target_school = self.TargetSchoolFactory.build()

        self.assertIsNotNone(target_school.school)
        self.assertIsNotNone(target_school.student)

    def test_has_school(self):
        school = self.SchoolFactory.create()
        target_school = self.TargetSchoolFactory.build(school=school)

        self.assertEqual(school, target_school.school)

    def test_has_student(self):
        student = self.StudentFactory.create()
        target_school = self.TargetSchoolFactory.build(student=student)

        self.assertEqual(student, target_school.student)
