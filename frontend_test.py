#!/usr/bin/env python3
"""
Frontend Test Suite for SIG-TE (Sistema Integrado de Gestão de Transporte Escolar)
Frontend UI/UX and Integration Testing

This test suite validates the frontend functionality including:
- Theme system
- Navigation and routing
- UI components
- Modal functionality
- Responsive design
- JavaScript functionality
"""

import sys
import re
import json
from datetime import datetime

class SIGTEFrontendTester:
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
    
    def test_theme_system_css(self):
        """Test CSS theme system implementation"""
        print("🎨 Checking CSS theme system...")
        
        try:
            with open('/app/Css.html', 'r') as f:
                css_content = f.read()
            
            # Check for theme variables
            theme_checks = [
                (':root', 'CSS custom properties root'),
                ('[data-theme="dark"]', 'Dark theme selector'),
                ('--primary-color:', 'Primary color variable'),
                ('--background-color:', 'Background color variable'),
                ('--text-primary:', 'Primary text color'),
                ('--text-secondary:', 'Secondary text color'),
                ('--surface-color:', 'Surface color variable'),
                ('--border-color:', 'Border color variable'),
                ('--shadow:', 'Shadow variables'),
                ('transition:', 'Smooth transitions')
            ]
            
            missing_features = []
            for check_pattern, check_name in theme_checks:
                if check_pattern not in css_content:
                    missing_features.append(check_name)
            
            if missing_features:
                print(f"❌ Missing theme features: {', '.join(missing_features)}")
                return False
            
            # Check for responsive design
            responsive_checks = [
                ('@media (max-width: 1024px)', 'Tablet responsive design'),
                ('@media (max-width: 768px)', 'Mobile responsive design'),
                ('@media (max-width: 480px)', 'Small mobile responsive design')
            ]
            
            for check_pattern, check_name in responsive_checks:
                if check_pattern not in css_content:
                    missing_features.append(check_name)
            
            if missing_features:
                print(f"❌ Missing responsive features: {', '.join(missing_features)}")
                return False
            
            print("✅ CSS theme system is complete and responsive")
            return True
            
        except FileNotFoundError:
            print("❌ Css.html file not found")
            return False
    
    def test_navigation_structure(self):
        """Test navigation structure in HTML"""
        print("🧭 Checking navigation structure...")
        
        try:
            with open('/app/Index.html', 'r') as f:
                html_content = f.read()
            
            # Check for navigation elements
            nav_checks = [
                ('<nav class="sidebar"', 'Sidebar navigation'),
                ('class="nav-menu"', 'Navigation menu'),
                ('class="nav-link"', 'Navigation links'),
                ('data-route="dashboard"', 'Dashboard route'),
                ('data-route="alunos"', 'Students route'),
                ('data-route="rotas"', 'Routes route'),
                ('data-route="onibus"', 'Bus route'),
                ('data-route="monitores"', 'Monitors route'),
                ('data-route="kanban"', 'Kanban route'),
                ('data-route="relatorios"', 'Reports route'),
                ('data-route="slides"', 'Slides route')
            ]
            
            missing_nav = []
            for check_pattern, check_name in nav_checks:
                if check_pattern not in html_content:
                    missing_nav.append(check_name)
            
            if missing_nav:
                print(f"❌ Missing navigation elements: {', '.join(missing_nav)}")
                return False
            
            print("✅ Navigation structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ Index.html file not found")
            return False
    
    def test_ui_components_structure(self):
        """Test UI components structure"""
        print("🎛️ Checking UI components structure...")
        
        try:
            with open('/app/Index.html', 'r') as f:
                html_content = f.read()
            
            # Check for essential UI components
            ui_checks = [
                ('<header class="header"', 'Header component'),
                ('class="theme-toggle"', 'Theme toggle button'),
                ('class="sidebar-toggle"', 'Sidebar toggle button'),
                ('<main class="main-content"', 'Main content area'),
                ('class="modal"', 'Modal component'),
                ('class="loading-overlay"', 'Loading overlay'),
                ('class="notification"', 'Notification component'),
                ('id="page-content"', 'Dynamic page content area')
            ]
            
            missing_components = []
            for check_pattern, check_name in ui_checks:
                if check_pattern not in html_content:
                    missing_components.append(check_name)
            
            if missing_components:
                print(f"❌ Missing UI components: {', '.join(missing_components)}")
                return False
            
            print("✅ UI components structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ Index.html file not found")
            return False
    
    def test_javascript_spa_structure(self):
        """Test JavaScript SPA structure and functionality"""
        print("⚡ Checking JavaScript SPA structure...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for SPA core functionality
            spa_checks = [
                ('class SIGTEApp', 'Main application class'),
                ('constructor()', 'Class constructor'),
                ('async init()', 'Initialization method'),
                ('setupTheme()', 'Theme setup method'),
                ('toggleTheme()', 'Theme toggle method'),
                ('setupEventListeners()', 'Event listeners setup'),
                ('navigateTo(', 'Navigation method'),
                ('loadRouteContent(', 'Route content loading'),
                ('showModal(', 'Modal display method'),
                ('closeModal()', 'Modal close method'),
                ('showNotification(', 'Notification method'),
                ('showLoading(', 'Loading overlay method')
            ]
            
            missing_spa = []
            for check_pattern, check_name in spa_checks:
                if check_pattern not in js_content:
                    missing_spa.append(check_name)
            
            if missing_spa:
                print(f"❌ Missing SPA functionality: {', '.join(missing_spa)}")
                return False
            
            print("✅ JavaScript SPA structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_module_rendering_methods(self):
        """Test module rendering methods"""
        print("📄 Checking module rendering methods...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for module rendering methods
            module_checks = [
                ('renderDashboard()', 'Dashboard rendering'),
                ('renderAlunos()', 'Students rendering'),
                ('renderRotas()', 'Routes rendering'),
                ('renderOnibus()', 'Bus rendering'),
                ('renderMonitores()', 'Monitors rendering'),
                ('renderKanban()', 'Kanban rendering'),
                ('renderRelatorios()', 'Reports rendering'),
                ('renderSlides()', 'Slides rendering')
            ]
            
            missing_modules = []
            for check_pattern, check_name in module_checks:
                if check_pattern not in js_content:
                    missing_modules.append(check_name)
            
            if missing_modules:
                print(f"❌ Missing module rendering methods: {', '.join(missing_modules)}")
                return False
            
            print("✅ Module rendering methods are complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_modal_functionality(self):
        """Test modal functionality implementation"""
        print("🪟 Checking modal functionality...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for modal methods
            modal_checks = [
                ('showStudentModal(', 'Student modal'),
                ('showRouteModal(', 'Route modal'),
                ('showBusModal(', 'Bus modal'),
                ('showMonitorModal(', 'Monitor modal'),
                ('showTaskModal(', 'Task modal'),
                ('saveStudent(', 'Save student method'),
                ('saveRoute(', 'Save route method'),
                ('saveBus(', 'Save bus method'),
                ('saveMonitor(', 'Save monitor method'),
                ('saveTask(', 'Save task method')
            ]
            
            missing_modals = []
            for check_pattern, check_name in modal_checks:
                if check_pattern not in js_content:
                    missing_modals.append(check_name)
            
            if missing_modals:
                print(f"❌ Missing modal functionality: {', '.join(missing_modals)}")
                return False
            
            print("✅ Modal functionality is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_crud_operations(self):
        """Test CRUD operations implementation"""
        print("🔄 Checking CRUD operations...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for CRUD methods
            crud_checks = [
                ('editStudent(', 'Edit student'),
                ('deleteStudent(', 'Delete student'),
                ('editRoute(', 'Edit route'),
                ('deleteRoute(', 'Delete route'),
                ('editBus(', 'Edit bus'),
                ('deleteBus(', 'Delete bus'),
                ('editMonitor(', 'Edit monitor'),
                ('deleteMonitor(', 'Delete monitor'),
                ('viewRoute(', 'View route'),
                ('viewBusHistory(', 'View bus history'),
                ('viewMonitorPerformance(', 'View monitor performance')
            ]
            
            missing_crud = []
            for check_pattern, check_name in crud_checks:
                if check_pattern not in js_content:
                    missing_crud.append(check_name)
            
            if missing_crud:
                print(f"❌ Missing CRUD operations: {', '.join(missing_crud)}")
                return False
            
            print("✅ CRUD operations are complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_kanban_functionality(self):
        """Test Kanban drag-and-drop functionality"""
        print("📋 Checking Kanban functionality...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for Kanban functionality
            kanban_checks = [
                ('setupKanbanDragAndDrop()', 'Kanban drag and drop setup'),
                ('renderKanbanCard(', 'Kanban card rendering'),
                ('updateTaskStatus(', 'Task status update'),
                ('dragstart', 'Drag start event'),
                ('dragend', 'Drag end event'),
                ('dragover', 'Drag over event'),
                ('drop', 'Drop event'),
                ('dragging', 'Dragging class')
            ]
            
            missing_kanban = []
            for check_pattern, check_name in kanban_checks:
                if check_pattern not in js_content:
                    missing_kanban.append(check_name)
            
            if missing_kanban:
                print(f"❌ Missing Kanban functionality: {', '.join(missing_kanban)}")
                return False
            
            print("✅ Kanban functionality is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_ai_integration_methods(self):
        """Test AI integration methods"""
        print("🤖 Checking AI integration methods...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for AI integration methods
            ai_checks = [
                ('generateReport(', 'Report generation'),
                ('generateAIReport()', 'AI report generation'),
                ('generateSlides(', 'Slides generation'),
                ('Gemini', 'Gemini AI reference'),
                ('IA', 'AI reference in Portuguese')
            ]
            
            missing_ai = []
            for check_pattern, check_name in ai_checks:
                if check_pattern not in js_content:
                    missing_ai.append(check_name)
            
            if missing_ai:
                print(f"❌ Missing AI integration: {', '.join(missing_ai)}")
                return False
            
            print("✅ AI integration methods are complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_mock_data_generator(self):
        """Test mock data generator functionality"""
        print("🎲 Checking mock data generator...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for mock data generator
            mock_checks = [
                ('class MockDataGenerator', 'Mock data generator class'),
                ('generateStudents(', 'Generate students'),
                ('generateRoutes(', 'Generate routes'),
                ('generateBuses(', 'Generate buses'),
                ('generateMonitors(', 'Generate monitors'),
                ('generateTasks(', 'Generate tasks'),
                ('firstNames', 'First names array'),
                ('lastNames', 'Last names array'),
                ('schools', 'Schools array'),
                ('busModels', 'Bus models array')
            ]
            
            missing_mock = []
            for check_pattern, check_name in mock_checks:
                if check_pattern not in js_content:
                    missing_mock.append(check_name)
            
            if missing_mock:
                print(f"❌ Missing mock data functionality: {', '.join(missing_mock)}")
                return False
            
            print("✅ Mock data generator is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def test_static_version_functionality(self):
        """Test static version functionality"""
        print("📄 Checking static version functionality...")
        
        try:
            with open('/app/TestStatic.html', 'r') as f:
                static_content = f.read()
            
            # Check for static version features
            static_checks = [
                ('SIG-TE', 'Application title'),
                ('theme-toggle', 'Theme toggle'),
                ('sidebar-toggle', 'Sidebar toggle'),
                ('navigateTo(', 'Navigation function'),
                ('localStorage', 'Local storage usage'),
                ('data-theme', 'Theme data attribute'),
                ('Dashboard', 'Dashboard content'),
                ('Alunos', 'Students section'),
                ('Rotas', 'Routes section'),
                ('Kanban', 'Kanban section')
            ]
            
            missing_static = []
            for check_pattern, check_name in static_checks:
                if check_pattern not in static_content:
                    missing_static.append(check_name)
            
            if missing_static:
                print(f"❌ Missing static version features: {', '.join(missing_static)}")
                return False
            
            print("✅ Static version functionality is complete")
            return True
            
        except FileNotFoundError:
            print("❌ TestStatic.html file not found")
            return False
    
    def test_form_validation_structure(self):
        """Test form validation structure"""
        print("📝 Checking form validation structure...")
        
        try:
            with open('/app/JavaScript.html', 'r') as f:
                js_content = f.read()
            
            # Check for form elements and validation
            form_checks = [
                ('form-input', 'Form input class'),
                ('form-select', 'Form select class'),
                ('form-textarea', 'Form textarea class'),
                ('form-label', 'Form label class'),
                ('form-group', 'Form group class'),
                ('required', 'Required field validation'),
                ('FormData', 'Form data handling'),
                ('Object.fromEntries', 'Form data conversion')
            ]
            
            missing_forms = []
            for check_pattern, check_name in form_checks:
                if check_pattern not in js_content:
                    missing_forms.append(check_name)
            
            if missing_forms:
                print(f"❌ Missing form validation features: {', '.join(missing_forms)}")
                return False
            
            print("✅ Form validation structure is complete")
            return True
            
        except FileNotFoundError:
            print("❌ JavaScript.html file not found")
            return False
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("🚀 Starting SIG-TE Frontend Test Suite")
        print("=" * 60)
        
        # Run all tests
        self.run_test("CSS Theme System", self.test_theme_system_css)
        self.run_test("Navigation Structure", self.test_navigation_structure)
        self.run_test("UI Components Structure", self.test_ui_components_structure)
        self.run_test("JavaScript SPA Structure", self.test_javascript_spa_structure)
        self.run_test("Module Rendering Methods", self.test_module_rendering_methods)
        self.run_test("Modal Functionality", self.test_modal_functionality)
        self.run_test("CRUD Operations", self.test_crud_operations)
        self.run_test("Kanban Functionality", self.test_kanban_functionality)
        self.run_test("AI Integration Methods", self.test_ai_integration_methods)
        self.run_test("Mock Data Generator", self.test_mock_data_generator)
        self.run_test("Static Version Functionality", self.test_static_version_functionality)
        self.run_test("Form Validation Structure", self.test_form_validation_structure)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 FRONTEND TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL FRONTEND TESTS PASSED! Frontend is ready for deployment.")
            return 0
        else:
            print(f"\n⚠️ {self.tests_run - self.tests_passed} frontend tests failed. Review the issues above.")
            
            # Print failed tests
            failed_tests = [test for test in self.test_results if test["status"] == "FAILED"]
            if failed_tests:
                print("\n❌ FAILED TESTS:")
                for test in failed_tests:
                    print(f"  - {test['test']}: {test['details']}")
            
            return 1

def main():
    """Main function to run the frontend test suite"""
    tester = SIGTEFrontendTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())