from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from sandbox.settings import RATING_MODEL

Rating = RATING_MODEL

SECTORS = (
    ('Software Engineers', 'Software Engineers'),
    ('UI/UX Designers', 'UI/UX Designers'),
    ('Tech Sales Engineers', 'Tech Sales Engineers '),
    ('Data Scientists', 'Data Scientists'),
    ('Product Managers', 'Product Managers'),
    ('Digital Marketing', 'Digital Marketing'),
)

WORK_EXP = (
    ('Less than 1 Year', 'Less than 1 Year'),
    ('2-5 years', '2-5 years'),
    ('5-7 years', '5-7 years'),
    ('7-10 years', '7-10 years'),
    ('10 years and above', '10 years and above')
)
GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)
JOB_CATEGORIES = (
    ('full time', 'Full Time'),
    ('remote', 'Remote'),
    ('contractual', 'Contractual'),
    ('internship', 'Internship'),
    ('voluntering', 'Voluntering'),
    ('freelance', 'Freelance'),
    ('part-time', 'Part Time'),
    ('temporary', 'Temporary'),
    ('internship', 'Internship')
)

PROFESSION_LEVEL = (
    ('beginner', 'Beginner Level'),
    ('intermediate', 'Intermediate Level'),
    ('advanced', 'Advanced Level'),
)


class Talent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, related_name="views", blank=True)
    profession = models.CharField(max_length=100, null=True)
    profession_level = models.CharField(max_length=100, choices=PROFESSION_LEVEL, null=True)
    about = models.TextField(null=True)
    category = models.CharField(max_length=100, choices=SECTORS, null=True)
    years_of_experience = models.CharField(max_length=100, choices=WORK_EXP, null=True)
    dob = models.DateTimeField(default=datetime.now)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    languages = models.CharField(max_length=100, null=True)
    salary_expectation = models.CharField(max_length=100, null=True)
    prefered_work_type = models.CharField(max_length=100, choices=JOB_CATEGORIES, null=True)
    phone = models.CharField(max_length=13, null=True)
    location = models.CharField(max_length=100, null=True)
    linkedIn = models.URLField(null=True, blank=True)
    slug = models.SlugField(default=User, unique=True, null=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')
    qualified = models.BooleanField(default=False)
    show_badge = models.BooleanField(default=False)
    started_talent_quiz = models.ForeignKey('TalentQuiz', on_delete=models.SET_NULL, null=True,
                                            related_name='started_talent_quiz', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Talent, self).save(*args, **kwargs)

    @property
    def get_skills(self):
        skills = Skill.objects.filter(talent=self.user)
        return skills

    @property
    def get_experience(self):
        exp = Experience.objects.filter(talent=self.user)
        return exp

    @property
    def get_education(self):
        edu = Education.objects.filter(talent=self.user)
        return edu

    @property
    def get_award(self):
        awd = Award.objects.filter(talent=self.user)
        return awd

    @property
    def get_rating(self):
        rating = Rating.objects.filter(rating_for=self.id)

        sum_of_user_rates = sum(rating.values_list('rating_value', flat=True))  # --> rating for one user filtered above

        all_ratings_to_talent = rating.count() * 5  # --> getting number of all ratings for a filtered user
        try:
            rates = round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
        except ZeroDivisionError:
            rates = 0
        return rates

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        user = self.user
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        else:
            return user.username


class Experience(models.Model):
    WORKING = (
        ('No', 'No'),
        ('Yes', "Yes")
    )
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    finish_date = models.DateTimeField(null=True, blank=True)
    still_working = models.CharField(max_length=100, null=True, blank=True, choices=WORKING)
    position = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)


class Education(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(max_length=100)
    school_name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)

    class Meta:
        verbose_name_plural = 'Education'


class Award(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    awarded_on = models.DateTimeField(default=datetime.now)
    details = models.TextField()

    def __str__(self):
        return str(self.talent)


class Skill(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    experience = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.talent)


# Quizzes
class Quiz(models.Model):
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128, choices=SECTORS)
    level = models.CharField(max_length=12, choices=(
        ("beginner", "Beginner Level"), ("intermediate", "Intermediate Level"), ("advanced", "Advanced Level")))
    questions = models.ManyToManyField('QuizQuestion')
    time_duration = models.FloatField(null=True, help_text="Quiz Duration in Minutes")
    passing_average = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-id",)
        db_table = "quizzes"
        indexes = [
            models.Index(
                fields=["title", "level"]
            )
        ]


class QuizQuestion(models.Model):
    title = models.CharField(max_length=128)
    answers = models.ManyToManyField('QuizQuestionAnswer')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-id",)
        db_table = "quiz_questions"
        indexes = [
            models.Index(
                fields=["title", ]
            )
        ]


class QuizQuestionAnswer(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)
    correct = models.BooleanField()

    def __str__(self):
        return f"{self.title} -> {self.correct.__str__()}"

    class Meta:
        ordering = ("-id",)
        db_table = "quiz_question_answers"
        indexes = [
            models.Index(
                fields=["title", "correct"]
            )
        ]


class TalentQuiz(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.ManyToManyField('QuizQuestionAnswer')
    time_left = models.FloatField(null=True)
    timed_out = models.BooleanField(default=False)

    def get_time_left(self):
        time_left = str(self.time_left).split(".")
        return int(time_left[0]), int(time_left[1])

    @property
    def get_minutes_left(self):
        return self.get_time_left()[0]

    @property
    def get_seconds_left(self):
        return self.get_time_left()[1]

    @property
    def score(self):
        try:
            correct_answers = self.answers.filter(correct=True)
            percent = (correct_answers.count() / self.answers.count()) * 100
            return percent
        except ZeroDivisionError:
            return 0

    @property
    def passed(self):
        percent = self.score
        return True if percent >= self.quiz.passing_average else False

    class Meta:
        ordering = ("-id",)
        db_table = "talent_quizzes"
        indexes = [
            models.Index(
                fields=["quiz", "talent", ]
            )
        ]


class TalentQuizAnswer(models.Model):
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(QuizQuestionAnswer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Q: {self.question.__str__()}, A: {self.answer}"

    class Meta:
        ordering = ("-id",)
        db_table = "talent_quiz_answer"
        indexes = [
            models.Index(
                fields=["question", ]
            )
        ]
