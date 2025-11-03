I have the following task that I need to work on. However I feel there is too much information missing. 
Can you help me ask some questions for clarification of the actual demmand? 

Investigate ways to migrate the data of one or more users between environments and regions. Below are some examples of usage for this requirement:

- A group of users have finished dogfooding a product in the beta environment and need to be moved to production environment
- There is an issue with an user in production and we would like to try to reproduce it in staging to further troubleshoot (in this case, a copy should be created, data should not be moved)
- A group of production users will start dogfooding new features of a product and need to be moved to the beta environment
- A QA has just finished testing changes in staging and would like to perform the same test in beta
- A group of users live in a country that has just set a new regulatory requirement that requires that data of applications being used in that country remain within the country - it should be possible to migrate data of such users to a region that is within that country

For all of the above examples, data cannot be lost in the migration process.

Absolutely, Lucas — great instinct to clarify before you build. Below is a **comprehensive discovery questionnaire** you can send to stakeholders to pin down the exact migration/copy requirements **without referencing any specific project**. I’ve organized it so you can pick the whole set or just the sections that apply to each scenario (copy to staging, move to beta, move across regions for residency, etc.).

---

## 1) Objectives & Scope

**1.1 Goals & Scenarios**

- What scenarios do we need to support? (e.g., **copy** for troubleshooting, **move** for dogfooding, **copy** for QA parity, **move** for data residency).
- For each scenario, is it a **one-time** operation, **repeatable workflow**, or **self-service tool**?
- What is the **definition of success** for each scenario?

**1.2 Entities in Scope**

- Which entities must be included? (e.g., **user**, **organization/company/tenant**, **teams**, **groups**, **subscriptions**, **roles**, **permissions**).
- Should the operation include **transitive associations** (e.g., forms, tasks, settings, attachments, messages, comments, events, preferences, tokens, webhooks, subscriptions, device bindings)?
- Are we migrating/copying **current state only**, **event history**, or both?

**1.3 Move vs Copy Semantics**

- For each scenario, should data be **moved** (removed/disabled at source after cutover) or **copied** (source remains intact)?
- If moved, what should happen to the **source account** post-migration (disabled, deprovisioned, deleted, left read-only)?
- If copied, should the target be **anonymized or masked**?

---

## 2) Environment & Region Topology

**2.1 Environments**

- Which environments are involved? (e.g., dev, test, staging, beta, production).
- Are **schema versions**, **feature flags**, and **configuration** aligned across environments? If not, what are the required **version mappings** or **compatibility rules**?

**2.2 Regions & Residency**

- Which **regions** are involved (source/target)?
- Are there **data residency** or **sovereignty** requirements (e.g., keep all data—including **backups**, **logs**, **telemetry**, **analytics**, **search indices**) in-region?
- Any **encryption** or **key management** constraints (e.g., customer-managed keys, in-country KMS, HSM)?

---

## 3) Identity, Access, & Tenancy

**3.1 Identity & Auth**

- How are identities managed (internal DB, external IdP)? Should we **preserve user IDs** or **re-seed new ones** in target?
- Do we need to migrate **passwords**, **SSO bindings**, **MFA/2FA** factors, **device tokens**, **API keys**?

**3.2 Access Control**

- Should **roles**, **permissions**, **entitlements**, and **feature flags** be replicated exactly or remapped by environment?
- Do we need to **mask or downscope** permissions in non-production targets?

**3.3 Tenancy/Company Handling**

- For multi-tenant data: when copying a user, should we **also copy the company/tenant**?
- If a company has been copied before, should subsequent users from that company be **attached to the existing copied company** or **create a new company**?
- How should **global uniqueness** be maintained (e.g., tenant aliases, namespace prefixes, GUID collision handling)?

---

## 4) Data Model, Associations & External Systems

**4.1 Data Inventory**

- List **all data stores** involved (databases, object storage, caches, search, analytics warehouse, message queues, config stores).
- For each, identify **entities** and **relationships** that must be included.

**4.2 Associations**

- Which associated objects must be included? (e.g., forms, tasks, tickets, files, comments, notifications, calendars, sessions, device bindings, webhooks).
- Should we copy **derived data** (indexes, caches, materialized views) or **rebuild** them at target?
- What about **audit logs**, **metrics**, and **usage analytics**?

