# AI Automated Testing Framework for a Coupled DEVS Model

## Overview
This project is an **automated testing framework** designed to verify the **supervisory controller** of an autonomous helicopter. The framework models the controller as a **coupled DEVS (Discrete Event System Specification) system** and uses **GPT-4o** to generate test cases, enabling rigorous integration and behavior testing across various operational scenarios.

---

## Features
- **Coupled DEVS model testing**: Verify the interaction of multiple subcomponents in the helicopter’s supervisory controller.  
- **Automated test case generation**: Use AI-driven techniques to generate diverse and boundary-focused test inputs.  
- **Scenario simulation**: Simulate mission-critical events, including edge cases, unexpected inputs, and failure modes.  
- **Results validation**: Compare expected vs. actual behavior to identify system deviations or bugs.  
- **Extensible framework**: Modular design allows adding new test scenarios, controllers, or AI test generators.

---

## Technologies Used
- **Programming Languages**: Python, C++  
- **Simulation/Modeling**: Cadmium DEVS simulator  
- **AI Tools**: OpenAI API (GPT-4o)  
- **Testing Methodology**: Integration testing, boundary analysis, black-box testing  
- **Data Analysis**: CSV/JSON test result logging, automated report generation  

---

## Installation
1. Clone the repository:  
```bash
git clone https://github.com/Areej504/CapstoneProject_vm.git
```
2. Navigate to the project folder:
```bash
cd CapstoneProject_vm
```
3. Install required Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To execute the automated testing framework, simply run:
```bash
python run_td.py
```
All test scenarios and configurations are handled within the framework, and results are automatically saved in the results/ folder.

## Contributors
Areej Mahmoud

Mahnoor Fatima

Javeria Sohail
