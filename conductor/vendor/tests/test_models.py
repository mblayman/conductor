from conductor.tests import TestCase


class TestPromptSchool(TestCase):
    def test_factory(self) -> None:
        prompt_school = self.PromptSchoolFactory.create()

        self.assertNotEqual("", prompt_school.name)
        self.assertNotEqual("", prompt_school.slug)
        self.assertIsNone(prompt_school.school)

    def test_has_name(self) -> None:
        name = "University of Virginia"
        prompt_school = self.PromptSchoolFactory.create(name=name)

        self.assertEqual(name, prompt_school.name)

    def test_has_slug(self) -> None:
        slug = "university-of-virginia"
        prompt_school = self.PromptSchoolFactory.create(slug=slug)

        self.assertEqual(slug, prompt_school.slug)

    def test_has_school(self) -> None:
        school = self.SchoolFactory.create()
        prompt_school = self.PromptSchoolFactory.create(school=school)

        self.assertEqual(school, prompt_school.school)