**4.3 External Integrations**

- Are there **third-party links** to replicate (webhooks, OAuth connections, billing providers, CRM, support systems)?
- How should we handle **secrets** and **tokens**? Reissue at target or migrate as-is (compliance/security permitting)?

---

## 5) Data Quality, Consistency & Integrity

**5.1 Consistency Requirements**

- What **consistency guarantees** are required (strong, eventual)?
- Do we need a **point-in-time snapshot** or **incremental CDC** (change data capture) to avoid downtime?

**5.2 Conflict Resolution**

- How to handle **existing records** at target (skip, overwrite, merge, fail)?
- If IDs must be preserved but exist at target, how do we **resolve collisions**?
- Should we **lock/freeze** source user/company during final sync?

**5.3 Validation**

- What are the **pre-flight checks** (schema compatibility, quotas, rate limits, capacity)?
- What are the **post-migration checks** (record counts, referential integrity, functional login, permissions, end-to-end smoke tests)?
- Define **acceptance criteria** and **rollback criteria**.

---

## 6) Security, Privacy & Compliance

**6.1 PII/PHI/Confidential Data**

- For copies to non-production, must data be **masked, tokenized, or subsetted**?
- Are there **retention** and **right-to-be-forgotten** implications across copies?

**6.2 Legal & Compliance**

- Which frameworks apply (e.g., GDPR/LGPD/CCPA/HIPAA/SOC2)?
- Is **user consent** required for cross-environment/region movement?
- Do we need **audit trails** and **chain-of-custody** for the migration?

**6.3 Encryption & Keys**

- Requirements for **encryption in transit/at rest**; **key locality**; **key rotation** and **access controls**.

---

## 7) Operational Model & SLAs

**7.1 Scheduling & Downtime**

- What are the **allowed maintenance windows**, **RTO**, and **RPO** targets?
- Expected **volume** (users/companies) and data size (DB rows, GB/TB, object count)?
- Throughput/performance targets (e.g., N users/hour).

**7.2 Runbook & Ownership**

- Who **requests**, **approves**, **executes**, and **validates** the migration?
- Do we need **change management** (tickets, CAB approval)?
- **Rollback plan** and time limits for reverting.
- **Monitoring**, **alerting**, and **on-call** expectations.

**7.3 Tooling**

- Preferred approach: **API-based**, **export/import**, **database replication**, **event replay**, or **bespoke orchestrator**?
- Constraints: **rate limits**, **quotas**, **batch sizes**, **idempotency** requirements.

---

## 8) Scenario-Specific Clarifications

**A) Copy user(s) from production to staging for troubleshooting**

- Should data be **masked** in staging?
- Which **time window** of data is needed (last N days, full history)?
- Include **background jobs** and **scheduled triggers**? (e.g., notifications, webhooks)
- Include **attachments/files** and **search indices**, or rebuild indices only?

**B) Move user(s) from beta to production (dogfooding complete)**

- Do we **preserve identifiers** so links remain valid?
- What is the **cutover plan** (freeze → delta sync → switch → source disable)?
- Post-move, should **source data remain read-only** for audit?

**C) Move production users to beta to try new features**

- Is this **temporary** (need a dual-home or back-migration plan) or **permanent**?
- Any **feature flag/entitlement** changes needed on arrival?

**D) Replicate QA-tested data from staging to beta**

- Should staging data be **treated as non-authoritative** (conflict policy at beta)?
- Are there **schema/feature flag** differences between staging and beta?

**E) Regional moves for new residency requirements**

- Confirm **in-country storage** for **all** data types: primary DB, backups, logs, telemetry, analytics, object storage, caches, search.
- **Cross-border** restrictions for **migration pipeline** itself (can data transit other regions temporarily?).
- **Keys/KMS** location; **DR/failover** must also remain in-country?

---

## 9) Edge Cases & Non-Goals

- How to handle **partially migrated** entities if a failure occurs mid-flight?
- What if a user already exists on target with **divergent state**?
- Should we migrate **disabled/deleted** users or **archived** entities?
- Explicit **non-goals** (e.g., not migrating analytics, not preserving historical event streams, not moving webhooks).

---

## 10) Request Intake Template (you can reuse this)

**High-level Request**

- Purpose/scenario:
- Source environment/region:
- Target environment/region:
- Move or copy:
- One-time or repeatable:

