total_earthquakes = """
SELECT region, EXTRACT(MONTH FROM time) AS month, COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY region, month;
"""

avg_magnitude = """
SELECT region, source, AVG(magnitude) AS avg_magnitude
FROM earthquakes
GROUP BY region, source;
"""

top_earthquakes = """
SELECT *
FROM earthquakes
ORDER BY magnitude DESC, time DESC
LIMIT 10;
"""

depth_range = """
SELECT region, MAX(depth) AS max_depth, MIN(depth) AS min_depth
FROM earthquakes
GROUP BY region;
"""

delete_invalid = """
DELETE FROM earthquakes
WHERE magnitude < 0
   OR magnitude > 10
   OR depth < 0;
"""

update_null_magnitude = """
UPDATE earthquakes
SET magnitude = 0
WHERE magnitude IS NULL;
"""

update_null_depth = """
UPDATE earthquakes
SET depth = 0
WHERE depth IS NULL;
"""

create_indexes = """
CREATE INDEX idx_region ON earthquakes(region);
CREATE INDEX idx_time ON earthquakes(time);
CREATE INDEX idx_magnitude ON earthquakes(magnitude);
"""
