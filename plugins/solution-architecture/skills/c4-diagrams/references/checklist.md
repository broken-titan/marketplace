# Review checklist

Run on every emit and in **review** mode. A fail is a named finding (diagram, box or edge, what is wrong).

1. **Every box named.** No anonymous nodes, no empty labels, no "system 1".
2. **No orphan edges.** Every edge joins two named boxes that exist on *this* diagram. No edge to a missing id.
3. **Levels agree.** Every Container belongs to a Context system. Deployment nodes host containers that exist on the Container diagram. A person or neighbor system does not appear as a container inside this system unless the evidence says it is in-process.
4. **One purpose per diagram.** Context does not sprout databases. Container does not sprout classes. Deployment does not re-tell the Context story with different names.
5. **Relationships have verbs.** "Uses", "reads", "authenticates", "publishes" — not a bare line.
6. **Names match the evidence.** SAD / RSCOP / repo names win. A new name is a labeled assumption or a fail.

Review mode stops at the findings list. Design / prose / update modes fix the diagram, then re-run this list.
