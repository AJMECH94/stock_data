import pytest
from main import process_stock_data


def test_cli_command():
    result = process_stock_data('aapl', '2022-2-3', '2023-2-3')
    assert result['msg']=='Sucess'
