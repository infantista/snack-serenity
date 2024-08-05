from flask import Flask, request, jsonify
from datetime import datetime, timedelta

import jwt

from config import getParameters
from guard import validate_mobile_no
from spanneroperations import check_existing_user, send_sms, read_write_transaction,create_user_with_otp

# Initialize the Flask app
app = Flask(__name__)

# Load parameters from the config
parameters = getParameters()

# Endpoint to send OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        data = request.json
        mobile_number = data.get('mobile_number')

        # Validate mobile number format
        if not validate_mobile_no(mobile_number):
            return jsonify({"error": "Invalid mobile number"}), 400

        # Send OTP and get details
        success, otp, otp_log_date = send_sms(mobile_number)
        if not success:
            return jsonify({"error": "Failed to send OTP"}), 500

        # Create user with mobile number and OTP
        if not create_user_with_otp(mobile_number, otp):
            return jsonify({"error": "Failed to store OTP details"}), 500

        return jsonify({
            "message": "OTP sent successfully",
            "otp_expiry": otp_log_date
        }), 200

    except Exception as e:
        print(f"Error in /send_otp: {str(e)}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)