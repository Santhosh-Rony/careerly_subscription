from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"], 
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Load configuration from environment variables (Railway) or config file (local)
def load_email_config():
    # Try environment variables first (for Railway deployment)
    if os.getenv('EMAIL_USER'):
        return {
            'host': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
            'port': int(os.getenv('EMAIL_PORT', 587)),
            'user': os.getenv('EMAIL_USER'),
            'password': os.getenv('EMAIL_PASSWORD')
        }
    
    # Fallback to config.json for local development
    try:
        with open('config.json') as f:
            config = json.load(f)
        return {
            'host': config.get('email', {}).get('host', 'smtp.gmail.com'),
            'port': config.get('email', {}).get('port', 587),
            'user': config.get('email', {}).get('user'),
            'password': config.get('email', {}).get('password')
        }
    except FileNotFoundError:
        print("Warning: config.json not found, using environment variables only")
        return {
            'host': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
            'port': int(os.getenv('EMAIL_PORT', 587)),
            'user': os.getenv('EMAIL_USER'),
            'password': os.getenv('EMAIL_PASSWORD')
        }

email_config = load_email_config()
EMAIL_HOST = email_config['host']
EMAIL_PORT = email_config['port']
EMAIL_USER = email_config['user']
EMAIL_PASSWORD = email_config['password']

# Store subscriptions in a JSON file
SUBSCRIPTIONS_FILE = 'subscriptions.json'

def load_subscriptions():
    if os.path.exists(SUBSCRIPTIONS_FILE):
        with open(SUBSCRIPTIONS_FILE, 'r') as f:
            return json.load(f)
    return {'email': []}

def save_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, 'w') as f:
        json.dump(subscriptions, f, indent=2)

def send_email_notification(email, job_link):
    print(f"Attempting to send email to: {email}")
    print(f"Job link: {job_link}")
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"Careerly Job Alerts <{EMAIL_USER}>"
    msg['To'] = email
    msg['Subject'] = 'New Job Alert'

    # Create clean, professional HTML email template (not too flashy)
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f9f9f9; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border: 1px solid #e1e5e9; border-radius: 8px;">
            
            <!-- Header -->
            <div style="background-color: #4a90e2; padding: 25px 30px; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
                    Careerly
                </h1>
                <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 14px;">
                    Job Notification
                </p>
            </div>
            
            <!-- Content -->
            <div style="padding: 30px;">
                <h2 style="color: #2c3e50; margin: 0 0 20px 0; font-size: 20px; font-weight: 600;">
                    New Job Posted
                </h2>
                
                <p style="color: #555; font-size: 16px; margin: 0 0 20px 0;">
                    Hello,
                </p>
                
                <p style="color: #555; font-size: 16px; margin: 0 0 25px 0; line-height: 1.6;">
                    A new job opportunity has been posted on Careerly. You can view the details using the link below.
                </p>
                
                <!-- Simple CTA Button -->
                <div style="margin: 30px 0;">
                    <a href="{job_link}" style="background-color: #4a90e2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: 500; font-size: 16px; display: inline-block;">
                        View Job Details
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px; margin: 25px 0 0 0; line-height: 1.5;">
                    We recommend applying early as positions may fill quickly.
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f8f9fa; padding: 20px 30px; border-top: 1px solid #e1e5e9; border-radius: 0 0 8px 8px;">
                <p style="color: #666; font-size: 14px; margin: 0 0 10px 0;">
                    Best regards,<br>
                    The Careerly Team
                </p>
                
                <p style="color: #999; font-size: 12px; margin: 15px 0 0 0;">
                    You're receiving this because you subscribed to job alerts. 
                    
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    # Plain text fallback for email clients that don't support HTML
    text_body = f"""
    NEW JOB ALERT - CAREERLY

    Hello,

    A new job opportunity has been posted on Careerly. You can view the details using the link below.

    View Job Details: {job_link}

    We recommend applying early as positions may fill quickly.

    Best regards,
    The Careerly Team

    ---
    You're receiving this because you subscribed to job alerts.
    To unsubscribe, please contact us.
    """

    # Attach both HTML and plain text versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        print(f"Connecting to SMTP server: {EMAIL_HOST}:{EMAIL_PORT}")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        #print("Connected to SMTP server")
        
        server.starttls()
        #print("TLS started")
        
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        #print("Login successful")
        
        server.send_message(msg)
        print(f"Email sent successfully to {email}")
        
        server.quit()
        print("SMTP connection closed")
        return True
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/api/subscribe', methods=['POST', 'OPTIONS'])
def subscribe():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        print(f"Received subscription request: {data}")  # Debug
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        contact_method = data.get('contactMethod')
        contact_value = data.get('contactValue')

        if not contact_method or not contact_value:
            return jsonify({'error': 'Missing required fields'}), 400

        if contact_method != 'email':
            return jsonify({'error': 'Only email subscriptions are supported'}), 400

        subscriptions = load_subscriptions()
        
        # Check if already subscribed
        if contact_value in subscriptions['email']:
            return jsonify({'message': 'Already subscribed'}), 200

        # Add new subscription
        subscriptions['email'].append(contact_value)
        save_subscriptions(subscriptions)
        
        print(f"Successfully subscribed: {contact_value}")  # Debug

        return jsonify({'message': 'Successfully subscribed'}), 200
        
    except Exception as e:
        print(f"Error in subscribe endpoint: {e}")  # Debug
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/unsubscribe', methods=['POST', 'OPTIONS'])
def unsubscribe():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.json
    contact_method = data.get('contactMethod')
    contact_value = data.get('contactValue')

    if not contact_method or not contact_value:
        return jsonify({'error': 'Missing required fields'}), 400

    if contact_method != 'email':
        return jsonify({'error': 'Only email subscriptions are supported'}), 400

    subscriptions = load_subscriptions()
    
    if contact_value in subscriptions['email']:
        subscriptions['email'].remove(contact_value)
        save_subscriptions(subscriptions)
        return jsonify({'message': 'Successfully unsubscribed'}), 200

    return jsonify({'message': 'Not subscribed'}), 200

@app.route('/api/notify', methods=['POST', 'OPTIONS'])
def notify_subscribers():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.json
    job_link = data.get('jobLink')

    if not job_link:
        return jsonify({'error': 'Missing job link'}), 400

    subscriptions = load_subscriptions()
    results = {
        'email': {'success': 0, 'failed': 0}
    }

    # Send email notifications
    for email in subscriptions['email']:
        if send_email_notification(email, job_link):
            results['email']['success'] += 1
        else:
            results['email']['failed'] += 1

    return jsonify({
        'message': 'Notifications sent',
        'results': results
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'careerly-subscription-api',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Careerly Subscription API',
        'version': '1.0.0',
        'endpoints': [
            'POST /api/subscribe',
            'POST /api/unsubscribe', 
            'POST /api/notify',
            'GET /health'
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port) 