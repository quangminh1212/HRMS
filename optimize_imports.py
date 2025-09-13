#!/usr/bin/env python3
"""
Code optimization script - Remove unused imports and fix PEP 8 issues
International standards compliance
"""

import ast
import os


def analyze_imports(file_path):
    """Analyze and optimize imports in Python file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return None
    
    imports = []
    used_names = set()
    
    # Extract all imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(('import', alias.name, alias.asname))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(('from', node.module, alias.name, alias.asname))
        elif isinstance(node, ast.Name):
            used_names.add(node.id)
    
    return imports, used_names


def main():
    files_to_optimize = [
        'app.py',
        'run.py', 
        'src/components/design.py',
        'src/utils/utils.py'
    ]
    
    print("🔍 Analyzing imports for optimization...")
    for file_path in files_to_optimize:
        if os.path.exists(file_path):
            result = analyze_imports(file_path)
            if result:
                imports, used_names = result
                print(f"\n📁 {file_path}:")
                print(f"  - Total imports: {len(imports)}")
                print(f"  - Used names: {len(used_names)}")
        else:
            print(f"❌ File not found: {file_path}")


if __name__ == "__main__":
    main()
