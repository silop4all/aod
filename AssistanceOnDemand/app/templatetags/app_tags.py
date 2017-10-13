from django import template
from django.utils.translation import ugettext as _

register = template.Library()

def pay_free_of_charge(charging_policy_id):
    """Check if the payment policy of the service is free of charge.
    
    Args:
        charging_policy_id (int): the id of the charging policy

    Returns:
        bool: If the policy is free of charge return True. Otherwise, return False.
    """
    if charging_policy_id is None:
        return False
    if int(charging_policy_id) == 1:
        return True
    return False
register.filter('pay_free_of_charge', pay_free_of_charge)


def pay_per_use_or_one_off(charging_policy_id):
    """Check if the payment policy of the service is per usage or one-off.
    
    Args:
        charging_policy_id (int): the id of the charging policy

    Returns:
        bool: If the policy is per usage or one-off return True. Otherwise, return False.
    """
    if charging_policy_id is None:
        return False
    if int(charging_policy_id) in [2, 3]:
        return True
    return False
register.filter('pay_per_use_or_one_off', pay_per_use_or_one_off)


def pay_as_subscriber(charging_policy_id):
    """Check if the payment policy of the service is per usage or one-off.
    
    Args:
        charging_policy_id (int): the id of the charging policy

    Returns:
        bool: If the policy is per usage or one-off return True. Otherwise, return False.
    """
    if charging_policy_id is None:
        return False
    if int(charging_policy_id) in [4, 5, 6, 7]:
        return True
    return False
register.filter('pay_as_subscriber', pay_as_subscriber)
