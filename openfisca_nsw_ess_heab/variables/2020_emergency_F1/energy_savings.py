# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np


class baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline efficiency for the relevant product type, in' \
            ' kWh per day per m2?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        baseline_efficiency = parameters(period).F1_emergency.emergency_V2_baseline_efficiency[product_class]
        return baseline_efficiency


class emergency_baseline_efficiency(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the baseline efficiency for the relevant product type, in' \
            ' kWh per day per m2?'

    def formula(buildings, period, parameters):
        product_type = buildings('product_type', period)
        baseline_efficiency = parameters(period).F1_emergency.emergency_V1_baseline_efficiency[product_type]
        return baseline_efficiency


class total_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the total electricity consumption, in kWh per day, of the' \
            ' installed product?'


class total_display_area(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the total display area, in m2, of the installed product?'


class lifetime(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the lifetime for the relevant product type?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        lifetime = parameters(period).F1_emergency.lifetime[product_class]
        return lifetime


class emergency_lifetime(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the lifetime for the relevant product type?'

    def formula(buildings, period, parameters):
        product_type = buildings('product_type', period)
        lifetime = parameters(period).F1_emergency.emergency_lifetime[product_type]
        return lifetime


class F1_emergency_deemed_equipment_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the deemed equipment electricity savings for the' \
            ' installed product, as defined in Activity Definition F1?'

    def formula(buildings, period, parameters):
        baseline_efficiency = buildings('emergency_baseline_efficiency', period)
        total_electricity_consumption = buildings('total_energy_consumption', period)
        total_display_area = buildings('total_display_area', period)
        lifetime = buildings('emergency_lifetime', period)
        days_in_year = parameters(period).ESS_general.days_in_year
        kWh_to_MWh_conversion = parameters(period).unit_conversion_factors['kWh_to_MWh']
        electricity_savings = ((baseline_efficiency * total_display_area - total_electricity_consumption)
        * days_in_year * lifetime / kWh_to_MWh_conversion)
        return electricity_savings


class F1_emergency_ESCs(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the deemed equipment electricity savings for the' \
            ' installed product, as defined in Activity Definition F1?'

    def formula(buildings, period, parameters):
        electricity_savings = buildings('F1_emergency_deemed_equipment_electricity_savings', period)
        number_of_ESCs = electricity_savings * 1.06
        return np.floor(number_of_ESCs)


class ProductType(Enum):
    rs_1_unlit_shelves = 'Product is in the RS1 product class, with unlit shelves.'
    rs_1_lit_shelves = 'Product is in the RS1 product class, with lit shelves.'
    rs_2_unlit_shelves = 'Product is in the RS2 product class, with unlit shelves.'
    rs_2_lit_shelves = 'Product is in the RS2 product class, with lit shelves.'
    rs_3_unlit_shelves = 'Product is in the RS3 product class, with unlit shelves.'
    rs_3_lit_shelves = 'Product is in the RS3 product class, with lit shelves.'
    rs_4_glass_door = 'Product is in the RS4 product class, with glass doors.'
    rs_6_gravity_coil = 'Product is in the RS6 product class, with gravity coil.'
    rs_6_fan_coil = 'Product is in the RS6 product class, with fan coil.'
    rs_7_fan_coil = 'Product is in the RS7 product class, with fan coil.'
    rs_8_gravity_coil = 'Product is in the RS8 product class, with gravity coil.'
    rs_8_fan_coil = 'Product is in the RS8 product class, with fan coil.'
    rs_9_fan_coil = 'Product is in the RS9 product class, with fan coil.'
    rs_10_fan_coil = 'Product is in the RS10 product class, with fan coil.'
    rs_11 = 'Product is in the RS11 product class.'
    rs_12 = 'Product is in the RS12 product class.'
    rs_13_solid_sided = 'Product is in the RS13 product class, and is solid sided.'
    rs_13_glass_sided = 'Product is in the RS13 product class, and is glass sided.'
    rs_14_solid_sided = 'Product is in the RS14 product class, and is solid sided.'
    rs_14_glass_sided = 'Product is in the RS14 product class, and is glass sided.'
    rs_15_glass_door = 'Product is in the RS15 product class, and has a glass door.'
    rs_16_glass_door = 'Product is in the RS16 product class, and has a glass door.'
    rs_18 = 'Product is in the RS18 product class.'
    rs_19 = 'Product is in the RS19 product class.'
    hc_1_m1 = 'Product is in the HC1 product class, with temperature class M1.'
    hc_1_m2 = 'Product is in the HC1 product class, with temperature class M2.'
    hc_4_m1 = 'Product is in the HC4 product class, with temperature class M1.'
    hc_4_m2 = 'Product is in the HC4 product class, with temperature class M2.'
    hf_4_l1 = 'Product is in the HF4 product class, with temperature class L1.'
    hf_4_l2 = 'Product is in the HF4 product class, with temperature class L2.'
    hf_6_l1 = 'Product is in the HF6 product class, with temperature class L1.'
    hf_6_l2 = 'Product is in the HF6 product class, with temperature class L2.'
    vc_1_m1 = 'Product is in the VC1 product class, with temperature class M1.'
    vc_1_m2 = 'Product is in the VC1 product class, with temperature class M2.'
    vc_2_m1 = 'Product is in the VC2 product class, with temperature class M1.'
    vc_2_m2 = 'Product is in the VC2 product class, with temperature class M2.'
    vc4_a_m1 = 'Product is in the VC4 (a) product class, with temperature class M1.'
    vc4_a_m2 = 'Product is in the VC4 (a) product class, with temperature class M2.'
    vc4_b_m1 = 'Product is in the VC4 (b) product class, with temperature class M1.'
    vc4_b_m2 = 'Product is in the VC4 (b) product class, with temperature class M2.'
    vf4_a_l1 = 'Product is in the VF4 (a) product class, with temperature class L1.'
    vf4_a_l2 = 'Product is in the VF4 (a) product class, with temperature class L2.'
    vf4_b_l1 = 'Product is in the VF4 (b) product class, with temperature class L1.'
    vf4_b_l2 = 'Product is in the VF4 (a) product class, with temperature class L2.'


class product_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = ProductType
    default_value = ProductType.rs_1_unlit_shelves
    definition_period = ETERNITY
    label = 'What is the product type to be used within Activity Definition F1?'
