# TA Quarterly Report Generator

This is an automated quarterly report tool for the Technical Architecture team at SafetyCulture. It generates a branded PowerPoint deck from Salesforce opportunity data queried through Hex.

## Architecture

- **CLI (Python)** handles prompt generation (`prompt`) and deck building (`build`)
- **Claude Code** orchestrates the middle steps: Hex queries via MCP and insight generation
- Do NOT try to call Hex APIs from Python — use the MCP tools (`create_thread`, `get_thread`)

## Workflow

When the user asks to generate a quarterly report, follow these steps in order. Do not skip steps or combine them.

### Step 1: Get the CSV

Ask the user for the path to their Salesforce opportunity CSV file. The CSV should have columns: `opportunity_id, technical_architect, region`. If the user provides opportunity IDs directly, that works too.

### Step 2: Generate the Hex prompt

Run:
```bash
uv run python -m src.main prompt --csv <path> -o output/hex_prompt.txt
```

If the user specifies a quarter or fiscal year, pass `--quarter` and `--fy` flags.

### Step 3: Review gate

Ask the user: **"The Hex prompt has been written to output/hex_prompt.txt. Have you reviewed it? (Y/N)"**

- **Y** → Proceed to Step 4
- **N** → Ask what they'd like to change. Options: open the file for editing, regenerate with different flags, or exit

Do NOT proceed to Hex until the user confirms.

### Step 4: Send to Hex

1. Read `output/hex_prompt.txt`
2. Call `create_thread` with the prompt contents
3. Wait 30 seconds, then poll `get_thread` up to 5 times with 30-second waits between each check. **When polling, only check the `status` field. Do not summarize, analyze, or comment on the response until status is `IDLE`.**
4. Once `IDLE`, parse the 9 metric outputs and the `raw_opportunities` table from the thread response
5. **Validate raw_opportunities completeness:** Compare the opportunity IDs returned in `raw_opportunities` against the IDs in the input CSV (the CSV is the source of truth). If any IDs are missing:
   - Collect the missing IDs
   - Call `continue_thread` asking Hex to return only the missing records
   - Wait 30 seconds, then poll `get_thread` up to 5 times (same rules as above)
   - Append the returned records to `raw_opportunities`
   - Repeat until every ID from the CSV is present in `raw_opportunities`
6. Write structured data to `output/report_data.json`

### Step 5: Generate insights

Use the analysis prompt at `src/templates/ta_analysis_prompt.md` to guide this step. Read that file first, then read `output/report_data.json` and perform the analysis it describes.

**Important:** Let the data lead. Do not start with a predetermined narrative. Every insight must reference specific numbers from the data.

Once the analysis is complete, map the findings to the `Insights` model and write `output/insights.json`:

```json
{
  "strong_signals": [
    "Data-anchored finding classified as a strong signal (include specific numbers)"
  ],
  "watch_evolve": [
    "Preliminary pattern that needs more data or has caveats (include specific numbers)"
  ],
  "whats_next": [
    {
      "heading": "Short action item title",
      "description": "1-2 sentence explanation of the recommended action and why"
    }
  ],
  "closing_statement": "Brief summary of the function's trajectory for the quarter"
}
```

Guidelines for mapping analysis to slides:
- **strong_signals** (Slide 5, left column) — Findings where the data is conclusive. 3–5 bullets.
- **watch_evolve** (Slide 5, right column) — Patterns that are emerging but have small sample sizes or caveats. 3–5 bullets.
- **whats_next** (Slide 6) — Concrete action items that follow from the analysis. 3–4 items.
- **closing_statement** (Slide 7) — One sentence summarizing the quarter's story.

Keep each bullet concise enough to fit on a slide (1–2 lines max). Reference numbers but don't overload — these are for a presentation, not a report.

### Step 6: Build the deck

Run:
```bash
uv run python -m src.main build
```

Tell the user where the .pptx file was saved.

## Important

- Follow the steps sequentially. Do not jump ahead.
- Always wait for user confirmation at the review gate (Step 3).
- If something fails, explain what went wrong and offer to retry that specific step.
- The deck is for Phil Goldie (Global Head of GTM).
