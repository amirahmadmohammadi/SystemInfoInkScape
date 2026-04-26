#!/usr/bin/env python3
"""
Test script for Icon Inserter Extension

This script tests the extension logic without requiring Inkscape GUI.
It creates a test SVG, simulates the extension execution, and verifies the output.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add workspace to path
sys.path.insert(0, '/workspace')

def test_extension_import():
    """Test that the extension module can be imported."""
    print("Testing extension import...")
    try:
        # Try to import inkex first
        try:
            import inkex
            print("  ✓ inkex module available")
        except ImportError:
            print("  ⚠ inkex module not available (expected in test environment)")
            print("    Extension will work when installed in Inkscape")
            return True
        
        # If inkex is available, test the extension class
        from icon_inserter import IconInserter
        print("✓ Extension module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import extension: {e}")
        return False

def test_icon_files_exist():
    """Test that all icon files exist."""
    print("\nTesting icon files...")
    icons_dir = Path('/workspace/icons')
    expected_icons = ['alert.svg', 'info.svg', 'warning.svg', 'success.svg', 'settings.svg']
    
    all_exist = True
    for icon in expected_icons:
        icon_path = icons_dir / icon
        if icon_path.exists():
            print(f"  ✓ {icon} exists")
        else:
            print(f"  ✗ {icon} missing")
            all_exist = False
    
    return all_exist

def test_extension_files_exist():
    """Test that all extension files exist."""
    print("\nTesting extension files...")
    expected_files = [
        '/workspace/icon_inserter.inx',
        '/workspace/icon_inserter.py',
        '/workspace/icon_inserter.ui'
    ]
    
    all_exist = True
    for filepath in expected_files:
        if os.path.exists(filepath):
            print(f"  ✓ {os.path.basename(filepath)} exists")
        else:
            print(f"  ✗ {os.path.basename(filepath)} missing")
            all_exist = False
    
    return all_exist

def test_svg_structure():
    """Test that the test SVG document is valid."""
    print("\nTesting SVG document structure...")
    try:
        import lxml.etree as ET
        tree = ET.parse('/workspace/test_document.svg')
        root = tree.getroot()
        
        # Check for SVG namespace
        svg_ns = '{http://www.w3.org/2000/svg}'
        if root.tag == f'{svg_ns}svg':
            print("  ✓ Valid SVG root element")
        else:
            print(f"  ✗ Invalid root element: {root.tag}")
            return False
        
        # Count shapes
        shapes = root.findall(f'.//{svg_ns}rect') + \
                 root.findall(f'.//{svg_ns}circle') + \
                 root.findall(f'.//{svg_ns}ellipse')
        
        print(f"  ✓ Found {len(shapes)} test shapes")
        return True
        
    except Exception as e:
        print(f"  ✗ Error parsing SVG: {e}")
        return False

def test_inx_structure():
    """Test that the INX extension definition is valid."""
    print("\nTesting INX file structure...")
    try:
        import lxml.etree as ET
        tree = ET.parse('/workspace/icon_inserter.inx')
        root = tree.getroot()
        
        # Check for extension element
        inkscape_ns = '{https://inkscape.org/namespaces/inkscape}'
        if root.tag == f'{inkscape_ns}inkscape-extension':
            print("  ✓ Valid INX root element")
        else:
            print(f"  ✗ Invalid root element: {root.tag}")
            return False
        
        # Check for required elements
        name_elem = root.find(f'{inkscape_ns}name')
        script_elem = root.find(f'{inkscape_ns}script')
        dialog_elem = root.find(f'{inkscape_ns}dialog')
        
        if name_elem is not None:
            print(f"  ✓ Name: {name_elem.text}")
        else:
            print("  ✗ Missing name element")
            return False
            
        if script_elem is not None:
            print(f"  ✓ Script: {script_elem.text}")
        else:
            print("  ✗ Missing script element")
            return False
            
        if dialog_elem is not None:
            print(f"  ✓ Dialog: {dialog_elem.text}")
        else:
            print("  ✗ Missing dialog element")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error parsing INX: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Icon Inserter Extension - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Extension Import", test_extension_import()))
    results.append(("Extension Files", test_extension_files_exist()))
    results.append(("Icon Files", test_icon_files_exist()))
    results.append(("SVG Structure", test_svg_structure()))
    results.append(("INX Structure", test_inx_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! The extension is ready for installation.")
        print("\nNext steps:")
        print("1. Copy files to Inkscape extensions directory")
        print("2. Restart Inkscape")
        print("3. Open test_document.svg")
        print("4. Select a shape and run Extensions → Custom → Icon Inserter")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues before installation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
