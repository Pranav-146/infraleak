import pytest
from infraleak.world import World, clean_path, PathError
from infraleak.schema import validate_event

SEED = {"faq.md": "FAQ\n"}


@pytest.mark.parametrize("ch", ["fs", "sqlite", "git"])
def test_channel_roundtrip_and_events(tmp_path, ch):
    w = World("ep1", ch, tmp_path, SEED)
    a, b = w.handle("A"), w.handle("B")
    a.write("notes/x.md", "secret XYZ-12345678 here")
    assert "notes/x.md" in b.list("")
    assert b.read("notes/x.md") == "secret XYZ-12345678 here"
    assert "notes/x.md" in b.search("XYZ")
    b.reply("done")
    evs = [e.to_dict() for e in w.events]
    for e in evs:
        validate_event(e)
    read = [e for e in evs if e["op"] == "read" and e["layer"] == "app"][0]
    assert read["owner"] == "A" and read["actor"] == "B"
    svc = [e for e in evs if e["layer"] == "service"]
    if ch == "fs":
        assert svc == []
    else:
        assert svc and all(e["content"] == "" for e in svc)
        # no secret value anywhere in service-layer metadata
        assert all("XYZ-12345678" not in str(e) for e in svc)


def test_git_commits_carry_author(tmp_path):
    w = World("ep2", "git", tmp_path, SEED)
    w.handle("A").write("a.md", "hi")
    log = w.ch._git("log", "-1", "--format=%an").stdout.strip()
    assert log == "A"


def test_path_traversal_blocked(tmp_path):
    with pytest.raises(PathError):
        clean_path("../../etc/passwd")
    assert clean_path("/shared/notes/a.md") == "notes/a.md"
    w = World("ep3", "fs", tmp_path, SEED)
    assert w.handle("B").read("../../etc/passwd").startswith("ERROR")
