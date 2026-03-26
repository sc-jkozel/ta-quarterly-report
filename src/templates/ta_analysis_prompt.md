# Technical Architect Function — Data Analysis Prompt

You are analyzing performance data for SafetyCulture's Technical Architect (TA) function. This is a pre-sales technical function that supports complex enterprise sales opportunities. The function is relatively new.

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

Consider (but don't limit yourself to) these analytical lenses:
- How do outcomes vary across the team, and what factors might explain differences?
- What does the pipeline composition suggest about deal complexity and the function's role?
- Are there patterns in which deals are won vs. lost (size, industry, deal cycle length, deal type)?
- What does the trajectory across quarters suggest about the function's maturation?
- Are there opportunities in the pipeline?
- What does the data NOT tell you that would be important to know?

## Audience

The primary audience is senior sales leadership who care about:
- Commercial outcomes and win rates
- Whether the function is engaged on the right (most complex, highest-value) opportunities
- Evidence that the function operates with analytical rigor

## Formatting

Organize your findings from strongest signal to weakest. Use specific numbers. Avoid vague qualitative language — anchor every claim in data.
