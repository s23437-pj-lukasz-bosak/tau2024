import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from bank_system import Account, Bank, InsufficientFundsError

# Fixture tworzące przykładowe konto
@pytest.fixture
def account():
    return Account("123456", "Jan Kowalski", 1_000_000.0)

# Fixture tworzące inne konto
@pytest.fixture
def another_account():
    return Account("654321", "Anna Nowak", 500_000.0)

# Fixture tworzące bank
@pytest.fixture
def bank():
    return Bank()

# Testy klasy Account
# Test poprawnego dodawania środków

def test_deposit(account):
    account.deposit(500_000.0)
    assert account.balance == 1_500_000.0

# Test błędnej wpłaty ujemnej kwoty

def test_deposit_negative(account):
    with pytest.raises(ValueError):
        account.deposit(-10_000.0)

# Test poprawnej wypłaty środków

def test_withdraw(account):
    account.withdraw(500_000.0)
    assert account.balance == 500_000.0

# Test wypłaty większej kwoty niż dostępne środki

def test_withdraw_insufficient_funds(account):
    with pytest.raises(InsufficientFundsError):
        account.withdraw(2_000_000.0)

# Test poprawnego transferu asynchronicznego między kontami
@pytest.mark.asyncio
async def test_transfer(account, another_account):
    await account.transfer(another_account, 500_000.0)
    assert account.balance == 500_000.0
    assert another_account.balance == 1_000_000.0

# Test transferu większej kwoty niż dostępne środki
@pytest.mark.asyncio
async def test_transfer_insufficient_funds(account, another_account):
    with pytest.raises(InsufficientFundsError):
        await account.transfer(another_account, 2_000_000.0)

# Testy klasy Bank
# Test poprawnego tworzenia konta

def test_create_account(bank):
    bank.create_account("111222", "Marek Wiśniewski", 2_000_000.0)
    assert bank.get_account("111222").balance == 2_000_000.0

# Test tworzenia konta o istniejącym numerze

def test_create_duplicate_account(bank):
    bank.create_account("111222", "Marek Wiśniewski", 2_000_000.0)
    with pytest.raises(ValueError):
        bank.create_account("111222", "Karol Zieliński", 3_000_000.0)

# Test pobierania nieistniejącego konta

def test_get_nonexistent_account(bank):
    with pytest.raises(ValueError):
        bank.get_account("000000")

# Test procesu transakcji asynchronicznej
@pytest.mark.asyncio
async def test_process_transaction(bank, account, another_account):
    async def mock_transaction():
        await account.transfer(another_account, 300_000.0)

    await bank.process_transaction(mock_transaction)
    assert account.balance == 700_000.0
    assert another_account.balance == 800_000.0

# Testy z mockowaniem
# Test z mockowaniem zewnętrznego systemu autoryzacji
@pytest.mark.asyncio
async def test_mock_external_authorization():
    mock_auth_service = AsyncMock()
    mock_auth_service.return_value = True
    with patch("bank_system.external_auth", mock_auth_service):
        result = await mock_auth_service()
        assert result is True