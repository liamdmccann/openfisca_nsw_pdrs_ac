# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class energy_efficiency_index(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Energy Efficiency Index (EEI) of the refrigerated' \
            ' cabinet?'

    def formula(buildings, period, parameters):
        annual_energy_consumption = buildings('annual_energy_consumption', period)
        reference_annual_energy_consumption = buildings('reference_annual_energy_consumption', period)
        return (annual_energy_consumption / reference_annual_energy_consumption) * 100


class annual_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Annual Energy Consumption of the Refrigerated' \
            ' Cabinet?'

    def formula(buildings, period, parameters):
        duty_class = buildings('duty_class', period)
        is_RDC = buildings('is_RDC', period)
        is_RSC = buildings('is_RSC', period)
        is_chiller = buildings('is_chiller', period)
        is_freezer = buildings('is_freezer', period)
        is_ice_cream_freezer_cabinet = buildings('is_ice_cream_freezer_cabinet', period)
        is_scooping_cabinet = buildings('is_scooping_cabinet', period)
        is_remote = buildings('is_remote_cabinet', period)
        is_integral = buildings('is_integral_cabinet', period)
        is_low_sales_volume = buildings('is_low_sales_volume_product', period)
        is_oversize = buildings('is_oversize_product', period)
        daily_energy_consumption = buildings('total_energy_consumption', period)
        adjustment_factor = buildings('adjustment_factor', period)
        direct_energy_consumption = buildings('direct_energy_consumption', period)
        refrigeration_energy_consumption = buildings('refrigeration_energy_consumption', period)
        annual_energy_consumption = select([(is_RDC + ((not(is_low_sales_volume)) * (not(is_oversize)))),
                                            (is_scooping_cabinet),
                                            (is_ice_cream_freezer_cabinet),
                                            (is_RSC + (not(is_low_sales_volume))),
                                            (is_RDC * is_remote * (is_low_sales_volume + is_oversize)),
                                            (is_RDC * is_integral * (is_low_sales_volume + is_oversize)),
                                            (is_RSC * is_low_sales_volume)],
                                            [(daily_energy_consumption * 365),
                                            (daily_energy_consumption * 365),
                                            (daily_energy_consumption * 365),
                                            (daily_energy_consumption * adjustment_factor * 365),
                                            ((direct_energy_consumption + refrigeration_energy_consumption) * adjustment_factor * 365),
                                            (daily_energy_consumption * adjustment_factor * 365),
                                            (daily_energy_consumption * adjustment_factor * 365)])
        return annual_energy_consumption


class direct_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Direct Energy Consumption of the Refrigerated' \
            ' Cabinet? Direct Energy Consumption is the energy consumption of' \
            ' the electricial components of the RDC, excluding the consumption' \
            ' of the remote refrigeration system that runs the RDC.'


class refrigeration_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Remote Energy Consumption of the Refrigerated' \
            ' Cabinet? Remote Energy Consumption is the measure of the' \
            ' refrigeration system which runs the RDC.'


