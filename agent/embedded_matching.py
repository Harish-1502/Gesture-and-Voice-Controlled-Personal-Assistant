from sentence_transformers import SentenceTransformer, util
import torch
# from agent.intent_router import combined
from .shared_data import combined


embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare lists for matching the cmd actions
cmd_texts = list(combined.keys())

# convert each action into vectors
cmd_embs = embedder.encode(cmd_texts, normalize_embeddings=True, convert_to_tensor=True)

def match_command(user_text, threshold=0.70):

    emb_user = embedder.encode(user_text, normalize_embeddings=True, convert_to_tensor=True)

    # compares the similarity between user text and the listed actions
    scores = util.cos_sim(emb_user, cmd_embs)[0]

    # Gets index of highest score and .item converts that into a number
    best_idx = torch.argmax(scores).item()
    best_score = scores[best_idx].item()

    if best_score >= threshold:
        matched_key = cmd_texts[best_idx]
        return combined[matched_key], best_score  # return full action dict
    return None, best_score