from HackShak import create_app, db, bcrypt, __STUDENT_ROLE, __ADMIN_ROLE, __TEACHER_ROLE
from HackShak.HackShak.models import Campaign

from HackShak.models import User, Student, Teacher, Admin, Role, RoleAssignment, Course, Rank, Quest, QuestSubmission, SubmissionStatus, Activity
app = create_app()
app.app_context().push()

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
db.session.commit()

# Create Campaigns 
db.session.add(Campaign(name="Orientation", description=""))
db.session.add(Campaign(name="Introductions", description=""))
db.session.add(Campaign(name="Python Basics I", description=""))
db.session.add(Campaign(name="Python Interactive I", description=""))
db.session.add(Campaign(name="Python Practice I", description=""))
db.session.add(Campaign(name="Python Challenges", description=""))
db.session.add(Campaign(name="Godot Basics", description=""))
db.session.add(Campaign(name="Godot 2D Platformer", description=""))
db.session.add(Campaign(name="The History of Video Games", description=""))
db.session.add(Campaign(name="HTML Basics", description=""))
db.session.add(Campaign(name="HTML Interactive", description=""))
db.session.add(Campaign(name="HTML Theory", description=""))
db.session.add(Campaign(name="HTML5 Basics", description=""))
db.session.add(Campaign(name="CSS Theory", description=""))
db.session.add(Campaign(name="CSS Interactive", description=""))
db.session.add(Campaign(name="CSS Mockups", description=""))
db.session.add(Campaign(name="Digital Amateur II", description=""))
db.session.add(Campaign(name="Media Literacy", description=""))
db.session.add(Campaign(name="Digital Apprentice II", description=""))
db.session.add(Campaign(name="How the Internet Works", description=""))
db.session.add(Campaign(name="Fact Checker School", description=""))
db.session.add(Campaign(name="Digital Novice II", description=""))
db.session.add(Campaign(name="Pixel Art Basics", description=""))
db.session.add(Campaign(name="How Computers Work", description=""))
db.session.add(Campaign(name="How AI Works", description=""))

# Create Quests
# title, description, xp, expiry, repeatable, details, submission_instructions
db.session.add(Quest(title="Welcome to the HackShack Online", 
    description="PlaceHolderText", 
    xp=3,
    expiry="None",
    repeatable="No",
    details="PlaceHolderText",
    submission_instructions ="PlaceHolderText",
    author_id = learnrich.id))
db.session.add(Quest(title="How XP Works",
    description="PlaceHolderText", 
    xp=2,
    eexpiry="None",
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
In Hinduism, an avatar is a deliberate descent of a deity to Earth, or a descent of the Supreme Being (e.g., Vishnu for Vaishnavites), and is mostly translated into English as "incarnation", but more accurately as "appearance" or "manifestation" - Wikipedia
In computing, an avatar is the graphical representation of the user or the user's alter ego or character. It may take either a three-dimensional form, as in games or virtual worlds, or a two-dimensional form as an icon in Internet forums and other online communities. - Wikipedia
Create your Avatar
This avatar should physically resemble you, such that you can be recognized by your avatar!  Avatars that don't look like you (according to my arbitrary judgment) may be rejected.

Choose one of these online avatar creators and create your Hackerspace online manifestation!

<a href="http://www.avatarsinpixels.com/minipix/">http://www.avatarsinpixels.com/minipix/</a>
<a href="https://avatarmaker.com/">https://avatarmaker.com/</a>
<a href="https://getavataaars.com/">https://avatarmaker.com/</a>
Any other avatar creator you can find, or paint a self-portrait!

Download your Avatar
When your avatar is complete, download a PNG version of your avatar.  Make sure you remember where you download the image to, if you don't use the default Downloads folder!

Upload your Avatar to your Profile
Set the avatar as your HackShack profile picture:
Click on your username at the top right of the browser to visit your Profile page.
To edit your profile, click the button at the top beside your name that looks like a cog: 
Scroll down to where it says “Avatar” and click the "Browse..." button.
Locate your avatar image where you saved it, click on it to highlight it, and click “Open”
Scroll up to the top of your Profile page and click “Update.”
Your avatar should now appear next to your name at the top of your Profile.    
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

