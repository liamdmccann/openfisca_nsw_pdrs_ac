# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class peak_demand_savings(Variable):
    value_type = float  # check if this is a float - think it's correct
    entity = Building
    definition_period = ETERNITY
    label = 'What are the peak demand savings created by the peak demand' \
            ' reduction activity?'

    def formula(buildings, period, parameters):
        baseline_power_input = buildings('baseline_power_input', period)
        power_input = buildings('power_input', period)
        peak_window_duration = parameters(period).peak_demand_reduction_scheme.peak_window_duration
        forward_creation_period = parameters(period).peak_demand_reduction_scheme.forward_creation_period
        firmness_factor = parameters(period).peak_demand_reduction_scheme.firmness_factor
        return ((baseline_power_input - power_input) * peak_window_duration
                 * forward_creation_period * firmness_factor)


class baseline_power_input(Variable):
    value_type = float  # check if this is a float - think it's correct
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline power input of the air conditioner?'

    def formula(buildings, period, parameters):
        product_class = buildings('AC_product_class', period)
        new_or_replacement = buildings('new_or_replacement', period)
        baseline_power_input = parameters(period).peak_demand_reduction_scheme.baseline_power_input[product_class][new_or_replacement]
        return baseline_power_input


class power_input(Variable):
    value_type = float  # check if this is a float - think it's correct
    entity = Building
    definition_period = ETERNITY
    label = 'What is the power input of the air conditioner?'


class ACProductClass(Enum):
    product_class_one = 'AC is in product class one.'
    product_class_two = 'AC is in product class two.'
    product_class_three = 'AC is in product class three.'
    product_class_four = 'AC is in product class four.'
    product_class_five = 'AC is in product class five.'
    product_class_six = 'AC is in product class six.'
    product_class_seven = 'AC is in product class seven.'
    product_class_eight = 'AC is in product class eight.'
    product_class_nine = 'AC is in product class nine.'
    product_class_ten = 'AC is in product class ten.'
    product_class_eleven = 'AC is in product class eleven.'
    product_class_twelve = 'AC is in product class twelve.'
    product_class_thirteen = 'AC is in product class thirteen.'
    product_class_fourteen = 'AC is in product class fourteen.'
    product_class_fifteen = 'AC is in product class fifteen.'
    product_class_sixteen = 'AC is in product class sixteen.'
    product_class_seventeen = 'AC is in product class seventeen.'
    product_class_eighteen = 'AC is in product class eighteen.'
    product_class_nineteen = 'AC is in product class nineteen.'
    product_class_twenty = 'AC is in product class twenty.'
    product_class_twenty_one = 'AC is in product class twenty one.'


class AC_product_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = ACProductClass
    default_value = ACProductClass.product_class_one
    definition_period = ETERNITY
    label = 'What is the product class for the installed air conditioner?'


class NewOrReplacement(Enum):
    new_AC = 'The installed air conditioner is a new air conditioner.'
    replacement_AC = 'The installed air conditioner is a replacement air conditioner.'


class new_or_replacement(Variable):
    value_type = Enum
    entity = Building
    possible_values = NewOrReplacement
    default_value = NewOrReplacement.new_AC
    definition_period = ETERNITY
    label = 'Is the installed air conditioner a new air conditioner or' \
            ' a replacement air conditioner?'
