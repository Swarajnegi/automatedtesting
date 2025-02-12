# main.py

import logging
from web_testing import run_web_tests, save_test_results
from failure_classifier import train_failure_classifier, classify_failure

def main():
    # Run automated web tests and save the results
    logging.info("Starting automated web tests...")
    results = run_web_tests()
    save_test_results(results)
    
    # Train the AI failure classifier using the test results
    logging.info("Training failure classifier...")
    train_failure_classifier()
    
    # Example: classify a sample load time
    sample_load_time = 5.2  # Replace with actual load time as needed
    classification = classify_failure(sample_load_time)
    logging.info(f"Sample Load Time Classification: {classification}")

if __name__ == "__main__":
    main()
