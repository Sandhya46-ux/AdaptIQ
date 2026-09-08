from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Give me one simple Class 10 Physics question about electricity. Include the answer."
)

print("\n============================")
print("       GEMINI TEST")
print("============================\n")

print(interaction.output_text)