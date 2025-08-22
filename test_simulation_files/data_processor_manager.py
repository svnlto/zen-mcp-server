#!/usr/bin/env python3
import json
import os
from datetime import datetime


# Code smell: Large class with multiple responsibilities
class DataProcessorManager:
    def __init__(self, config_file):
        self.config = self._load_config(config_file)
        self.processed_count = 0
        self.error_count = 0
        self.log_file = "processing.log"

    def _load_config(self, config_file):
        """Load configuration from file"""
        with open(config_file, "r") as f:
            return json.load(f)

    # Code smell: Long method doing too many things (decompose opportunity)
    def process_user_data(self, user_data, validation_rules, output_format):
        """Process user data with validation and formatting"""
        # Validation logic
        if not user_data:
            print("Error: No user data")  # Code smell: print instead of logging
            return None

        if not isinstance(user_data, dict):
            print("Error: Invalid data format")
            return None

        # Check required fields
        required_fields = ["name", "email", "age"]
        for field in required_fields:
            if field not in user_data:
                print(f"Error: Missing field {field}")
                return None

        # Apply validation rules
        for rule in validation_rules:
            if rule["field"] == "email":
                if "@" not in user_data["email"]:  # Code smell: simple validation
                    print("Error: Invalid email")
                    return None
            elif rule["field"] == "age":
                if user_data["age"] < 18:  # Code smell: magic number
                    print("Error: Age too young")
                    return None

        # Data processing
        processed_data = {}
        processed_data["full_name"] = user_data["name"].title()
        processed_data["email_domain"] = user_data["email"].split("@")[1]
        processed_data["age_category"] = "adult" if user_data["age"] >= 18 else "minor"

        # Code smell: Duplicate date formatting logic
        if output_format == "json":
            processed_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = json.dumps(processed_data, ensure_ascii=False)
        elif output_format == "csv":
            processed_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = f"{processed_data['full_name']},{processed_data['email_domain']},{processed_data['age_category']}"
        else:
            processed_data["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = str(processed_data)

        # Logging and statistics
        self.processed_count += 1
        with open(self.log_file, "a") as f:  # Code smell: file handling without context
            f.write(f"Processed: {user_data['name']} at {datetime.now()}\n")

        return result

    # Code smell: Another long method (decompose opportunity)
    def batch_process_files(self, file_list, output_dir):
        """Process multiple files in batch"""
        results = []

        for file_path in file_list:
            # File validation
            if not os.path.exists(file_path):
                print(f"Error: File {file_path} not found")
                continue

            if not file_path.endswith(".json"):
                print(f"Error: File {file_path} is not JSON")
                continue

            # Read and process file
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Code smell: Nested loops and complex logic
                for user_id, user_data in data.items():
                    if isinstance(user_data, dict):
                        # Duplicate validation logic from process_user_data
                        if "name" in user_data and "email" in user_data:
                            if "@" in user_data["email"]:
                                # More processing...
                                processed = {
                                    "id": user_id,
                                    "name": user_data["name"].title(),
                                    "email": user_data["email"].lower(),
                                }
                                results.append(processed)

                # Write output file
                output_file = os.path.join(output_dir, f"processed_{os.path.basename(file_path)}")
                with open(output_file, "w") as f:
                    json.dump(results, f, indent=2)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                self.error_count += 1

        return results

    # Code smell: Method doing file I/O and business logic
    def generate_report(self):
        """Generate processing report"""
        report_data = {
            "total_processed": self.processed_count,
            "total_errors": self.error_count,
            "success_rate": (
                (self.processed_count / (self.processed_count + self.error_count)) * 100
                if (self.processed_count + self.error_count) > 0
                else 0
            ),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Write to multiple formats (code smell: duplicate logic)
        with open("report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        with open("report.txt", "w") as f:
            f.write(f"Processing Report\n")
            f.write(f"================\n")
            f.write(f"Total Processed: {report_data['total_processed']}\n")
            f.write(f"Total Errors: {report_data['total_errors']}\n")
            f.write(f"Success Rate: {report_data['success_rate']:.2f}%\n")
            f.write(f"Generated: {report_data['generated_at']}\n")

        return report_data


# Code smell: Utility functions that could be in a separate module
def validate_email(email):
    """Simple email validation"""
    return "@" in email and "." in email


def format_name(name):
    """Format name to title case"""
    return name.title() if name else ""


def calculate_age_category(age):
    """Calculate age category"""
    if age < 18:
        return "minor"
    elif age < 65:
        return "adult"
    else:
        return "senior"
