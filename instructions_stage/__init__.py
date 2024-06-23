from otree.api import *
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class Constants(BaseConstants):
    name_in_url = 'instructions_stage'
    players_per_group = None
    num_rounds = 4

class Subsession(BaseSubsession):

    @staticmethod
    def calculate_average(players, guess):
        valid_guesses = [getattr(p, guess) for p in players if getattr(p, guess) is not None]
        average = sum(valid_guesses) / len(valid_guesses) if valid_guesses else 0
        return average

    @staticmethod
    def calculate_histogram(players, guess):
        valid_guesses = [getattr(p, guess) for p in players if getattr(p, guess) is not None]
        hist, bin_edges = np.histogram(valid_guesses, bins=range(102))
        histogram_data = {
            'hist': hist.tolist(),
            'bin_edges': bin_edges.tolist()
        }
        return histogram_data

    @staticmethod
    def create_histogram_image(histogram_data):
        fig, ax = plt.subplots()
        ax.bar(histogram_data['bin_edges'][:-1], histogram_data['hist'], width=1, edgecolor="black")
        ax.set_xlim(min(histogram_data['bin_edges']), max(histogram_data['bin_edges']))
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title('Histogram')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('ascii')
        buf.close()
        plt.close(fig)  # Close the figure to free up memory

        return image_base64


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    guess1 = models.IntegerField(label="What is your guess?", min=0, max=100)
    guess2 = models.IntegerField(label="What is your guess?", min=0, max=100)
    guess3 = models.IntegerField(label="What is your guess?", min=0, max=100)
    guess4 = models.IntegerField(label="What is your guess?", min=0, max=100)

def creating_session(subsession):
    pass

class Round(Page):
    form_model = 'player'

    def get_form_fields(self):
        return [f'guess{self.round_number}']

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

class GuessWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        current_round = self.round_number
        guess = f'guess{current_round}'
        players = self.subsession.get_players()
        # Ensure all players have provided their guesses
        if not all(getattr(p, guess) is not None for p in players):
            self._is_frozen = True

class ResultsPage(Page):
    def vars_for_template(self):
        players = self.group.get_players()
        current_round = self.round_number
        guess = f'guess{current_round}'
        average = Subsession.calculate_average(players, guess)
        histogram_data = Subsession.calculate_histogram(players, guess)
        histogram_image = Subsession.create_histogram_image(histogram_data)

        return {
            'average': average,
            'two_thirds_average': (2 / 3) * average,
            'histogram_image': histogram_image,
            'guess': guess
        }

page_sequence = [
    Round, GuessWaitPage, ResultsPage,
    Round, GuessWaitPage, ResultsPage,
    Round, GuessWaitPage, ResultsPage,
    Round, GuessWaitPage, ResultsPage
]
