from typing import Protocol, runtime_checkable


@runtime_checkable
class HasTestContext(Protocol):
    module_output_dir: str
    test_suite_output_dir: str
    test_case_name: str
