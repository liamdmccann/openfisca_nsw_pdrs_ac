# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F1_2019_product_is_RDC_within_GEMS_2019(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product an RDC, as defined within the terms of the' \
            ' Greenhouse and Minimum Standards (Refrigerated Cabinets)' \
            ' Determination 2020?'


class below_77_EEI(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product have an Energy Efficiency Index of below 77 EEI?'


class F1_2019_product_is_registered_within_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product a registered product under GEMS?'


class F1_2019_product_complies_with_GEMS_2019_RC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Refrigerated Display Cabinets) Determination 2012?'


class F1_2019_complies_with_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment comply with all of the Equipment Requirements' \
            ' defined within Activity Definition F1?'

    def formula(buildings, period, parameters):
        is_RDC_within_GEMS_2019 = buildings('F1_2019_product_is_RDC_within_GEMS_2019', period)
        below_77_EEI = buildings('below_77_EEI', period)
        registered_in_GEMS_2019 = buildings('F1_2019_product_is_registered_within_GEMS', period)
        complies_with_GEMS_2019 = buildings('F1_2019_product_complies_with_GEMS_2019_RC', period)
        return (is_RDC_within_GEMS_2019 * below_77_EEI * registered_in_GEMS_2019 * complies_with_GEMS_2019)
