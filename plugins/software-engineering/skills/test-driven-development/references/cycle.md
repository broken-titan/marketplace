# Cycle

One behavior at a time.

1. Write a test that states the missing behavior.
2. Run it and watch it fail for the missing behavior; keep that command output.
3. Write the smallest production change that makes this test pass. Do not implement the next behavior.
4. Run the same command and keep the passing output.
5. Refactor only now, and only while the suite stays green.
6. Repeat for the next behavior.

## Output

- The test
- The RED command and its output
- The minimal production change
- The GREEN command and its output
