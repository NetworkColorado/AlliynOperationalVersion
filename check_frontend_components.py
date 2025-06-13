
import requests
import re
import sys
import json

def check_frontend_components():
    """Check if the frontend contains the expected components"""
    try:
        # Get the frontend HTML
        response = requests.get("http://localhost:3000")
        html = response.text
        
        # Check if it's a React app
        if '<div id="root"></div>' not in html:
            print("❌ React root element not found")
            return False
        
        # Check for script tags
        script_tags = re.findall(r'<script[^>]*src="([^"]*)"[^>]*>', html)
        if not script_tags:
            print("❌ No script tags found")
            return False
        
        # Get the main bundle
        main_bundle = None
        for src in script_tags:
            if re.search(r'(bundle|main|chunk|app)\.js', src):
                main_bundle = src
                break
        
        if not main_bundle:
            print("❌ Main bundle not found")
            return False
        
        print(f"✅ Found main bundle: {main_bundle}")
        
        # Get the bundle content
        if not main_bundle.startswith('http'):
            if main_bundle.startswith('/'):
                main_bundle = f"http://localhost:3000{main_bundle}"
            else:
                main_bundle = f"http://localhost:3000/{main_bundle}"
        
        bundle_response = requests.get(main_bundle)
        if bundle_response.status_code != 200:
            print(f"❌ Failed to get bundle. Status: {bundle_response.status_code}")
            return False
        
        bundle_content = bundle_response.text
        
        # Check for expected components
        components = {
            "Authentication": ["login", "signup", "signin", "authentication", "auth"],
            "Profile Management": ["profile", "edit profile", "user profile", "company profile"],
            "Matchmaker": ["matchmaker", "swipe", "match", "partnership"],
            "Matches": ["matches", "connections", "partners"],
            "Deals": ["deals", "agreements", "contracts"],
            "Settings": ["settings", "preferences", "configuration"],
            "Sponsorship": ["sponsor", "sponsorship", "advertise"],
            "Admin Panel": ["admin", "admin panel", "admin dashboard"]
        }
        
        found_components = {}
        for component, keywords in components.items():
            found = False
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', bundle_content, re.IGNORECASE):
                    found = True
                    break
            found_components[component] = found
        
        # Print results
        print("\nComponent Detection Results:")
        print("===========================")
        for component, found in found_components.items():
            status = "✅" if found else "❌"
            print(f"{status} {component}")
        
        # Check for specific features
        features = {
            "Swiping Interface": ["swipe", "swipeleft", "swiperight", "drag"],
            "Location-based Filtering": ["location", "distance", "miles", "radius", "local", "national"],
            "Premium Upgrade": ["premium", "upgrade", "subscription", "payment"],
            "Admin Login": ["admin login", "admin access", "admin credentials"],
            "Profile Image Upload": ["upload", "image", "photo", "logo", "file"],
            "Matching Algorithm": ["algorithm", "probability", "score", "compatibility"],
            "Settings Persistence": ["localstorage", "save settings", "persist"]
        }
        
        found_features = {}
        for feature, keywords in features.items():
            found = False
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', bundle_content, re.IGNORECASE):
                    found = True
                    break
            found_features[feature] = found
        
        print("\nFeature Detection Results:")
        print("=========================")
        for feature, found in found_features.items():
            status = "✅" if found else "❌"
            print(f"{status} {feature}")
        
        # Overall assessment
        component_score = sum(1 for found in found_components.values() if found)
        feature_score = sum(1 for found in found_features.values() if found)
        total_score = component_score + feature_score
        max_score = len(components) + len(features)
        
        print(f"\nOverall Score: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
        
        if total_score >= max_score * 0.7:
            print("✅ Frontend appears to have most expected components and features")
            return True
        else:
            print("⚠️ Frontend may be missing some expected components or features")
            return False
    
    except Exception as e:
        print(f"❌ Error checking frontend components: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_frontend_components()
    sys.exit(0 if success else 1)
