"""Kiểm tra các tình huống dễ làm sai cách ghép cảnh báo và survey."""

import unittest

from demo import build_fixture, report


class AlertSurveyDemoTests(unittest.TestCase):
    """Xác nhận quy tắc demo độc lập, không chứng minh mô hình nghiên cứu."""

    def setUp(self):
        """Tạo database giả lập mới cho mỗi kiểm tra."""
        self.connection = build_fixture()
        self.addCleanup(self.connection.close)

    def indexed(self):
        """Đánh chỉ mục kết quả theo structure để đối chiếu kỳ vọng."""
        return {row["structure_id"]: row for row in report(self.connection)["structures"]}

    def test_event_count_differs_from_student_count(self):
        """Một học viên nhiều cảnh báo không làm tăng số người tương ứng."""
        first = self.indexed()["LS01"]
        self.assertEqual((first["alert_count"], first["mapped_students"]), (3, 2))
        self.assertAlmostEqual(first["linked_alert_fraction"], 2 / 3)

    def test_boundary_event_is_assigned_once(self):
        """Click đúng biên thuộc phân đoạn sau theo quy ước demo."""
        rows = self.indexed()
        self.assertEqual(rows["LS01"]["alert_count"], 3)
        self.assertEqual(rows["LS02"]["alert_count"], 2)
        self.assertEqual(sum(row["alert_count"] for row in rows.values()), 5)

    def test_missing_survey_is_not_false_or_confidence_zero(self):
        """Giữ tình trạng thiếu liên kết thay vì suy ra câu trả lời phủ định."""
        first = self.indexed()["LS01"]
        self.assertEqual(first["students_without_linked_survey"], 1)
        self.assertIsNone(first["confidence"])
        self.connection.execute("INSERT INTO surveys VALUES ('SV02', 'L01', 'ST02', 0)")
        first = self.indexed()["LS01"]
        self.assertEqual(first["students_without_linked_survey"], 0)
        self.assertEqual(first["linked_alert_fraction"], 1)

    def test_no_alerts_preserves_undefined_denominator(self):
        """Không có cảnh báo không sinh tỷ lệ 0 có thể gây hiểu sai."""
        third = self.indexed()["LS03"]
        self.assertEqual(third["status"], "no_alerts")
        self.assertIsNone(third["linked_alert_fraction"])

    def test_unmapped_clicker_is_visible(self):
        """Giữ cảnh báo thiếu gán học viên và đánh dấu tình trạng liên kết."""
        second = self.indexed()["LS02"]
        self.assertEqual(second["unmapped_event_records"], 1)
        self.assertEqual(second["status"], "incomplete_linkage")

    def test_click_count_is_summed_not_just_rows(self):
        """Một bản ghi gom nhiều click phải giữ tổng số cảnh báo."""
        self.connection.execute("UPDATE clicks SET click_count = 3 WHERE event_id = 'C01'")
        first = self.indexed()["LS01"]
        self.assertEqual(first["event_records"], 3)
        self.assertEqual(first["alert_count"], 5)

    def test_clicker_assignment_is_scoped_to_lecture(self):
        """Clicker tái sử dụng ở buổi khác không ghép nhầm survey/học viên."""
        self.connection.execute("INSERT INTO assignments VALUES ('L02', 'U01', 'OTHER')")
        self.connection.execute("INSERT INTO surveys VALUES ('SV03', 'L02', 'OTHER', 0)")
        first = self.indexed()["LS01"]
        self.assertEqual((first["alert_count"], first["mapped_students"]), (3, 2))

    def test_overlapping_intervals_are_rejected(self):
        """Không cho phép khoảng chồng lấn âm thầm nhân số cảnh báo."""
        self.connection.execute("UPDATE structures SET start_time = '2026-10-06T08:03:00' WHERE structure_id = 'LS02'")
        with self.assertRaises(ValueError):
            report(self.connection)

    def test_outside_event_is_reported(self):
        """Cảnh báo ngoài cấu trúc được phát hiện, không tự biến mất khỏi kiểm tra."""
        self.connection.execute("INSERT INTO clicks VALUES ('OUT', 'L01', 'U01', '2026-10-06T09:00:00', 1)")
        self.assertEqual(report(self.connection)["events_outside_structures"], 1)


if __name__ == "__main__":
    unittest.main()
