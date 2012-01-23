from livesettings import *
from django.utils.translation import ugettext as _

SHIP_MODULES = config_get('SHIPPING', 'MODULES')
#SHIP_MODULES.add_choice(('makingsuds.apost_satchel', 'AusPost Satchel'))
#SHIPPING_GROUP = config_get_group('SHIPPING')

SHIP_MODULES.add_choice(('apost_satchel', 'AusPost Satchel'))
SHIPPING_GROUP = ConfigurationGroup('apost_satchel',
  _('AusPost Satchel Settings'),
  requires = SHIP_MODULES,
  requiresvalue='apost_satchel',
  ordering = 101
)

config_register_list(
    DecimalValue(SHIPPING_GROUP, 'ap_under', description=_("AusPost Under 500g"), requiresvalue='makingsuds.apost_satchel', default="6.00"),
    DecimalValue(SHIPPING_GROUP, 'ap_over', description=_("AusPost Over 500g"), requiresvalue='makingsuds.apost_satchel', default="9.00"),
    StringValue(SHIPPING_GROUP, 'single_free', description=_("Free ship for single item"), help_text=_("Comma seperated list with no spaces of product SKU values"), requiresvalue='makingsuds.apost_satchel')
    )
