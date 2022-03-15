from ..HackShak import create_app, db, bcrypt, __STUDENT_ROLE, __ADMIN_ROLE, __TEACHER_ROLE

from ..HackShak.models import User, Student, Teacher, Admin, Role, RoleAssignment, Course, Campaign, Rank, Quest, QuestSubmission, SubmissionStatus, Activity

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
    code='TTSIT13--Y-00',
    title='Teachers Testing Stuff',
    description= 'This course is for teachers, so that they can have access to all the quests to view them as a student would',
    grade = "13",
	block = "0",
	term = "Sem 0 2021",
)

db.session.add(course)
db.session.commit()


coding_course = Course(
    code='MADIT09--Y-01',
    title='Computer Programming 9',
    description= 'Grade 9 computer programming',
    grade = '9',
	block = "1",
	term = "Sem 1 2021",
)
db.session.add(coding_course)
db.session.commit()

course.teachers.append(t_user)
coding_course.teachers.append(t_user)

# create the test class 
coding_course.students.append(s_user)
db.session.commit()

# Get the LearnRich Teacher for reference to author quests.
learnrich = Teacher.query.filter_by(username='richardson_b').first()

# Create Ranks
db.session.add(Rank(name='Digital Noob',xp=0, symbol_html='<i class="bi bi-circle">'))
db.session.add(Rank(name='Digital Novice',xp=60, symbol_html='<i class="bi bi-chevron-up">'))
db.session.add(Rank(name='Digital Novice II',xp=125, symbol_html='<i class="bi bi-chevron-double-up">'))
db.session.add(Rank(name='Digital Amateur',xp=185, symbol_html='<i class="bi bi-chevron-expand">')) 
db.session.add(Rank(name='Digital Amateur II',xp=250, symbol_html='<i class="bi bi-chevron-bar-expand">')) 
db.session.add(Rank(name='Digital Apprentice',xp=310, symbol_html='<i class="bi bi-star">'))
db.session.add(Rank(name='Digital Apprentice II',xp=375, symbol_html='<i class="bi bi-star-fill">'))
db.session.add(Rank(name='Digital Journeyman',xp=495, symbol_html='<i class="bi bi-journal">'))
db.session.add(Rank(name='Digital Journeyman II',xp=595, symbol_html='<i class="bi bi-journal-bookmark">'))
db.session.add(Rank(name='Digital Journeyman III',xp=665, symbol_html='<i class="bi bi-journals">'))
db.session.add(Rank(name='Digital Crafter',xp=725, symbol_html='<i class="bi bi-screwdriver">'))
db.session.add(Rank(name='Expert Digital Crafter',xp=855, symbol_html='<i class="bi bi-wrench">'))
db.session.add(Rank(name='Master Digital Crafter',xp=1000, symbol_html='<i class="bi bi-tools">'))


# Create Campaigns 
db.session.add(Campaign(title="Orientation", description=""))
db.session.add(Campaign(title="Introductions", description=""))
db.session.add(Campaign(title="Python Basics I", description=""))
db.session.add(Campaign(title="Python Interactive I", description=""))
db.session.add(Campaign(title="Python Practice I", description=""))
db.session.add(Campaign(title="Python Challenges", description=""))
db.session.add(Campaign(title="Godot Basics", description=""))
db.session.add(Campaign(title="Godot 2D Platformer", description=""))
db.session.add(Campaign(title="The History of Video Games", description=""))
db.session.add(Campaign(title="HTML Basics", description=""))
db.session.add(Campaign(title="HTML Interactive", description=""))
db.session.add(Campaign(title="HTML Theory", description=""))
db.session.add(Campaign(title="HTML5 Basics", description=""))
db.session.add(Campaign(title="CSS Theory", description=""))
db.session.add(Campaign(title="CSS Interactive", description=""))
db.session.add(Campaign(title="CSS Mockups", description=""))
db.session.add(Campaign(title="Digital Amateur II", description=""))
db.session.add(Campaign(title="Media Literacy", description=""))
db.session.add(Campaign(title="Digital Apprentice II", description=""))
db.session.add(Campaign(title="How the Internet Works", description=""))
db.session.add(Campaign(title="Fact Checker School", description=""))
db.session.add(Campaign(title="Digital Novice II", description=""))
db.session.add(Campaign(title="Pixel Art Basics", description=""))
db.session.add(Campaign(title="How Computers Work", description=""))
db.session.add(Campaign(title="How AI Works", description=""))

