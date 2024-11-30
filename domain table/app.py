import json
import os
from flask import Flask, jsonify, request, render_template
import ssl
import socket
from datetime import datetime
import requests

app = Flask(__name__)

# Path to JSON file
DOMAIN_FILE = "domain.json"


def load_domains():
    """Load domains from the JSON file."""
    if os.path.exists(DOMAIN_FILE):
        with open(DOMAIN_FILE, "r") as file:
            return json.load(file)
    return []


def save_domains(domains):
    """Save domains to the JSON file."""
    with open(DOMAIN_FILE, "w") as file:
        json.dump(domains, file, indent=4)


def get_ssl_info(domain):
    """Retrieve SSL expiration and issuer information for a domain."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                ssl_expiration = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                ssl_issuer = dict(x[0] for x in cert['issuer'])
                return {
                    "ssl_expiration": ssl_expiration.strftime("%Y-%m-%d"),
                    "ssl_issuer": ssl_issuer.get("organizationName", "Unknown")
                }
    except Exception:
        return {
            "ssl_expiration": "N/A",
            "ssl_issuer": "Unknown"
        }


def check_domain_status(domain):
    """Check if a domain is alive or down."""
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        return "Up" if response.status_code == 200 else f"Down ({response.status_code})"
    except requests.RequestException:
        return "Down"


@app.route('/')
def index():
    """Render the main page."""
    return render_template('domain.html')


@app.route('/get_domains', methods=['GET'])
def get_domains():
    """Return the list of domains."""
    return jsonify(load_domains())


@app.route('/add_domain', methods=['POST'])
def add_domain():
    """Add a domain to the monitoring list."""
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required."}), 400

    domains = load_domains()

    if any(d["domain"] == domain for d in domains):
        return jsonify({"error": "Domain already exists."}), 400

    # Check domain status and SSL information
    status = check_domain_status(domain)
    ssl_info = get_ssl_info(domain)

    domain_entry = {
        "domain": domain,
        "status": status,
        "ssl_expiration": ssl_info["ssl_expiration"],
        "ssl_issuer": ssl_info["ssl_issuer"]
    }

    domains.append(domain_entry)
    save_domains(domains)

    return jsonify(domain_entry)


@app.route('/remove_domain', methods=['POST'])
def remove_domain():
    """Remove a domain from the monitoring list."""
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required."}), 400

    domains = load_domains()
    updated_domains = [d for d in domains if d["domain"] != domain]

    if len(updated_domains) == len(domains):
        return jsonify({"error": "Domain not found."}), 404

    save_domains(updated_domains)
    return jsonify({"message": f"Domain {domain} removed successfully."})


if __name__ == '__main__':
    if not os.path.exists(DOMAIN_FILE):
        save_domains([])
    app.run(debug=True)
