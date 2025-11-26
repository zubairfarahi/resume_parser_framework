# API Testing Command

Create comprehensive API tests for: $ARGUMENTS

## Testing Strategy

Test the following API endpoints and scenarios based on $ARGUMENTS:

1. **Happy Path Testing**:
   - Valid request formats
   - Expected response structures
   - Proper HTTP status codes (200, 201, 204)
   - Correct data serialization/deserialization

2. **Error Handling Testing**:
   - Invalid request payloads (400 Bad Request)
   - Authentication failures (401 Unauthorized)
   - Authorization edge cases (403 Forbidden)
   - Resource not found (404 Not Found)
   - Rate limiting scenarios (429 Too Many Requests)
   - Server errors (500 Internal Server Error)

3. **Edge Cases**:
   - Boundary value testing
   - Large payload handling (file size limits)
   - Concurrent request handling
   - Network timeout scenarios
   - Malformed data handling

4. **Security Testing**:
   - File upload validation
   - Input sanitization
   - Path traversal prevention
   - API key validation

## Test Structure Template

Create tests in `tests/api/test_{endpoint_name}.py`:

```python
"""API tests for {endpoint_name} endpoint."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app  # or wherever your FastAPI app is
from app.core.models.resume_data import ResumeData


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_resume_file():
    """Provide sample resume file for testing."""
    return Path("tests/fixtures/sample_resume.pdf")


@pytest.fixture
def valid_auth_headers():
    """Provide valid authentication headers."""
    return {"Authorization": "Bearer valid_token_here"}


class Test{EndpointName}API:
    """Test suite for {endpoint_name} API endpoint."""

    def test_post_endpoint_with_valid_data(self, client, sample_resume_file, valid_auth_headers):
        """Test POST /{endpoint} with valid data returns 200/201."""
        with open(sample_resume_file, "rb") as f:
            response = client.post(
                "/{endpoint}",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers=valid_auth_headers
            )

        assert response.status_code == 200
        assert "name" in response.json()
        assert "email" in response.json()
        assert "skills" in response.json()

    def test_post_endpoint_with_invalid_file_type(self, client, valid_auth_headers):
        """Test POST /{endpoint} with invalid file type returns 400."""
        invalid_file = b"Not a valid PDF or DOCX file"

        response = client.post(
            "/{endpoint}",
            files={"file": ("invalid.txt", invalid_file, "text/plain")},
            headers=valid_auth_headers
        )

        assert response.status_code == 400
        assert "error" in response.json()

    def test_post_endpoint_with_file_too_large(self, client, valid_auth_headers):
        """Test POST /{endpoint} with file exceeding size limit returns 413."""
        # Create file larger than MAX_FILE_SIZE
        large_file = b"x" * (11 * 1024 * 1024)  # 11MB

        response = client.post(
            "/{endpoint}",
            files={"file": ("large.pdf", large_file, "application/pdf")},
            headers=valid_auth_headers
        )

        assert response.status_code == 413
        assert "File too large" in response.json()["error"]

    def test_post_endpoint_requires_authentication(self, client, sample_resume_file):
        """Test POST /{endpoint} without auth returns 401."""
        with open(sample_resume_file, "rb") as f:
            response = client.post(
                "/{endpoint}",
                files={"file": ("resume.pdf", f, "application/pdf")}
            )

        assert response.status_code == 401
        assert "Unauthorized" in response.json()["error"]

    def test_post_endpoint_with_invalid_token(self, client, sample_resume_file):
        """Test POST /{endpoint} with invalid token returns 401."""
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        with open(sample_resume_file, "rb") as f:
            response = client.post(
                "/{endpoint}",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers=invalid_headers
            )

        assert response.status_code == 401

    def test_post_endpoint_with_missing_file(self, client, valid_auth_headers):
        """Test POST /{endpoint} without file returns 422."""
        response = client.post(
            "/{endpoint}",
            headers=valid_auth_headers
        )

        assert response.status_code == 422
        assert "field required" in response.json()["detail"][0]["msg"].lower()

    @pytest.mark.parametrize("malformed_data", [
        b"",  # Empty file
        b"\\x00\\x01\\x02",  # Binary garbage
        b"<script>alert('xss')</script>",  # XSS attempt
    ])
    def test_post_endpoint_with_malformed_data(
        self, client, valid_auth_headers, malformed_data
    ):
        """Test POST /{endpoint} with malformed data is handled gracefully."""
        response = client.post(
            "/{endpoint}",
            files={"file": ("malformed.pdf", malformed_data, "application/pdf")},
            headers=valid_auth_headers
        )

        # Should return 400 or 422, not crash
        assert response.status_code in [400, 422]

    def test_get_endpoint_returns_resource(self, client, valid_auth_headers):
        """Test GET /{endpoint}/{id} returns resource with 200."""
        resource_id = "test-id-123"

        response = client.get(
            f"/{endpoint}/{resource_id}",
            headers=valid_auth_headers
        )

        assert response.status_code == 200
        assert response.json()["id"] == resource_id

    def test_get_endpoint_resource_not_found(self, client, valid_auth_headers):
        """Test GET /{endpoint}/{id} with invalid ID returns 404."""
        response = client.get(
            "/{endpoint}/non-existent-id",
            headers=valid_auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["error"].lower()

    def test_get_endpoint_list_with_pagination(self, client, valid_auth_headers):
        """Test GET /{endpoint} with pagination parameters."""
        response = client.get(
            "/{endpoint}?page=1&limit=10",
            headers=valid_auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert len(data["items"]) <= 10

    @pytest.mark.slow
    def test_concurrent_requests_handling(self, client, sample_resume_file, valid_auth_headers):
        """Test API handles concurrent requests correctly."""
        import concurrent.futures

        def make_request():
            with open(sample_resume_file, "rb") as f:
                return client.post(
                    "/{endpoint}",
                    files={"file": ("resume.pdf", f, "application/pdf")},
                    headers=valid_auth_headers
                )

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [f.result() for f in futures]

        # All requests should succeed or fail gracefully
        for response in responses:
            assert response.status_code in [200, 201, 429, 503]

    def test_rate_limiting(self, client, sample_resume_file, valid_auth_headers):
        """Test rate limiting is enforced (if applicable)."""
        responses = []

        # Make multiple rapid requests
        for _ in range(100):
            with open(sample_resume_file, "rb") as f:
                response = client.post(
                    "/{endpoint}",
                    files={"file": ("resume.pdf", f, "application/pdf")},
                    headers=valid_auth_headers
                )
                responses.append(response.status_code)

        # Should get at least one 429 (Too Many Requests)
        assert 429 in responses, "Rate limiting not enforced"

    def test_response_time_within_acceptable_range(
        self, client, sample_resume_file, valid_auth_headers
    ):
        """Test response time is within acceptable range."""
        import time

        start_time = time.time()

        with open(sample_resume_file, "rb") as f:
            response = client.post(
                "/{endpoint}",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers=valid_auth_headers
            )

        duration = time.time() - start_time

        assert response.status_code == 200
        assert duration < 15.0, f"Request took {duration}s, expected < 15s"


# Integration tests
class Test{EndpointName}Integration:
    """Integration tests for {endpoint_name} endpoint."""

    def test_end_to_end_resume_parsing(self, client, valid_auth_headers):
        """Test complete end-to-end resume parsing flow."""
        # 1. Upload resume
        resume_file = Path("tests/fixtures/sample_resume.pdf")
        with open(resume_file, "rb") as f:
            upload_response = client.post(
                "/{endpoint}",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers=valid_auth_headers
            )

        assert upload_response.status_code == 200
        parsed_data = upload_response.json()

        # 2. Verify parsed data
        assert parsed_data["name"] is not None
        assert parsed_data["email"] is not None
        assert len(parsed_data["skills"]) > 0

        # 3. Get parsed resume by ID (if applicable)
        resume_id = parsed_data.get("id")
        if resume_id:
            get_response = client.get(
                f"/{endpoint}/{resume_id}",
                headers=valid_auth_headers
            )
            assert get_response.status_code == 200
            assert get_response.json() == parsed_data
```

