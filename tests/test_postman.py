import subprocess
import json


def run_newman_collection(data_file, collection_name, test_name):
    """
    Runs a Newman collection with the specified data file and returns the result summary and exit code.
    """
    try:
        newman_path = r"C:\Users\User\AppData\Roaming\npm\newman.cmd"  # Adjust this path if needed

        # Run Newman with the specified collection and data file
        result = subprocess.run(
            [
                newman_path,
                "run",
                f"collections/{collection_name}",
                "--iteration-data",
                data_file,
                "--reporters",
                "json",
                "--reporter-json-export",
                f"reports/{test_name}_summary.json",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Print the output for debugging purposes
        print(f"--- {test_name} ---")
        print("Standard Output:\n", result.stdout)
        print("Standard Error:\n", result.stderr)

        # Load the JSON report
        with open(f"reports/{test_name}_summary.json", "r", encoding="utf-8") as file:
            summary = json.load(file)

        return summary, result.returncode

    except FileNotFoundError:
        print("Newman executable not found at the specified path.")
        return None, 1
    except Exception as e:
        print(f"Error running Newman: {e}")
        return None, 1


# 1. Test: Status Code Verification
def test_status_code():
    data_file = "data/status_codes.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Status_Code_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Status Code Test failed with exit code {exit_code}"

    # Validate status codes from Newman response
    for execution in summary["run"]["executions"]:
        response_code = execution["response"]["code"]
        expected_code = execution["assertions"][0]["assertion"]
        assert response_code == int(expected_code), f"Expected {expected_code}, got {response_code}"


# 2. Test: Response Time Verification
def test_response_time():
    data_file = "data/status_codes.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Response_Time_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Response Time Test failed with exit code {exit_code}"

    # Verify that response time is under the threshold (e.g., 500 ms)
    for execution in summary["run"]["executions"]:
        response_time = execution["response"]["responseTime"]
        assert response_time < 500, f"Response time too high: {response_time} ms"


# 3. Test: Content-Type Verification
def test_content_type():
    data_file = "data/status_codes.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Content_Type_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Content-Type Test failed with exit code {exit_code}"

    # Verify that Content-Type is application/json
    for execution in summary["run"]["executions"]:
        headers = execution["response"]["headers"]
        content_type = next((header["value"] for header in headers if header["key"] == "Content-Type"), None)
        assert content_type == "application/json", f"Invalid Content-Type: {content_type}"


# 4. Test: Data Validation
def test_data_validation():
    data_file = "data/user_data.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Data_Validation_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Data Validation Test failed with exit code {exit_code}"

    # Validate name and email in the response body
    for execution in summary["run"]["executions"]:
        response_body = json.loads(execution["response"]["stream"])
        expected_name = execution["assertions"][0]["assertion"]
        expected_email = execution["assertions"][1]["assertion"]

        assert response_body["name"] == expected_name, f"Expected name '{expected_name}', got '{response_body['name']}'"
        assert response_body["email"] == expected_email, f"Expected email '{expected_email}', got '{response_body['email']}'"


# 5. Test: Negative Testing
def test_negative():
    data_file = "data/negative_tests.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Negative_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Negative Test failed with exit code {exit_code}"

    # Verify expected error codes for invalid inputs
    for execution in summary["run"]["executions"]:
        response_code = execution["response"]["code"]
        expected_code = execution["assertions"][0]["assertion"]
        assert response_code == int(expected_code), f"Expected {expected_code}, got {response_code}"


# 6. Test: Parameterized Testing
def test_parameterized():
    data_file = "data/parameterized_tests.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Parameterized_Test"

    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Parameterized Test failed with exit code {exit_code}"

    # Validate responses for different parameter values
    for execution in summary["run"]["executions"]:
        response_body = json.loads(execution["response"]["stream"])
        assert "id" in response_body, "ID not found in response"



#Pagination Testing
def test_pagination():
    data_file = "data/pagination_tests.csv"
    collection_name = "JSONPlaceholder.postman_collection.json"
    test_name = "Pagination_Test"

    # Run the Newman collection
    summary, exit_code = run_newman_collection(data_file, collection_name, test_name)
    assert exit_code == 0, f"Pagination Test failed with exit code {exit_code}"

    # Debug the summary output
    print("Summary:", json.dumps(summary, indent=2))

    # Validate the responses
    for execution in summary["run"]["executions"]:
        request_name = execution["item"]["name"]  # Get the request name
        response_body = json.loads(execution["response"]["stream"])
        expected_count = int(execution["assertions"][0]["assertion"])  # Get expected count

        # Validate the number of items in the response
        assert len(response_body) == expected_count, f"{request_name}: Expected {expected_count} items, got {len(response_body)}"




# PyTest Entry Point
if __name__ == "__main__":
    test_status_code()
    test_response_time()
    test_content_type()
    test_data_validation()
    test_negative()
    test_parameterized()
    test_pagination()
