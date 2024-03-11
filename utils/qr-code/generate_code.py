import qrcode
import sys

# Check if a GitHub URL is passed as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_qr.py <GitHub_Repo_URL>")
    sys.exit(1)

# The URL of the GitHub repository from the command-line argument
github_repo_url = sys.argv[1]

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(github_repo_url)
qr.make(fit=True)

# Create an Image object from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
img.save("github_repo_qr.png")

print("QR code generated and saved as github_repo_qr.png")
