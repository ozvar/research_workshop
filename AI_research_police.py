import getpass

import pyttsx3
import playsound

from modules.simulations.statistical_power import p_value_sonata
from modules.simulations.statistical_power import simulate_experiments
from modules.simulations.statistical_power import simulate_correlations
from modules.simulations.statistical_power import simulate_file_drawer


class __DefaultSentences:
    '''
    Doctring here
    '''
    def __init__(self):
        self.greetings = 'Greetings human, I am your friendly neighborhood' \
            ' robot research assistant'
        self.time_to_research = 'Time to do some research!'
        self.job_done = 'Job done, impeccable execution as usual'
        self.ready_to_rumble = 'I am ready to rumble'
        self.you_are_right = 'That seems right, get yourself a +1 in intellect'
        self.you_are_wrong = 'You got it wrong mate, maybe try doing an ' \
            'evolutionary leap?'
        self.farewell = 'It is time for me to go now, you can go back' \
            ' to do some mediocre research'


class RobotResearchAssistant(__DefaultSentences):
    '''
    Class implementing the functions manager
    '''
    def __init__(self, mute=False):
        '''
        '''
        self.cosmic_password = getpass.getpass(
            'Initialize with cosmic password '
        )
        super(RobotResearchAssistant, self).__init__()
        self.brain = {
            'play p value sonata': p_value_sonata,
            'simulate experiments': simulate_experiments,
            'simulate correlations': simulate_correlations,
            'simulate filedrawer': simulate_file_drawer,
        }
        self.vocal_apparatus = pyttsx3.init()
        self.mute = mute

        self.speak(
            sentences=[self.greetings]
        )

    def __del__(self):
        '''
        Docstring here
        '''
        self.speak(
            sentences=[self.farewell]
        )

    def __unlock_cosmic_powers(self, cosmic_password):
        '''
        '''
        if cosmic_password != self.cosmic_password:
            self.speak(
                sentences=[self.you_are_wrong]
            )
            return False
        else:
            self.speak(
                sentences=[self.you_are_right,
                           'I am initializing my deep, deep, deep, deeeeeep'
                           ' neural network',
                           'titutitututu',
                           'tutituti',
                           'titi',
                           'tu'
                           ]
            )
            playsound.playsound('sounds\\pcp.mp3')
            self.speak(
                sentences=[self.ready_to_rumble,
                           self.time_to_research
                           ]
            )
            return True

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
            sentences=['I am going to {}'.format(experiment_function)]
        )
        self.brain[experiment_function](**kwargs)

    def do_research(self, expriments_parameters):
        '''
        '''
        self.speak(
            sentences=['Please, unlock my artificially intelligent brain ']
        )
        unlocked = False
        while not unlocked:

            cosmic_password = getpass.getpass('Cosmic password: ')
            unlocked = self.__unlock_cosmic_powers(cosmic_password)

        for function, parameters in expriments_parameters.items():

            input('Next')
            self.do_experiment(
                experiment_function=function,
                **parameters
            )
            if parameters['verbose']:
                self.speak(
                    sentences=[self.job_done]
                )


if __name__ == '__main__':
    experiments_parameters = {
        'play p value sonata': {
            'sample_size': 30,
            'effect_size': 0.4,
            'n_experiments': 20,
            'threshold': 0.05,
            'sounds_path': 'sounds',
            'verbose': True
        },
        'simulate experiments': {
            'sample_sizes': [5, 10, 20, 40, 80, 160, 320],
            'effect_size': 0.4,
            'n_experiments': 100,
            'alpha': 0.05,
            'viz_path': 'figures',
            'verbose': False
        },
        'simulate correlations': {
            'correlations': [0.05, 0.2, 0.6],
            'sample_0': 20,
            'sample_1': 2000,
            'viz_path': 'figures',
            'verbose': False
        },
        'simulate filedrawer': {
            'sample_size': 30,
            'effect_size_mu': 0.3,
            'effect_size_sigma': 0.1,
            'n_experiments': 1000,
            'alpha': 0.05,
            'viz_path': 'figures',
            'verbose': False
        }
    }
    rra = RobotResearchAssistant()
    rra.do_research(expriments_parameters=experiments_parameters)
    del rra
