import pytest
from unittest.mock import MagicMock, patch
from backend import main
from backend.database import hash_password

TEST_EMAIL = "test_admin@example.com"
TEST_PASSWORD = "secure123"
TEST_USERNAME = "TestAdmin"

@pytest.fixture
def mock_conn_cursor():
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    yield mock_conn, mock_cursor

@patch("backend.main.get_database_connection")
def test_create_admin(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    # Simuleer delete admin (doet niks)
    main.delete_admin_from_table(TEST_EMAIL, mock_conn)

    # Simuleer create_admin
    main.create_admin(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD, mock_conn)

    # Check of execute werd aangeroepen met juiste SQL en parameters
    args, kwargs = mock_cursor.execute.call_args
    sql = args[0]
    params = args[1]

    assert "INSERT INTO admins" in sql
    assert TEST_USERNAME in params
    assert TEST_EMAIL in params

@patch("backend.main.get_database_connection")
def test_authenticate_admin_success(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    # Simuleer database return waarde met password_hash
    hashed_pw = hash_password(TEST_PASSWORD)
    mock_cursor.fetchone.return_value = (hashed_pw,)

    result = main.authenticate_admin(TEST_EMAIL, TEST_PASSWORD, mock_conn)

    assert result["authenticated"] is True

@patch("backend.main.get_database_connection")
def test_authenticate_admin_failure_wrong_password(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    hashed_pw = hash_password(TEST_PASSWORD)
    mock_cursor.fetchone.return_value = (hashed_pw,)

    result = main.authenticate_admin(TEST_EMAIL, "wrongpassword", mock_conn)

    assert result["authenticated"] is False

@patch("backend.main.get_database_connection")
def test_authenticate_admin_failure_nonexistent_email(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    mock_cursor.fetchone.return_value = None

    result = main.authenticate_admin("nonexistent@example.com", "any", mock_conn)

    assert result["authenticated"] is False

@patch("backend.main.get_database_connection")
def test_delete_admin(mock_get_conn, mock_conn_cursor):
    mock_conn, mock_cursor = mock_conn_cursor
    mock_get_conn.return_value = mock_conn

    main.delete_admin_from_table(TEST_EMAIL, mock_conn)

    mock_cursor.execute.assert_called_with("DELETE FROM admins WHERE email = %s", (TEST_EMAIL,))
    mock_conn.commit.assert_called_once()
