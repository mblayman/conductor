from conductor.tests import TestCase
from planner.forms import AddSchoolForm, AddStudentForm


class TestAddSchoolForm(TestCase):

    def test_valid(self):
        school = self.SchoolFactory.create()
        student = self.StudentFactory.create()
        data = {
            'school': str(school.id),
        }
        form = AddSchoolForm(student, data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(school, form.cleaned_data['school'])

    def test_school_in_student_list(self):
        school = self.SchoolFactory.create()
        student = self.StudentFactory.create()
        self.TargetSchoolFactory.create(school=school, student=student)
        data = {
            'school': str(school.id),
        }
        form = AddSchoolForm(student, data=data)

        self.assertFalse(form.is_valid())
        self.assertIn('school', form.errors)

    def test_save(self):
        school = self.SchoolFactory.create()
        student = self.StudentFactory.create()
        data = {
            'school': str(school.id),
        }
        form = AddSchoolForm(student, data=data)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual([school], list(student.schools.all()))


class TestAddStudentForm(TestCase):

    def test_save(self):
        semester = self.SemesterFactory.create()
        data = {
            'first_name': 'Joe',
            'last_name': 'Student',
            'matriculation_semester': str(semester.id),
        }
        user = self.UserFactory.create()
        form = AddStudentForm(data=data)
        self.assertTrue(form.is_valid())

        form.save(user)

        student = user.students.first()
        self.assertEqual('Joe', student.first_name)
        self.assertEqual('Student', student.last_name)
        self.assertEqual(semester, student.matriculation_semester)
