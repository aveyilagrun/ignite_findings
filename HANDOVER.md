# Where the project stands

## In one paragraph

The project measures gender representation and research impact in energy research publications.
- **The UK phase (2024)** was completed as an MSc project. It covered representation, impact, topic modelling, word embeddings and networks.
- **The multi-country phase (2025)** extended the representation and impact analysis to 8 countries and 6 Elsevier journals. Results were presented at the IGNITE Network+ Annual Event 2025.
- **The paper.** An article draft for *Energy Research & Social Science* (`paper/main.tex`).

## Decisions needed

1. Should we keep article–country records (17,148) or use unique articles (15,730)? The 1,267 multi-country articles are counted once per country at the moment.
2. Gender-classification validation is the biggest weakness. Should we hand-label a sample (stratified by country), or compare against a second tool (e.g. just giving the info to Claude/GPT to classify)?
3. Usage and social media metrics are not comparable across countries (29.7% of UK records have a usage value, against 1–3% elsewhere).

## Suggested next steps

1. Expand the literature review and references.
2. Justify the choice of countries and journals in the introduction, and work through the blue [NOTE] items in the paper.
3. Fix the duplication at the source: when `process_data.ipynb` or the notebook is next used, drop the *Solar Energy Materials and Solar Cells* rows from the `solar_energy_<country>` files, or de-duplicate on DOI and country as the script does.
4. Remaining checks:
   - Use career age instead of h-index as the seniority control? The h-index is measured at collection time and includes the citations of the paper itself.
   - Cluster standard errors by first author (12,139 unique first authors for 17,148 records).
5. Graphical abstract: last step, once the paper is in good shape.
