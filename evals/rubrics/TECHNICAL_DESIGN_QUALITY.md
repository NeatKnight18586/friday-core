# Technical Design Quality Rubric

Assess whether the proposed design is adequate, proportionate, secure and implementable for the actual project. Adapt software-oriented categories to hardware, service, event or mixed systems.

| Dimension | Strong evidence | Weak / failing evidence |
|---|---|---|
| Fit and simplicity | Each component exists for a validated requirement, constraint or justified risk reduction; simplest adequate design considered. | Framework/stack fashion, speculative scale, unnecessary agents, databases or cloud services. |
| Boundaries | Users, external actors, responsibilities, trust boundaries and out-of-scope dependencies are explicit. | Unclear ownership, hidden coupling or implicit trust. |
| Data lifecycle | Data classes, sensitivity, ownership, purpose, validation, minimization, retention, deletion, backup and migration are considered. | Indefinite retention, unnecessary collection, unclear source of truth. |
| Interfaces | Contracts, field definitions, validation, authn/authz, idempotency, errors, versioning and compatibility are specified where relevant. | Unverified API assumptions or informal contracts. |
| Security and safety | Threats/misuse, assets, least privilege, secrets, abuse cases, fail-safe behavior and residual risks are addressed. | Boilerplate assurances or missing trust-boundary analysis. |
| Reliability | Failure modes, timeouts, bounded retries, degradation, fallback, recovery, rollback and stop conditions. | Assumes perfect networks, people or vendors. |
| Human factors | Accessibility, language, operating environment, training, ergonomics and user error considered. | Technical functionality treated as sufficient. |
| Operations | Deployment/setup, ownership, observability, maintenance, incident handling and resource/cost monitoring. | No support or ownership model. |
| Verification | Requirements map to tests, inspections, analysis, demonstrations or measurements; planned work is distinguished from results. | Testing is deferred, vague or claimed without evidence. |
| Alternatives | Consequential choices compare feasible alternatives and their trade-offs. | Chosen design is asserted as obviously best. |

Mark irrelevant categories N/A with rationale. Do not force software architecture onto non-software projects. Unverified vendor capabilities remain assumptions until checked against current authoritative documentation or experiments. Human or specialist sign-off is required when the risk warrants it.
