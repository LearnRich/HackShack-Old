from HackShak import create_app, db, bcrypt, __STUDENT_ROLE, __ADMIN_ROLE, __TEACHER_ROLE

from HackShak.models import User, Student, Teacher, Admin, Role, RoleAssignment, Course, Rank, ClassList, Quest, QuestSubmission, SubmissionStatus

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

admin_user_role = Role(name=__ADMIN_ROLE)
db.session.add(admin_user_role)
db.session.commit()

teacher_user_role = Role(name=__TEACHER_ROLE)
db.session.add(teacher_user_role)
db.session.commit()

student_user_role = Role(name=__STUDENT_ROLE)
db.session.add(student_user_role)
db.session.commit()

su_user = Admin(
    username='learnrich',
    email='richardson_b@surreyschools.ca',
	firstname = 'Ben',
	lastname = 'Richardson',
    alias='superuser',
    password= bcrypt.generate_password_hash('id10t$pr00f')
)
db.session.add(su_user)

t_user = Teacher(
    username='richardson_b',
	firstname = 'Ben',
	lastname = 'Teacher',
    email='b.richardson.teach@gmail.com',
    password= bcrypt.generate_password_hash('It3ach&l3arn2')
)
db.session.add(t_user)

s_user = Student(
    username='RichStudent',
	firstname = 'Ben',
	lastname = 'Richardson',
    email='benrichar@gmail.com',
    grad_year = 2021,
    password= bcrypt.generate_password_hash('student')
)
db.session.add(s_user)
db.session.commit()


RoleAssignment.create(admin_user_role.name, su_user.id)
RoleAssignment.create(teacher_user_role.name, su_user.id)

RoleAssignment.create(teacher_user_role.name, t_user.id)

RoleAssignment.create(student_user_role.name, s_user.id)


course = Course(
    course_name='Teachers Testing Stuff',
    description= 'This course is for teachers, so that they can have access to all the quests to view them as a student would',
    grade_level = "13",
	block = "0",
	school_year = "2021",
	term = "AY",
	teacher_id = t_user.id
)
db.session.add(course)

coding_course = Course(
    course_name='Computer Programming 9',
    description= 'Crade 9 computer programming',
    grade_level = "9",
	block = "1",
	school_year = "2021",
	term = "S1",
	teacher_id = t_user.id
)
db.session.add(coding_course)
db.session.commit()
# create the test class 
ClassList.create(coding_course.id, s_user.id)

q1 = Quest(
    title="First Quest", 
    description='Test Quest description',
    xp=5,
    author_id=t_user.id
)
db.session.add(q1)
db.session.commit()

q2 = Quest(
    title="Message your teacher", 
    description='Using Teams, Email, Discord, Instagram, send message to your teacher!',
    xp=1,
    author_id=t_user.id
)
db.session.add(q2)
db.session.commit()

q3 = Quest(
    title="Class Contract", 
    description='Agree and you will ab able to use the tools in the lab',
    xp=2,
    author_id=t_user.id
)
db.session.add(q3)
db.session.commit()

qs1 = QuestSubmission(quest_id=q2.id, student_id=s_user.id, course_id=coding_course.id)
db.session.add(qs1)
db.session.commit()

qs1 = QuestSubmission(quest_id=q3.id, student_id=s_user.id, course_id=coding_course.id, status=SubmissionStatus.SUBMITTED)
db.session.add(qs1)
db.session.commit()

qs2 = QuestSubmission(quest_id=q1.id, student_id=s_user.id, course_id=coding_course.id, xp_awarded=200, status=SubmissionStatus.RETURNED)
db.session.add(qs2)
db.session.commit()


noob = Rank(
    name='Digital Noob',
    xp = 0, 
    symbol_html = '<i class="bi bi-circle">'
)
db.session.add(noob)

novice = Rank(
    name = 'Digital Novice',
    xp = 60, 
    symbol_html = '<i class="bi bi-chevron-up">'
)
db.session.add(novice)

novice_ii = Rank(
    name = 'Digital Novice II',
    xp = 125, 
    symbol_html = '<i class="bi bi-chevron-double-up">'
)
db.session.add(novice_ii)

amateur = Rank(
    name = 'Digital Amateur',
    xp = 185, 
    symbol_html = '<i class="bi bi-chevron-expand">'
) 
db.session.add(amateur)

amateur_ii = Rank(
    name = 'Digital Amateur II',
    xp = 250, 
    symbol_html = '<i class="bi bi-chevron-bar-expand">'
)
db.session.add(amateur_ii)

apprentice = Rank(
    name = 'Digital Apprentice',
    xp = 310, 
    symbol_html = '<i class="bi bi-star">'
)
db.session.add(apprentice)

apprentice_ii = Rank(
    name = 'Digital Apprentice II',
    xp = 375, 
    symbol_html = '<i class="bi bi-star-fill">'
)
db.session.add(apprentice_ii)

journeyman = Rank(
    name = 'Digital Journeyman',
    xp = 495, 
    symbol_html = '<i class="bi bi-journal">'
)
db.session.add(journeyman)

journeyman_ii = Rank(
    name = 'Digital Journeyman II',
    xp = 595, 
    symbol_html = '<i class="bi bi-journal-bookmark">'
)
db.session.add(journeyman_ii)

journeyman_iii = Rank(
    name = 'Digital Journeyman III',
    xp = 665, 
    symbol_html = '<i class="bi bi-journals">'
)
db.session.add(journeyman_iii)

crafter = Rank(
    name = 'Digital Crafter',
    xp = 725, 
    symbol_html = '<i class="bi bi-screwdriver">'
)
db.session.add(crafter)

crafter_expert = Rank(
    name = 'Expert Digital Crafter',
    xp = 855, 
    symbol_html = '<i class="bi bi-wrench">'
)
db.session.add(crafter_expert)

crafter_master = Rank(
    name = 'Master Digital Crafter',
    xp = 1000, 
    symbol_html = '<i class="bi bi-tools">'
)
db.session.add(crafter_master)
db.session.commit()

