
CREATE FUNCTION foo(facid integer) RETURNS SETOF calendar
    AS $$
select * from edw.calendar

$$
    LANGUAGE sql STABLE CONTAINS SQL;


ALTER FUNCTION edw.foo(facid integer) OWNER TO psteffek;
