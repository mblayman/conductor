from conductor.tests import TestCase
from planner.forms import AddStudentForm


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
