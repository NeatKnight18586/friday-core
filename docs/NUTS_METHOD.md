# NUTS — Cross-Domain Innovation Method

**Status:** Experimental Peanuts method; Stage 0.5 specification draft  
**Version:** 0.2.0-draft  
**Guiding phrase:** Nothing New Under the Sun

## 1. Purpose

NUTS is Peanuts' method for learning from existing systems and exploring whether their useful mechanisms can be transferred to a different problem. It is inspired by *Steal Like an Artist*, analogical reasoning research, biomimicry, historical and engineering case analysis, and design practice.

NUTS is **not** a claim that novelty is impossible, a license to copy, or proof that a proposed concept is original. The Peanuts procedure itself is experimental and must be evaluated.

## 2. Core distinction: copy a mechanism, not an appearance

A weak analogy notices surface resemblance: two things look alike or share a word.

A stronger analogy identifies relationships and mechanisms: what entities interact, what constraints they face, what process produces the result, and which relationships may map onto the target problem.

Dedre Gentner's Structure-Mapping Theory is a useful theoretical foundation: analogical reasoning maps relational structure from a base domain to a target domain, rather than relying only on object similarity. This is a thinking aid, not a guarantee that a transfer will work.

## 3. Source domains

Choose domains based on the function and context of the target problem. Possible families include:

| Domain | Useful mechanisms to investigate | Suitable questions |
|---|---|---|
| Nature and biology | Adaptation, sensing, resilience, distributed coordination, resource efficiency, feedback, self-organization. | How does the organism/ecosystem perform the function under its environmental constraints? |
| History and civilization | Logistics, relay networks, governance, communication, trade, collective action, resource allocation. | What historical context created the need, and how did the system coordinate people/resources? |
| Engineering and physical systems | Feedback control, redundancy, modularity, load distribution, fault tolerance, materials, optimization. | What constraints or trade-offs did the design resolve? |
| Culture and social systems | Norms, trust, incentives, rituals, peer coordination, informal networks, shared knowledge. | What social mechanism changes behavior or coordinates groups? |
| Economics and operations | Matching, queues, markets, routing, inventory, distributed work, incentives. | How are scarce resources allocated and bottlenecks managed? |
| Existing products and processes | Interaction patterns, service design, workflow, architecture, business model. | What already solves part of the problem, and what can be adapted or improved? |

Not every domain is relevant to every project. Do not require a minimum number of inspiration sources or force a biology analogy when another domain is more relevant.

## 4. NUTS process

### Step 1 — Define the target function and constraints

Describe the problem without assuming a solution. Identify the function that must be performed, context, constraints, stakeholders, success criteria, and failure conditions.

### Step 2 — Search selectively across domains

Choose the most promising source families based on the function. Search for documented examples, not just attractive images or repeated internet anecdotes. Follow a small number of promising leads deeply rather than searching every domain exhaustively.

### Step 3 — Understand the source system

Establish its original problem, context, actors/components, inputs, outputs, constraints, operating process, strengths, and limitations. Use reliable sources. Avoid anachronistic or oversimplified historical claims.

### Step 4 — Map relationships and mechanisms

Identify what interacts with what, how information/material/people/resources move, what triggers action, what feedback exists, and how the system handles failure or constraint. Separate essential relationships from incidental features.

### Step 5 — Abstract the transferable principle

Restate the mechanism in domain-neutral language. For example: “A task can move through a sequence of local handoffs when no single direct connection spans the entire route.” This is an abstract pattern, not yet a product idea.

### Step 6 — Transfer and inspect the mismatch

Ask how the principle might apply to the target problem. Compare the source and target contexts. Identify which relationships map, which assumptions differ, and what breaks in transfer. A valid source mechanism can still be unsuitable for the target context.

### Step 7 — Recombine where useful

Consider combining two or more mechanisms only if each contributes a clear function. Explain the contribution of each source and the integration trade-offs. More inspirations do not automatically make a better idea.

### Step 8 — Check existing solutions and prior art

Search whether the proposed mechanism or combination is already used in products, research, patents, or open-source work. Distinguish “new to this project/team” from “new to the world.” Do not promise legal novelty or freedom to operate.

### Step 9 — Create a testable concept hypothesis

Describe the proposed mechanism, target user/problem, expected benefit, key assumptions, likely failure modes, and smallest useful experiment or prototype.

### Step 10 — Evaluate and attribute

Assess source accuracy, mechanism abstraction, relational mapping, transfer fit, user value, feasibility, limitations, existing alternatives, and attribution. Reject analogies that add decoration but no decision value.

## 5. Analogy Card schema (conceptual)

Each useful source should be captured with:

- `analogy_id`
- Source name and domain.
- Original context and problem.
- Primary/credible sources and access date.
- Actors/components and relationships.
- Mechanism and constraints.
- Abstract principle.
- Proposed target problem and transfer mapping.
- Transfer gaps and failure conditions.
- Existing solutions/prior-art check.
- Potential concept(s) and testable hypotheses.
- Attribution and rights/licensing notes.
- Confidence and unresolved questions.

The exact machine-readable schema will be designed in the data/schema milestone; this conceptual record is not a final JSON schema.

## 6. Branch-specific methods

- **Biological inspiration:** use the Biomimicry Design Spiral where appropriate: Define, Biologize, Discover, Abstract, Emulate, Evaluate. Biological strategies must be understood in their real ecological context; do not turn an organism's trait into a simplistic product metaphor.
- **Historical inspiration:** reconstruct context, constraints, actors, incentives, logistics, and outcomes before abstracting. Separate documented history from popular retellings.
- **Engineering inspiration:** use functional decomposition, constraint analysis, feedback/control concepts, reliability patterns, and TRIZ-style contradiction analysis when appropriate.
- **Cultural/social inspiration:** examine norms, institutions, trust, incentives, governance, power, and context. Avoid stereotypes and assumptions that a mechanism transfers unchanged between cultures.
- **Existing product/process inspiration:** compare workflows, value propositions, architecture, and limitations. Respect intellectual property, licenses, and confidentiality.

## 7. Evaluation criteria

Evaluate NUTS outputs against:

1. Relevance to the real problem.
2. Source accuracy and provenance.
3. Quality of mechanism understanding.
4. Strength of relational mapping.
5. Explicit recognition of transfer mismatch.
6. Usefulness of recombination.
7. Differentiation from known alternatives (within the search scope).
8. User value and feasibility.
9. Actionable testability.
10. Attribution and rights awareness.

A good result may be “no useful analogy found.” The method should not be rewarded for generating many analogies if they are inaccurate or irrelevant.

## 8. Creative attribution and intellectual property

Austin Kleon's *Steal Like an Artist* is a creative influence for collecting and recombining ideas; it is not evidence that the NUTS procedure works and not permission to reproduce the book's expression. Peanuts should credit identifiable influences and respect copyright, patents, trademarks, licenses, confidentiality, and cultural knowledge rights. It cannot certify legal originality or freedom to operate.

## 9. References

- Gentner, D. (1983). “Structure-mapping: A theoretical framework for analogy.” *Cognitive Science*, 7(2), 155–170. https://doi.org/10.1016/S0364-0213(83)80009-3
- Biomimicry Institute, Biomimicry Design Process: https://toolbox.biomimicry.org/methods/process/
- Austin Kleon, *Steal Like an Artist*: https://austinkleon.com/steal/
