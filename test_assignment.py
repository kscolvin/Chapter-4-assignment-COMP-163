"""
COMP 163 - Chapter 4 Assignment Tests
Automated grading script for GitHub Classroom

Usage:
    python test_assignment.py              # Run all tests
    python test_assignment.py --test 1     # Run only Test 1
    python test_assignment.py --test 2     # Run only Test 2
    python test_assignment.py --test 3     # Run only Test 3
    python test_assignment.py --test 4     # Run only Test 4
"""

import ast
import sys
import os
import argparse
from unittest.mock import patch

class AssignmentTester:
    def __init__(self, filename):
        self.filename = filename
        
        # Read the student's code
        try:
            with open(filename, 'r') as f:
                self.code = f.read()
            self.tree = ast.parse(self.code)
        except FileNotFoundError:
            print(f"\n❌ ERROR: Could not find {filename}")
            print("Make sure your file is named correctly: [username]_assignment_4.py")
            print("\nExample: If your username is 'jsmith', name it: jsmith_assignment_4.py")
            sys.exit(1)
        except SyntaxError as e:
            print(f"\n❌ SYNTAX ERROR in your code:")
            print(f"   Line {e.lineno}: {e.msg}")
            print(f"\nFix the syntax error and try again.")
            sys.exit(1)
    
    def find_variables(self):
        """Extract all variable assignments from the code"""
        variables = {}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables[target.id] = node.value
        return variables
    
    def check_operators(self, operator_types):
        """Check if specific operators are present in the code"""
        found = []
        for node in ast.walk(self.tree):
            for op_type in operator_types:
                if isinstance(node, op_type):
                    found.append(op_type.__name__)
        return found
    
    def count_if_statements(self):
        """Count if/elif/else structures"""
        if_count = 0
        elif_count = 0
        else_count = 0
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                if_count += 1
                elif_count += len(node.orelse) - (1 if node.orelse and isinstance(node.orelse[0], ast.If) else 0)
                if node.orelse and not isinstance(node.orelse[0], ast.If):
                    else_count += 1
        
        return if_count, elif_count, else_count
    
    def check_nested_ifs(self, min_depth=2):
        """Check for nested if statements"""
        def get_depth(node, current_depth=0):
            max_depth = current_depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.If):
                    depth = get_depth(child, current_depth + 1)
                    max_depth = max(max_depth, depth)
                else:
                    depth = get_depth(child, current_depth)
                    max_depth = max(max_depth, depth)
            return max_depth
        
        max_depth = get_depth(self.tree)
        return max_depth >= min_depth
    
    def test_1_foundation(self):
        """Test 1: Foundation Setup - 15 points"""
        print("\n" + "="*70)
        print("TEST 1: FOUNDATION SETUP")
        print("Points: 15")
        print("="*70)
        
        passed_checks = []
        failed_checks = []
        
        # Check for required variables
        variables = self.find_variables()
        required_vars = ['student_name', 'current_gpa', 'study_hours', 'social_points', 'stress_level']
        
        print("\n📋 CHECKING REQUIRED VARIABLES...")
        print("-" * 70)
        missing_vars = []
        for var_name in required_vars:
            if var_name not in variables:
                missing_vars.append(var_name)
                print(f"  ❌ MISSING: {var_name}")
                failed_checks.append(f"Missing variable: {var_name}")
            else:
                print(f"  ✅ FOUND: {var_name}")
        
        if not missing_vars:
            passed_checks.append("All required variables present")
        
        # Check if code runs without errors
        print("\n🔧 CHECKING IF CODE RUNS...")
        print("-" * 70)
        try:
            with patch('builtins.input', return_value='quit'):
                exec_globals = {}
                exec(self.code, exec_globals)
                print("  ✅ Code runs without errors")
                passed_checks.append("Code executes successfully")
        except Exception as e:
            error_msg = str(e).split('\n')[0][:100]
            print(f"  ❌ Runtime error: {error_msg}")
            failed_checks.append(f"Runtime error: {error_msg}")
        
        # Check for print statements
        print("\n💬 CHECKING FOR OUTPUT STATEMENTS...")
        print("-" * 70)
        has_print = any(isinstance(node, ast.Call) and 
                       isinstance(node.func, ast.Name) and 
                       node.func.id == 'print' 
                       for node in ast.walk(self.tree))
        
        if has_print:
            print("  ✅ Program has print statements")
            passed_checks.append("Program displays output")
        else:
            print("  ❌ No print statements found")
            failed_checks.append("No output statements found")
        
        # Print summary
        print("\n" + "="*70)
        print("TEST 1 RESULTS")
        print("="*70)
        
        if passed_checks:
            print("\n✅ PASSED:")
            for check in passed_checks:
                print(f"   • {check}")
        
        if failed_checks:
            print("\n❌ FAILED:")
            for check in failed_checks:
                print(f"   • {check}")
            print("\n💡 HOW TO FIX:")
            print("   1. Make sure you have ALL required variables:")
            print("      student_name, current_gpa, study_hours, social_points, stress_level")
            print("   2. Check for syntax errors")
            print("   3. Add print statements to display game information")
        
        success = len(failed_checks) == 0
        print("\n" + "="*70)
        if success:
            print("🎉 TEST 1: PASSED (15/15 points)")
        else:
            print(f"⚠️  TEST 1: FAILED ({len(passed_checks)}/{len(passed_checks) + len(failed_checks)} checks passed)")
        print("="*70 + "\n")
        
        return 0 if success else 1
    
    def test_2_course_planning(self):
        """Test 2: Course Planning Decision - 20 points"""
        print("\n" + "="*70)
        print("TEST 2: COURSE PLANNING DECISION")
        print("Points: 20")
        print("="*70)
        
        passed_checks = []
        failed_checks = []
        
        # Check for if/elif/else structure
        if_count, elif_count, else_count = self.count_if_statements()
        
        print("\n🔀 CHECKING CONDITIONAL STRUCTURE...")
        print("-" * 70)
        
        if if_count >= 1:
            print(f"  ✅ Found {if_count} if statement(s)")
            passed_checks.append(f"Has if statements ({if_count} found)")
        else:
            print("  ❌ No if statements found")
            failed_checks.append("No if statements found")
        
        if elif_count >= 1:
            print(f"  ✅ Found {elif_count} elif statement(s)")
            passed_checks.append(f"Has elif statements ({elif_count} found)")
        else:
            print("  ❌ No elif statements found")
            failed_checks.append("No elif statements found")
        
        if else_count >= 1:
            print(f"  ✅ Found {else_count} else statement(s)")
            passed_checks.append(f"Has else statements ({else_count} found)")
        else:
            print("  ❌ No else statements found")
            failed_checks.append("No else statements found")
        
        # Check for comparison operators
        print("\n⚖️  CHECKING COMPARISON OPERATORS...")
        print("-" * 70)
        comparison_ops = [ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq]
        found_ops = self.check_operators(comparison_ops)
        
        if found_ops:
            unique_ops = list(set(found_ops))
            print(f"  ✅ Found comparison operators: {', '.join(unique_ops)}")
            passed_checks.append(f"Uses comparison operators ({len(unique_ops)} types)")
        else:
            print("  ❌ No comparison operators found")
            print("     Missing: >, <, >=, <=, ==, !=")
            failed_checks.append("No comparison operators found")
        
        # Print summary
        print("\n" + "="*70)
        print("TEST 2 RESULTS")
        print("="*70)
        
        if passed_checks:
            print("\n✅ PASSED:")
            for check in passed_checks:
                print(f"   • {check}")
        
        if failed_checks:
            print("\n❌ FAILED:")
            for check in failed_checks:
                print(f"   • {check}")
            print("\n💡 HOW TO FIX:")
            print("   1. Use if/elif/else structure for decision making")
            print("   2. Add comparison operators to check conditions")
            print("      Example: if current_gpa >= 3.0:")
            print("   3. Make sure your choices have different outcomes")
        
        success = len(failed_checks) == 0
        print("\n" + "="*70)
        if success:
            print("🎉 TEST 2: PASSED (20/20 points)")
        else:
            print(f"⚠️  TEST 2: FAILED ({len(passed_checks)}/{len(passed_checks) + len(failed_checks)} checks passed)")
        print("="*70 + "\n")
        
        return 0 if success else 1
    
    def test_3_study_strategy(self):
        """Test 3: Study Strategy Decision - 15 points"""
        print("\n" + "="*70)
        print("TEST 3: STUDY STRATEGY DECISION")
        print("Points: 15")
        print("="*70)
        
        passed_checks = []
        failed_checks = []
        
        # Check for membership operators
        print("\n📝 CHECKING MEMBERSHIP OPERATORS...")
        print("-" * 70)
        
        membership_found = False
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, (ast.In, ast.NotIn)):
                        membership_found = True
                        break
        
        if membership_found:
            print("  ✅ Found membership operators (in/not in)")
            passed_checks.append("Uses membership operators (in/not in)")
        else:
            print("  ❌ No membership operators found")
            print("     Missing: in, not in")
            failed_checks.append("No membership operators found")
        
        # Check for logical operators
        print("\n🔗 CHECKING LOGICAL OPERATORS...")
        print("-" * 70)
        
        logical_ops = [ast.And, ast.Or, ast.Not]
        found_logical = self.check_operators(logical_ops)
        
        if found_logical:
            unique_logical = list(set(found_logical))
            print(f"  ✅ Found logical operators: {', '.join(unique_logical)}")
            passed_checks.append(f"Uses logical operators ({len(unique_logical)} types)")
        else:
            print("  ❌ No logical operators found")
            print("     Missing: and, or, not")
            failed_checks.append("No logical operators found")
        
        # Print summary
        print("\n" + "="*70)
        print("TEST 3 RESULTS")
        print("="*70)
        
        if passed_checks:
            print("\n✅ PASSED:")
            for check in passed_checks:
                print(f"   • {check}")
        
        if failed_checks:
            print("\n❌ FAILED:")
            for check in failed_checks:
                print(f"   • {check}")
            print("\n💡 HOW TO FIX:")
            print("   1. Create a list of valid options")
            print("      Example: subjects = ['Math', 'English', 'History']")
            print("   2. Use 'in' to check if choice is in the list")
            print("      Example: if choice in subjects:")
            print("   3. Use logical operators for complex conditions")
            print("      Example: if gpa > 3.0 and stress < 50:")
        
        success = len(failed_checks) == 0
        print("\n" + "="*70)
        if success:
            print("🎉 TEST 3: PASSED (15/15 points)")
        else:
            print(f"⚠️  TEST 3: FAILED ({len(passed_checks)}/{len(passed_checks) + len(failed_checks)} checks passed)")
        print("="*70 + "\n")
        
        return 0 if success else 1
    
    def test_4_final_assessment(self):
        """Test 4: Final Semester Assessment - 20 points"""
        print("\n" + "="*70)
        print("TEST 4: FINAL SEMESTER ASSESSMENT")
        print("Points: 20")
        print("="*70)
        
        passed_checks = []
        failed_checks = []
        
        # Check for identity operators
        print("\n🆔 CHECKING IDENTITY OPERATORS...")
        print("-" * 70)
        
        has_is = False
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Compare):
                for op in node.ops:
                    if isinstance(op, (ast.Is, ast.IsNot)):
                        has_is = True
                        break
        
        if has_is:
            print("  ✅ Found identity operators (is/is not)")
            passed_checks.append("Uses identity operators (is/is not)")
        else:
            print("  ⚠️  No identity operators found")
            print("     Expected: is, is not")
            failed_checks.append("No identity operators found")
        
        # Check for nested if statements
        print("\n🏗️  CHECKING NESTED IF STATEMENTS...")
        print("-" * 70)
        
        has_nested = self.check_nested_ifs(min_depth=2)
        
        if has_nested:
            print("  ✅ Found nested if statements (2+ levels deep)")
            passed_checks.append("Has nested conditional logic")
        else:
            print("  ❌ No nested if statements found")
            print("     Need at least 2 levels of nesting")
            failed_checks.append("No nested if statements (need 2+ levels)")
        
        # Check for comprehensive concept usage
        print("\n🎨 CHECKING COMPREHENSIVE CONCEPT USAGE...")
        print("-" * 70)
        
        if_count, _, _ = self.count_if_statements()
        has_comparison = bool(self.check_operators([ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq]))
        has_logical = bool(self.check_operators([ast.And, ast.Or, ast.Not]))
        
        if if_count >= 3:
            print(f"  ✅ Multiple conditional branches ({if_count} if statements)")
            passed_checks.append(f"Multiple decision points ({if_count} if statements)")
        else:
            print(f"  ⚠️  Limited conditional branches ({if_count} if statements)")
            failed_checks.append("Need more decision points (3+ if statements)")
        
        if has_comparison and has_logical:
            print("  ✅ Combines comparison and logical operators")
            passed_checks.append("Combines multiple operator types")
        else:
            missing = []
            if not has_comparison:
                missing.append("comparison operators")
            if not has_logical:
                missing.append("logical operators")
            print(f"  ❌ Missing: {', '.join(missing)}")
            failed_checks.append(f"Missing: {', '.join(missing)}")
        
        # Print summary
        print("\n" + "="*70)
        print("TEST 4 RESULTS")
        print("="*70)
        
        if passed_checks:
            print("\n✅ PASSED:")
            for check in passed_checks:
                print(f"   • {check}")
        
        if failed_checks:
            print("\n❌ FAILED:")
            for check in failed_checks:
                print(f"   • {check}")
            print("\n💡 HOW TO FIX:")
            print("   1. Add identity operators for type checking")
            print("      Example: if type(gpa) is float:")
            print("   2. Create nested if statements (if inside if)")
            print("      Example:")
            print("         if gpa >= 3.5:")
            print("             if stress < 40:")
            print("                 # nested logic here")
            print("   3. Create multiple possible endings (3+)")
            print("   4. Combine all concepts learned in this chapter")
        
        success = len(failed_checks) == 0
        print("\n" + "="*70)
        if success:
            print("🎉 TEST 4: PASSED (20/20 points)")
        else:
            print(f"⚠️  TEST 4: FAILED ({len(passed_checks)}/{len(passed_checks) + len(failed_checks)} checks passed)")
        print("="*70 + "\n")
        
        return 0 if success else 1
    
    def run_all_tests(self):
        """Run all tests and generate final report"""
        print("\n" + "="*70)
        print("COMP 163 - CHAPTER 4 ASSIGNMENT: AUTOMATED TEST SUITE")
        print("="*70)
        print("Running all 4 tests...")
        
        results = []
        results.append(("Test 1: Foundation", 15, self.test_1_foundation()))
        results.append(("Test 2: Course Planning", 20, self.test_2_course_planning()))
        results.append(("Test 3: Study Strategy", 15, self.test_3_study_strategy()))
        results.append(("Test 4: Final Assessment", 20, self.test_4_final_assessment()))
        
        # Calculate scores
        total_possible = sum(r[1] for r in results)
        total_earned = sum(r[1] for r in results if r[2] == 0)
        passed = sum(1 for r in results if r[2] == 0)
        failed = len(results) - passed
        
        # Final summary
        print("\n" + "="*70)
        print("FINAL TEST SUMMARY")
        print("="*70)
        
        for name, points, exit_code in results:
            status = "✅ PASSED" if exit_code == 0 else "❌ FAILED"
            earned = points if exit_code == 0 else 0
            print(f"{status}  {name:30} {earned:2}/{points:2} points")
        
        print("-" * 70)
        print(f"Total Automated Score: {total_earned}/{total_possible} points ({(total_earned/total_possible)*100:.1f}%)")
        print(f"Tests Passed: {passed}/4")
        print(f"Tests Failed: {failed}/4")
        
        print("\n" + "="*70)
        if failed == 0:
            print("🎉 CONGRATULATIONS! All automated tests passed!")
            print("\nRemember: This is 70% of your grade.")
            print("Make sure you also have:")
            print("  • Proper header in your Python file (5 points)")
            print("  • Quality comments explaining your logic (10 points)")
            print("  • Descriptive commit messages (5 points)")
            print("  • Complete README.md documentation (10 points)")
        else:
            print("⚠️  Some tests failed. Review the feedback above.")
            print("\nTo see detailed output for a specific test, run:")
            print("  python test_assignment.py --test 1")
            print("  python test_assignment.py --test 2")
            print("  python test_assignment.py --test 3")
            print("  python test_assignment.py --test 4")
        print("="*70 + "\n")
        
        return 1 if failed > 0 else 0

