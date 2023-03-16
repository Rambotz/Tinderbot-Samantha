import imp
import zipfile
import os
from pathlib import Path
cwd = os.getcwd()

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""

def get_proxy_extension(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS , profile_name):
    print(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    proxy_data = f"{cwd}/proxy/"
    profile_proxy = f"{cwd}/proxy/{profile_name}_proxy"
    if not os.path.isdir(proxy_data):
            os.mkdir(proxy_data)
    if not os.path.isdir(profile_proxy):
            os.mkdir(profile_proxy)
    background_path = os.path.join(profile_proxy, 'background.js')
    manifast_path = os.path.join(profile_proxy, 'manifest.json')
    with open(background_path, 'w') as f:
        f.write(background_js % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS))
    with open(manifast_path, 'w') as f:
        f.write(manifest_json)
        
    return profile_proxy

    