# Aircraft Maintenance Compliance System

This project provides two different approaches to determine whether an aircraft is affected by Airworthiness Directives (ADs): a **Rule-Based Approach** and an **Agentic Approach** using Google's Agent Development Kit (ADK).

## Project Overview

The system checks aircraft compliance against maintenance requirements defined in FAA and EASA Airworthiness Directives. It determines if a specific aircraft model is affected by an AD, considering modifications and exceptions.

---

## Approach 1: Rule-Based System

**Location:** `rulebased_approach/main.py`

### Description

A traditional rule-based system that uses hard-coded rules to check aircraft compliance. Rules are defined as Python dictionaries containing AD numbers, affected aircraft models, and their exceptions (modifications that exempt an aircraft from the AD).

### How It Works

1. **Rules Definition**: Each rule contains:
   - AD identifier (e.g., "FAA AD 2025-23-53", "EASA AD 2025-0254")
   - List of affected aircraft models
   - Exceptions (modifications that exempt the aircraft)

2. **Compliance Check**: The `check_rules()` function:
   - Takes an aircraft with its model and current modifications
   - Iterates through all defined rules
   - Matches the aircraft model against rule criteria
   - Checks if any exempting modifications are present
   - Returns compliance status with reasoning

### Supported ADs

- **FAA AD 2025-23-53**: Affects MD-11, DC-10, MD-10, and KC-10 variants (no exceptions)
- **EASA AD 2025-0254**: Affects A320 and A321 variants with modification exceptions

### Usage

```powershell
python rulebased_approach/main.py
```

### Pros
- Fast and deterministic
- Easy to debug and understand
- No external dependencies
- Complete control over logic

### Cons
- Requires manual rule creation for each AD
- No flexibility for natural language queries
- Difficult to scale with many ADs
- Requires code changes to update rules

---

## Approach 2: Agentic System

**Location:** `agentic/`

### Description

An AI-powered system using Google's Agent Development Kit (ADK) that employs multiple specialized agents to read maintenance documents, extract rules, and determine compliance dynamically.

### Architecture

#### Single Agent (`single_agent/agent.py`)
A simplified version with one agent:
- **root_agent**: Acts as an Aircraft Maintenance Compliance Officer
- Directly processes documents and determines compliance
- Outputs JSON format with aircraft model, affected status, and reasoning

#### Multi-Agent System (`multi_agents/agent.py`)
An advanced system with specialized agents and quality control:

1. **document_reader**: 
   - Reads maintenance documents
   - Extracts text segments defining affected/excluded aircraft
   - Focuses on aircraft modifications and exceptions

2. **json_rule_maker**:
   - Converts extracted text into structured JSON rules
   - Follows schema: `{"ad": string, "aircraft": [{"aircraft_model": {"exceptions": [string]}}]}`
   - Lists all aircraft models with their exceptions

3. **compliance_reviewer**:
   - Verifies JSON rule correctness
   - Compares against original document text
   - Outputs "pass" or "fail"

4. **CheckStatusAndEscalate**:
   - Monitors compliance reviewer output
   - Decides whether to continue refinement or stop

5. **refinement_loop**:
   - Ensures rule accuracy through iterative refinement
   - Maximum 5 iterations
   - Continues until compliance reviewer approves

6. **root_agent**:
   - Main coordinator
   - Determines final compliance status
   - Provides reasoning for decisions

### Setup

1. Install dependencies:
```powershell
pip install -r agentic/requirements.txt
```

2. Run the ADK web interface:
```powershell
cd agentic
adk web
```

## Getting Started

### Rule-Based Approach
```powershell
# Navigate to project root
cd soji-challenge

# Run the rule-based system
python rulebased_approach/main.py
```

### Agentic Approach
```powershell
# Install dependencies
pip install -r agentic/requirements.txt

# Navigate to agentic folder
cd agentic

# Launch ADK web interface
adk web

```
upload both of EASA documents and add this as the prompt
`aircrafts = [
        {
            "aircraft model": "MD-11",
            "MSN": "48123",
            "modifications": []
        },
        {
            "aircraft model": "DC-10-30F",
            "MSN": "47890",
            "modifications": []
        },
        {
            "aircraft model": "Boeing 737-800",
            "MSN": "30123",
            "modifications": []
        },
        {
            "aircraft model": "A320-214",
            "MSN": "5234",
            "modifications": []
        },
        {
            "aircraft model": "A320-232",
            "MSN": "6789",
            "modifications": ["mod 24591 (production)"]
        },
        {
            "aircraft model": "A320-214",
            "MSN": "7456",
            "modifications": ["SB A320-57-1089 Rev 04"]
        },
        {
            "aircraft model": "A321-111",
            "MSN": "8123",
            "modifications": []
        },
        {
            "aircraft model": "A321-112",
            "MSN": "364",
            "modifications": ["mod 24977 (production)"]
        },
        {
            "aircraft model": "A319-100",
            "MSN": "9234",
            "modifications": []
        },
        {
            "aircraft model": "MD-10-10F",
            "MSN": "46234",
            "modifications": []
        },

        
    ]`