def find_student_file():
    """Find the student's assignment file"""
    python_files = [f for f in os.listdir('.') if f.endswith('_assignment_4.py') and not f.startswith('EXAMPLE')]
    
    if not python_files:
        print("\n❌ ERROR: No assignment file found!")
        print("   Your file must be named: [username]_assignment_4.py")
        print("   Example: jsmith_assignment_4.py")
        sys.exit(1)
    
    if len(python_files) > 1:
        print("\n⚠️  WARNING: Multiple assignment files found:")
        for f in python_files:
            print(f"   • {f}")
        print(f"\nUsing: {python_files[0]}")
    
    return python_files[0]

def main():
    parser = argparse.ArgumentParser(description='Test COMP 163 Chapter 4 Assignment')
    parser.add_argument('--test', type=int, choices=[1, 2, 3, 4],
                       help='Run specific test (1-4)')
    args = parser.parse_args()
    
    # Find student file
    student_file = find_student_file()
    tester = AssignmentTester(student_file)
    
    # Run requested test(s)
    if args.test == 1:
        exit_code = tester.test_1_foundation()
    elif args.test == 2:
        exit_code = tester.test_2_course_planning()
    elif args.test == 3:
        exit_code = tester.test_3_study_strategy()
    elif args.test == 4:
        exit_code = tester.test_4_final_assessment()
    else:
        exit_code = tester.run_all_tests()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
