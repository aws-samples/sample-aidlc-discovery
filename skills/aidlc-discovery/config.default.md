# AI-DLC Discovery Workshop Configuration

## Data Sources

```yaml
# How the customer data comes in: production | signal-briefs | synthetic
data_input: "production"

# Where it is: a folder relative to the working folder, or an Amazon Quick Space name.
# Recommended folder: "discovery/data/", which Handoff keeps out of git.
data_location: "discovery/data/"
```

## Output Settings

```yaml
# Where the workshop is saved: local (the working folder) | space (an Amazon Quick team Space, see discovery-team-space)
storage: "local"

# With storage: space, the team Space. The team creates and names it; empty: use the Space attached to the chat
space_name: ""

# Where to save generated artifacts (default: discovery/[project]/ in the working folder)
output_folder: "discovery/"

# Document format for generated reports
doc_format: "markdown"  # markdown | docx
```

## Run Settings

```yaml
# Project folder name under output_folder (empty: ask)
project: ""

# Engagement reference for the Discovery brief, if a facilitator gave you one (empty: ask; "Self-serve" when running on your own)
engagement_reference: ""

# true: run all phases without checkpoints or questions (automated tests only)
unattended: false
```

## Analysis Settings

```yaml
# Default time window for feedback analysis (days)
default_days: 30

# Maximum feedback items to include in LLM context
max_context_items: 50

# Default number of personas to generate
default_persona_count: 3

# Default categories (comma-separated, or "auto" for AI detection)
categories: "auto"
```

## Survey Settings

```yaml
# Default survey theme
survey_theme:
  primary_color: "#3B82F6"
  background_color: "#FFFFFF"
  text_color: "#1F2937"
  border_radius: "8px"

# Default rating type: stars | nps | emoji | scale
default_rating_type: "stars"
```
