
import requests
import re
import sys

def check_frontend():
    """Check if the frontend is properly serving the React application"""
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
        
        print(f"Found {len(script_tags)} script tags:")
        for i, src in enumerate(script_tags):
            print(f"  {i+1}. {src}")
        
        # Check for app-specific content
        app_indicators = ['alliyn', 'business', 'network', 'match', 'partner']
        found_indicators = [ind for ind in app_indicators if re.search(ind, html, re.IGNORECASE)]
        
        if found_indicators:
            print(f"✅ Found app indicators: {', '.join(found_indicators)}")
        else:
            print("⚠️ No app-specific indicators found")
        
        # Check for bundle.js or similar
        js_bundles = [src for src in script_tags if re.search(r'(bundle|main|chunk|app)\.js', src)]
        if js_bundles:
            print(f"✅ Found JS bundles: {', '.join(js_bundles)}")
        else:
            print("⚠️ No JS bundles found")
        
        # Try to access one of the script files
        if script_tags:
            script_url = script_tags[0]
            if not script_url.startswith('http'):
                if script_url.startswith('/'):
                    script_url = f"http://localhost:3000{script_url}"
                else:
                    script_url = f"http://localhost:3000/{script_url}"
            
            print(f"Checking script URL: {script_url}")
            script_response = requests.get(script_url)
            if script_response.status_code == 200:
                print(f"✅ Script file accessible (size: {len(script_response.content)} bytes)")
                
                # Check if the script contains React code
                script_content = script_response.text
                react_indicators = ['React', 'createElement', 'Component', 'useState', 'useEffect']
                found_react = [ind for ind in react_indicators if ind in script_content]
                
                if found_react:
                    print(f"✅ Script contains React code: {', '.join(found_react)}")
                else:
                    print("⚠️ No React indicators found in script")
            else:
                print(f"❌ Script file not accessible. Status: {script_response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking frontend: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_frontend()
    sys.exit(0 if success else 1)
