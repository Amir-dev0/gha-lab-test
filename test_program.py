"""
Unit tests for program module.

This module contains pytest test cases for program conversion functions
using mocking to simulate API responses.
"""

import pytest
from unittest.mock import patch, Mock
import requests
from program import get_usd_to_irr, convert_usd_to_irr, format_price


class TestGetUsdToIrr:
    """Test cases for get_usd_to_irr function."""
    
    @patch('program.requests.get')
    def test_successful_api_call(self, mock_get):
        """
        Test successful API response with valid exchange rate.
        
        Given: API returns success response with IRR rate
        When: get_usd_to_irr is called
        Then: Should return the exchange rate
        """
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {'rates': {'IRR': 42000}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = get_usd_to_irr()
        
        # Assert
        assert result == 42000
        mock_get.assert_called_once()
    
    @patch('program.requests.get')
    def test_api_connection_error(self, mock_get):
        """
        Test API connection failure.
        
        Given: Network error occurs
        When: get_usd_to_irr is called
        Then: Should return None gracefully
        """
        # Arrange
        mock_get.side_effect = requests.RequestException("Connection error")
        
        # Act
        result = get_usd_to_irr()
        
        # Assert
        assert result is None
    
    @patch('program.requests.get')
    def test_api_timeout_error(self, mock_get):
        """
        Test API timeout scenario.
        
        Given: API request times out
        When: get_usd_to_irr is called
        Then: Should return None gracefully
        """
        # Arrange
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        # Act
        result = get_usd_to_irr()
        
        # Assert
        assert result is None
    
    @patch('program.requests.get')
    def test_missing_rate_in_response(self, mock_get):
        """
        Test API response missing IRR rate.
        
        Given: API returns response without IRR rate
        When: get_usd_to_irr is called
        Then: Should raise KeyError
        """
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {'rates': {'EUR': 0.85}}  # No IRR
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(KeyError):
            get_usd_to_irr()


class TestConvertUsdToIrr:
    """Test cases for convert_usd_to_irr function."""
    
    def test_successful_conversion(self):
        """
        Test successful USD to IRR conversion.
        
        Given: Exchange rate is 42000 IRR per USD
        When: Converting 100 USD
        Then: Should return 4,200,000 IRR
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=42000):
            # Act
            result = convert_usd_to_irr(100)
            
            # Assert
            assert result == 4200000
    
    def test_conversion_with_zero_amount(self):
        """
        Test conversion with zero USD amount.
        
        Given: Exchange rate is available
        When: Converting 0 USD
        Then: Should return 0 IRR
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=42000):
            # Act
            result = convert_usd_to_irr(0)
            
            # Assert
            assert result == 0
    
    def test_conversion_when_rate_unavailable(self):
        """
        Test conversion when exchange rate fetch fails.
        
        Given: get_usd_to_irr returns None
        When: Converting any amount
        Then: Should return None
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=None):
            # Act
            result = convert_usd_to_irr(100)
            
            # Assert
            assert result is None
    
    def test_conversion_with_float_amount(self):
        """
        Test conversion with floating point amount.
        
        Given: Exchange rate is available
        When: Converting 25.5 USD
        Then: Should return correct converted amount
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=42000):
            # Act
            result = convert_usd_to_irr(25.5)
            
            # Assert
            assert result == 1071000  # 25.5 * 42000


class TestFormatPrice:
    """Test cases for format_price function."""
    
    def test_format_large_number(self):
        """
        Test formatting large number with thousand separators.
        
        Given: Large amount like 4,200,000
        When: format_price is called
        Then: Should return formatted string with commas
        """
        result = format_price(4200000)
        assert result == "4,200,000"
    
    def test_format_small_number(self):
        """
        Test formatting small number with thousand separators.
        
        Given: Small amount like 1000
        When: format_price is called
        Then: Should return formatted string with comma
        """
        result = format_price(1000)
        assert result == "1,000"
    
    def test_format_zero(self):
        """
        Test formatting zero amount.
        
        Given: Zero amount
        When: format_price is called
        Then: Should return "0"
        """
        result = format_price(0)
        assert result == "0"
    
    def test_format_negative_number(self):
        """
        Test formatting negative number.
        
        Given: Negative amount like -5000
        When: format_price is called
        Then: Should return formatted negative string
        """
        result = format_price(-5000)
        assert result == "-5,000"
    
    def test_format_decimal_number(self):
        """
        Test formatting decimal number.
        
        Given: Float amount like 12345.67
        When: format_price is called
        Then: Should format with thousand separators (no decimals)
        """
        result = format_price(12345.67)
        assert result == "12,346"  # Rounded with :.0f


class TestIntegration:
    """Integration test cases for complete workflow."""
    
    def test_end_to_end_conversion_workflow(self):
        """
        Test complete conversion workflow from USD to formatted IRR.
        
        Given: Exchange rate is available
        When: Converting 50 USD to formatted price
        Then: Should return correct formatted string
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=42000):
            # Act
            amount_usd = 50
            irr_amount = convert_usd_to_irr(amount_usd)
            formatted = format_price(irr_amount)
            
            # Assert
            assert irr_amount == 2100000
            assert formatted == "2,100,000"
    
    def test_workflow_with_api_failure(self):
        """
        Test complete workflow when API fails.
        
        Given: Exchange rate unavailable
        When: Trying to convert and format
        Then: Should handle gracefully with None
        """
        # Arrange
        with patch('program.get_usd_to_irr', return_value=None):
            # Act
            irr_amount = convert_usd_to_irr(50)
            
            # Assert
            assert irr_amount is None