import requests
import cv2

client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'

# Request an access token
response = requests.post('https://accounts.spotify.com/api/token', data={
    'grant_type': 'authorization_code',
    'code': 'authorization_code_from_user',
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
})

# Get the access token from the response
access_token = response.json()['access_token']

response = requests.get('https://api.spotify.com/v1/me/playlists', headers={
    'Authorization': 'Bearer ' + access_token
})

playlist_info = response.json()

# Get the playlist's title
playlist_title = playlist_info['name']

# Create a new image with a specific size and background color
width, height = 3000, 3000
background_color = (255, 255, 255)
image = np.zeros((height, width, 3), np.uint8)
image[:] = background_color

# Define font and color
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0,0,0)

# Define position and write text
position = (50, 50)
cv2.putText(image,playlist_title, position, font, 1, color, 2, cv2.LINE_AA)

import cv2

# Open the Spotify logo image
logo = cv2.imread("logo.png")

#Resize the logo
logo = cv2.resize(logo, (100, 100))

# Paste the logo on the left side of the image
image[0:100, 0:100] = logo

# Define the sharpen kernel
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

# Apply the sharpen filter
image = cv2.filter2D(image, -1, kernel)

cv2.imwrite("playlist_cover.png", image)

# Get the playlist's id
playlist_id = "your_playlist_id"

# Get the image file
image_file = open("playlist_cover.jpg", "rb")

# Upload the image as the playlist's cover
response = requests.put(
    f"https://api.spotify.com/v1/playlists/{playlist_id}/images",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "image/jpeg"
    },
    data=image_file
)
