

url_id = "0lbCgqjRwsA&t=29s"
alpha_url_id = ""

for character in url_id:
    if character.isalnum():
        alpha_url_id += character

print(alpha_url_id)