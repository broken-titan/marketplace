# Property overlay

Use a property-based check only when the claim is algebraic and the repo already has (or the user asked for) that harness.

Fits:

- Round-trip (encode then decode)
- Inverse (apply then undo)
- Idempotent (apply twice equals apply once)

Keep the interesting regression as a **named row** in a concrete table.
