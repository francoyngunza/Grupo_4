import random
from otree.api import *
import re




doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    # Initial amount allocated to each player
    ENDOWMENT = cu(50)
    MULTIPLIER = 3
    FM_ROLE = 'First mover'
    SM_ROLE = 'Second mover'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,default=cu(0),
        doc="""Amount sent by P1""",
        label="Por favor, ingrese un monto del 0 al 50:",
    )
    sent_back_amount = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(0), label="Ingrese el monto que desea devolver:")
    
    @classmethod
    def validate_integer(cls, value):
        if not re.match(r'^\d+$', str(value)):
            raise ValueError("Please enter a valid integer.")

    def units_error_message(self, value):
        try:
            self.validate_integer(value)
        except ValueError as e:
            return str(e)

class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.sent_amount * C.MULTIPLIER



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount


# Funciones avanzadas> lista desplegable
def sent_amount_choices(group):
    montos = range(0,int(C.ENDOWMENT)+1,5)
    lista = list(montos)
    choices = lista
    return(choices)

# PAGES
class welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Send(Page):
    
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    title_text = "Por favor, espere"
    body_text = "Esperando a que los otros participantes tomen una decisión"
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    title_text = "Por favor, espere"
    body_text = "Esperando a que los otros participantes tomen una decisión"
    after_all_players_arrive = set_payoffs
    


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        
        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)


class FinalResults(Page):
    """This page shows the final payoff for each player"""
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        round_payoffs = [player.in_round(r).payoff for r in range(1, C.NUM_ROUNDS + 1)]
        # Seleccionar aleatoriamente un pago entre los obtenidos en las tres rondas
        final_payoff = random.choice(round_payoffs)
        return {'final_payoff': final_payoff}


page_sequence = [
    welcome,
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
    FinalResults,
]