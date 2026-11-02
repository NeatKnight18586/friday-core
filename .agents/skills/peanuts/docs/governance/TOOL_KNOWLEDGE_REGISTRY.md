# Tool and Knowledge Registry

**Status:** Initial governance specification; candidate inventory only  
**Version:** 0.4.0-draft  
**Last reviewed:** 2026-11-01

## 1. Purpose

Peanuts should select tools and knowledge sources to answer a defined question or perform a specific operation. This registry prevents indiscriminate tool use, hidden dependencies, stale recommendations, and confusion between a source of information and a tool that acts on information.

The registry is a governance model, not a claim that every listed tool is installed, accessible, free, authoritative for every task, or required.

## 2. Distinguish resource types

- **Knowledge source:** contains information or evidence (standard, research paper, official event page, dataset, patent, manual).
- **Discovery/index tool:** helps locate knowledge (academic search, DOI index, patent search, web search).
- **Execution tool:** performs an operation (code interpreter, spreadsheet, API client, design/prototype tool, terminal).
- **Validation tool:** checks an output (test runner, schema validator, linter, evaluator, accessibility checker).
- **Integration/connector:** accesses an external service or account under granted permissions.
- **Runtime/platform:** provides the environment where a skill or agent operates (Claude Code, Codex, ChatGPT Project, API sandbox).

Do not confuse a search index with a primary source, a code snippet with a tested integration, or an AI summary with verified evidence.

## 3. Tool selection procedure

Before selecting a tool, record:

1. Task/question and expected result.
2. Required capability (search, read, compare, calculate, edit, execute, test, publish, etc.).
3. Authority and directness needed.
4. Whether the current runtime actually provides access.
5. Data sensitivity and permission implications.
6. Cost, usage limits, licensing, and time constraints.
7. Limitations and a fallback.

Prefer the least powerful tool that can reliably complete the task. Do not request broad permissions for a narrow operation. If a required tool is unavailable, state the limitation and use an honest fallback; never invent tool output or imply that a task ran.

## 4. Candidate resource categories

| Category | Candidate sources/tools | Typical use | Selection caution |
|---|---|---|---|
| Official event intelligence | Organizer site, rulebook, official FAQ, submission portal | Eligibility, dates, deliverables, judging, restrictions | Prefer the current official edition; preserve access date and exact source. |
| Academic discovery | Google Scholar, Semantic Scholar, Crossref, publisher sites | Research literature and citation trails | Search indexes are discovery aids; inspect original papers and methods. Crossref REST API can retrieve deposited scholarly metadata; metadata is not full text or a quality judgment. |
| Nature inspiration | AskNature, scientific papers, biological databases | Biological functions and strategies | Confirm actual biological mechanism and ecological context. |
| History | Archives, libraries, scholarly books/articles, primary records | Historical systems, mechanisms, chronology | Corroborate popular claims and avoid anachronism. |
| Patent/prior art | WIPO PATENTSCOPE, Google Patents, national patent offices | Related inventions and technical landscape | A search does not establish legal novelty or freedom to operate. |
| Product/UX research | Direct interviews/observation, product documentation, NN/g, IDEO Design Kit | User needs, usability, alternatives | Respect consent, sample limits, accessibility, and privacy. |
| Standards and assurance | ISO, IEEE, NIST, OWASP, NASA handbooks | Requirements, quality, risk, security | Verify status/edition and use only relevant parts. Standards may require paid access. |
| Software documentation | Official language, framework, API and vendor docs | Technical capability and implementation choices | Check version, deprecation, quotas, pricing, license, and support. |
| Evaluation | Unit/integration tests, schema validators, traces, graders, user tests | Correctness, reliability, quality, regression | A passing check proves only what that check covers. |
| Collaboration/prototyping | Diagramming, spreadsheets, design tools, issue trackers | Make workflows and ideas inspectable | Check exportability, access controls, terms, and ongoing cost. |

## 5. B5 research tool-selection notes

