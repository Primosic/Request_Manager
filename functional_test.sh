#!/bin/bash

# ==========================================
# Request Manager API Functional Tests
# ==========================================

# Color definitions for output
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# Set the base API URL
HOST="localhost"
PORT="8000"
BASE_URL="http://${HOST}:${PORT}/api"
CHECK_URL="http://${HOST}:${PORT}/api"

# Track test results
total_tests=0
passed_tests=0

# Read request ID from file if it exists
REQUEST_ID_FILE="request_id.txt"
if [ -f "$REQUEST_ID_FILE" ]; then
    DEFAULT_ID=$(cat "$REQUEST_ID_FILE")
    echo -e "${BLUE}Found request ID in file:${NC} $DEFAULT_ID"
else
    # Default request ID (in case create request fails)
    DEFAULT_ID="1"
    echo -e "${YELLOW}No request ID file found. Using default ID: ${DEFAULT_ID}${NC}"
fi

# ==========================================
# Helper Functions
# ==========================================

# Function to display test results
display_result() {
    local test_name="$1"
    local status_code="$2"
    local expected_code="$3"
    
    total_tests=$((total_tests+1))
    
    echo -e "${BLUE}Test:${NC} $test_name"
    echo -e "${BLUE}Status Code:${NC} $status_code (Expected: $expected_code)"
    
    if [ "$status_code" -eq "$expected_code" ]; then
        echo -e "${GREEN}\u2713 Test Passed${NC}"
        return 0
    else
        echo -e "${RED}\u2717 Test Failed${NC}"
        return 1
    fi
}

# ==========================================
# Check if server is running
# ==========================================
echo -e "${YELLOW}=== Request Manager API Functional Tests ===${NC}\n"

echo "Checking if the server is running at: ${CHECK_URL}"

response=$(curl -s -o /dev/null -w "%{http_code}" ${CHECK_URL} -m 5)
if [ "$response" != "200" ] && [ "$response" != "404" ]; then
    echo -e "${RED}Error: Server is not running at ${CHECK_URL}${NC}"
    echo -e "${YELLOW}Please start the server before running the tests.${NC}"
    exit 1
fi

echo -e "\nRunning tests against: ${BASE_URL}\n"

# ==========================================
# Test 1: Create Request
# ==========================================
echo -e "${BLUE}1. Testing Create Request endpoint...${NC}"

response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/request" \
    -H "Content-Type: application/json" \
    -d '{
        "nm_system": "lab_a",
        "id_person": "123456",
        "tp_document": "CC"
    }')

# Split response into body and status code
response_body=$(echo "$response" | head -n 1)
status_code=$(echo "$response" | tail -n 1)

echo -e "${BLUE}Response:${NC} $response_body"
if display_result "Create Request" "$status_code" "201"; then
    passed_tests=$((passed_tests+1))
    # Extract request ID
    id_request=$(echo "$response_body" | grep -o '"id_request":[0-9]*' | cut -d ':' -f2)
    if [ -z "$id_request" ]; then
        id_request=$DEFAULT_ID
        echo -e "${YELLOW}Could not extract ID from response. Using ID from file: ${DEFAULT_ID}${NC}"
    fi
else
    # Use default ID if request creation failed
    id_request=$DEFAULT_ID
    echo -e "${YELLOW}Using ID from file or default: ${DEFAULT_ID} for subsequent tests.${NC}"
fi

echo -e "\n${BLUE}Using ID:${NC} $id_request for subsequent tests\n"

# ==========================================
# Test 2: Update Verification Status
# ==========================================
echo -e "${BLUE}2. Testing Update Verification Status endpoint...${NC}"

response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/verify" \
    -H "Content-Type: application/json" \
    -d "{
        \"id_request\": $id_request,
        \"id_system_process\": 2,
        \"st_system_verify\": 1,
        \"ds_reason_verify_refuse\": null
    }")

response_body=$(echo "$response" | head -n 1)
status_code=$(echo "$response" | tail -n 1)

echo -e "${BLUE}Response:${NC} $response_body"
if display_result "Update Verification Status" "$status_code" "200"; then
    passed_tests=$((passed_tests+1))
fi

# ==========================================
# Test 3: Update Request Status
# ==========================================
echo -e "\n${BLUE}3. Testing Update Request Status endpoint...${NC}"

response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/request/status" \
    -H "Content-Type: application/json" \
    -d "{
        \"id_request\": $id_request,
        \"id_system_process\": 2,
        \"st_system_request\": 1
    }")

response_body=$(echo "$response" | head -n 1)
status_code=$(echo "$response" | tail -n 1)

echo -e "${BLUE}Response:${NC} $response_body"
if display_result "Update Request Status" "$status_code" "200"; then
    passed_tests=$((passed_tests+1))
fi

# ==========================================
# Test 4: Get Request Status
# ==========================================
echo -e "\n${BLUE}4. Testing Get Request Status endpoint...${NC}"

response=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/request/$id_request/status" \
    -H "Content-Type: application/json")

response_body=$(echo "$response" | head -n 1)
status_code=$(echo "$response" | tail -n 1)

echo -e "${BLUE}Response:${NC} $response_body"
if display_result "Get Request Status" "$status_code" "200"; then
    passed_tests=$((passed_tests+1))
fi

# ==========================================
# Test Summary
# ==========================================
echo -e "${YELLOW}=== Test Summary ===${NC}"
echo -e "${BLUE}Total Tests:${NC} $total_tests"
echo -e "${BLUE}Passed Tests:${NC} $passed_tests"
echo -e "${BLUE}Failed Tests:${NC} $((total_tests - passed_tests))"

if [ "$passed_tests" -eq "$total_tests" ]; then
    echo -e "\n${GREEN}All tests passed successfully!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed!${NC}"
    exit 1
fi