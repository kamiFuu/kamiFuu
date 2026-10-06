"""Minh họa độc lập cách kiểm tra cảnh báo và survey bằng dữ liệu giả lập."""

from contextlib import closing
import json
import sqlite3


SCHEMA = """
CREATE TABLE structures (
    structure_id TEXT PRIMARY KEY, lecture_id TEXT NOT NULL,
    start_time TEXT NOT NULL, end_time TEXT NOT NULL
);
CREATE TABLE assignments (
    lecture_id TEXT, clicker_id TEXT, student_id TEXT NOT NULL,
    PRIMARY KEY (lecture_id, clicker_id)
);
CREATE TABLE clicks (
    event_id TEXT PRIMARY KEY, lecture_id TEXT NOT NULL, clicker_id TEXT NOT NULL,
    timestamp TEXT NOT NULL, click_count INTEGER NOT NULL CHECK (click_count > 0)
);
CREATE TABLE surveys (
    survey_id TEXT PRIMARY KEY, lecture_id TEXT NOT NULL, student_id TEXT NOT NULL,
    tired INTEGER CHECK (tired IN (0, 1)), UNIQUE (lecture_id, student_id)
);
"""

REPORT_QUERY = """
SELECT ls.structure_id,
       COUNT(c.event_id) AS event_records,
       COALESCE(SUM(c.click_count), 0) AS alert_count,
       COUNT(DISTINCT c.clicker_id) AS distinct_clickers,
       COUNT(DISTINCT a.student_id) AS mapped_students,
       COUNT(DISTINCT CASE WHEN s.survey_id IS NOT NULL THEN a.student_id END)
           AS students_with_linked_survey,
       COUNT(DISTINCT CASE WHEN a.student_id IS NOT NULL AND s.survey_id IS NULL
           THEN a.student_id END) AS students_without_linked_survey,
       COALESCE(SUM(CASE WHEN s.survey_id IS NOT NULL THEN c.click_count ELSE 0 END), 0)
           AS survey_linked_alerts,
       COALESCE(SUM(CASE WHEN c.event_id IS NOT NULL AND a.student_id IS NULL
           THEN 1 ELSE 0 END), 0) AS unmapped_event_records
FROM structures AS ls
LEFT JOIN clicks AS c ON c.lecture_id = ls.lecture_id
    AND c.timestamp >= ls.start_time AND c.timestamp < ls.end_time
LEFT JOIN assignments AS a ON a.lecture_id = c.lecture_id AND a.clicker_id = c.clicker_id
LEFT JOIN surveys AS s ON s.lecture_id = c.lecture_id AND s.student_id = a.student_id
GROUP BY ls.structure_id
ORDER BY ls.structure_id
"""


def build_fixture():
    """Tạo dữ liệu mới hoàn toàn, không truy cập file hoặc database nghiên cứu."""
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    connection.executemany("INSERT INTO structures VALUES (?, ?, ?, ?)", [
        ("LS01", "L01", "2026-10-06T08:00:00", "2026-10-06T08:04:00"),
        ("LS02", "L01", "2026-10-06T08:04:00", "2026-10-06T08:07:00"),
        ("LS03", "L01", "2026-10-06T08:07:00", "2026-10-06T08:09:00"),
    ])
    connection.executemany("INSERT INTO assignments VALUES (?, ?, ?)", [
        ("L01", "U01", "ST01"), ("L01", "U02", "ST02"),
    ])
    connection.executemany("INSERT INTO clicks VALUES (?, ?, ?, ?, ?)", [
        ("C01", "L01", "U01", "2026-10-06T08:01:00", 1),
        ("C02", "L01", "U01", "2026-10-06T08:02:00", 1),
        ("C03", "L01", "U02", "2026-10-06T08:03:00", 1),
        ("C04", "L01", "U01", "2026-10-06T08:04:00", 1),
        ("C05", "L01", "U99", "2026-10-06T08:05:00", 1),
    ])
    connection.execute("INSERT INTO surveys VALUES (?, ?, ?, ?)", ("SV01", "L01", "ST01", 1))
    return connection


def validate_intervals(connection):
    """Từ chối khoảng rỗng hoặc chồng lấn để không đếm một cảnh báo nhiều lần."""
    previous = {}
    for row in connection.execute("SELECT * FROM structures ORDER BY lecture_id, start_time"):
        if row["start_time"] >= row["end_time"]:
            raise ValueError("Structure interval must have positive duration")
        if row["lecture_id"] in previous and previous[row["lecture_id"]] > row["start_time"]:
            raise ValueError("Structure intervals must not overlap within a lecture")
        previous[row["lecture_id"]] = row["end_time"]


def report(connection):
    """Trả số đếm và độ phủ liên kết, giữ confidence chưa định nghĩa là None."""
    validate_intervals(connection)
    structures = []
    for raw in connection.execute(REPORT_QUERY):
        row = dict(raw)
        count = row["alert_count"]
        row["linked_alert_fraction"] = row["survey_linked_alerts"] / count if count else None
        row["confidence"] = None
        row["status"] = "no_alerts" if not count else (
            "incomplete_linkage" if row["unmapped_event_records"] or row["students_without_linked_survey"]
            else "linked"
        )
        structures.append(row)
    outside = connection.execute("""
        SELECT COUNT(*) FROM clicks AS c
        WHERE NOT EXISTS (
            SELECT 1 FROM structures AS ls WHERE ls.lecture_id = c.lecture_id
            AND c.timestamp >= ls.start_time AND c.timestamp < ls.end_time
        )
    """).fetchone()[0]
    return {"data_kind": "synthetic", "interval_policy": "[start, end)",
            "confidence_status": "not_estimated", "structures": structures,
            "events_outside_structures": outside}


def main():
    """In báo cáo minh họa, không tạo hoặc ghi file dữ liệu."""
    with closing(build_fixture()) as connection:
        print(json.dumps(report(connection), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
