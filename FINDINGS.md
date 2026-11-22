# Findings

Only findings reproduced by the scripts on the current data. Numbers are in `results/headline_stats.md` and `results/extra_analysis.md`.

## Data

- 6 Elsevier journals, 8 countries, 2010–2025.
- 17,148 article–country records, 15,730 unique articles. 1,267 articles appear under more than one country.
- 2025 is partial (141 records).
- Gender is the Namsor prediction for the first author, with no confidence threshold.

## Representation

1. Women are 26.8% of first authors (4,593/17,148; 95% CI 26.1–27.5). Counting each article once gives the same 26.8%.
2. By journal: Appl. Catal. A 34.4%, Energy Policy 28.8%, IJ Greenhouse Gas Control 28.6%, IJ Hydrogen Energy 26.0%, Sol. Energy Mater. Sol. Cells 24.3%, Solar Energy 22.2% (p < 0.001). The ranking is the same at confidence thresholds 0.6 and 0.7.
3. By country: Singapore 32.2%, France 30.4%, USA 29.3%, Switzerland 27.8%, UK 26.6%, South Africa 26.2%, Canada 23.5%, Germany 23.4% (p < 0.001). The ranking depends on the classifier (see 21).
4. Country and journal differences both remain when modelled together, so journal mix does not explain the country differences. Odds ratios vs Germany: Singapore 1.58, France 1.40, USA 1.30, Switzerland 1.28, UK 1.15.
5. Country differences are not the same in every journal (interaction p < 0.001). For example, Switzerland is 37.9% in Energy Policy but 16.0% in Solar Energy.

## Trend

6. Female first authorship rose by 0.37 pp/year over 2010–2024 (r = 0.79, p < 0.001): 26.6% in 2010, a low of 22.8% in 2013, 29.8% in 2024.
7. The trend holds at confidence ≥ 0.6 (+0.34) and ≥ 0.7 (+0.25), with one row per article (+0.34), and with country and journal controls.
8. Including the partial year 2025 makes the trend non-significant (p = 0.25). This is where the old "no trend" result came from.
9. By journal, the rise is strongest in Solar Energy (15.9% in 2010–14 to 25.5% in 2020–24) and Energy Policy (25.4% to 32.3%). Both are significant. The other four journals rise less and are not clearly significant.
10. By country, the rise is significant in the USA (24.3% to 33.8%), Germany (20.4% to 27.2%) and Canada (20.5% to 26.6%). France is flat at about 30%. Trends differ between countries (p = 0.03).
11. Among authors appearing as first author for the first time, the female share rose from 25.6% (2012) to 30.1% (2024), +0.42 pp/year (p = 0.005).

## Seniority and careers

12. The female share falls steadily with seniority: 30.6% of articles by first authors with h-index 0–2, 25.4% at h 11–20, 20.9% at h 21–40 and 13.4% at h 41+. The pattern is the same per unique author and at confidence ≥ 0.6.
13. Female first authors have lower h-indices: mean 11.2 vs 14.7, median 8 vs 10 (p < 0.001). Counting each author once: mean 10.3 vs 13.0.
14. Women are less likely to appear again as first author: 16.0% of female first authors have two or more articles in the data, against 19.6% of men (p < 0.001). Women are 29.0% of authors with one article and 16.9% of authors with five or more.
15. Female first authors are less often the most senior person on the paper: they have the highest h-index in the team in 7.2% of articles, against 11.6% for men.

## Teams

16. Female-first-authored articles have slightly larger teams (mean 5.0 vs 4.8 authors, p < 0.001).
17. Women are 19.1% of first authors on solo-authored articles, against 27.1% on multi-authored ones. Most solo articles are in Energy Policy (15.3% of its articles), where women are 23.7% of solo authors and 29.8% of first authors in teams.
18. Articles with authors in more than one study country have the same female share as the rest (28.0% vs 26.7%, p = 0.31).

## Citations

19. Raw gap: male-first-authored papers get 7.13% more citations (mean 43.10 vs 40.23, median 24 vs 23). Not significant (p = 0.10).
20. With controls for year, journal and country the difference is +1.9% for women (p = 0.25). Adding team size and co-author seniority gives +1.1% (p = 0.53). No model shows a citation penalty for women.
21. Adding first-author h-index gives +6.0% for women (p < 0.001) in the main model, but only +3.3% (p = 0.20) in a Poisson model and +2.9% (p = 0.21) at confidence ≥ 0.7. So "no penalty" is safe, "women are cited more" is not.
22. Women are equally represented among highly cited articles: 25.7% of the top 10% within journal and year, against 26.4% overall. 10.0% of female-first-authored and 10.4% of male-first-authored articles reach the top 10% (p = 0.55).
23. The gap did not narrow after 2020: 4.2% (2010–19) vs 4.8% (2020–25), neither significant.
24. Captures, usage and social media show no gender difference. Mentions are slightly higher for women (0.39 vs 0.34, p = 0.04).

## Countries and topics

25. Citations follow output. Germany and the UK have 40.1% of citations and 40.7% of records.
26. Usage and social media cannot be compared across countries. 29.7% of UK records have a usage value, against 1–3% elsewhere. One record holds 26.6% of all usage.
27. Journal mix differs by country. Hydrogen is 55.9% of Canada, 51.1% of South Africa and 44.6% of France. Solar materials is 29.5% of Switzerland and 21.1% of Germany. Energy Policy is 30.6% of the UK, 27.2% of Switzerland and 26.1% of the USA.
28. Keywords differ by gender. Highest female share: oxygen reduction reaction (49.3%), dark fermentation (44.6%), life cycle assessment (42.9%), energy transition (41.4%). Lowest: silicon (10.2%), wind power (11.3%), simulation (15.5%), hydrogen safety (16.2%). 25 of 134 common keywords differ from the average at p < 0.05, where about 7 would be expected by chance.

## Gender classification

29. Namsor is less confident for female-predicted names (mean 0.707) than male-predicted ones (0.829), even for clear names: Sarah, Laura and Julia average 0.69–0.74, Michael, Thomas and David 0.94–0.96.
30. The female share falls as the confidence threshold rises: 26.8% with none, 24.5% at 0.6, 17.2% at 0.7, 9.5% at 0.8, 4.9% at 0.9. A threshold removes women disproportionately.
31. Low-confidence labels are close to guesses: 46–48% of records below 0.7 are labelled female. So 26.8% is probably somewhat too high.
32. The country ranking is sensitive to this. At confidence ≥ 0.7 Singapore drops from first (32.2%) to second-lowest (15.4%) and keeps only 40% of its records. France stays near the top and Canada at the bottom at every threshold.
33. 755 records (4.4%) have a first author with initials only. Excluding them changes nothing (26.9%).
