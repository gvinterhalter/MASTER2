CREATE or replace view missing_connections as

with kw2go_info as (
  select kw.ac as kw, kw.name "kwname", go.id, go.name "goname", go.namespace
  from keywords kw FULL OUTER JOIN kw2go on kw.ac=kw2go.kw
                   FULL OUTER JOIN goterms go on kw2go.go=go.id
  where kw.category='KW-9992' -- molecular function
)
  -- 91 kw
, missing as (
  SELECT DISTINCT kw, kwname FROM kw2go_info
  WHERE namespace IS NULL OR namespace != 'MF'
  EXCEPT
  SELECT DISTINCT kw, kwname FROM kw2go_info
  WHERE namespace = 'MF'
)
-- 7 kljucnih reci nema nema ni jedan protein
-- KW-1275 KW-1255 KW-1028 KW-0776 KW-0737 KW-0499 KW-0437
    SELECT missing.kw, missing.kwname, prot2kw.prot, prot2go.go, g.name goname
    FROM missing JOIN prot2kw ON missing.kw = prot2kw.kw
                 LEFT JOIN prot2go ON prot2kw.prot = prot2go.prot
                 join goterms g ON prot2go.go = g.id
    WHERE namespace='MF'
;

select * from missing_connections


-- 84 kw
with conn_info as (
    SELECT kw,
      count(DISTINCT prot) n_prot,
      count(DISTINCT go)   n_go
    FROM missing_connections
    GROUP BY kw
)
, go_info as (
    select gos.go, count(distinct prot) go_n_prot
    from ( SELECT distinct go FROM missing_connections) as gos
      join prot2go on prot2go.go=gos.go
    group by gos.go
)
-- , missing_go_info as (
--     SELECT go, goname, count(DISTINCT prot) n_prot, count(DISTINCT kw)   n_kw
--     FROM connections
--     GROUP BY go, goname
-- )
,  possible_mappings as (

    SELECT *, max(p_count) over(PARTITION BY kw) "max_p_count"
    FROM
    (
        SELECT kw, kwname, count(DISTINCT prot) p_count, go, goname
        FROM missing_connections
        GROUP BY kw, kwname, go, goname
    ) as some_alias
)



select amp.kw, kwname, keywords.def, amp.go, goname, goterms.def, p_count, n_prot as kw_n_prot, go_n_prot
    , round(p_count*1.0 / (n_prot+go_n_prot - 2*p_count), 3) as similarity
from possible_mappings amp JOIN conn_info ci on amp.kw=ci.kw
     join keywords on keywords.ac=amp.kw
     join goterms on goterms.id = amp.go
     join go_info on go_info.go = amp.go
where p_count > max_p_count*0.3
      and p_count > 5
order by kw, p_count desc;


-----------------------------

select * FROM missing_connections;


with kw2go_info as (
    select kw.ac as kw, kw.name "kwname", go.id, go.name "goname", go.namespace
    from keywords kw FULL OUTER JOIN kw2go on kw.ac=kw2go.kw
      FULL OUTER JOIN goterms go on kw2go.go=go.id
    where kw.category='KW-9992' -- molecular function
)
  -- 91 kw
  , missing as (
  SELECT DISTINCT kw, kwname FROM kw2go_info
  WHERE namespace IS NULL OR namespace != 'MF'
  EXCEPT
  SELECT DISTINCT kw, kwname FROM kw2go_info
  WHERE namespace = 'MF'
)
, conn as (
    select all_conn.*
    from missing
      join ( SELECT unnest(kw)   AS kw, id as prot, unnest(gomf) AS go from swissprot ) as all_conn
        on all_conn.kw=missing.kw
)

  , n_kwprot as (select kw, count(distinct prot) n_kwprot from conn group by kw)
  , n_goprot as (select go, count(distinct prot) n_goprot from conn group by go)
  , n_prot as (select kw, go, count(distinct prot) n_prot from conn group by kw, go)

, res as (
    SELECT
      n_prot.kw,
      n_prot.go,
      round(1.0 * n_prot / (n_kwprot + n_goprot - n_prot), 2) AS score,
      n_prot,
      n_kwprot,
      n_goprot
    FROM
      n_prot
      JOIN n_kwprot ON n_prot.kw = n_kwprot.kw
      JOIN n_goprot ON n_prot.go = n_goprot.go
    ORDER BY kw, score DESC
)

  select res.*, keywords.name, goterms.name, keywords.def, goterms.def from (
    select *, row_number() over (partition by kw order by score desc ) as rank from res
  ) as res join keywords on res.kw=keywords.ac
           join goterms on res.go=goterms.id
  where rank <= 5 and score != 0
order by n_kwprot desc, kw,  rank;








-- -- 7 kljucnih reci nema nema ni jedan protein
-- -- KW-1275 KW-1255 KW-1028 KW-0776 KW-0737 KW-0499 KW-0437
-- SELECT missing.kw, missing.kwname, prot2kw.prot, prot2go.go, g.name goname
-- FROM missing JOIN prot2kw ON missing.kw = prot2kw.kw
--   LEFT JOIN prot2go ON prot2kw.prot = prot2go.prot
--   join goterms g ON prot2go.go = g.id
-- WHERE namespace='MF'
-- ;

---------------------------------------------------------------------------------------------------

with kw2go_info as (
    select kw.ac as kw, kw.name "kwname", go.id, go.name "goname", go.namespace
    from keywords kw FULL OUTER JOIN kw2go on kw.ac=kw2go.kw
      FULL OUTER JOIN goterms go on kw2go.go=go.id
    where kw.category='KW-9992' -- molecular function
          and namespace='MF'
)

, missing as (
SELECT DISTINCT kw, kwname FROM kw2go_info
WHERE namespace = 'MF'
)
, conn as (
select all_conn.*
from missing
join ( SELECT unnest(kw)   AS kw, id as prot, unnest(gomf) AS go from swissprot ) as all_conn
on all_conn.kw=missing.kw
)

, n_kwprot as (select kw, count(distinct prot) n_kwprot from conn group by kw)
, n_goprot as (select go, count(distinct prot) n_goprot from conn group by go)
, n_prot as (select kw, go, count(distinct prot) n_prot from conn group by kw, go)

, res as (
SELECT
n_prot.kw,
n_prot.go,
round(1.0 * n_prot / (n_kwprot + n_goprot - n_prot), 2) AS score,
n_prot,
n_kwprot,
n_goprot
FROM
n_prot
JOIN n_kwprot ON n_prot.kw = n_kwprot.kw
JOIN n_goprot ON n_prot.go = n_goprot.go
ORDER BY kw, score DESC
)

, correct as (
    SELECT
      res.*,
      keywords.name,
      kw2go_info.goname = goterms.name AS correct,
      goterms.name,
      kw2go_info.goname,
      keywords.def,
      goterms.def
    FROM (
           SELECT
             *,
             row_number()
             OVER (
               PARTITION BY kw
               ORDER BY score DESC ) AS rank
           FROM res
         ) AS res
      JOIN keywords ON res.kw = keywords.ac
      JOIN goterms ON res.go = goterms.id
      JOIN kw2go_info ON kw2go_info.kw = res.kw
    WHERE rank <= 5 AND score != 0
    ORDER BY n_kwprot DESC, kw, rank
)



-- 0.57, 0.58
select count(*) as n, sum(correct::int), avg(correct::int) from correct
--88, 90

