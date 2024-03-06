from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='Edad', min=18, max=100)
    gender = models.StringField(
        choices=[['H', 'Hombre'], ['F','Mujer']],
        label='Sexo',
        widget=widgets.RadioSelect,
    )
    
    residencia = models.StringField(
        choices=[['lima', 'Lima'], ['provincia', 'Provincia']],
        label='¿En dónde vives?'
    )
    
    ocup = models.StringField(
        choices=[['estu', 'estudiante'], ['egre', 'egresado']],
        label='Ocupación',
        widget=widgets.RadioSelect,
    )
    labor = models.StringField(
        choices=[['T', 'Trabajo'], ['NT', 'No Trabajo']],
        label='¿Estás trabajando?',
        #widget=widgets.RadioSelect,
    )
    universidad = models.StringField(
        choices=[['up', 'UP'], ['udep', 'UDEP'], ['pucp','PUCP'],['san marcos', 'UNMSM'], ['upc', 'UPC'], ['lima','U de Lima'],
                 ['untrm', 'UNTRM'], ['esan', 'ESAN'], ['unprg','UNPRG']],
        #label='¿Cuál es tu ocupación?',
        #widget=widgets.RadioSelect,
    )


    
# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender','residencia','labor','ocup']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['universidad']

class Agradecimientos(Page):
    pass


page_sequence = [Demographics, CognitiveReflectionTest, Agradecimientos]
