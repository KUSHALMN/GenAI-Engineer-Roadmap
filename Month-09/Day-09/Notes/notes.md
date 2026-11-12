# 📝 Notes — Day 09: FlashAttention & KMP String Matching

- **Online Softmax Rescaling Formula:**
  $$m_{\text{new}} = \max(m_{\text{old}}, x_i), \quad \ell_{\text{new}} = e^{m_{\text{old}} - m_{\text{new}}} \ell_{\text{old}} + e^{x_i - m_{\text{new}}}$$
- **KMP Invariant:** At all times, `needle[0..j-1]` matches the preceding characters in the haystack.
