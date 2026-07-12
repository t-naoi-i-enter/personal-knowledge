"""aggregate_feedback.py のテスト: レポート品質指標の集計(設計書11章)"""

from scripts.aggregate_feedback import compute_metrics


def _fb(labels=None, action_status=None, topic="ai_coding"):
    fb = {
        "feedback_id": "FB-20260711-001",
        "report_type": "daily",
        "labels": labels or [],
        "topic": {"primary": topic},
    }
    if action_status:
        fb["action_feedback"] = {"status": action_status}
    return fb


class TestComputeMetrics:
    def test_useful_item_rate(self):
        m = compute_metrics([_fb(["important"]), _fb(["useful"]), _fb(["not_relevant"])])
        assert m["total_items"] == 3
        assert m["useful_count"] == 2
        assert m["useful_item_rate"] == round(2 / 3, 3)

    def test_noise_rate_counts_not_relevant_and_already_known(self):
        m = compute_metrics([_fb(["not_relevant"]), _fb(["already_known"]), _fb(["important"])])
        assert m["noise_count"] == 2
        assert m["noise_rate"] == round(2 / 3, 3)

    def test_action_conversion_rate(self):
        m = compute_metrics(
            [
                _fb(action_status="will_do"),
                _fb(action_status="already_doing"),
                _fb(action_status="not_worth_it"),
                _fb(),  # アクション提案なし → 分母に含めない
            ]
        )
        assert m["action_proposals"] == 3
        assert m["action_conversion_rate"] == round(2 / 3, 3)

    def test_by_topic_tally(self):
        m = compute_metrics([_fb(["important"]), _fb(["not_relevant"], topic="mba")])
        assert m["by_topic"]["ai_coding"]["useful"] == 1
        assert m["by_topic"]["mba"]["noise"] == 1

    def test_empty_feedback_returns_zero_rates(self):
        m = compute_metrics([])
        assert m["total_items"] == 0
        assert m["useful_item_rate"] == 0.0
        assert m["noise_rate"] == 0.0
        assert m["action_conversion_rate"] == 0.0
