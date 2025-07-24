def interpret_alignment(method, score, identity, align1, align2, question=None):
    score = float(score)
    identity = float(identity)

    base_response = f"Based on the {method} alignment:\n\n"
    base_response += f"- Alignment Score: {score}\n"
    base_response += f"- Identity: {identity}%\n"

    if identity > 90 and score > 80:
        base_response += "🧬 This indicates a very strong match — the sequences are likely homologous."
    elif identity > 70:
        base_response += "🔬 This is a moderately good alignment — some level of similarity exists."
    else:
        base_response += "❗ This alignment is weak — the sequences might not be related."

    if question:
        question = question.lower()
        if "similar" in question or "match" in question:
            base_response += "\n\n💬 Yes, the sequences show similarity based on the identity score."
        elif "mutation" in question:
            base_response += "\n\n🧪 This result may indicate possible mutations or variations."
        elif "conserved" in question:
            base_response += "\n\n🌿 There could be conserved regions, depending on local alignments."
        else:
            base_response += "\n\n🤖 I need more specific wording to give a better answer."

    return base_response