- Prefer the runtime's current native web search and page/document inspection tools for event and broad web research. Verify the tool is actually available before planning around it.
- Use Crossref for DOI resolution and scholarly metadata discovery where useful. It is a metadata service, not a full-text repository or study-quality evaluator. Its public REST API requires no registration; the polite pool can be requested with an identifying `mailto` parameter. Do not hardcode personal contact details into the public repository. See https://www.crossref.org/documentation/retrieve-metadata/rest-api/ and https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/.
- Use Semantic Scholar or other scholarly indexes to discover papers and citation trails; inspect the original paper/publisher record for material claims.
- Use official organizer sites for event rules; academic databases are not authoritative for current deadlines or eligibility.
- Use direct interviews/observation only when the team can meet consent, privacy, accessibility, safety and analysis requirements.
- A tool unavailable in one host must have a documented fallback or be marked `not_available`; a skill must not invent search results or imply a tool ran.

## 6. Tool record (future registry entry)

For a tool that becomes a recurring dependency, record:

- Tool ID/name, provider, URL, category.
- Supported task/capability and expected output.
- Access path/runtime and permission required.
- Source authority/directness if it is a knowledge source.
- Version, last checked date, and lifecycle/deprecation state.
- Cost, quotas, license/terms, and availability conditions.
- Data sent, retention/privacy/security implications.
- Known limitations and failure modes.
- Fallback/alternative.
- Evaluation or acceptance check.

For one-off web research, a full registry entry is unnecessary; record sources and dates in the project's evidence register.

## 7. Knowledge quality rules

- Prefer the primary source for the claim being made.
- Check publication/updated date and whether the claim is time-sensitive.
- Inspect methods, sample, context, conflicts, and limitations for empirical research.
- Record source access date and exact version/edition for standards or software.
- Do not infer content from a search-result snippet when the full source is inaccessible.
- Preserve contradictory credible evidence.
- Recheck important vendor/platform capabilities during implementation.

## 8. Governance

Candidate tools are not automatically approved dependencies. Before a tool becomes part of the core workflow, assess whether it is necessary, replaceable, maintainable, sufficiently available, permissioned, and worth its ongoing cost. Prefer vendor-neutral output artifacts where practical. Do not let a tool choice dictate the problem definition.


## 6. B6 NUTS tool-selection notes

Select only the resource that fits the source domain and claim. These are discovery/knowledge candidates, not required dependencies or guaranteed runtime tools.

| Need | Candidate resource | Appropriate use | Limitation |
|---|---|---|---|
| Biological strategy discovery | AskNature | Search biological strategies by function | Discovery aid; verify key mechanism and ecological context in relevant scientific sources. |
| Biomimicry method | Biomimicry Toolbox Design Spiral | Define, biologize, discover, abstract, emulate, evaluate | Biology-specific; not the entire NUTS procedure. |
| Analogical reasoning foundation | Gentner (1983), Structure-Mapping | Distinguish relational mapping from surface resemblance | Theory guides analysis; it does not prove a transfer works. |
| Historical source criticism | ALA/RUSA, Library of Congress, archives and reputable scholarship | Find and interrogate primary sources; contextualize and corroborate | Primary sources can be biased, incomplete, altered, or misinterpreted. |
| Engineering contradiction | MATRIZ methodology and credible engineering sources | Investigate TRIZ where a genuine contradiction exists | Do not assume a matrix suggestion is a tested solution. |
| Prior-art discovery | WIPO PATENTSCOPE, national patent office tools, Google Patents | Identify potentially related patent publications and technical disclosures | Search is not a legal opinion, novelty determination, or freedom-to-operate analysis. |

NUTS must log actual tool access and source inspection. If a candidate tool is unavailable, use an honest fallback and mark the limitation. Do not claim that a database was searched when only its public landing page or a search-result snippet was seen.


## 8. Context/resource tools and measurements (B6.5)

Context tools are a distinct operational category: file/path inspection, project-state retrieval, schema filtering, indexing, summarization, and deterministic validators. Prefer repository-native scripts for exact tasks when they reduce repeated model-side processing and can be inspected/tested. A script result is only as reliable as its implementation and inputs; it does not establish factual truth unless the check is designed to do so.

When comparing approaches, use the same host/model/task/evidence setup where possible. Record exact input/output/cache tokens or cost only when the runtime exposes them. Otherwise use separately labelled proxies (files loaded, words/characters, tool calls, iterations, output length). Never infer provider token counts from character/word counts.

Do not add a vector database, embeddings, hosted retrieval service, or multi-agent orchestrator simply because the knowledge base grows. First test path/index/grep/structured records and host-native file search. Add heavier retrieval only when evaluation shows a concrete recall, latency, or usability problem that simpler methods cannot solve.
