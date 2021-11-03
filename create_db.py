from HackShak import create_app, db, bcrypt, __STUDENT_ROLE, __ADMIN_ROLE, __TEACHER_ROLE

from HackShak.models import User, Role, RoleAssignment, Announcement

app = create_app()
app.app_context().push()

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

su_user = User(
    username='learnrich',
    email='richardson_b@surreyschools.ca',
	firstname = 'Ben',
	lastname = 'Richardson',
    password= bcrypt.generate_password_hash('id10t$pr00f')
)
db.session.add(su_user)

t_user = User(
    username='hemrick_w',
	firstname = 'Will',
	lastname = 'Nilson',
    email='hemrick_w@surreyschools.ca',
    password= bcrypt.generate_password_hash('It3ach&l3arn2')
)
db.session.add(t_user)

s_user = User(
    username='RichStudent',
	firstname = 'Ben',
	lastname = 'Richardson',
    email='b.richardson.teach@gmail.com',
    password= bcrypt.generate_password_hash('student')
)
db.session.add(s_user)
db.session.commit()


RoleAssignment.create(admin_user_role.name, su_user.id)
RoleAssignment.create(teacher_user_role.name, su_user.id)

RoleAssignment.create(teacher_user_role.name, t_user.id)

RoleAssignment.create(student_user_role.name, s_user.id)

