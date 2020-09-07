# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class product_is_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product installed?'


class F1_2020_emergency_complies_with_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment comply with all of the Installation Requirements' \
            ' defined within Activity Definition F1?'

    def formula(buildings, period, parameters):
        product_is_installed = buildings('product_is_installed', period)
        return product_is_installed
