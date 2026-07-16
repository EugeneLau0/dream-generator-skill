---
name: dream-generator
description: Generate literary dream narratives from a user's words, phrases, images, emotions, motifs, or style requests. Use when the user asks to write, create, expand, transform, or generate a dream, dream fragment, surreal dream, nightmare, poetic dream, dream journal entry, or "梦境/做梦/写个梦/梦境生成器/用这些词写梦/把几个词扩写成梦"; also use when the user provides a few keywords or short clauses and wants them woven into a complete dream-like passage.
---

# Dream Generator

## Purpose

Turn sparse inputs into complete dream narratives with vivid imagery, emotional continuity, and loosened dream logic. Prefer Chinese unless the user requests another language.

## Default Contract

When the user gives words, phrases, emotions, or motifs, generate the dream directly.

Default output:
- Write in first person.
- Write one complete dream narrative, usually 400-800 Chinese characters.
- Include a short title only when it improves the result or the user asks for one.
- Do not explain the symbolism, process, or source keywords unless asked.
- Do not output an outline, bullet list, prompt analysis, or preface.
- Enter the scene directly. Avoid routine framing phrases such as "我梦见", "在梦里", "醒来前", or "醒来时" unless the user explicitly asks for a dream journal style.
- End with an open, resonant moment of disappearance, arrival, recognition, interruption, or suspended motion. Do not rely on waking as the default ending.
- Keep validation and scoring internal by default. Only show evaluation results when the user explicitly asks to test, review, score, debug, or validate the output.

If the user specifies length, tone, perspective, language, or format, follow that request over the defaults.

## Input Handling

Extract these controls from the user request:
- Motifs: concrete nouns, places, people, objects, colors, sounds, actions, memories, or abstract states.
- Tone: gentle, eerie, lonely, funny, terrifying, healing, nostalgic, cyberpunk, fairytale, etc.
- Length: short dream, long dream, fixed word count, one paragraph, diary style.
- Constraints: "do not explain", "not too scary", "like a nightmare", "more poetic", "less literary".

If the user gives no motifs, ask for 2-5 images or emotions unless they clearly want surprise generation. For surprise generation, create a self-contained dream with 3-4 internally chosen motifs.

## Generation Procedure

1. Anchor the opening in an ordinary scene: a room, street, vehicle, school, shore, station, meal, phone call, or familiar errand.
2. Introduce one subtle impossibility early: wrong season, shifting architecture, changed identity, impossible object, repeated sound, doubled person, altered gravity, or time folding.
3. Weave every user motif into the dream naturally. Let important motifs return in changed forms instead of appearing only once.
4. Keep emotion continuous even when events jump. The dream may break normal logic, but the feeling should travel from one image to the next.
5. Use sensory details: light, texture, smell, temperature, sound, body sensation, distance, weight, and silence.
6. Avoid explaining what the dream means. Let images carry meaning by association.
7. Close on an image with aftertaste, not a moral, diagnosis, or explicit waking statement.

## Style Selection

Use `references/style-guide.md` when the user asks for a specific style, when the tone is ambiguous, or when the output needs stronger differentiation.

Use `references/examples.md` when calibrating examples, regression tests, or output shape.

Use `references/evaluation.md` when reviewing, scoring, or automatically evaluating generated dream outputs.

For local heuristic checks, run `scripts/evaluate_dream_output.py` with a prompt and generated output. Treat script results as regression signals, not as a replacement for literary judgment.

Do not include script scores or validation summaries in the final answer unless the user asked for them.

## Safety Boundaries

Dreams can be strange, frightening, or emotionally intense, but keep the default output literary rather than graphic.

Do:
- Soften explicit gore into atmosphere, aftermath, symbols, shadows, stains, distance, or implication.
- Treat trauma, grief, illness, minors, and real people with restraint.
- For "解梦" requests, provide literary reflection or possible themes, not diagnosis or certainty.
- Redirect self-harm content away from actionable detail while preserving emotional support and symbolic language.

Do not:
- Provide explicit sexual content involving minors or coercion.
- Provide instructions for self-harm, violence, abuse, or evasion.
- Turn nightmares into gratuitous gore when the user only asked for "恐怖" or "噩梦".
- Claim psychological, medical, or prophetic certainty from a dream.

## Quality Checklist

Before finalizing, check:
- All requested motifs are present or clearly transformed.
- The text feels like a dream, not a conventional plot summary.
- The emotional arc is legible.
- The requested length, language, and perspective are respected.
- The narration does not lean on explicit dream/waking labels when immersion would be stronger.
- The answer does not include unwanted analysis or meta-commentary.
- Evaluation results are omitted unless requested.