**Population**

- Users (IDs/emails):
- Companies/tenants (IDs):
- Associated entities to include (checklist):
    - ☐ Organization
    - ☐ Roles/Permissions
    - ☐ Forms/Tasks/Workflows
    - ☐ Files/Attachments
    - ☐ Messages/Comments
    - ☐ Subscriptions/Webhooks
    - ☐ Device tokens/API keys
    - ☐ Audit logs/Events
    - ☐ Analytics/Reports
    - ☐ Search indices
    - ☐ Other: ________

**Data Handling**

- Preserve IDs? ☐ Yes ☐ No
- Conflict policy: ☐ Skip ☐ Overwrite ☐ Merge ☐ Fail
- Masking required? ☐ Yes ☐ No (rules: ________)
- Time window: ☐ All ☐ Last N days: __

**Operational**

- Desired window/date:
- Downtime allowed: __ minutes/hours
- RPO/RTO targets:
- Volume estimate (users, GB, objects):
- Approval owners:
- Rollback plan:

**Compliance & Security**

- Residency constraints:
- Encryption/key constraints:
- Audit trail required: ☐ Yes ☐ No

**Validation**

- Pre-flight checks:
- Post-migration acceptance criteria:
- Stakeholder sign-off:

---

## 11) Implementation-Level Clarifications (for engineers)

- Required **idempotency** and **reentrancy** (safe retries).
- **Namespace strategy** to avoid collisions (e.g., environment prefixes).
- **Schema drift** handling and **transform mappings**.
- **Dependency ordering** (organizations → groups → users → associations).
- **Batching** & **rate limiting** plan.
- **Observability**: metrics, logs, trace IDs per migration job.
- **Backfill** vs **live CDC** sync design.
- **Dry-run** mode and **diff reports**.

---

## 12) Definitions (to avoid ambiguity)

- **Copy**: Duplicate to target; source remains unchanged/active unless specified; may require masking.
- **Move**: Transfer authoritative ownership to target; source deactivated or deleted after verification.
- **Entity**: A primary object (user, company/tenant).
- **Association**: Any related object linked to an entity (forms, tasks, files, roles, messages, settings).
- **Cutover**: Final switch when target is authoritative.

---

### Want me to tailor this into a one-page intake form or a checklist you can send out as-is?

If you share:

- the environments/regions you use,
- typical data volume,
- and whether you need a **one-time migration** or a **self-serve tool**,

I can condense this into a clean form and a ready-to-run **migration runbook** (pre-flight → execute → validate → rollback).


Let's add a tag to all questions like 1.1.1, etc.  
Some questions I think I can already answer from the context I have, so I'll answer so you can make more specific questions:  
1.1.1 Preferably all of them  
1.1.2 We need to be flexible, so we should study a way to be compatible with both one-time and repeatable workflow  
1.1.3 That one we should probably keep  
1.2.1 That one we should probably keep and also ask how to generalize between projects  
1.2.2 Keep and also ask how to generalize between different projects  
1.2.3 Keep and also ask how to generalize between different projects  
1.3.1 This is very clear in the description. No data should be lost  
1.3.2 Also clear in the description, nothing should change in the original account  
1.3.3 Why would it need to be masked or anonymized?  
2.1.1 Assume all  
2.1.2 This one we should keep, perhaps even break into more questions to get even more details  
2.2.1 Keep, but we can also check this by ourselves so no need to clarify. You should assume I have access to check somethings  
2.2.2 Break into more questions to get more details  
2.2.3 Break into more questions to get more details 


3.1.1 Keep or break into more questions to get more details  
3.1.2 Keep or break into more questions to get more details  
3.2.1 Keep or break into more questions to get more details  
3.2.2 Keep or break into more questions to get more details  
3.2.1 Break into more questions to get more details  
3.2.2​ ‌Break into more questions to get more details 
3.3.1 This question is confusing. What do you mean by multi-tenant data. Explain these terms add examples if necessary to make the question clearer
3.3.2 ‌Break into more questions to get more details 
3.3.3 This question is confusing. Explain these terms add examples if necessary to make the question clearer.

4.1 No questions were asked
4.2.1 Assume all
4.2.2 Assume yes
4.2.3 Assume yes

4.3.1 Break into more questions to get more details 
4.3.2 