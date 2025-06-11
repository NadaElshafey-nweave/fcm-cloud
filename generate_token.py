import google.auth.transport.requests
import google.oauth2.service_account

# Path to your Firebase Admin SDK JSON key file
SERVICE_ACCOUNT_JSON = 'serviceAccountKey.json'

# Load credentials from the service account file
credentials = google.oauth2.service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON,
    scopes=['https://www.googleapis.com/auth/firebase.messaging'] 
)

# Refresh the credentials to fetch an access token
request = google.auth.transport.requests.Request()
credentials.refresh(request)

# Get the access token
access_token = credentials.token

print("Access Token:", access_token)

