#!/usr/bin/env python3
"""
Test script to debug roll number generation
"""

import json
import os

def load_students():
    """Load students from JSON file"""
    if os.path.exists('students.json'):
        with open('students.json', 'r') as f:
            return json.load(f)
    return []

def generate_roll_number():
    """Generate a unique roll number"""
    students = load_students()
    if not students:
        return "2024001"
    
    # Get all existing roll numbers and find the next available one
    existing_rolls = []
    for student in students:
        try:
            roll_num = int(student['roll_number'][3:])
            existing_rolls.append(roll_num)
        except (ValueError, KeyError, IndexError):
            # Skip invalid roll numbers
            continue
    
    if not existing_rolls:
        return "2024001"
    
    existing_rolls.sort()
    print(f"Existing roll numbers: {existing_rolls}")
    
    # Find the first gap or use the next number after the highest
    next_roll = 1
    for roll in existing_rolls:
        if roll == next_roll:
            next_roll += 1
        else:
            break
    
    # Ensure we don't exceed 999 students
    if next_roll > 999:
        raise ValueError("Maximum number of students (999) reached")
    
    result = f"2024{next_roll:03d}"
    print(f"Generated roll number: {result}")
    return result

if __name__ == "__main__":
    print("Testing roll number generation...")
    students = load_students()
    print(f"Current students: {students}")
    next_roll = generate_roll_number()
    print(f"Next roll number: {next_roll}") 