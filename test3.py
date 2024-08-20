# import subprocess

# process = subprocess.Popen(
#     ["./detector/scripts/build.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
# )

# stdout, stderr = process.communicate()

# print("STDOUT:")
# print(stdout.decode())
# print("STDERR:")
# print(stderr.decode())
from string import ascii_lowercase, ascii_uppercase


text = "The sunset sets at twelve o' clock."

result = " "
for letter in text.lower():
    if letter.isalpha():
        result.join([f"{letter}"])
print(result)
