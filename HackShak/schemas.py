from HackShak import ma
from HackShak.models import Quest, Campaign, QuestMap

class QuestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Quest
        load_instance = True  # Optional: deserialize to model instances

    id = ma.auto_field()
    title = ma.auto_field()
    xp = ma.auto_field()

class CampaignSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Campaign
        load_instance = True  # Optional: deserialize to model instances

    id = ma.auto_field()
    title = ma.auto_field()

class QuestMapSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuestMap
        load_instance = True  # Optional: deserialize to model instances

    id = ma.auto_field()
    title = ma.auto_field()

