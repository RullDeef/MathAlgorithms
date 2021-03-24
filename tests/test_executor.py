import sys
from matalg.executor import main, ErrorCode


def test_main():
    assert main([]) == ErrorCode.HELP_SHOWN
    assert main(["-f", "./algorithms/MT/clear.txt", "-T", "-M"]) == ErrorCode.BAD_MODEL
    assert main(["-f", "./algorithms/MT/clear.txt", "-T", "-i", "-3"]) == ErrorCode.BAD_TIMEOUT_VALUE

    assert main(["-f", "./algorithms/MT/clear.txt", "-T", ""]) == ErrorCode.SUCCESS
    assert main(["-f", "./algorithms/MT/clear.txt", "-T", "abcac"]) == ErrorCode.SUCCESS
    assert main(["-f", "./algorithms/MT/clear.txt", "-T", "acdb", "-i", "0.1"]) == ErrorCode.TIMEOUT_EXCEED
