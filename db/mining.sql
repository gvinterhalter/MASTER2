with kw2go_mapping as (
select kw.name, go.name, go.namespace, kw.ac, go.id
from keywords kw FULL OUTER JOIN kw2go on kw.ac=kw2go.kw
                 FULL OUTER JOIN goterms go on kw2go.go=go.id
where kw.category='KW-9992')
--
-- select namespace, count(*) from kw2go_mapping
-- GROUP BY namespace;

, missing as (
    SELECT DISTINCT org.ac as kw
    FROM kw2go_mapping AS org
    WHERE namespace IS NULL OR NOT exists(SELECT *
                                          FROM kw2go_mapping AS dup
                                          WHERE dup.id = org.id AND dup.namespace = 'MF')
)


, counts as (
    SELECT
      missing.kw,
      prot2go.go,
      count(prot2kw.prot) as n
    FROM missing
      JOIN prot2kw ON prot2kw.kw = missing.kw
      JOIN prot2go ON prot2go.prot = prot2kw.prot
      JOIN goterms g ON prot2go.go = g.id

    WHERE TRUE
          --   and missing.kw='KW-0731'
          AND g.namespace = 'MF'
    GROUP BY missing.kw, prot2go.go
  --having count(prot2kw.prot) >20
)
, tmp as (
  select kw, max(n) as n from counts
  group by kw
)

, mapping as (
    SELECT
      counts.kw,
      counts.n,
      go
    FROM counts
      JOIN tmp ON tmp.kw = counts.kw AND tmp.n = counts.n
    --WHERE counts.n > 10
)

select n, kw, keywords.name, go, goterms.name, goterms.namespace
from mapping join keywords on keywords.ac=mapping.kw
             join  goterms on goterms.id=mapping.go
order by n, kw



