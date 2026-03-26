# Technical Architect Function — Data Analysis Prompt

You are analyzing performance data for SafetyCulture's Technical Architect (TA) function. Before analyzing, read the charter context in `src/templates/ta_charter_context.md` — it defines what TAs do, what they don't do, and how they engage. All insights and recommendations must stay within that scope.

TAs are a **presales** function — not salespeople. They help GTM win bigger and close faster through technical discovery, solution architecture, integration design, risk mitigation, and building trust with IT leaders. They do NOT own revenue targets, pricing, standard demos, solution delivery, or project management.

## Team Context (update before each use)

| Technical Architect | Start Date            | Region |
|---------------------|--------------------|--------|
| Matt McManus        |       January 2025    | APAC   |
| Jonathan Soakell    |     September 2025    | EMEA   |
| Scotty Loewen       |      November 2025    | AMER   |
| Cinco Coates        |      February 2026    | AMER   |

## Data Structure

The attached JSON contains:
- **raw_opportunities**: Every opportunity a TA has been assigned to, including stage, deal value (AUD), industry, region, created/closed dates, and fiscal quarter
- **closed_won_count / closed_won_total_aud**: Wins by TA and quarter
- **closed_lost_count**: Losses by TA and quarter
- **win_rate**: Win percentage (closed won / total closed) by TA and quarter
- **open_pipeline**: Active (non-closed) opportunities by TA and quarter
- **average_deal_size**: Mean closed-won AUD by TA and quarter
- **opportunity_velocity**: Average days from opportunity creation to close (won deals) by TA and quarter
- **industry_closed_won**: Wins broken down by industry vertical
- **industry_open_pipeline**: Open pipeline broken down by industry vertical

## Your Task

Analyze this data set and surface the most significant patterns, trends, and insights. Do not approach this with a predetermined narrative. Let the data lead.

For each insight you identify:
1. State the finding clearly
2. Reference the specific data points that support it
3. Note any caveats, small sample sizes, or alternative explanations
4. Flag whether this is a strong signal or a preliminary pattern that needs more data

## Interpreting Losses

Closed Lost is not inherently negative for the TA function. A core part of the TA role is **derisking opportunities** — identifying technical gaps, misaligned requirements, or integration blockers early in the sales cycle. A deal that is qualified out because a TA surfaced a fundamental technical mismatch is a success, not a failure. It prevents wasted cycles for the AE, the customer, and post-sales teams.

When analyzing losses:
- Do NOT frame loss volume as a problem by default
- Consider whether losses indicate the function is doing its job — qualifying out bad-fit deals
- Only flag losses as concerning when there is evidence of systemic issues (e.g., losses concentrated in a specific stage suggesting late engagement, or losses where deal size suggests the TA shouldn't have been engaged)
- The data does not tell you *why* a deal was lost — avoid assuming losses are TA failures without evidence

Consider (but don't limit yourself to) these analytical lenses:
- How do outcomes vary across the team, and what factors might explain differences?
- What does the pipeline composition suggest about deal complexity and the function's role?
- Are there patterns in which deals are won vs. lost (size, industry, deal cycle length, deal type)?
- What does the trajectory across quarters suggest about the function's maturation?
- Are TAs being engaged on the right opportunities (100k+ AUD, complex integrations, highly strategic)?
- Are there opportunities in the pipeline?
- Are losses showing healthy deal qualification, or are there patterns that suggest something else?
- What does the data NOT tell you that would be important to know?

## Action Item Guardrails

When generating action items ("What's Next"), recommendations MUST be within the TA function's scope:

**In scope:**
- Improving technical discovery quality or coverage
- Engagement criteria adherence (are TAs on the right deals?)
- Solution architecture and integration patterns
- Derisking pipeline (technical validation, SAO completion)
- Building trust with IT leaders / technical stakeholders
- Handoff quality to post-sales teams
- Team enablement (industry knowledge, technical depth)
- Regional coverage and capacity planning

**Out of scope — do NOT recommend:**
- Revenue targets or quota attainment strategies
- Pricing or discounting tactics
- Demo improvements (standard demos are field team responsibility)
- Solution delivery or post-sales activities
- Product management or feature requests
- Project management activities

## Audience

The primary audience is senior sales leadership who care about:
- Commercial outcomes and win rates
- Whether the function is engaged on the right (most complex, highest-value) opportunities
- Evidence that the function operates with analytical rigor

## Formatting

Organize your findings from strongest signal to weakest. Use specific numbers. Avoid vague qualitative language — anchor every claim in data.
