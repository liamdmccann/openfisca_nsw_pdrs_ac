# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class product_is_RDC_within_AS1731_14(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product an RDC, as defined within the meaning of AS1731.14?'


class product_is_high_efficiency_within_AS1731_14(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product a high efficiency product, as defined within' \
            ' the meaning of AS1731.14?'


class product_is_RDC_within_GEMS_2020(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product an RDC, as defined within the terms of the' \
            ' Greenhouse and Minimum Standards (Refrigerated Cabinets)' \
            ' Determination 2020?'


class product_is_registered_within_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product a registered product under GEMS?'


class product_complies_with_GEMS_2012_RDC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Refrigerated Display Cabinets) Determination 2012?'


class product_complies_with_GEMS_2020_RC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product comply with the Greenhouse and Energy Minimum' \
            ' Standards (Refrigerated Display Cabinets) Determination 2012?'


class F1_2020_emergency_complies_with_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment comply with all of the Equipment Requirements' \
            ' defined within Activity Definition F1?'

    def formula(buildings, period, parameters):
        is_RDC_within_AS1731_14 = buildings('product_is_RDC_within_AS1731_14', period)
        is_high_efficiency_within_AS1731_14 = buildings('product_is_high_efficiency_within_AS1731_14', period)
        is_RDC_within_GEMS_2020 = buildings('product_is_RDC_within_GEMS_2020', period)
        registered_in_GEMS = buildings('product_is_registered_within_GEMS', period)
        complies_with_GEMS_2012 = buildings('product_complies_with_GEMS_2012_RDC', period)
        complies_with_GEMS_2020 = buildings('product_complies_with_GEMS_2020_RC', period)
        return (((is_RDC_within_AS1731_14 * is_high_efficiency_within_AS1731_14) + is_RDC_within_GEMS_2020)
        * (registered_in_GEMS * (complies_with_GEMS_2012 + complies_with_GEMS_2020)))
