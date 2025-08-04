#!/usr/bin/env python3
import json
import os

def load_students():
    if os.path.exists('students.json'):
        with open('students.json', 'r') as f:
            return json.load(f)
    return []

def generate_roll_number():
    students = load_students()
    print(f"Total students: {len(students)}")
    
    if not students:
        return "2024001"
    
    existing_rolls = []
    for student in students:
        try:
            if 'roll_number' in student and student['roll_number']:
                roll_num = int(student['roll_number'][3:])
                existing_rolls.append(roll_num)
                print(f"Found roll: {student['roll_number']} -> {roll_num}")
        except (ValueError, KeyError, IndexError) as e:
            print(f"Invalid roll for {student.get('name', 'Unknown')}: {e}")
            continue
    
    print(f"All existing rolls: {existing_rolls}")
    
    if not existing_rolls:
        return "2024001"
    
    existing_rolls = sorted(existing_rolls)
    next_roll = 1
    for roll in existing_rolls:
        if roll == next_roll:
            next_roll += 1
        else:
            break
    
    print(f"Next roll number: {next_roll}")
    result = f"2024{next_roll:03d}"
    print(f"Final result: {result}")
    return result

if __name__ == "__main__":
    print("=== Testing Roll Number Generation ===")
    students = load_students()
    print("\nCurrent students:")
    for s in students:
        print(f"  {s['name']}: {s['roll_number']}")
    
    print(f"\nNext roll number would be: {generate_roll_number()}") 