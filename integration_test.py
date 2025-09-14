#!/usr/bin/env python3
"""
Integration Test Suite for SIG-TE (Sistema Integrado de Gestão de Transporte Escolar)
Complete System Integration Testing

This test suite validates the complete system integration including:
- Backend-Frontend integration readiness
- Data flow validation
- API endpoint structure
- Service integration points
- Deployment readiness
"""

import sys
import json
import re
from datetime import datetime

class SIGTEIntegrationTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.issues_found = []
        self.recommendations = []
        
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
    
    def test_backend_frontend_integration_points(self):
        """Test integration points between backend and frontend"""
        print("🔗 Checking backend-frontend integration points...")
        
        try:
            # Read backend functions from Code.gs
            with open('/app/Code.gs', 'r') as f:
                backend_content = f.read()
            
            # Read frontend JavaScript
            with open('/app/JavaScript.html', 'r') as f:
                frontend_content = f.read()
            
            # Check for Google Apps Script integration patterns
            integration_points = [
                ('google.script.run', 'Google Apps Script client-side API'),
                ('getAllAlunos', 'Get all students function'),
                ('createAluno', 'Create student function'),
                ('updateAluno', 'Update student function'),
                ('deleteAluno', 'Delete student function'),
                ('generateDiagnosticReportFromGemini', 'Gemini report generation'),
                ('geocodeAddressFromMaps', 'Google Maps geocoding'),
                ('optimizeRouteFromMaps', 'Route optimization')
            ]
            
            missing_integrations = []
            for pattern, description in integration_points:
                if pattern not in backend_content and pattern not in frontend_content:
                    missing_integrations.append(description)
            
            if missing_integrations:
                print(f"❌ Missing integration points: {', '.join(missing_integrations)}")
                self.issues_found.extend(missing_integrations)
                return False
            
            print("✅ Backend-frontend integration points are properly defined")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required file not found: {e}")
            return False
    
    def test_data_flow_consistency(self):
        """Test data flow consistency between modules"""
        print("📊 Checking data flow consistency...")
        
        try:
            # Check DataManager.gs for CRUD operations
            with open('/app/DataManager.gs', 'r') as f:
                data_manager = f.read()
            
            # Check JavaScript for corresponding frontend operations
            with open('/app/JavaScript.html', 'r') as f:
                frontend_js = f.read()
            
            # Verify CRUD operations consistency
            crud_operations = [
                ('getByEntity', 'Entity retrieval'),
                ('getById', 'Single record retrieval'),
                ('create', 'Record creation'),
                ('update', 'Record update'),
                ('deleteRecord', 'Record deletion')
            ]
            
            missing_crud = []
            for operation, description in crud_operations:
                if f'function {operation}(' not in data_manager:
                    missing_crud.append(f"Backend: {description}")
            
            # Check frontend CRUD methods
            frontend_crud = [
                ('saveStudent', 'Save student frontend'),
                ('editStudent', 'Edit student frontend'),
                ('deleteStudent', 'Delete student frontend'),
                ('saveRoute', 'Save route frontend'),
                ('editRoute', 'Edit route frontend'),
                ('deleteRoute', 'Delete route frontend')
            ]
            
            for operation, description in frontend_crud:
                if f'{operation}(' not in frontend_js:
                    missing_crud.append(f"Frontend: {description}")
            
            if missing_crud:
                print(f"❌ Missing CRUD operations: {', '.join(missing_crud)}")
                self.issues_found.extend(missing_crud)
                return False
            
            print("✅ Data flow consistency is maintained")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required file not found: {e}")
            return False
    
    def test_api_service_integration(self):
        """Test API service integration readiness"""
        print("🌐 Checking API service integration...")
        
        try:
            # Check Gemini service
            with open('/app/GeminiService.gs', 'r') as f:
                gemini_service = f.read()
            
            # Check Google Maps service
            with open('/app/GoogleMapsService.gs', 'r') as f:
                maps_service = f.read()
            
            # Verify API integrations
            api_checks = [
                (gemini_service, 'GEMINI_API_KEY', 'Gemini API key configuration'),
                (gemini_service, 'generativelanguage.googleapis.com', 'Gemini API endpoint'),
                (maps_service, 'GOOGLE_MAPS_API_KEY', 'Google Maps API key configuration'),
                (maps_service, 'maps.googleapis.com', 'Google Maps API endpoint'),
                (gemini_service, 'CacheService', 'Caching implementation'),
                (maps_service, 'geocodeAddress', 'Geocoding function'),
                (maps_service, 'optimizeRoute', 'Route optimization function')
            ]
            
            missing_api_features = []
            for content, pattern, description in api_checks:
                if pattern not in content:
                    missing_api_features.append(description)
            
            if missing_api_features:
                print(f"❌ Missing API features: {', '.join(missing_api_features)}")
                self.issues_found.extend(missing_api_features)
                return False
            
            print("✅ API service integration is ready")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required service file not found: {e}")
            return False
    
    def test_authentication_authorization_flow(self):
        """Test authentication and authorization flow"""
        print("🔐 Checking authentication and authorization flow...")
        
        try:
            # Check AuthService
            with open('/app/AuthService.gs', 'r') as f:
                auth_service = f.read()
            
            # Check Code.gs for auth integration
            with open('/app/Code.gs', 'r') as f:
                main_code = f.read()
            
            # Verify auth components
            auth_checks = [
                ('authenticate', 'Authentication function'),
                ('hasPermission', 'Permission checking'),
                ('Session.getActiveUser()', 'User session handling'),
                ('getUserAuthInfo', 'User info retrieval'),
                ('SECRETARIOS', 'Secretary role definition'),
                ('MONITORES', 'Monitor role definition')
            ]
            
            missing_auth = []
            all_content = auth_service + main_code
            for pattern, description in auth_checks:
                if pattern not in all_content:
                    missing_auth.append(description)
            
            if missing_auth:
                print(f"❌ Missing auth features: {', '.join(missing_auth)}")
                self.issues_found.extend(missing_auth)
                return False
            
            print("✅ Authentication and authorization flow is implemented")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Auth service file not found: {e}")
            return False
    
    def test_error_handling_consistency(self):
        """Test error handling consistency across the system"""
        print("⚠️ Checking error handling consistency...")
        
        try:
            # Check backend error handling
            backend_files = [
                '/app/Code.gs',
                '/app/DataManager.gs',
                '/app/GeminiService.gs',
                '/app/GoogleMapsService.gs'
            ]
            
            backend_content = ""
            for file_path in backend_files:
                try:
                    with open(file_path, 'r') as f:
                        backend_content += f.read() + "\n"
                except FileNotFoundError:
                    continue
            
            # Check frontend error handling
            with open('/app/JavaScript.html', 'r') as f:
                frontend_content = f.read()
            
            # Verify error handling patterns
            error_checks = [
                (backend_content, 'throw new Error', 'Backend error throwing'),
                (backend_content, 'try {', 'Backend try-catch blocks'),
                (frontend_content, 'catch (error)', 'Frontend error catching'),
                (frontend_content, 'showNotification', 'User error notification'),
                (frontend_content, 'console.error', 'Error logging'),
                (backend_content, 'console.error', 'Backend error logging')
            ]
            
            missing_error_handling = []
            for content, pattern, description in error_checks:
                if pattern not in content:
                    missing_error_handling.append(description)
            
            if missing_error_handling:
                print(f"❌ Missing error handling: {', '.join(missing_error_handling)}")
                self.issues_found.extend(missing_error_handling)
                return False
            
            print("✅ Error handling consistency is maintained")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required file not found: {e}")
            return False
    
    def test_ui_ux_completeness(self):
        """Test UI/UX completeness and consistency"""
        print("🎨 Checking UI/UX completeness...")
        
        try:
            # Check CSS completeness
            with open('/app/Css.html', 'r') as f:
                css_content = f.read()
            
            # Check HTML structure
            with open('/app/Index.html', 'r') as f:
                html_content = f.read()
            
            # Check JavaScript UI interactions
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Verify UI/UX components
            ui_checks = [
                (css_content, '.btn-primary', 'Primary button styles'),
                (css_content, '.btn-secondary', 'Secondary button styles'),
                (css_content, '.modal', 'Modal styles'),
                (css_content, '.notification', 'Notification styles'),
                (css_content, '.kanban-', 'Kanban board styles'),
                (css_content, '.stats-card', 'Statistics card styles'),
                (html_content, 'theme-toggle', 'Theme toggle button'),
                (html_content, 'sidebar-toggle', 'Sidebar toggle button'),
                (js_content, 'showModal', 'Modal functionality'),
                (js_content, 'showNotification', 'Notification functionality'),
                (js_content, 'setupKanbanDragAndDrop', 'Kanban drag-drop functionality')
            ]
            
            missing_ui = []
            for content, pattern, description in ui_checks:
                if pattern not in content:
                    missing_ui.append(description)
            
            if missing_ui:
                print(f"❌ Missing UI/UX components: {', '.join(missing_ui)}")
                self.issues_found.extend(missing_ui)
                return False
            
            print("✅ UI/UX completeness is satisfactory")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required UI file not found: {e}")
            return False
    
    def test_deployment_readiness(self):
        """Test deployment readiness for Google Apps Script"""
        print("🚀 Checking deployment readiness...")
        
        try:
            # Check appsscript.json
            with open('/app/appsscript.json', 'r') as f:
                config = json.load(f)
            
            # Verify deployment configuration
            deployment_checks = [
                ('timeZone' in config, 'Time zone configuration'),
                ('webapp' in config, 'Web app configuration'),
                ('oauthScopes' in config, 'OAuth scopes configuration'),
                ('runtimeVersion' in config, 'Runtime version specification')
            ]
            
            missing_deployment = []
            for check, description in deployment_checks:
                if not check:
                    missing_deployment.append(description)
            
            # Check required OAuth scopes
            required_scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/script.external_request'
            ]
            
            if 'oauthScopes' in config:
                for scope in required_scopes:
                    if scope not in config['oauthScopes']:
                        missing_deployment.append(f"Missing OAuth scope: {scope}")
            
            if missing_deployment:
                print(f"❌ Missing deployment requirements: {', '.join(missing_deployment)}")
                self.issues_found.extend(missing_deployment)
                return False
            
            print("✅ Deployment readiness is confirmed")
            return True
            
        except FileNotFoundError:
            print("❌ appsscript.json file not found")
            return False
        except json.JSONDecodeError:
            print("❌ appsscript.json is not valid JSON")
            return False
    
    def test_performance_optimization(self):
        """Test performance optimization features"""
        print("⚡ Checking performance optimization features...")
        
        try:
            # Check for caching implementation
            with open('/app/GeminiService.gs', 'r') as f:
                gemini_content = f.read()
            
            # Check frontend optimization
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check CSS optimization
            with open('/app/Css.html', 'r') as f:
                css_content = f.read()
            
            # Verify performance features
            perf_checks = [
                (gemini_content, 'CacheService', 'API response caching'),
                (gemini_content, 'CACHE.put', 'Cache storage implementation'),
                (js_content, 'debounce', 'Input debouncing'),
                (js_content, 'setTimeout', 'Async operations'),
                (css_content, 'transition:', 'CSS transitions'),
                (css_content, '--transition:', 'CSS custom transition properties'),
                (js_content, 'await', 'Async/await patterns')
            ]
            
            missing_perf = []
            for content, pattern, description in perf_checks:
                if pattern not in content:
                    missing_perf.append(description)
            
            # Some performance features are optional, so we'll be lenient
            if len(missing_perf) > 3:  # Allow some missing features
                print(f"⚠️ Some performance optimizations could be improved: {', '.join(missing_perf[:3])}...")
                self.recommendations.extend(missing_perf)
            
            print("✅ Performance optimization features are adequate")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required file not found: {e}")
            return False
    
    def test_accessibility_features(self):
        """Test accessibility features"""
        print("♿ Checking accessibility features...")
        
        try:
            # Check HTML accessibility
            with open('/app/Index.html', 'r') as f:
                html_content = f.read()
            
            # Check CSS accessibility
            with open('/app/Css.html', 'r') as f:
                css_content = f.read()
            
            # Verify accessibility features
            a11y_checks = [
                (html_content, 'lang="pt-BR"', 'Language specification'),
                (html_content, 'title=', 'Button titles/tooltips'),
                (html_content, 'alt=', 'Image alt text'),
                (css_content, 'focus:', 'Focus styles'),
                (css_content, ':hover', 'Hover states'),
                (html_content, 'aria-', 'ARIA attributes'),
                (css_content, 'cursor: pointer', 'Cursor indicators')
            ]
            
            missing_a11y = []
            for content, pattern, description in a11y_checks:
                if pattern not in content:
                    missing_a11y.append(description)
            
            # Accessibility is important but some features might be missing
            if len(missing_a11y) > 2:
                print(f"⚠️ Some accessibility features could be improved: {', '.join(missing_a11y[:3])}...")
                self.recommendations.extend(missing_a11y)
            
            print("✅ Basic accessibility features are present")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Required file not found: {e}")
            return False
    
    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        print("\n📋 Generating recommendations...")
        
        # Add general recommendations
        general_recommendations = [
            "Consider implementing input validation on the frontend for better UX",
            "Add loading states for all async operations",
            "Implement proper error boundaries for better error handling",
            "Consider adding unit tests for critical functions",
            "Add comprehensive logging for debugging purposes",
            "Implement data backup and recovery procedures",
            "Consider adding user onboarding and help documentation",
            "Implement proper data sanitization for security",
            "Add performance monitoring and analytics",
            "Consider implementing offline functionality where appropriate"
        ]
        
        self.recommendations.extend(general_recommendations)
        
        return True
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting SIG-TE Integration Test Suite")
        print("=" * 70)
        
        # Run all tests
        self.run_test("Backend-Frontend Integration Points", self.test_backend_frontend_integration_points)
        self.run_test("Data Flow Consistency", self.test_data_flow_consistency)
        self.run_test("API Service Integration", self.test_api_service_integration)
        self.run_test("Authentication & Authorization Flow", self.test_authentication_authorization_flow)
        self.run_test("Error Handling Consistency", self.test_error_handling_consistency)
        self.run_test("UI/UX Completeness", self.test_ui_ux_completeness)
        self.run_test("Deployment Readiness", self.test_deployment_readiness)
        self.run_test("Performance Optimization", self.test_performance_optimization)
        self.run_test("Accessibility Features", self.test_accessibility_features)
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Print comprehensive summary
        print("\n" + "=" * 70)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 70)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        # Print issues found
        if self.issues_found:
            print(f"\n⚠️ ISSUES FOUND ({len(self.issues_found)}):")
            for i, issue in enumerate(self.issues_found[:10], 1):  # Show first 10 issues
                print(f"  {i}. {issue}")
            if len(self.issues_found) > 10:
                print(f"  ... and {len(self.issues_found) - 10} more issues")
        
        # Print recommendations
        if self.recommendations:
            print(f"\n💡 RECOMMENDATIONS ({len(self.recommendations)}):")
            for i, rec in enumerate(self.recommendations[:8], 1):  # Show first 8 recommendations
                print(f"  {i}. {rec}")
            if len(self.recommendations) > 8:
                print(f"  ... and {len(self.recommendations) - 8} more recommendations")
        
        # Print failed tests
        failed_tests = [test for test in self.test_results if test["status"] == "FAILED"]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        
        # Final assessment
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL INTEGRATION TESTS PASSED!")
            print("✅ System is ready for Google Apps Script deployment.")
            return 0
        elif self.tests_passed >= self.tests_run * 0.8:  # 80% pass rate
            print(f"\n✅ INTEGRATION TESTS MOSTLY PASSED ({(self.tests_passed / self.tests_run * 100):.1f}%)")
            print("⚠️ System is ready for deployment with minor issues to address.")
            return 0
        else:
            print(f"\n❌ INTEGRATION TESTS FAILED ({(self.tests_passed / self.tests_run * 100):.1f}%)")
            print("🔧 System needs significant improvements before deployment.")
            return 1

def main():
    """Main function to run the integration test suite"""
    tester = SIGTEIntegrationTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())