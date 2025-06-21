```plantuml
@startuml
' Dark theme
skinparam backgroundColor #2B2B2B
skinparam defaultTextColor #EEEEEE
skinparam rectangle {
  BackgroundColor #333333
  BorderColor #AAAAAA
  RoundCorner 15
}

title Modelo OCC (Ortony, Clore & Collins)

' Top-level categories
rectangle "Goals" as Goals

rectangle "Consequences of Events" as CE
rectangle "Actions of Agents" as AA
rectangle "Aspects of Objects\n(Attitudes)" as AO

Goals --> CE
Goals --> AA
Goals --> AO

' Consequences of Events subtree
rectangle "Focusing On" as FO
CE --> FO

rectangle "Consequences for Other" as COther
rectangle "Consequences for Self" as CSelf
FO --> COther
FO --> CSelf

' Fortunes of Others
rectangle "Desirable for Other" as DesOther
rectangle "Undesirable for Other" as UndesOther
COther --> DesOther
COther --> UndesOther

DesOther --> "Happy-for"
UndesOther --> "Resentment\nGloating\nPity"

' Consequences for Self: Prospect-based
rectangle "Prospect Relevant" as ProspectRel
rectangle "Prospect Irrelevant" as ProspectIrrel
CSelf --> ProspectRel
CSelf --> ProspectIrrel

ProspectRel --> "Hope\nFear"
ProspectIrrel --> "Joy\nDistress" <<Well-Being>>

' Prospect-confirmed / disconfirmed
rectangle "Confirmed" as Confirmed
rectangle "Disconfirmed" as Disconfirmed
ProspectRel --> Confirmed : prospect-confirmed
ProspectRel --> Disconfirmed : prospect-disconfirmed

Confirmed --> "Satisfaction\nFear-confirmed"
Disconfirmed --> "Relief\nDisappointment"

' Well-being / Attribution compounds
rectangle "Well-Being\n/ Attribution" as WBAttr
ProspectIrrel --> WBAttr

WBAttr --> "Gratification\nRemorse"
WBAttr --> "Gratitude\nAnger"

' Actions of Agents subtree
rectangle "Approving / Disapproving" as Approvals
AA --> Approvals

rectangle "Self-Agent" as SelfAgent
rectangle "Other-Agent" as OtherAgent
Approvals --> SelfAgent
Approvals --> OtherAgent

SelfAgent --> "Pride\nShame" <<Attribution>>
OtherAgent --> "Admiration\nReproach"

' Aspects of Objects subtree
rectangle "Appealing-ness" as Appealing
AO --> Appealing

Appealing --> "Liking\nDisliking" 
"Liking\nDisliking" --> "Joy\nDistress" <<Attraction>>
@enduml
```
![plantuml.com/plantuml/dsvg/VLNVRzCm47xtNt4A4cmI4GB4opHDItzqW42Pkg6zzCLDBfsfOmVRcQWG_plEkKtT9IFJrFlntVc-hnVtsZfkN5jBzWPct6p1FMADp6w5QhZXDQnviTqOtQfoggKsyEh3fFkB42LMl9Nk7d-xFMHEJmGnM3YkDXBX3mEOF6_vaPukeqs9PX_DwF7HPO0QXGRUVs9_6NF2-LxVTObIGpwTmbbkd5Qxjp3rfGYlmVUGGjbpvddTwoQL-8GI2kvmeur0ouuZ9JUQIvi0jq0MYtDJhIp-Qb4LQ45NC7z2vG9uEe-1MU64LeJ9DZqcoqumjl4EOVBrpyvSgRFCUJPjYVOyLEICqHYGfbV-ZCZ9ijZ9EshZuu5jryuWncSlTD5QeJQGApfdaRFfd3fvwqN6bJQG-vKmWJ6P_mNVeQm2jhFO8WyqgB3tAEMdNsZZMXKc9uIDUy_G2iFNtZoTmiS7S_nGvGjeoWHyc896c0rZCPBv_36HVEPDiqjztuGHA4ejqQ9ojVzVgHkfkVCIhzIjSBkaOpYgpmNS6ashaAwvnJ8cSiZ04ltASkM8n27gWwFWByQCmIdCI6wQDcupZ0OqYq1xzhh1bLeWz_HFi27zLUzMQYQiCsXj0fUN3oXbEa4lnDMLr-18jj2g4gR64jv1AMplFbke40nBD0QPKMc4YWE3yViMS05DFCauFFGQLfpCo_gcGO8xxeIjEDq0GQdqE26BMnwMHWgiI3M_MLg41QA58V7MdNXUfCmv8zPjrnOANJVTFMXZAOvIhzG9d7Hvc7IHuNTsIB3m6MQwCPv49GeUI2onriPYCi3GNRLIcTgWeOa75z_OxPCrNicdm2gm3YxD6PBTpPjbTD0n4FVe5ZQb8wYgSycBCVHcHY3o0wflIaTGzJ0U5x0U4zZV6j4nltlaDNPx7idj5vqA8tHMriBqOleZUF58UWr-15uI3Bdq2gKAhIKkVOXbT8z60TQRuV1lOkjjMZ19PW9i93Z-0XCnNknvNQCgsrh-0m00](https://www.plantuml.com/plantuml/dsvg/VLNVRzCm47xtNt4A4cmI4GB4opHDItzqW42Pkg6zzCLDBfsfOmVRcQWG_plEkKtT9IFJrFlntVc-hnVtsZfkN5jBzWPct6p1FMADp6w5QhZXDQnviTqOtQfoggKsyEh3fFkB42LMl9Nk7d-xFMHEJmGnM3YkDXBX3mEOF6_vaPukeqs9PX_DwF7HPO0QXGRUVs9_6NF2-LxVTObIGpwTmbbkd5Qxjp3rfGYlmVUGGjbpvddTwoQL-8GI2kvmeur0ouuZ9JUQIvi0jq0MYtDJhIp-Qb4LQ45NC7z2vG9uEe-1MU64LeJ9DZqcoqumjl4EOVBrpyvSgRFCUJPjYVOyLEICqHYGfbV-ZCZ9ijZ9EshZuu5jryuWncSlTD5QeJQGApfdaRFfd3fvwqN6bJQG-vKmWJ6P_mNVeQm2jhFO8WyqgB3tAEMdNsZZMXKc9uIDUy_G2iFNtZoTmiS7S_nGvGjeoWHyc896c0rZCPBv_36HVEPDiqjztuGHA4ejqQ9ojVzVgHkfkVCIhzIjSBkaOpYgpmNS6ashaAwvnJ8cSiZ04ltASkM8n27gWwFWByQCmIdCI6wQDcupZ0OqYq1xzhh1bLeWz_HFi27zLUzMQYQiCsXj0fUN3oXbEa4lnDMLr-18jj2g4gR64jv1AMplFbke40nBD0QPKMc4YWE3yViMS05DFCauFFGQLfpCo_gcGO8xxeIjEDq0GQdqE26BMnwMHWgiI3M_MLg41QA58V7MdNXUfCmv8zPjrnOANJVTFMXZAOvIhzG9d7Hvc7IHuNTsIB3m6MQwCPv49GeUI2onriPYCi3GNRLIcTgWeOa75z_OxPCrNicdm2gm3YxD6PBTpPjbTD0n4FVe5ZQb8wYgSycBCVHcHY3o0wflIaTGzJ0U5x0U4zZV6j4nltlaDNPx7idj5vqA8tHMriBqOleZUF58UWr-15uI3Bdq2gKAhIKkVOXbT8z60TQRuV1lOkjjMZ19PW9i93Z-0XCnNknvNQCgsrh-0m00)


```
@startuml
' Dark theme styling
skinparam backgroundColor #2B2B2B
skinparam defaultTextColor #EEEEEE
skinparam rectangle {
  BackgroundColor #333333
  BorderColor #AAAAAA
  RoundCorner 15
}

title DETT Architecture (Ortony, Clore & Collins Extension)

' Core BDI-like loop
rectangle "Beliefs" as Beliefs
rectangle "Intentions" as Intentions

' DETT modules
rectangle "Disposition\nModule" as Disposition
rectangle "Trigger\nModule" as Trigger
rectangle "Emotion\nGenerator" as Emotion
rectangle "Tendency\nModule" as Tendency

' Relationships
Beliefs --> Disposition : appraise according to
Beliefs --> Trigger     : identify trigger
Disposition --> Emotion : shapes evaluation
Trigger --> Emotion     : triggers appraisal
Emotion --> Tendency    : influences
Tendency --> Intentions : modifies intentions

@enduml
```

![https://www.plantuml.com/plantuml/dsvg/TPBFRnC_4CNl_Yj6_KfVKga51SI50sgIXef3HKGgJhrCxSd6YjTUZUsb4U9_PxoR7oOIarlcyvvVtkGk9kIKMwVUm3to3jAMMeAOzixwHiMTzHqojl22UjTmoDuiWWiC_xsVbqz56DfWTkc9NjC1MGvJ8KmweMySmIy5CB-q_31CsGGsn8TlPyCeWEyZofuOfX_LRwMIJUArUloo9kvXndfh4-cKcM2ojgudRj439K3tzbh9JrmdssPd0Rs1ZbXJbspmwfphwa0y-ydIzvQ3RyadTF3LTpd5wol0U7IfPQkJcIWVWycEHlQyaFTBLD2XxO8NrrWRp6rmeTd3Et5dYl7PhxRxQ0Fy3qjFtEm7Dw5gqSDw1KzC9FJa8Q2BDw96Rv1Dl147fWqnUKs7uCBNycKRIZ1qCEiwHXlHYT5q2jyM2rYXvODisSg-n5-4njjaUv9KzDgLd1VrdOcn1F6RvQPqI0RkITiY65q5_IlCoUyi7IhGwAIL7yGl9QW-7g7mIXqFUdlxkQeQP3wD1vOegbeKJaeim0Zbpc0Yw8QoomKkQUdiJEFO4q5lSMYpyX9uREe8n-6GOCi_HmdyJx2SeSVXnH6kjWMMfge8JSFKbCmvMMVJNbNhGfTYJdGaHpeDvoAT4wbgM-1ZVwErBXaYu6PJH3y3EwFko9lSkZy0]

![https://www.plantuml.com/plantuml/dsvg/TPBFRnC_4CNl_Yj6_KfVKga51SI50sgIXef3HKGgJhrCxSd6YjTUZUsb4U9_PxoR7oOIarlcyvvVtkGk9kIKMwVUm3to3jAMMeAOzixwHiMTzHqojl22UjTmoDuiWWiC_xsVbqz56DfWTkc9NjC1MGvJ8KmweMySmIy5CB-q_31CsGGsn8TlPyCeWEyZofuOfX_LRwMIJUArUloo9kvXndfh4-cKcM2ojgudRj439K3tzbh9JrmdssPd0Rs1ZbXJbspmwfphwa0y-ydIzvQ3RyadTF3LTpd5wol0U7IfPQkJcIWVWycEHlQyaFTBLD2XxO8NrrWRp6rmeTd3Et5dYl7PhxRxQ0Fy3qjFtEm7Dw5gqSDw1KzC9FJa8Q2BDw96Rv1Dl147fWqnUKs7uCBNycKRIZ1qCEiwHXlHYT5q2jyM2rYXvODisSg-n5-4njjaUv9KzDgLd1VrdOcn1F6RvQPqI0RkITiY65q5_IlCoUyi7IhGwAIL7yGl9QW-7g7mIXqFUdlxkQeQP3wD1vOegbeKJaeim0Zbpc0Yw8QoomKkQUdiJEFO4q5lSMYpyX9uREe8n-6GOCi_HmdyJx2SeSVXnH6kjWMMfge8JSFKbCmvMMVJNbNhGfTYJdGaHpeDvoAT4wbgM-1ZVwErBXaYu6PJH3y3EwFko9lSkZy0]
