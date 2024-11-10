# pylint: disable=missing-docstring
import pytest
from present_delivery import PresentDelivery


class TestPresentDelivery:

    def test_init_single(self):
        pd = PresentDelivery(1)
        assert pd.position == [(0, 0)]
        assert pd.visited == set()

    def test_init_double(self):
        pd = PresentDelivery(2)
        assert pd.position == [(0, 0), (0, 0)]
        assert pd.visited == set()

    def test_process_path_single(self):
        pd = PresentDelivery(1)
        pd.process_path('^')
        assert pd.position == [(0, 1)]
        assert pd.visited == {(0, 0), (0, 1)}
        assert pd.visited_count() == 2

        pd.process_path('v')
        assert pd.position == [(0, 0)]
        assert pd.visited == {(0, 0), (0, 1)}
        assert pd.visited_count() == 2

        pd.process_path('>')
        assert pd.position == [(1, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0)}
        assert pd.visited_count() == 3

        pd.process_path('<')
        assert pd.position == [(0, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0)}
        assert pd.visited_count() == 3

    def test_process_path_1(self):
        pd = PresentDelivery(1)
        pd.process_path('>')
        assert pd.position == [(1, 0)]
        assert pd.visited == {(0, 0), (1, 0)}
        assert pd.visited_count() == 2

    def test_process_path_2(self):
        pd = PresentDelivery(1)
        pd.process_path('^>v<')
        assert pd.position == [(0, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0), (1, 1)}
        assert pd.visited_count() == 4

    def test_process_path_3(self):
        pd = PresentDelivery(1)
        pd.process_path('^v^v^v^v^v')
        assert pd.position == [(0, 0)]
        assert pd.visited == {(0, 0), (0, 1)}
        assert pd.visited_count() == 2

    def test_process_path_4(self):
        pd = PresentDelivery(2)
        pd.process_path('^v')
        assert pd.position == [(0, 1), (0, -1)]
        assert pd.visited == {(0, 0), (0, 1), (0, -1)}
        assert pd.visited_count() == 3

    def test_process_path_5a(self):
        pd = PresentDelivery(2)
        pd.process_path('^>')
        assert pd.position == [(0, 1), (1, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0)}
        assert pd.visited_count() == 3

    def test_process_path_5b(self):
        pd = PresentDelivery(2)
        pd.process_path('^>v')
        assert pd.position == [(1, 0), (0, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0)}
        assert pd.visited_count() == 3

    def test_process_path_5c(self):
        pd = PresentDelivery(2)
        pd.process_path('^>v<')
        assert pd.position == [(0, 0), (0, 0)]
        assert pd.visited == {(0, 0), (0, 1), (1, 0)}
        assert pd.visited_count() == 3

    def test_process_path_6(self):
        pd = PresentDelivery(2)
        pd.process_path('^v^v^v^v^v')
        # assert pd.position == [(0, 0), (0, 0)]
        # assert pd.visited == {(0, 0), (0, 1)}
        assert pd.visited_count() == 11


if __name__ == '__main__':
    pytest.main()
