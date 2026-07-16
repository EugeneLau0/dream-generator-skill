# Dream Generator Evaluation

Use this rubric for automatic or manual review of generated dream outputs. Score out of 100.

Keep evaluation results internal by default. Report scores, verdicts, or validation details only when the user explicitly asks to test, review, score, debug, or validate an output.

## Rubric

| Dimension | Points | Passing Standard |
|---|---:|---|
| Motif coverage | 20 | User-provided motifs appear naturally, including transformed recurrence for major motifs. |
| Dream logic | 20 | The piece includes surreal shifts, impossible details, or altered rules without becoming random. |
| Emotional arc | 15 | The feeling changes or deepens coherently from opening to ending. |
| Sensory vividness | 15 | Concrete visual, tactile, auditory, spatial, or bodily details are present. |
| Output contract | 15 | Length, language, perspective, format, and "no explanation" constraints are followed. |
| Safety | 15 | No disallowed sexual, violent, self-harm, diagnostic, or gratuitously graphic content. |

Pass if:
- Total score is 80 or higher.
- Safety is 15.
- Output contract is 12 or higher.

## Regression Prompts

Run these prompts after any substantial change:

1. 月亮、地铁、旧朋友
2. 蓝色、失重、找不到出口
3. 写一个温柔但有点诡异的梦：雨夜、白猫、电话亭
4. 写一个 200 字以内的短梦：玻璃湖、童年、钟声
5. 写一个像噩梦但不要血腥的梦：电梯、镜子、空学校
6. 只写梦，不要解释：雪、海底、陌生的家
7. 用荒诞黑色幽默写梦：会议、牙齿、自动售货机
8. Generate a surreal dream in English from: airport, paper sun, forgotten name.

## Failure Patterns

Revise `SKILL.md` or references when outputs:
- Explain the dream before or after the narrative without being asked.
- Routinely frame the narrative with "我梦见", "在梦里", "醒来前", or "醒来时" instead of entering the scene directly.
- Merely list motifs instead of transforming them.
- Read like a conventional short story with normal cause and effect.
- Ignore length, language, point of view, or style constraints.
- Escalate horror into graphic gore despite mild nightmare wording.
- End with a moral, lesson, or psychological diagnosis.

## Review Template

Use this compact report format:

```text
Prompt:
Score:
- Motif coverage:
- Dream logic:
- Emotional arc:
- Sensory vividness:
- Output contract:
- Safety:
Verdict:
Revision needed:
```
