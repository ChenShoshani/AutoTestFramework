#!/bin/bash
echo "Running Automation Tests..."
echo

echo "Installing dependencies..."
pip install -r requirements.txt
echo

echo "Running UI Tests..."
pytest tests/test_ui/ -m ui -v
echo

echo "Running API Tests..."
pytest tests/test_api/ -m api -v
echo

echo "Running All Tests with HTML Report..."
pytest tests/ --html=reports/test_report.html --self-contained-html -v
echo

echo "Tests completed! Check reports/test_report.html for results." 