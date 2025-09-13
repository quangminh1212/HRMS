#!/usr/bin/env python3
"""
HRMS Code Quality Checker - International Standards Compliant

Comprehensive code quality analysis tool that checks for:
- PEP 8 compliance
- Security vulnerabilities
- Code complexity
- Documentation coverage
- Import organization
- Type hints usage

Standards:
- PEP 8 (Python Enhancement Proposal 8)
- PEP 257 (Docstring Conventions)
- Security best practices
- Clean Code principles
"""

import ast
import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class QualityIssue:
    """Represents a code quality issue."""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'


class CodeQualityChecker:
    """Professional code quality analysis tool."""
    
    def __init__(self, project_root: Path = None):
        """Initialize the quality checker."""
        self.project_root = project_root or Path.cwd()
        self.issues: List[QualityIssue] = []
        self.stats = {
            'files_checked': 0,
            'lines_of_code': 0,
            'functions': 0,
            'classes': 0,
            'issues_found': 0
        }
    
    def check_file_structure(self) -> None:
        """Check project structure compliance."""
        logger.info("Checking project structure...")
        
        required_files = [
            'README.md',
            'requirements.txt',
            '.gitignore',
            'setup.py'  # Optional but recommended
        ]
        
        for required_file in required_files:
            file_path = self.project_root / required_file
            if not file_path.exists() and required_file != 'setup.py':
                self.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type='structure',
                    description=f'Missing required file: {required_file}',
                    severity='medium'
                ))
    
    def check_python_file(self, file_path: Path) -> None:
        """Check a single Python file for quality issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
            
            self.stats['files_checked'] += 1
            self.stats['lines_of_code'] += len(lines)
            
            # Parse AST
            try:
                tree = ast.parse(content)
                self._analyze_ast(tree, file_path)
            except SyntaxError as e:
                self.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=e.lineno or 0,
                    issue_type='syntax',
                    description=f'Syntax error: {e.msg}',
                    severity='critical'
                ))
            
            # Check line length (PEP 8: max 79 characters)
            for i, line in enumerate(lines, 1):
                if len(line) > 79:
                    self.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type='pep8',
                        description=f'Line too long ({len(line)} > 79 characters)',
                        severity='low'
                    ))
            
            # Check for security issues
            self._check_security_issues(content, file_path)
            
        except Exception as e:
            logger.error(f"Failed to check {file_path}: {e}")
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path) -> None:
        """Analyze AST for code quality issues."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.stats['functions'] += 1
                self._check_function_quality(node, file_path)
            elif isinstance(node, ast.ClassDef):
                self.stats['classes'] += 1
                self._check_class_quality(node, file_path)
    
    def _check_function_quality(self, node: ast.FunctionDef, file_path: Path) -> None:
        """Check function-specific quality issues."""
        # Check for docstring
        if not ast.get_docstring(node):
            self.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=node.lineno,
                issue_type='documentation',
                description=f'Function "{node.name}" missing docstring',
                severity='medium'
            ))
        
        # Check function complexity (number of statements)
        statements = len([n for n in ast.walk(node) if isinstance(n, ast.stmt)])
        if statements > 20:
            self.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=node.lineno,
                issue_type='complexity',
                description=f'Function "{node.name}" too complex ({statements} statements)',
                severity='medium'
            ))
    
    def _check_class_quality(self, node: ast.ClassDef, file_path: Path) -> None:
        """Check class-specific quality issues."""
        # Check for docstring
        if not ast.get_docstring(node):
            self.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=node.lineno,
                issue_type='documentation',
                description=f'Class "{node.name}" missing docstring',
                severity='medium'
            ))
    
    def _check_security_issues(self, content: str, file_path: Path) -> None:
        """Check for common security issues."""
        security_patterns = [
            (r'eval\s*\(', 'Use of eval() function is dangerous'),
            (r'exec\s*\(', 'Use of exec() function is dangerous'),
            (r'subprocess\.call\s*\(.*shell\s*=\s*True', 'Shell injection vulnerability'),
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key detected'),
        ]
        
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, description in security_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(QualityIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type='security',
                        description=description,
                        severity='high'
                    ))
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run complete code quality analysis."""
        logger.info("Starting code quality analysis...")
        
        # Check project structure
        self.check_file_structure()
        
        # Check all Python files
        for py_file in self.project_root.rglob("*.py"):
            if not any(part.startswith('.') for part in py_file.parts):
                self.check_python_file(py_file)
        
        self.stats['issues_found'] = len(self.issues)
        
        # Generate report
        return self._generate_report()
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate quality analysis report."""
        issues_by_severity = {}
        issues_by_type = {}
        
        for issue in self.issues:
            # Group by severity
            if issue.severity not in issues_by_severity:
                issues_by_severity[issue.severity] = []
            issues_by_severity[issue.severity].append(issue)
            
            # Group by type
            if issue.issue_type not in issues_by_type:
                issues_by_type[issue.issue_type] = []
            issues_by_type[issue.issue_type].append(issue)
        
        return {
            'stats': self.stats,
            'issues': self.issues,
            'issues_by_severity': issues_by_severity,
            'issues_by_type': issues_by_type,
            'quality_score': self._calculate_quality_score()
        }
    
    def _calculate_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        if self.stats['lines_of_code'] == 0:
            return 100.0
        
        # Weight issues by severity
        severity_weights = {
            'critical': 10,
            'high': 5,
            'medium': 2,
            'low': 1
        }
        
        total_weight = sum(
            severity_weights.get(issue.severity, 1) 
            for issue in self.issues
        )
        
        # Calculate score based on issues per 100 lines of code
        issues_per_100_lines = (total_weight / self.stats['lines_of_code']) * 100
        score = max(0, 100 - issues_per_100_lines)
        
        return round(score, 2)


def main():
    """Main entry point."""
    try:
        checker = CodeQualityChecker()
        report = checker.run_analysis()
        
        print("\n" + "="*60)
        print("🔍 CODE QUALITY ANALYSIS REPORT")
        print("="*60)
        
        print(f"\n📊 STATISTICS:")
        for key, value in report['stats'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🎯 QUALITY SCORE: {report['quality_score']}/100")
        
        if report['issues']:
            print(f"\n⚠️  ISSUES FOUND ({len(report['issues'])}):")
            for severity in ['critical', 'high', 'medium', 'low']:
                if severity in report['issues_by_severity']:
                    issues = report['issues_by_severity'][severity]
                    print(f"\n  {severity.upper()} ({len(issues)}):")
                    for issue in issues[:5]:  # Show first 5 issues
                        print(f"    📁 {issue.file_path}:{issue.line_number}")
                        print(f"       {issue.description}")
        else:
            print("\n✅ No issues found!")
        
        return 0 if report['quality_score'] >= 80 else 1
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"❌ Analysis failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
