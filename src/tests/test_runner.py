import runner
import runner_lib


def test_list_cmd(capsys):
    # this is a pretty silly test, but it at least ensures we imported `runner`
    assert runner.list_cmd(None, None) == None
    captured = capsys.readouterr()
    assert "<all>: all" in captured.out


def test_sample_discovery():
    # make sure some of the samples are discovered -- doesn't need to be everything
    assert 'git' in runner_lib.discovered_samples.keys()
    assert 'core' in runner_lib.discovered_samples.keys()
