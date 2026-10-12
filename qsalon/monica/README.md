# Monica (ElevenLabs agent agent_0801m3w2p2tzef7tkcm6vcf93vmv)

## Modes
- **Texting mode (normal):** tool_ids = [tool_2201m3w4yv1tf8argz9gbn638s73] (send_booking_link). Prompt: `prompt-texting.md`.
- **No-text mode (temporary, from 2026-10-12):** SMS not yet authorized, so Monica says the booking link out loud
  (theqsalonsrq.com/book -> SQUIRE) and offers a callback.
  tool_ids = [tool_4301m4r9m8x5fbqtsaht55rnt77d] (take_callback_request -> n8n ERkPVlw95CKmRogl -> email info@, cc Kris).
  Prompt: `prompt-no-text.md`.

To switch back: set the prompt to prompt-texting.md and tool_ids to [send_booking_link] (optionally keep take_callback_request too).