# Create Quests
# title, description, xp, expiry, repeatable, details, submission_instructions
db.session.add(Quest(title="Welcome to the HackShack Online", 
    description="What the heck is the HackShack Online? Let me take you on a tour!", 
    xp=3,
    expiry="None",
    repeatable="No",
    details='''
A hackerspace (also referred to as a hacklab, makerspace, or hackspace) is a community-operated workspace where people with common interests, often in computers, technology, science, digital art or electronic art, can meet, socialize and/or collaborate… Many hackerspaces, including this one, participate in the use and development of free software, open hardware, and alternative media.
<h3>HackShack - Online Video Tour</h3>
Put on your headphones and Mr. Richardson will give you a tour of this place!
--Insert Video--
I watched the tour, now what?
Once you have read through the details of a quest, and followed any instructions it gives you, head down to the Submission Instructions which will explain what you need to do to complete the quest.''',
    submission_instructions ='''
Each quest will have different submission criteria. For this quest, your task was to watch the Video Tour. 
Often you will be required to attach a document or answer some questions in the Quest Submission Form below, as evidence for your learning. For this quest, however, you just have to hit the "Submit Quest for Completion" button below.  After hitting the button:
<ul>
<li>You will get a confirmation that your quest was successfully submitted,</li>
<li>This quest will move from your "In Progress" tab to your "Completed" tab,</li>
<li>You will be granted a badge for completing your first quest,</li>
<li>Your XP score will increase by 4 (3 for this quest and 1 for your first badge), and</li>
<li>Any quests that require this one as a prerequisite will become available to you!</li>
</ul>
    ''',
    author_id = learnrich.id))
db.session.add(Quest(title="How XP Works",
    description="PlaceHolderText", 
    xp=2,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="A Short Questionnaire", 
    description="", 
    xp=3,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="Who owns your creation", 
    description="", 
    xp=3,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="How to Sulli Computer", 
    description="", 
    xp=5,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="HackShack Class Contract", 
    description="", 
    xp=2,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="Create an Avatar", 
    description="Create a small digital image of yourself to represent you on the Hackerspace website. You'll also practice embedding an image into a quest submission.", 
    xp=5,
    expiry="None",
    repeatable="No",
details='''
<blockquote>In Hinduism, an avatar is a deliberate descent of a deity to Earth, or a descent of the Supreme Being (e.g., Vishnu for Vaishnavites), and is mostly translated into English as "incarnation", but more accurately as "appearance" or "manifestation" - Wikipedia</blockquote>
<blockquote>In computing, an avatar is the graphical representation of the user or the user's alter ego or character. It may take either a three-dimensional form, as in games or virtual worlds, or a two-dimensional form as an icon in Internet forums and other online communities. - Wikipedia</blockquote>
<h3>Create your Avatar</h3>
<p>This avatar should physically resemble you, such that you can be recognized by your avatar!  Avatars that don't look like you (according to my arbitrary judgment) may be rejected.
Choose one of these online avatar creators and create your HackShack online manifestation!
<ul>
<li><a href="http://www.avatarsinpixels.com/minipix/">http://www.avatarsinpixels.com/minipix/</a></li>
<li><a href="https://avatarmaker.com/">https://avatarmaker.com/</a></li>
<li><a href="https://getavataaars.com/">https://avatarmaker.com/</a></li>
<li>Any other avatar creator you can find, or paint a self-portrait!</li>
</ul>
</p>
<h3>Download your Avatar</h3>
<p>When your avatar is complete, download a PNG version of your avatar.  Make sure you remember where you download the image to, if you don't use the default Downloads folder!</p>
<h3>Upload your Avatar to your Profile</h3>
<p>Set the avatar as your HackShack profile picture:
<ul>
<li>Click on your username at the top right of the browser to visit your Profile page.</li>
<li>To edit your profile, click the button at the top beside your name that looks like a cog: </li>
<li>Scroll down to where it says “Avatar” and click the "Browse..." button.</li>
<li>Locate your avatar image where you saved it, click on it to highlight it, and click “Open”</li>
<li>Scroll up to the top of your Profile page and click “Update.”</li>
</ul>
Your avatar should now appear next to your name at the top of your Profile.</p>
    ''',
    submission_instructions ='''
To complete this quest you need to show two things:

<ol>
<li>Your profile image on the Hackerspace should now show an avatar that looks like you. Remember that avatars that don't look like you (according to my arbitrary judgement) may be rejected!</li>
<li>You also need to embed the downloaded avatar image into your submission:
<ul>
<li>In the Quest Submission Form below, click the button in the toolbar that looks like a picture </li>
<li>Click "Browse..." or "Choose Files" and find your avatar file. Once you've selected the file, click "Open" </li>
<li>The image should now appear in your submission form!</li>
</ul>
</li>
</ol>
    ''',
    author_id = learnrich.id))
db.session.add(Quest(title="How to Screenshot", 
    description="", 
    xp=2,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.commit()