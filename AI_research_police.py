import pyttsx3

from modules.simulations import p_value_sonata
from modules.simulations import simulate_experiments
from modules.simulations import simulate_correlations
from modules.simulations import simulate_file_drawer


class RobotResearchAssistant:
    '''
    '''
    def __init__(self, file_drawer, picture_drawer, mute=False):
        '''
        '''
        self.brain = {
            'play p value sonata': p_value_sonata,
            'simulate experiments': simulate_experiments,
            'simulate correlations': simulate_correlations,
            'simulate file_drawer': simulate_file_drawer,
        }
        self.vocal_apparatus = pyttsx3.init()
        self.file_drawer = file_drawer
        self.picture_drawer = picture_drawer
        self.mute = mute

    def speak(self, sentences):
        '''
        '''
        for sentence in sentences:

            self.vocal_apparatus.say(sentence)

        if not self.mute:
            self.vocal_apparatus.runAndWait()

    def do_experiment(self, experiment_function, **kwargs):
        '''
        '''
        self.speak(
            senteces=['I am going to {}'.format(experiment_function)]
        )
        self.brain['experiment_function'](**kwargs)

    def do_research(self, expriments_parameters):
        '''
        '''
        for function, parameters in expriments_parameters.items():

            self.do_experiment(
                experiment_function=function
            )
