"""
This dummy module can be used as a basis for creating your own

- Copy this module to a new name
- Make the changes described below
"""

# Note, make sure you use decimal math everywhere!
from decimal import Decimal
from django.utils.translation import ugettext as _
from shipping.modules.base import BaseShipper
from livesettings import config_get_group
import logging

log = logging.getLogger('apost')

class Shipper(BaseShipper):

    flatRateFee = Decimal("15.00")
    id = "apost"

    def __str__(self):
        """
        This is mainly helpful for debugging purposes
        """
        return "AusPost PrePaid Satchel"

    def description(self):
        """
        A basic description that will be displayed to the user when selecting their shipping options
        """
        return _("Regular AusPost Shipping")

    def calculate(self, cart, contact):
        self.cart = cart
        self.contact = contact
        self.large_order = False

        settings =  config_get_group('apost_satchel')

        if settings.single_free.value:
            free_ship_skus = settings.single_free.value.split(',')
        else:
            free_ship_skus = []	

        if len(cart.get_shipment_list()) == 1 and cart.get_shipment_list()[0].sku in free_ship_skus:
            self.shipping_cost = 0
            self._calculated = True

        else:
            total_weight = Decimal('0')

            for product in cart.get_shipment_list():
                log.debug(product.name)
                if product.weight == 'na':
                    total_weight += Decimal('0.3')
                elif product.weight:
                    total_weight += Decimal(product.weight)
                else:
                    total_weight += Decimal(0)

            if total_weight <= Decimal('0.5'):
                self.shipping_cost = Decimal(settings.ap_under.value)
            elif total_weight > Decimal('0.5') and total_weight < Decimal('3.0'):
                self.shipping_cost = Decimal(settings.ap_over.value)
            elif total_weight > Decimal('3.0'):
                log.debug(total_weight)
                lrg_bag_count = 0

                while total_weight > 3:
                    total_weight -= 3
                    lrg_bag_count += 1

                log.debug(lrg_bag_count)
                large_bags = settings.ap_over.value*lrg_bag_count

                if total_weight > Decimal('0.5'):
                    fract_bags = settings.ap_over.value
                else:
                    fract_bags = settings.ap_under.value

                self.shipping_cost = Decimal(str(large_bags+fract_bags))

            if self.shipping_cost > Decimal('0'):
                log.debug(self.shipping_cost)
                self._calculated = True

    def cost(self):
        """
        Complex calculations can be done here as long as the return value is a decimal figure
        """
        assert(self._calculated)
        return(self.shipping_cost)

    def method(self):
        """
        Describes the actual delivery service (Mail, FedEx, DHL, UPS, etc)
        """
        return _("AusPost")

    def expectedDelivery(self):
        """
        Can be a plain string or complex calcuation returning an actual date
        """
        return _("3 - 4 business days")

    def valid(self, order=None):
        """
        Can do complex validation about whether or not this option is valid.
        For example, may check to see if the recipient is in an allowed country
        or location.
        """
        return True

