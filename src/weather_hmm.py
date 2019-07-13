'''weather prediction HMM'''
from pomegranate import HiddenMarkovModel, DiscreteDistribution, State

model = HiddenMarkovModel(name='weather')

sunny_emissions = DiscreteDistribution({'yes': 0.1, 'no': 0.9})
sunny_state = State(sunny_emissions, name='sunny')

rainy_emissions = DiscreteDistribution({'yes': 0.8, 'no': 0.2})
rainy_state = State(rainy_emissions, name='rainy')

model.add_states(sunny_state, rainy_state)
