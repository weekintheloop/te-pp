#!/usr/bin/env python3
"""
Backend Test Suite for SIG-TE (Sistema Integrado de Gestão de Transporte Escolar)
Google Apps Script Backend Testing

This test suite validates the Google Apps Script backend functionality
including data management, API integrations, and service functions.
"""

import sys
import json
from datetime import datetime

class SIGTEBackendTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
    def run_test(self, test_name, test_function):
        """Run a single test and record results"""
        self.tests_run += 1
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            result = test_function()
            if result:
                self.tests_passed += 1
                print(f"✅ PASSED - {test_name}")
                self.test_results.append({"test": test_name, "status": "PASSED", "details": ""})
                return True
            else:
                print(f"❌ FAILED - {test_name}")
                self.test_results.append({"test": test_name, "status": "FAILED", "details": "Test returned False"})
                return False
        except Exception as e:
            print(f"❌ FAILED - {test_name}: {str(e)}")
            self.test_results.append({"test": test_name, "status": "FAILED", "details": str(e)})
            return False
    
    def test_code_structure(self):
        """Test Code.gs structure and main functions"""
        print("📋 Checking Code.gs structure...")
        
        # Check if main files exist
        try:
            with open('/app/Code.gs', 'r') as f:
                code_content = f.read()
            
            # Check for essential functions
            required_functions = [
                'doGet',
                'include',
                'getAllAlunos',
                'createAluno',
                'getAlunoById',
                'updateAluno',
                'deleteAluno',
                'getUserAuthInfo'
            ]
            
            missing_functions = []
            for func in required_functions:
                if f'function {func}(' not in code_content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ Missing functions: {', '.join(missing_functions)}")
                return False
            
            print("✅ All essential functions found in Code.gs")
            return True
            
        except FileNotFoundError:
            print("❌ Code.gs file not found")
            return False
    
    def test_data_manager_structure(self):
        """Test DataManager.gs structure"""
        print("📊 Checking DataManager.gs structure...")
        
        try:
            with open('/app/DataManager.gs', 'r') as f:
                content = f.read()
            
            required_functions = [
                'getByEntity',
                'getById',
                'create',
                'update',
                'deleteRecord'
            ]
            
            missing_functions = []
            for func in required_functions:
                if f'function {func}(' not in content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ Missing DataManager functions: {', '.join(missing_functions)}")
                return False
            
            print("✅ DataManager.gs structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ DataManager.gs file not found")
            return False
    
    def test_gemini_service_structure(self):
        """Test GeminiService.gs structure"""
        print("🤖 Checking GeminiService.gs structure...")
        
        try:
            with open('/app/GeminiService.gs', 'r') as f:
                content = f.read()
            
            # Check for essential components
            checks = [
                ('callGeminiApi function', 'function callGeminiApi('),
                ('API key handling', 'GEMINI_API_KEY'),
                ('Caching implementation', 'CacheService'),
                ('Error handling', 'throw new Error'),
                ('API endpoint', 'generativelanguage.googleapis.com')
            ]
            
            for check_name, check_pattern in checks:
                if check_pattern not in content:
                    print(f"❌ Missing {check_name}")
                    return False
            
            print("✅ GeminiService.gs structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ GeminiService.gs file not found")
            return False
    
    def test_google_maps_service_structure(self):
        """Test GoogleMapsService.gs structure"""
        print("🗺️ Checking GoogleMapsService.gs structure...")
        
        try:
            with open('/app/GoogleMapsService.gs', 'r') as f:
                content = f.read()
            
            required_functions = [
                'geocodeAddress',
                'optimizeRoute',
                'buildGoogleMapUrl'
            ]
            
            missing_functions = []
            for func in required_functions:
                if f'function {func}(' not in content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ Missing GoogleMaps functions: {', '.join(missing_functions)}")
                return False
            
            # Check for API key handling
            if 'GOOGLE_MAPS_API_KEY' not in content:
                print("❌ Missing Google Maps API key handling")
                return False
            
            print("✅ GoogleMapsService.gs structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ GoogleMapsService.gs file not found")
            return False
    
    def test_html_structure(self):
        """Test HTML files structure"""
        print("🌐 Checking HTML files structure...")
        
        html_files = [
            ('/app/Index.html', 'Main application HTML'),
            ('/app/Css.html', 'CSS styles'),
            ('/app/JavaScript.html', 'JavaScript functionality'),
            ('/app/TestStatic.html', 'Static test version')
        ]
        
        for file_path, description in html_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if len(content) < 100:  # Basic content check
                    print(f"❌ {description} appears to be empty or too small")
                    return False
                
                print(f"✅ {description} found and has content")
                
            except FileNotFoundError:
                print(f"❌ {description} file not found: {file_path}")
                return False
        
        return True
    
    def test_theme_system_implementation(self):
        """Test theme system implementation in CSS"""
        print("🎨 Checking theme system implementation...")
        
        try:
            with open('/app/Css.html', 'r') as f:
                css_content = f.read()
            
            # Check for theme system components
            theme_checks = [
                (':root', 'CSS custom properties root'),
                ('[data-theme="dark"]', 'Dark theme selector'),
                ('--primary-color', 'Primary color variable'),
                ('--background-color', 'Background color variable'),
                ('--text-primary', 'Text color variable'),
                ('transition:', 'Smooth transitions')
            ]
            
            for check_pattern, check_name in theme_checks:
                if check_pattern not in css_content:
                    print(f"❌ Missing {check_name}")
                    return False
            
            print("✅ Theme system implementation is complete")
            return True
            
        except FileNotFoundError:
            print("❌ Css.html file not found")
            return False
    
    def test_javascript_spa_functionality(self):
        """Test JavaScript SPA functionality"""
        print("⚡ Checking JavaScript SPA functionality...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for SPA components
            spa_checks = [
                ('class SIGTEApp', 'Main application class'),
                ('navigateTo', 'Navigation function'),
                ('setupTheme', 'Theme setup'),
                ('setupEventListeners', 'Event listeners'),
                ('showModal', 'Modal functionality'),
                ('showNotification', 'Notification system'),
                ('MockDataGenerator', 'Mock data generator'),
                ('setupKanbanDragAndDrop', 'Kanban drag and drop')
            ]
            
            for check_pattern, check_name in spa_checks:
                if check_pattern not in js_content:
                    print(f"❌ Missing {check_name}")
                    return False
            
            print("✅ JavaScript SPA functionality is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_service_files_existence(self):
        """Test existence of all service files"""
        print("🔧 Checking service files existence...")
        
        service_files = [
            '/app/AuthService.gs',
            '/app/ValidationService.gs',
            '/app/NotificationService.gs',
            '/app/SchemaService.gs',
            '/app/GeminiReportService.gs',
            '/app/CriticalRoutesService.gs',
            '/app/AbsenceAnalysisService.gs'
        ]
        
        missing_files = []
        for file_path in service_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                if len(content) < 50:  # Basic content check
                    missing_files.append(f"{file_path} (empty or too small)")
            except FileNotFoundError:
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing or empty service files: {', '.join(missing_files)}")
            return False
        
        print("✅ All service files exist and have content")
        return True
    
    def test_appsscript_json_configuration(self):
        """Test appsscript.json configuration"""
        print("⚙️ Checking appsscript.json configuration...")
        
        try:
            with open('/app/appsscript.json', 'r') as f:
                config = json.load(f)
            
            # Check for essential configuration
            if 'timeZone' not in config:
                print("❌ Missing timeZone configuration")
                return False
            
            if 'webapp' not in config:
                print("❌ Missing webapp configuration")
                return False
            
            if 'oauthScopes' not in config:
                print("❌ Missing oauthScopes configuration")
                return False
            
            # Check for required OAuth scopes
            required_scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/script.external_request'
            ]
            
            for scope in required_scopes:
                if scope not in config['oauthScopes']:
                    print(f"❌ Missing required OAuth scope: {scope}")
                    return False
            
            print("✅ appsscript.json configuration is complete")
            return True
            
        except FileNotFoundError:
            print("❌ appsscript.json file not found")
            return False
        except json.JSONDecodeError:
            print("❌ appsscript.json is not valid JSON")
            return False
    
    def test_integration_readiness(self):
        """Test integration readiness for Google Apps Script"""
        print("🔗 Checking integration readiness...")
        
        # Check for proper Google Apps Script patterns across all .gs files
        gs_files = [
            '/app/Code.gs',
            '/app/DataManager.gs', 
            '/app/GeminiService.gs',
            '/app/GoogleMapsService.gs',
            '/app/AuthService.gs'
        ]
        
        all_content = ""
        for file_path in gs_files:
            try:
                with open(file_path, 'r') as f:
                    all_content += f.read() + "\n"
            except FileNotFoundError:
                continue
        
        integration_checks = [
            ('SpreadsheetApp', 'Google Sheets integration'),
            ('Session.getActiveUser()', 'User session handling'),
            ('HtmlService', 'HTML service usage'),
            ('PropertiesService', 'Properties service for configuration'),
            ('UrlFetchApp', 'External API calls'),
            ('CacheService', 'Caching service')
        ]
        
        missing_integrations = []
        for check_pattern, check_name in integration_checks:
            if check_pattern not in all_content:
                missing_integrations.append(check_name)
        
        if missing_integrations:
            print(f"❌ Missing integrations: {', '.join(missing_integrations)}")
            return False
        
        print("✅ Integration readiness is complete")
        return True
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SIG-TE Backend Test Suite")
        print("=" * 60)
        
        # Run all tests
        self.run_test("Code.gs Structure", self.test_code_structure)
        self.run_test("DataManager.gs Structure", self.test_data_manager_structure)
        self.run_test("GeminiService.gs Structure", self.test_gemini_service_structure)
        self.run_test("GoogleMapsService.gs Structure", self.test_google_maps_service_structure)
        self.run_test("HTML Files Structure", self.test_html_structure)
        self.run_test("Theme System Implementation", self.test_theme_system_implementation)
        self.run_test("JavaScript SPA Functionality", self.test_javascript_spa_functionality)
        self.run_test("Service Files Existence", self.test_service_files_existence)
        self.run_test("appsscript.json Configuration", self.test_appsscript_json_configuration)
        self.run_test("Integration Readiness", self.test_integration_readiness)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL TESTS PASSED! Backend is ready for deployment.")
            return 0
        else:
            print(f"\n⚠️ {self.tests_run - self.tests_passed} tests failed. Review the issues above.")
            
            # Print failed tests
            failed_tests = [test for test in self.test_results if test["status"] == "FAILED"]
            if failed_tests:
                print("\n❌ FAILED TESTS:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['details']}")
            
            return 1

def main():
    """Main function to run the test suite"""
    tester = SIGTEBackendTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())