class adjustment_factor(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the adjustment factor for the purposes of calculating Annual' \
            ' Energy Consumption?'

    def formula(buildings, period, parameters):
        duty_class = buildings('duty_class', period)
        is_RDC = buildings('is_RDC', period)
        is_RSC = buildings('is_RSC', period)
        is_chiller = buildings('is_chiller', period)
        is_freezer = buildings('is_freezer', period)
        is_remote = buildings('is_remote_cabinet', period)
        is_integral = buildings('is_integral_cabinet', period)
        is_low_sales_volume = buildings('is_low_sales_volume_product', period)
        is_oversize = buildings('is_oversize_product', period)
        is_light_duty = (duty_class == DutyClass.light_duty)
        is_normal_duty = (duty_class == DutyClass.normal_duty)
        is_heavy_duty = (duty_class == DutyClass.heavy_duty)
        adjustment_factor = select([(is_light_duty * is_RSC * is_chiller),
                                    (is_light_duty * is_RSC * is_freezer),
                                    (is_RDC * is_remote * (is_low_sales_volume + is_oversize)),
                                    (is_RDC * is_integral * (is_low_sales_volume + is_oversize)),
                                    (is_RSC * is_low_sales_volume * is_heavy_duty),
                                    (is_RSC * is_low_sales_volume * (is_light_duty + is_normal_duty))],
                                    [1.2, 1.1, 1.1304, 1.1304, 1.15, 1.1875])
        condition_adjustment_factor = ((adjustment_factor == 1.2) + (adjustment_factor == 1.1)
                                    + (adjustment_factor == 1.1304) + (adjustment_factor == 1.15)
                                    + (adjustment_factor == 1.1875))
        return where(condition_adjustment_factor, adjustment_factor, 1)


class reference_annual_energy_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the Reference Annual Energy Consumption of the Refrigerated' \
            ' Cabinet?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        duty_class = buildings('duty_class', period)
        is_RDC = buildings('is_RDC', period)
        is_RSC = buildings('is_RSC', period)
        is_chiller = buildings('is_chiller', period)
        is_freezer = buildings('is_freezer', period)
        is_ice_cream_freezer_cabinet = buildings('is_ice_cream_freezer_cabinet', period)
        is_scooping_cabinet = buildings('is_scooping_cabinet', period)
        is_remote = buildings('is_remote_cabinet', period)
        is_integral = buildings('is_integral_cabinet', period)
        is_low_sales_volume = buildings('is_low_sales_volume_product', period)
        is_oversize = buildings('is_oversize_product', period)
        coefficient_M = parameters(period).F1_2019.coefficients.M[product_class]
        coefficient_N = parameters(period).F1_2019.coefficients.N[product_class]
        adjustment_factor = buildings('adjustment_factor', period)
        net_cabinet_volume = buildings('net_cabinet_volume', period)
        daily_energy_consumption = buildings('total_energy_consumption', period)
        total_display_area = buildings('total_display_area', period)
        direct_energy_consumption = buildings('direct_energy_consumption', period)
        refrigeration_energy_consumption = buildings('refrigeration_energy_consumption', period)
        reference_annual_energy_consumption = select([(is_RDC + ((not(is_low_sales_volume)) * (not(is_oversize)))),
                                            (is_scooping_cabinet),
                                            (is_ice_cream_freezer_cabinet),
                                            (is_RSC + (not(is_low_sales_volume))),
                                            (is_RDC * is_remote * (is_low_sales_volume + is_oversize)),
                                            (is_RDC * is_integral * (is_low_sales_volume + is_oversize)),
                                            (is_RSC * is_low_sales_volume)],
                                            [((coefficient_M + (coefficient_N * total_display_area)) * 365),
                                            ((coefficient_M + (coefficient_N * total_display_area)) * 365),
                                            ((coefficient_M + (coefficient_N * net_cabinet_volume)) * 365),
                                            ((coefficient_M * net_cabinet_volume) * coefficient_N),
                                            ((direct_energy_consumption + refrigeration_energy_consumption) * 365),
                                            (daily_energy_consumption * 365),
                                            (daily_energy_consumption * 365)])
        return reference_annual_energy_consumption


class net_cabinet_volume(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the net cabinet volume, in L?'


class ProductClass(Enum):
    IRH = 'Product is an RDC - chiller (IRH), that is integral and horizontal,' \
          ' and is registered in Product Class 1 of the 2019 GEMS Determination.'
    IFH = 'Product is an RDC - freezer (IFH),  that is integral and horizontal,' \
          ' and is registered in Product Class 2 of the 2019 GEMS Determination.'
    SRH = 'Product is an RSC - chiller (SRH), that is horizontal and is registered in Product Class 3' \
          ' of the 2019 GEMS Determination.'
    SFH = 'Product is an RSC - freezer (SFH), and is registered in Product Class 4' \
          ' of the 2019 GEMS Determination.'
    IFH_5 = 'Product is an ice cream freezer cabinet (IFH-5), and is registered' \
            ' in Product Class 5 of the 2019 GEMS Determination.'
    GSC = 'Product is an scooping cabinet (GSC), and is registered in Product' \
          ' Class 6 of the 2019 GEMS Determination.'
    ISC = 'Product is an scooping cabinet (ISC), and is registered in Product' \
          ' Class 6 of the 2019 GEMS Determination.'
    IRV = 'Product is an RDC - chiller (IRV), and is registered in Product' \
          ' Class 7 of the 2019 GEMS Determination.'
    IFV = 'Product is an RDC - freezer (IFV), and is registered in Product' \
          ' Class 8 of the 2019 GEMS Determination.'
    SRV = 'Product is an RSC - chiller (SRV), and is registered in Product' \
          ' Class 9 of the 2019 GEMS Determination.'
    SFV = 'Product is an RSC - freezer (SFV), and is registered in Product' \
          ' Class 10 of the 2019 GEMS Determination.'
    IRV_4 = 'Product is an RDC - chiller (IRV-4), and is registered in Product' \
          ' Class 11 of the 2019 GEMS Determination.'
    RRH = 'Product is an RDC - chiller (RRH), and is registered in Product' \
          ' Class 12 of the 2019 GEMS Determination.'
    RFH = 'Product is an RDC - chiller (RFH), and is registered in Product' \
          ' Class 13 of the 2019 GEMS Determination.'
    RRV = 'Product is an RDC - chiller (RRV), and is registered in Product' \
          ' Class 14 of the 2019 GEMS Determination.'
    RRV_2 = 'Product is an RDC - chiller (RRV-2), and is registered in Product' \
          ' Class 14 of the 2019 GEMS Determination.'
    RFV = 'Product is an RDC - chiller (RRV-2), and is registered in Product' \
          ' Class 15 of the 2019 GEMS Determination.'


class product_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = ProductClass
    default_value = ProductClass.IRH
    definition_period = ETERNITY
    label = 'What is the Product Class for the Refrigerated Cabinet, as defined' \
            ' in the 2019 GEMS Determination?'


class is_low_sales_volume_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet a low sales volume product?'
    #  I don't think there's value in coding the criteria for this


class is_oversize_product(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an oversize product?'
    #  I don't think there's value in coding the criteria for this


class is_RDC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an RDC?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_RDC = ((product_class == ProductClass.IRH) + (product_class == ProductClass.IFH)
                 + (product_class == ProductClass.IRV) + (product_class == ProductClass.IFV)
                 + (product_class == ProductClass.IRV_4) + (product_class == ProductClass.RRH)
                 + (product_class == ProductClass.RFH) + (product_class == ProductClass.RRV)
                 + (product_class == ProductClass.RRV_2) + (product_class == ProductClass.RFV))
        return is_RDC


class is_RSC(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an RSC?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_RSC = ((product_class == ProductClass.SRH) + (product_class == ProductClass.SFH)
                 + (product_class == ProductClass.SRV) + (product_class == ProductClass.SFV))
        return is_RSC


class is_ice_cream_freezer_cabinet(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an ice cream freezer cabinet?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_ice_cream_freezer_cabinet = (product_class == ProductClass.IFH_5)
        return is_ice_cream_freezer_cabinet


class is_scooping_cabinet(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet a scooping cabinet?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_scooping_cabinet = ((product_class == ProductClass.GSC) + (product_class == ProductClass.ISC))
        return is_scooping_cabinet



class is_chiller(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet a chiller?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_chiller = ((product_class == ProductClass.IRH) + (product_class == ProductClass.SRH)
                     + (product_class == ProductClass.IRV) + (product_class == ProductClass.SRV)
                     + (product_class == ProductClass.IRV_4) + (product_class == ProductClass.RRH)
                     + (product_class == ProductClass.RRV) + (product_class == ProductClass.RRV_2))
        return is_chiller


class is_freezer(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet a freezer?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_freezer = ((product_class == ProductClass.IFH) + (product_class == ProductClass.SFH)
                     + (product_class == ProductClass.IFH_5) + (product_class == ProductClass.IFV)
                     + (product_class == ProductClass.SFV) + (product_class == ProductClass.RFH)
                     + (product_class == ProductClass.RFV))
        return is_freezer





class is_integral_cabinet(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an integral cabinet?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_integral = ((product_class == ProductClass.IRH) + (product_class == ProductClass.IFH)
                      + (product_class == ProductClass.SRH) + (product_class == ProductClass.SFH)
                      + (product_class == ProductClass.IFH_5) + (product_class == ProductClass.GSC)
                      + (product_class == ProductClass.ISC) + (product_class == ProductClass.IRV)
                      + (product_class == ProductClass.IFV) + (product_class == ProductClass.SRV)
                      + (product_class == ProductClass.SFV) + (product_class == ProductClass.IRV_4))
        return is_integral


class is_remote_cabinet(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the refrigerated cabinet an integral cabinet?'

    def formula(buildings, period, parameters):
        product_class = buildings('product_class', period)
        is_remote = ((product_class == ProductClass.RRH) + (product_class == ProductClass.RFH)
                    + (product_class == ProductClass.RRV) + (product_class == ProductClass.RRV_2)
                    + (product_class == ProductClass.RFV))
        return is_remote


class DutyClass(Enum):
    light_duty = 'cabinet is a light duty cabinet.'
    normal_duty = 'cabinet is a normal duty cabinet.'
    heavy_duty = 'cabinet is a heavy duty cabinet.'


class duty_class(Variable):
    value_type = Enum
    entity = Building
    possible_values = DutyClass
    default_value = DutyClass.normal_duty
    definition_period = ETERNITY
    label = 'What is the duty class of the Refrigerated Cabinet, as tested in' \
            ' accordance with EN 16825?'