## Usage Examples

### Test a specific endpoint

```bash
pytest tests/api/test_{endpoint_name}.py -v
```

### Run with coverage

```bash
pytest tests/api/test_{endpoint_name}.py --cov=app --cov-report=html
```

### Run only fast tests (skip slow tests)

```bash
pytest tests/api/test_{endpoint_name}.py -v -m "not slow"
```

### Run with detailed output

```bash
pytest tests/api/test_{endpoint_name}.py -vv -s
```

## Additional Test Utilities

Create test utilities in `tests/utils/api_helpers.py`:

```python
"""Helper utilities for API testing."""

from typing import Dict, Any
from pathlib import Path


def create_test_file(content: bytes, filename: str = "test.pdf") -> Path:
    """Create a temporary test file."""
    test_file = Path(f"/tmp/{filename}")
    test_file.write_bytes(content)
    return test_file


def assert_valid_resume_data(data: Dict[str, Any]) -> None:
    """Assert that response data matches ResumeData schema."""
    assert "name" in data
    assert "email" in data
    assert "skills" in data
    assert isinstance(data["skills"], list)


def create_auth_headers(token: str) -> Dict[str, str]:
    """Create authentication headers."""
    return {"Authorization": f"Bearer {token}"}
```

## Notes

- Use `@pytest.mark.slow` for tests that take longer than 1 second
- Use `@pytest.mark.integration` for integration tests
- Mock external API calls (LLM providers) in unit tests
- Use fixtures for common test data and setup
- Follow AAA pattern: Arrange, Act, Assert
- Test both success and failure scenarios
- Include security and performance tests
