"""
Module for currency conversion using exchange rate API.
"""

import requests

def get_usd_to_irr():
    """
    Get the dollar to toman conversion rate from API.
    
    Returns:
        float or None: Exchange rate if successful, None otherwise.
    """
    try:
        response = requests.get(
            'https://api.exchangerate-api.com/v4/latest/USD',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return data['rates']['IRR']
    except requests.RequestException:
        return None

def convert_usd_to_irr(usd_amount):
    """
    Convert USD to IRR.
    
    Args:
        usd_amount (float): Amount in USD.
    
    Returns:
        float or None: Converted amount in IRR, None if rate fetch fails.
    """
    rate = get_usd_to_irr()
    if rate is None:
        return None
    return usd_amount * rate

def format_price(irr_amount):
    """
    Separating thousands for better display.
    
    Args:
        irr_amount (float): Amount in IRR.
    
    Returns:
        str: Formatted amount with thousand separators.
    """
    return f"{irr_amount:,.0f}"
