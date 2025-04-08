import os

if 'KDE' in os.environ:
  print("KDE in os.environ")
else:
  print("KDE not in os.environ")

print(os.environ["XDG_SESSION_TYPE"])
print(os.environ["XDG_SESSION_DESKTOP"])
print(os.environ["XDG_CURRENT_DESKTOP"])

# Print the entire os.environ dictionary
print(os.environ)

# Alternatively, iterate through and print each key-value pair:
print("\nIterating through environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")
