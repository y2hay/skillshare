---
name: context7-mcp
description: This skill should be used when the user asks about libraries, frameworks, API references, or needs code examples. Activates for setup questions, code generation involving libraries, or mentions of specific frameworks like React, Vue, Next.js, Prisma, Supabase, etc.
version: 1
triggers: ["library docs", "API reference", "resolve library", "query docs"]
---

## When to Use

Activate this skill when the user:

- Asks setup or configuration questions ("How do I configure Next.js middleware?")
- Requests code involving libraries ("Write a Prisma query for...")
- Needs API references ("What are the Supabase auth methods?")
- Mentions specific frameworks (React, Vue, Svelte, Express, Tailwind, etc.)

## Steps

### Step 1: Resolve the Library ID

Call `resolve-library-id` with:

- `libraryName`: The library name extracted from the user's question
- `query`: The user's full question (improves relevance ranking)

### Step 2: Select the Best Match

From the resolution results, choose based on:

- Exact or closest name match to what the user asked for
- Higher benchmark scores indicate better documentation quality
- If the user mentioned a version (e.g., "React 19"), prefer version-specific IDs

### Step 3: Fetch the Documentation

Call `query-docs` with:

- `libraryId`: The selected Context7 library ID (e.g., `/vercel/next.js`)
- `query`: The user's specific question

### Step 4: Use the Documentation

Incorporate the fetched documentation into your response:

- Answer the user's question using current, accurate information
- Include relevant code examples from the docs
- Cite the library version when relevant

## Guidelines

- **Be specific**: Pass the user's full question as the query for better results
- **Version awareness**: When users mention versions ("Next.js 15", "React 19"), use version-specific library IDs if available from the resolution step
- **Prefer official sources**: When multiple matches exist, prefer official/primary packages over community forks

## Success Criteria

- Library resolution returns relevant, well-scored matches for the user's query
- Selected library ID corresponds to the correct framework/library the user asked about
- Fetched documentation includes accurate, current API signatures and code examples
- Response incorporates live documentation rather than relying on potentially outdated training data
- Version-specific library IDs are used when the user mentions a specific version
