from google import genai
import os
client_ai = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

def get_embedding(text):
    return client_ai.models.embed_content(model="gemini-embedding-001", contents=text).embeddings[0].values

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    return dot / (sum(x**2 for x in a)**0.5 * sum(x**2 for x in b)**0.5)

if __name__ == "__main__":
    print("=" * 60)
    print("STEP 2: EMBEDDING")
    print("=" * 60)
    sample = "Years 0-2: 15 days/year. Years 3-5: 20 days/year."
    emb = get_embedding(sample)
    print(f"Dimensions: {len(emb)}")
    for t in ["How many PTO days?", "What is the vacation policy?", "What are the password requirements?"]:
        print(f"  {t} -> {cosine_sim(emb, get_embedding(t)):.4f}")
