# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the documentation site for **Pigsty** - a PostgreSQL infrastructure management platform. The docs are built with **Next.js 15** and **Fumadocs**, supporting internationalization (English/Chinese) and featuring comprehensive documentation for Pigsty's various modules.

## Development Commands

### Core Development
```bash
# Start development server with turbo mode
npm run dev
# or with higher concurrency
TURBO_CONCURRENCY=25 npm run dev

# Build for production
npm run build

# Start production server
npm start

# Quick development shortcuts (via Makefile)
make dev    # or make d
make build  # or make b
make view   # or make v - opens http://localhost:3000
```

### Content Processing
```bash
# Process MDX files (runs automatically after install)
fumadocs-mdx
```

## Architecture

### Content Structure
- **`content/docs/`**: Main documentation content organized by modules
  - Each module (pgsql, infra, node, redis, etc.) has its own directory
  - Contains `.mdx` files for content and `meta.json` for navigation structure
  - Supports both English and Chinese versions (`.cn.mdx` files)

### Key Components
- **`lib/source.ts`**: Content source adapter - provides interface to access documentation content
- **`app/layout.config.tsx`**: Shared layout configuration and navigation items
- **`source.config.ts`**: Fumadocs MDX configuration with frontmatter schemas
- **`lib/i18n.ts`**: Internationalization configuration (en/cn support)

### Routing Structure
- **`app/(home)/`**: Landing page and showcase routes
- **`app/[lang]/docs/`**: Documentation pages with i18n support
- **`app/api/search/route.ts`**: Search functionality

### Frontmatter Schema
All `.mdx` files use this frontmatter structure:
```yaml
---
title: Page Title
description: Page description for SEO and navigation
icon: LucideIconName  # Uses lucide-react icons
full: false          # Optional: full-width layout
---
```

### Meta Configuration
Navigation structure is defined in `meta.json` files:
- **`content/docs/meta.json`**: Root navigation structure
- **Module-specific meta.json**: Individual module navigation

## Development Guidelines

### Content Creation
- Place documentation in appropriate module directories under `content/docs/`
- Use `.mdx` extension for all content files
- Include proper frontmatter with title, description, and icon
- For Chinese versions, create `.cn.mdx` files alongside English versions
- Update corresponding `meta.json` for navigation structure

### MDX Features
- Supports standard Markdown with React components
- Fumadocs UI components available (tabs, callouts, etc.)
- Math rendering with KaTeX
- Code syntax highlighting with Shiki
- Mermaid diagrams supported

### Image Handling
Remote image patterns are configured in `next.config.ts` for:
- asciinema.org (terminal recordings)
- pigsty.io/pigsty.cc (project images)
- img.shields.io (badges)
- www.star-history.com (GitHub statistics)

### Internationalization
- Default language: English (`en`)
- Supported languages: English (`en`), Chinese (`cn`)
- URL structure: `/{lang}/docs/...`
- Content files: `.mdx` (English), `.cn.mdx` (Chinese)

## Module Documentation Structure

Each Pigsty module follows a consistent documentation structure:
- **index.mdx**: Module overview and introduction
- **concept.mdx**: Core concepts and architecture
- **config.mdx**: Configuration guidance
- **param.mdx**: Parameter reference
- **playbook.mdx**: Automation playbooks
- **admin.mdx**: Administration procedures
- **monitor.mdx**: Monitoring and dashboards
- **faq.mdx**: Frequently asked questions

This structure ensures consistency across all Pigsty modules and provides comprehensive coverage of each component.

## Content

This repo provides docs for pigsty https://github.com/pgsty/pigsty

The official docs is in http://pigsty.io/docs

The author may ask you to help write docs and summarize pigsty features.
You can consult the above two sources for official information

