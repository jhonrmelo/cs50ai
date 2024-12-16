# Analysis

## Layer 12, Head 6

This layer demonstrates a strong focus on **final tokens** such as the period (`.`) and the special `[SEP]` token. This behavior suggests that this head is likely capturing **sentence boundaries** or serving as a **global sentence-level summarizer**.

### **Observed Behavior**:
- The attention weights are concentrated primarily on the **final punctuation** and **[SEP]** token, with other tokens receiving minimal attention.
- This indicates that this head may not be actively contributing to resolving the `[MASK]` token itself, but instead encoding sentence termination and structural markers for sentence coherence.

### **Example Sentences**:
1. _"We turned down a narrow lane and passed through a small [MASK] ."_
   - Attention flows heavily toward the `.` and `[SEP]`.
2. _"We arrived at [MASK] ."_
   - The attention highlights the period, signaling sentence completion.

---

## **Layer 5, Head 8**

This layer displays a **broader attention distribution** that includes:
1. **The final `[SEP]` token** (as in Layer 12, Head 6) – maintaining a focus on sentence boundaries.
2. **Contextual tokens throughout the sentence**, suggesting this head plays a role in encoding **global contextual relationships** within the sentence.

### **Observed Behavior**:
- Attention is distributed across the **previous tokens** in the input sentence, with slightly stronger focus on words close to the `[MASK]` token.
- This indicates the head is incorporating context from multiple parts of the sentence to help the model make an informed prediction about the masked token.

### **Example Sentences**:
1. _"We turned down a narrow lane and passed through a small [MASK] ."_
   - Attention spreads across "narrow lane" and "small", while also pointing to `[SEP]`.
2. _"We arrived at [MASK] ."_
   - Broader attention spans "arrived at", with residual focus on `[SEP]`.

---

## **Key Insights**:
- **Layer 12, Head 6**: Focuses on sentence-level markers like punctuation and `[SEP]`, likely summarizing sentence boundaries.
- **Layer 5, Head 8**: Balances attention between sentence boundaries (`[SEP]`) and contextual tokens, indicating its role in incorporating the broader context needed for `[MASK]` prediction.
