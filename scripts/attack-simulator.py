#!/usr/bin/env python3
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
                    
                time.sleep(0.1)  # Small
