import pytest

from solar.dblayer.solar_models import LogItem, NegativeCounter


def test_separate_logs():

    history = 'history'
    staged = 'staged'
    history_uids = []
    staged_uids = []
    for i in range(2):
        l = LogItem.new({'log': history})
        l.save()
        history_uids.append(l.key)
    for i in range(3):
        l = LogItem.new({'log': staged})
        l.save()
        staged_uids.append(l.key)

    assert LogItem.composite.filter({'log': history}) == history_uids
    assert LogItem.composite.filter({'log': staged}) == staged_uids


def test_multiple_filter():

    l1 = LogItem.new({'log': 'history', 'resource': 'a'})
    l2 = LogItem.new({'log': 'history', 'resource': 'b'})

    l1.save()
    l2.save()

    assert LogItem.composite.filter({'log': 'history', 'resource': 'a'}) == [l1.key]
    assert LogItem.composite.filter({'log': 'history', 'resource': 'b'}) == [l2.key]


def test_changed_index():

    l = LogItem.new({'log': 'staged', 'resource': 'a', 'action': 'run'})
    l.save()

    assert LogItem.composite.filter({'log': 'staged'}) == [l.key]

    l.log = 'history'
    l.save()

    assert LogItem.composite.filter({'log': 'staged'}) == []
    assert LogItem.composite.filter({'log': 'history'}) == [l.key]


def test_negative_counter():
    nc = NegativeCounter.get_or_create('non_exist')
    assert nc.count == 0


def test_reversed_order_is_preserved():
    l1 = LogItem.new({'log': 'history'})
    l2 = LogItem.new({'log': 'history'})
    l1.save()
    l2.save()
    assert LogItem.composite.filter({'log': 'history'}, max_results=1) == [l2.key]
