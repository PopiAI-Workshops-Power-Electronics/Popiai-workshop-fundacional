---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## CRITICAL: Brand Integration

**This skill works IN CONJUNCTION with the `brand-design` skill (if available), which is the AUTHORITATIVE source for all design decisions in this project.**

Before applying any creative techniques from this skill:
1. **FIRST** check if `.claude/skills/brand-design/SKILL.md` exists and read it
2. Use creative techniques from THIS skill only WITHIN brand constraints
3. When in doubt, brand guidelines ALWAYS take precedence
4. If no brand-design skill exists, propose a cohesive design direction and confirm with the user

**Hierarchy**: `brand-design` (required specifications) → `frontend-design` (creative techniques) → implementation

---

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: What feeling should the brand convey? (e.g., professional, warm, innovative, trustworthy)
- **Constraints**: Technical requirements (framework, performance, accessibility) + Brand requirements (if available).
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (React/Next.js with Tailwind) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail
- Compliant with brand guidelines (if available)

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Create hierarchy through size and weight, not font variety. Use the project's font system (Geist by default, or brand fonts if defined).
- **Color & Theme**: Use the brand color palette if available. If not, propose a cohesive palette. Use CSS variables for consistency.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Use an 8px grid system. Unexpected layouts within grid constraints. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere with creative forms like gradient meshes, layered transparencies, dramatic shadows, decorative borders.

**What to AVOID:**
- Generic AI aesthetics (purple gradients on white, cookie-cutter patterns)
- Overused font families (Inter as primary, Roboto, Arial)
- Cliched color schemes
- Predictable layouts

**What to EMBRACE:**
- Bold, intentional design choices
- High contrast and dramatic visual hierarchy
- Sophisticated, thoughtful animations
- Unique spatial compositions
- Attention to micro-details (shadows, borders, transitions)

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
